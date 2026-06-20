# Holy Grail — Context: How Astronomers Perform Wavelength Calibration

> *"One solution to rule them all."*

**Version:** 0.2 · **Last updated:** 2026-06-20
(see [Version history](#version-history) at the end)

This document summarizes everything we have learned about how astronomers
automatically identify and measure emission lines in arc-line spectra, and
how this is implemented in practice. It is built primarily from three
codebases:

- **PypeIt** (`PypeIt/`) — the production data-reduction pipeline whose
  `pypeit/core/wavecal/` package contains the current state of the art.
- **PypeIt development suite** (`PypeIt-development-suite/`) — the testing,
  validation, and archival-data harness.
- **`arclines`** (`arclines/`) — the now-defunct research sandbox that
  prototyped the "Holy Grail" auto-identification algorithm and the line-list
  database. Its `holy/` package was absorbed almost verbatim into PypeIt.

…augmented (as of v0.2) with a survey of the external literature (§13).

The document is intended to grow as the project proceeds.

---

## 0. Project goal — the Holy Grail

The ultimate aim of *The Holy Grail* project is **to generate an entirely new
wavelength-calibration algorithm that is better than any previous one.** More
precisely, the target is a system that ingests an **entirely unlabeled arc
spectrum** — no instrument, grating, central wavelength, dispersion, or even
lamp identity supplied — and:

1. **Identifies the arc lamp(s)** — determines from the spectrum alone which
   calibration source(s) produced it (e.g. ThAr vs. CuAr vs. HgCdNeAr vs. OH
   sky), and hence which reference line list(s) apply.
2. **Calibrates it** — derives the full pixel→wavelength solution `λ = f(pixel)`
   with no human input and no prior guess.

This is a substantial step beyond the current state of the art. PypeIt's
existing `holy-grail` method already attempts step 2 without a dispersion/zero-
point prior (via scale-invariant pattern matching, §5), but it (a) is *given*
the lamp list up front and (b) "can fail catastrophically," so production
reductions prefer archive-based re-identification (§6). **Step 1 — blind lamp
identification — is essentially absent from the published literature** (see
§13), which is a genuine gap this project can fill. The rest of this document
characterizes the current approaches (as the baseline to beat) and the relevant
external work (as prior art and ideas to draw on).

---

## 1. The problem

A spectrograph disperses light so that wavelength varies (approximately
monotonically) along the *spectral* axis of the detector. To turn raw pixel
positions into physical wavelengths we need a **wavelength solution**: a
function `λ = f(pixel)` for every spatial position (slit, order, or fiber).

The standard approach uses a **calibration ("arc") frame**: an exposure of a
lamp emitting many narrow emission lines at precisely known rest wavelengths
(or, in the IR, the night-sky OH emission lines). The calibration task is:

1. **Detect** the emission-line peaks along the spectral axis and measure
   their sub-pixel centroids.
2. **Identify** each detected peak — assign it the correct rest wavelength
   from a reference line list.
3. **Fit** a smooth pixel→wavelength function (low-order polynomial /
   Legendre) to the identified (pixel, wavelength) pairs, with iterative
   rejection of outliers.
4. **Validate** the solution, typically by its RMS residual (in pixels or Å).

Step 2 is the hard, historically manual part. The "Holy Grail" goal is to
automate it: identify lines with **no human input and no prior guess** of the
central wavelength or dispersion. Two broad strategies exist:

- **Pattern matching from scratch** ("Holy Grail" proper): exploit the fact
  that *ratios of line separations* are invariant to the (unknown) linear
  mapping between pixels and wavelength, so geometric patterns of lines can be
  matched between the detections and the line list without knowing the
  dispersion.
- **Re-identification from an archive**: cross-correlate the new arc against a
  previously-solved reference arc for the same instrument/grating, transfer
  the known line IDs, and refit. This is more robust when a good archive
  exists, and is the preferred production method.

---

## 2. Reference data: line lists and the solution archive

### 2.1 Arc line lists

The atomic reference data are per-ion line lists of known rest wavelengths
(vacuum Ångströms). In PypeIt these live in
[PypeIt/pypeit/data/arc_lines/lists/](../../PypeIt/pypeit/data/arc_lines/lists/),
one `<ION>_lines.dat` file per ion/lamp (e.g. `ArI_lines.dat`, `NeI_lines.dat`,
`ThAr_lines.dat`, plus instrument-specific and OH sky-line variants). Each is a
pipe-delimited fixed-width ASCII table:

```
| ion |       wave | NIST | Instr | amplitude | Source |
| ArI | 6967.3520  |    1 |    25 |     15530 | lrisr_600_7500_PYPIT.json |
```

- `wave` — vacuum Å.
- `NIST` — flag: 1 if the wavelength is NIST-verified.
- `Instr` — bitmask of which instruments have actually detected this line
  (defined in `pypeit/core/wavecal/defs.py::instruments()` /
  `LinesBitMask`).
- `amplitude`, `Source` — provenance.

`UNKNWNs.dat` holds lines that are empirically real but not yet attributed to
an ion. Crucially, these lists contain **only lines actually observed in real
spectrographs**, not the full NIST catalog — this keeps the matching search
space small and realistic. Lines are loaded and vstacked by
`waveio.load_line_lists()`
([PypeIt/pypeit/core/wavecal/waveio.py](../../PypeIt/pypeit/core/wavecal/waveio.py)).

**Lamp / line diversity.** Optical metal & noble-gas lamps: `ArI/ArII`, `NeI`,
`HeI`, `HgI`, `CdI`, `ZnI`, `KrI`, `XeI`, `CuI`, `FeI/FeII`, `FeAr`. High-res /
echelle: `ThAr` (and instrument variants `ThAr_HARPS`, `ThAr_MagE`,
`ThAr_XSHOOTER_{UVB,VIS}`). Infrared: night-sky OH emission (`OH_NIRES`,
`OH_GNIRS`, `OH_XSHOOTER`, `OH_MOSFIRE_{Y,J,H,K}`, …) used in lieu of lamps,
plus IR arc variants. The sentinel `'use_header'` means the lamp set is read
from FITS headers at runtime.

### 2.2 The solution archive (`reid_arxiv`)

The "one solution to rule them all" archive is
[PypeIt/pypeit/data/arc_lines/reid_arxiv/](../../PypeIt/pypeit/data/arc_lines/reid_arxiv/)
— ~245 files (mostly FITS, some legacy JSON) of fully-solved reference arcs,
one (or more) per instrument+grating+central-wavelength configuration. Naming
encodes the configuration, e.g.
`keck_lris_red_R600_7500_ArCdHgKrNeXeZn.fits`. Two layouts:

- **Longslit/multislit template** — a `BinTableHDU` with columns
  `['wave','flux']` and header metadata `BINSPEC` (spectral binning) and
  optionally `INSTR`. This is a reference arc spectrum *with* its wavelength
  axis solved.
- **Echelle angle-fit / composite-arc format** (HIRES, NIRSPEC, UVES) —
  multi-HDU files: a composite per-order arc plus polynomial fits of the
  solution coefficients vs. echelle / cross-disperser grating angle, so a
  solution can be *predicted* at an arbitrary grating angle.

These are read by `waveio.load_template()` / `load_reid_arxiv()` and built by
[templates.py](../../PypeIt/pypeit/core/wavecal/templates.py)
(`build_template()` stitches multiple solved arcs across wavelength cuts).
Template construction is a developer task, not part of a normal reduction.

---

## 3. The PypeIt wavelength-calibration workflow

Orchestration lives in
[PypeIt/pypeit/wavecalib.py](../../PypeIt/pypeit/wavecalib.py):

- **`WaveCalib`** (`wavecalib.py:33`) — the output `DataContainer` (written to
  FITS): per-slit fits (`wv_fits`, an array of `WaveFit` objects), an optional
  2D echelle solution (`wv_fit2d`), a spectral-FWHM map, the extracted arc
  spectra, slit IDs / echelle orders, the parameter string, and lamp list.
  `build_waveimg()` evaluates the fit at every pixel (using the tilt image) to
  produce the per-pixel wavelength image.
- **`BuildWaveCalib`** (`wavecalib.py:444`) — the engine. Its `run()`
  (`wavecalib.py:1155`) executes:
  1. **Extract 1D arcs** (`extract_arcs()`) — boxcar-extract an arc spectrum
     down the center of each unmasked slit/order → `arccen` of shape
     `(nspec, nslit)`.
  2. **Per-slit 1D solutions** (`build_wv_calib()`, `wavecalib.py:607`) —
     dispatch on `par['method']` (§4).
  3. **2D echelle fit** (if applicable) — `echelle_2dfit()` (§6).
  4. **Masking** — flag slits with no valid fit as `BADWVCALIB`.
  5. **Package** the `WaveCalib` container.

Line detection throughout uses `wvutils.arc_lines_from_spec()` →
`arc.detect_lines()`: continuum-subtract, find peaks, fit Gaussians for
sub-pixel centroids (`tcent`), widths, and significance (`nsig`); cut on
`sigdetect`; exclude lines above `nonlinear_counts`.

The pervasive **acceptance threshold** is
`wave_rms_thresh = rms_thresh_frac_fwhm × FWHM` (default `0.15 × FWHM` pixels).

---

## 4. Line-identification methods

`WavelengthSolutionPar.valid_methods()` (`pypeitpar.py`):
`['holy-grail', 'identify', 'reidentify', 'echelle', 'full_template']`.

| Method | Needs archive? | Use |
|---|---|---|
| `holy-grail` | No | Fully automated from-scratch pattern matching. Powerful but can fail catastrophically. |
| `reidentify` | Yes | **Preferred** multislit/echelle. Cross-correlate each arc against archived per-slit solutions and transfer IDs. |
| `full_template` | Yes | **Preferred** for many setups. Cross-correlate against one full-detector template, then reidentify in snippets. |
| `echelle` | Yes (angle fits) | Tiltable-grating cross-dispersed echelles (e.g. HIRES): predict order coverage & solutions from grating angles, then reidentify. |
| `identify` | n/a | Interactive GUI solution. (In-pipeline path currently `NotImplementedError`; the live tool is the standalone `pypeit_identify` — §7.) |

`reidentify` and `full_template` both ultimately call the same low-level
`autoid.reidentify()`; they differ only in the reference (archived per-slit
solutions vs. one stitched full-detector template).

---

## 5. The "Holy Grail" auto-identification algorithm

Implemented by class **`HolyGrail`**
([autoid.py](../../PypeIt/pypeit/core/wavecal/autoid.py)`:1881`), with the
geometric machinery in
[patterns.py](../../PypeIt/pypeit/core/wavecal/patterns.py). Two engines:
a brute-force path (`run_brute`, the default) and a KD-tree path (`run_kdtree`,
reserved for ThAr and currently disabled as "too unstable").

### 5.1 The scale-invariant geometric idea

A pattern of N lines is reduced to **scale- and offset-invariant ratios**, so
the same quantity can be computed in pixel space (from detections) and in
wavelength space (from the line list) *without knowing the dispersion or zero
point*.

- **`triangles()`** (`patterns.py:272`) — for anchors `s` (start) and `e`
  (end) with a middle line `b`, the invariant is `(b−s)/(e−s)`. A detected
  triangle matches a line-list triangle when their invariants agree within
  `pix_tol/(e−s)`. From each match it **back-solves the implied central
  wavelength and dispersion**:
  `disp = (λ_e − λ_s)/(pix_e − pix_s)`, then `wvcen` at the detector center.
- **`quadrangles()`** (`patterns.py:391`) — 4 lines with two invariants; more
  discriminating.

Because the pixel axis may correlate *or* anti-correlate with wavelength, both
sign hypotheses are tried.

### 5.2 Voting, peak detection, scoring (`solve_slit`, `autoid.py:2758`)

This is a Hough-transform-style voting scheme:

1. Every candidate pattern casts a vote at its implied `(wvcen, log10 disp)`
   into a **2D histogram** (a `(binw=300, bind=3000)` grid; wavelength spans
   the line list, dispersion spans `10^[-1.5, 2.0]` Å/pix). Correlate and
   anti-correlate hypotheses get separate histograms, then differenced.
2. `patterns.detect_2Dpeaks()` finds the densest cells (an 8-connected local
   maximum filter); the `nstore` largest peaks are candidate `(wvcen, disp)`
   global solutions.
3. For each peak, all patterns near it are passed to
   `patterns.solve_triangles()`: each detected line is assigned its
   most-frequently-voted line-list wavelength, graded by `score_triangles()`
   (`Perfect → Very Good → Good → OK → Risky → Ambitious` based on vote counts
   and uniqueness).
4. The candidate ID set is fit (`wv_fitting.fit_slit`); the winning solution
   maximizes the number of fitted lines subject to RMS < threshold.

The brute outer loop (`run_brute_loop`, `autoid.py:2040`) sweeps a small
parameter space — polygon type ∈ {3, 4}, `detsrch` and `lstsrch` ∈ [3,6),
`pix_tol=1.0` — and returns early once ≥`idthresh=0.5` of lines on both halves
of the spectrum are identified.

### 5.3 Cross-matching slits

After per-slit fits, `cross_match()` (`autoid.py:2321`) propagates IDs from
successful slits into failed ones via `wvutils.xcorr_shift_stretch`, iterating
up to 10 times, then refits.

---

## 6. Re-identification, templates, and echelle

### 6.1 `reidentify()` — the low-level transfer engine (`autoid.py:380`)

Given an input arc plus archived reference arc(s) and their solutions:

1. Detect & continuum-subtract lines in input and archive.
2. `wvutils.xcorr_shift_stretch()` finds the shift + (linear or quadratic)
   stretch mapping the archive onto the input, gated by a global
   cross-correlation threshold `cc_thresh` (0.70).
3. Transform archive line positions into the input frame; for each input
   detection within `match_toler` pixels of a transformed archive line, look
   up its archive wavelength and snap to the nearest line-list wavelength.
4. A **local** zero-lag cross-correlation (window `nlocal_cc=11`) validates
   each candidate (`cc_local_thresh=0.70`).
5. `patterns.solve_xcorr()` aggregates votes across all reference spectra;
   a line needs ≥`nreid_min` consistent matches and is graded; only `Perfect`
   lines are kept, ≥3 required to accept.

### 6.2 `full_template()` (`autoid.py:1034`)

Load the full-detector template (rebinned to the data's binning), find the
global shift via `wvutils.xcorr_shift` (amplitude-capped at `cc_percent_ceil`
so bright lines don't dominate), chop the input into `nsnippet` (default 2)
pieces to absorb nonlinearity, run each through `reidentify()`, then
`wv_fitting.iterative_fitting()`.

### 6.3 `ArchiveReid` (`autoid.py:1603`)

Loads per-slit archived solutions and reidentifies each slit. For
fixed-format echelles (NIRES, X-Shooter, ESI) it matches by **order number**
so only the correct archive order is used.

### 6.4 Tiltable-grating echelle — the `echelle` method

[echelle.py](../../PypeIt/pypeit/core/wavecal/echelle.py): for instruments like
HIRES where order coverage depends on grating angles —
`predict_ech_order_coverage()` (from cross-disperser angle),
`predict_ech_wave_soln()` (from echelle angle),
`predict_ech_arcspec()` (synthesize a predicted arc per order from a composite
archive), `identify_ech_orders()` (cross-correlate predicted vs observed
echellogram to pin absolute order numbers), then per-order reidentify & fit
(`autoid.echelle_wvcalib`).

### 6.5 The 2D echelle fit (`echelle_2dfit`, `wavecalib.py:969`)

Collects all good `(pixel, wavelength, order)` triples and calls
`arc.fit2darc()` — a 2D Legendre fit of `λ·order` vs `(spectral pixel, order)`,
orders `ech_nspec_coeff × ech_norder_coeff` (default 4×4), with `ech_sigrej`
clipping. Orders failing the RMS threshold are re-attempted
(`redo_echelle_orders`) using wavelengths predicted from the 2D fit.

---

## 7. The final fit ([wv_fitting.py](../../PypeIt/pypeit/core/wavecal/wv_fitting.py))

- **`fit_slit()`** purges UNKNOWN/non-NIST IDs (snapping each to the nearest
  NIST line; rejecting if the velocity offset > `vel_tol = 1 km/s`), then calls
  `iterative_fitting`.
- **`iterative_fitting()`** is the workhorse:
  - Robust Legendre fit (`func='legendre'`) of normalized pixel → wavelength,
    polynomial order ramping from `n_first` (2) to `n_final` (4).
  - Sigma-clipping rejection: `sigrej_first=2.0` early, `sigrej_final=3.0` last.
  - **Line growth**: after each iteration it re-evaluates the solution at all
    detected centroids and adds any line-list match within `match_toler`
    pixels — expanding the ID set, including weaker lines.
  - RMS is computed in Å then divided by the dispersion to report **RMS in
    pixels**, compared to the acceptance threshold.
  - Returns a **`WaveFit`** DataContainer (`pypeitfit`, `pixel_fit`,
    `wave_fit`, `wave_soln`, `cen_wave`, `cen_disp`, `rms`, `ion_bits`, …).

---

## 8. Interactive solution building — `pypeit_identify`

Script [PypeIt/pypeit/scripts/identify.py](../../PypeIt/pypeit/scripts/identify.py),
GUI engine [PypeIt/pypeit/core/gui/identify.py](../../PypeIt/pypeit/core/gui/identify.py).

`pypeit_identify <Arc file> <Slits file>` launches a matplotlib GUI in which a
human assigns wavelengths to detected peaks, fits, inspects residuals, and
iterates; auto-ID propagates IDs within `--pixtol`. On exit,
`store_solution()` optionally (a) saves the per-line pixel/wavelength IDs (so
new lines can be folded back into the master line lists), (b) writes the
`WaveCalib` calibration file — **gated by `final_fit['rms'] < --rmstol`
(default 0.1)** unless `--force_save` — and (c) saves the solution as a new
`reid_arxiv` template (auto-named `{spec}_{grat}_{angle}.fits`) for reuse. This
is the human path by which new instrument/grating configurations enter the
archive.

---

## 9. Validation in the development suite

- **Maintained regression test**:
  [PypeIt-development-suite/vet_tests/test_wavelengths.py](../../PypeIt-development-suite/vet_tests/test_wavelengths.py).
  After a full reduction produces `WaveCalib_*.fits`, it loads each and asserts
  `waveCalib.wv_fits[index].rms < rms` against instrument/setup-specific
  thresholds (Å), e.g. Shane/Kast 0.05–0.055, DEIMOS 0.1–0.35, LRIS red
  0.03–0.5, HIRES echelle 0.21–0.45, GMOS 0.25–0.30. The **per-slit/order RMS
  is the sole success criterion**. `test_redoslits_kastr` validates the
  `redo_slits` re-calibration workflow.
- The reductions vetted are registered in
  [PypeIt-development-suite/test_scripts/test_setups.py](../../PypeIt-development-suite/test_scripts/test_setups.py)
  (built from `setups.py::all_setups`), currently spanning ~59 instrument arms
  / ~224 setups.
- **Legacy algorithm harness**:
  [PypeIt-development-suite/wavecalib/](../../PypeIt-development-suite/wavecalib/)
  (`test_longslit.py`, `test_ThAr.py`) runs the auto-ID functions directly on
  canned arc spectra in `TEST_DATA/` and grades by RMS and minimum line count.
  This targets the internal algorithm rather than end-to-end calibration.

---

## 10. Lineage — `arclines` → PypeIt

[arclines/](../../arclines/) (JXP, 2016–2018) was the prototype, serving two
roles: a **database of observed arc lines** and a **sandbox for the Holy Grail
algorithm**. Its `holy/` package (`grail.py`, `patterns.py`, `fitting.py`) was
absorbed essentially verbatim into PypeIt's `pypeit/core/wavecal/`:

- The original quad-matching (`semi_brute`/`basic`, scale-invariant
  cross-ratios of 4-line patterns) and the later triangle + 2D-histogram
  voting (`general`) are the direct ancestors of `HolyGrail.run_brute`.
- `arclines.defs` (instrument/lamp bit flags), `arclines.io.load_line_lists`,
  and the `.dat` line-list format all carried over.
- The class is still literally named `HolyGrail`, and its docstring still
  refers to "the preliminary pattern matching algorithm."

PypeIt then went well beyond arclines: the KD-tree matcher, cross-slit
matching, archival `reidentify` / `full_template`, full echelle support
(angle-fit prediction + 2D fits), per-instrument template builders, FWHM
mapping, the `WavelengthSolutionPar` parameter system, and FITS DataContainers.
The KD-tree path itself is *new in PypeIt* (no KD-tree code exists in
`arclines`). `arclines` is now defunct — its code and data live on inside
PypeIt.

---

## 11. Key tunable parameters (`WavelengthSolutionPar`, `pypeitpar.py`)

- **Method/reference**: `method` (default `holy-grail`), `reference`
  (`arc`/`sky`/`pixel`), `lamps` (or `use_header`), `reid_arxiv`.
- **Detection**: `sigdetect` (5.0), `fwhm` (4.0), `fwhm_fromlines` (True),
  `nfitpix` (5), `boxcar_radius` (3).
- **Fit & acceptance**: `func` (`legendre`), `n_first` (2), `n_final` (4),
  `sigrej_first` (2.0), `sigrej_final` (3.0), `match_toler` (2.0),
  **`rms_thresh_frac_fwhm` (0.15)** — the central quality gate.
- **Cross-correlation / reidentify**: `nreid_min` (1), `cc_thresh` (0.70),
  `cc_local_thresh` (0.70), `nlocal_cc` (11), `cc_percent_ceil` (50.0),
  `stretch_func` (`quadratic`), `nsnippet` (2).
- **Echelle**: `echelle`, `ech_2dfit` (True), `ech_nspec_coeff` /
  `ech_norder_coeff` (4/4), `ech_sigrej` (2.0), `echelle_pad` (3).

---

## 12. Code-state caveats (current branches)

- In-pipeline `identify` method → `NotImplementedError` (`wavecalib.py:672`);
  use standalone `pypeit_identify`.
- ThAr KD-tree HolyGrail path → `NotImplementedError` (`autoid.py:1999`,
  "too unstable").
- Per-slit measured FWHM is currently hard-coded to 3.0 (`wavecalib.py:659`,
  marked "REMOVE THIS!!") — a work in progress.
- `patterns.curved_quadrangles()` is dead/buggy; only `triangles`/`quadrangles`
  are used.

---

## Q&A

*(Questions for the user are logged here.)*

1. **Scope / next steps.** Section 1 of the prompt asked to "begin with" these
   three codebases and noted "we will add more as we go." What should the next
   addition be — the technical documents on wavelength calibration mentioned in
   the goals (do you have specific papers/PDFs in mind?), or a deeper dive into
   one algorithm (e.g. the Holy Grail pattern matching) toward designing a new
   approach?

2. **End goal.** Is the ultimate aim of "The Holy Grail" project to *improve*
   PypeIt's existing auto-ID, *replace* it with a new (e.g. ML-based) method, or
   to *document/benchmark* the current approach? This will shape what detail
   this document should emphasize.

## Requests

*(Requests for additional material are logged here.)*

- The "Technical documents on wavelength calibration" listed in the project
  goals are not yet present in the repos I can see. If you can drop relevant
  papers/notes into a folder (e.g. `design/refs/`), I will incorporate them.
