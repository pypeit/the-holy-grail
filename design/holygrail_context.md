# Holy Grail — Context: How Astronomers Perform Wavelength Calibration

> *"One solution to rule them all."*

**Version:** 0.4 · **Last updated:** 2026-06-20
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
wavelength-calibration algorithm that solves the problem.** More
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

### 0.1 Data corpus to build on

The project will **leverage the existing PypeIt datasets as a labelled corpus**
(confirmed with the user). Three complementary, already-curated resources cover
both project steps:

1. **`PypeIt-development-suite/RAW_DATA/`** — real *raw* arc frames spanning ~45
   instrument arms (Keck LRIS/DEIMOS/HIRES/ESI/KCWI/MOSFIRE/NIRES/NIRSPEC,
   Gemini GMOS/GNIRS/Flamingos2, VLT, Magellan, Shane/Kast, GMOS, SOAR, …; see
   §9). **Lamp labels are available** per frame from the companion
   `pypeit_files/*.pypeit` setup tables (the `arc,tilt` frametype rows carry a
   lamp/target column, e.g. `CuAr`, `GCALflat`) and from the FITS headers /
   each spectrograph's default `lamps` parameter. This is the realistic, diverse,
   **labelled raw input** for the *lamp-ID* step (step 1).
2. **`PypeIt/pypeit/data/arc_lines/reid_arxiv/`** — **242 solved 1D reference
   arcs** (229 FITS + 13 legacy JSON): flux vs. *already-calibrated* wavelength,
   per instrument/grating config (§2.2). These give **calibration ground truth**
   (the wavelength solution) and clean per-configuration template spectra — ideal
   for the *calibration* step (step 2) and as DTW/reidentify templates. Caveat:
   lamp species are encoded in the *filenames* only inconsistently
   (`keck_lris_red_R600_7500_ArCdHgKrNeXeZn.fits` does, `gemini_gmos_b600_ham.fits`
   does not) — derive lamp truth from headers / the source setup, not the name.
3. **`PypeIt/pypeit/data/arc_lines/lists/`** — the per-ion atomic line lists
   (§2.1): the authoritative "which lines belong to which species" reference,
   usable both to *synthesize* labelled training spectra and as the match target.

Together these provide (a) a labelled set for lamp classification, (b) ground-
truth wavelength solutions for evaluating calibration accuracy (against the same
RMS gates the dev-suite already enforces, §9), and (c) the atomic data to
generate unlimited synthetic arcs with known lamp + dispersion for training/
stress-testing. A train/test split and any held-out instruments are TBD (see
Q&A); the natural caution is to **split by instrument/configuration** so the
algorithm is tested on setups it has never seen.

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

## 5. PypeIt's so-called "Holy Grail" auto-identification algorithm

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

## 13. External literature & references

A survey of prior art (added v0.2). All arXiv entries were verified by fetching
their abstract pages; web resources were checked where feasible. Items flagged
*(unverified)* were found via search but not directly fetched — double-check
before formal citation. **Note the standout gap:** automated *calibration*
(step 2) is well represented, but blind *lamp-type identification* (step 1) is
barely addressed anywhere — the closest is frame-type classification (SPIT),
not lamp-species identification.

### 13.1 Most directly relevant — automated / blind wavelength calibration

- **Veitch-Michaelis & Lam (2019)**, *RASCAL: Towards automated spectral
  wavelength calibration.* arXiv:[1912.05883](https://arxiv.org/abs/1912.05883),
  DOI [10.48550/arXiv.1912.05883](https://doi.org/10.48550/arXiv.1912.05883).
  Code: <https://github.com/jveitchmichaelis/rascal>, <https://pypi.org/project/rascal/>.
  Solver from a peak list + line list via Hough transform + RANSAC; the closest
  prior art for the calibration step. **Full text read — see §14.1** (PDF in
  [design/docs/veitch2019.pdf](docs/veitch2019.pdf)).
- **Brandt, Brandt & McCully (2020)**, *Automatic Échelle Spectrograph
  Wavelength Calibration (xwavecal).* AJ 160, 25.
  arXiv:[1910.08079](https://arxiv.org/abs/1910.08079),
  DOI [10.3847/1538-3881/ab929c](https://doi.org/10.3847/1538-3881/ab929c).
  Code: <https://github.com/gmbrandt/xwavecal>. "Blind" echelle calibration with
  no anchor positions/true order numbers; ~1 m/s (HARPS).
- **Davenport et al. (2025)**, *Automated Spectroscopic Wavelength Calibration
  using Dynamic Time Warping.*
  arXiv:[2508.05862](https://arxiv.org/abs/2508.05862),
  DOI [10.48550/arXiv.2508.05862](https://doi.org/10.48550/arXiv.2508.05862).
  DTW aligns an arc to a calibrated template to recover non-linear dispersion
  with no initial guess; robust to resolution differences and missing/spurious
  lines. The strongest single match to a sequence-alignment approach.
  **Full text read — see §14.2** (PDF in
  [design/docs/davenport2025.pdf](docs/davenport2025.pdf)).
- **Qin et al. (2010)**, *Adaptive Wavelength Calibration Algorithm for LAMOST.*
  PASA 27, 265, DOI [10.1071/AS09038](https://doi.org/10.1071/AS09038).
  Automated, no-manual-interaction ID + polynomial fit at survey scale.
- **Balona (2010)**, *Wavelength calibration of arc spectra using intensity
  modelling.* MNRAS 409, 1601,
  DOI [10.1111/j.1365-2966.2010.17403.x](https://doi.org/10.1111/j.1365-2966.2010.17403.x).
  Uses modelled line *intensities* (not just positions) — a complementary signal
  a lamp-ID step could exploit.
- **PypeIt — Wavelength Calibration docs** (the baseline to beat):
  <https://pypeit.readthedocs.io/en/latest/calibrations/wave_calib.html>;
  template construction:
  <https://pypeit.readthedocs.io/en/latest/calibrations/construct_template.html>.

### 13.2 Blind geometric / pattern matching (by analogy to line ID)

- **Lang, Hogg, Mierle, Blanton & Roweis (2010)**, *Astrometry.net: Blind
  astrometric calibration of arbitrary astronomical images.* AJ 139, 1782.
  arXiv:[0910.2233](https://arxiv.org/abs/0910.2233),
  DOI [10.1088/0004-6256/139/4/1782](https://doi.org/10.1088/0004-6256/139/4/1782).
  Hashes 4-star asterisms into shift/scale/rotation-invariant codes — the core
  analogy for blind arc-line ID under unknown dispersion.
- **Pál & Bakos (2006)**, *Astrometry in Wide-field Surveys.* PASP 118, 1474.
  arXiv:[astro-ph/0609658](https://arxiv.org/abs/astro-ph/0609658),
  DOI [10.1086/508573](https://doi.org/10.1086/508573).
  Symmetric point-set matching in continuous triangle space.
- **Beroiz, Cabral & Sánchez (2020)**, *Astroalign.* Astron. Comput. 32, 100384.
  arXiv:[1909.02946](https://arxiv.org/abs/1909.02946),
  DOI [10.1016/j.ascom.2020.100384](https://doi.org/10.1016/j.ascom.2020.100384).
  Reference 3-point asterism matching; portable to line-position triangles.
- **Groth (1986)**, *A pattern-matching algorithm for two-dimensional coordinate
  lists.* AJ 91, 1244, DOI [10.1086/114099](https://doi.org/10.1086/114099).
  Origin of similar-triangle matching (pre-arXiv). *(unverified)*
- **Valdes et al. (1995)**, *FOCAS Automatic Catalog Matching Algorithms.* PASP
  107, 1119, DOI [10.1086/133667](https://doi.org/10.1086/133667).
  Classic triangle-invariant catalog matching. *(unverified)*

### 13.3 Machine learning for spectral feature / frame identification

- **Jankov & Prochaska (2018)**, *The SPectral Image Typer (SPIT).*
  arXiv:[1807.01761](https://arxiv.org/abs/1807.01761),
  DOI [10.48550/arXiv.1807.01761](https://doi.org/10.48550/arXiv.1807.01761).
  CNN classifies raw frames (Bias/Arc/Flat/…) at 98.7% — the upstream frame-type
  analog; the nearest ML precedent, though it does *not* identify lamp species.
- **Parks, Prochaska, Dong & Cai (2018)**, *Deep Learning of Quasar Spectra to
  Discover and Characterize Damped Lyα Systems.*
  arXiv:[1709.04962](https://arxiv.org/abs/1709.04962),
  DOI [10.48550/arXiv.1709.04962](https://doi.org/10.48550/arXiv.1709.04962).
  Multi-task CNN locates/parameterizes line features in 1D spectra.
- **Zhao et al. (2019)**, *Identifying MgII Narrow Absorption Lines with Deep
  Learning.* arXiv:[1904.12192](https://arxiv.org/abs/1904.12192),
  DOI [10.48550/arXiv.1904.12192](https://doi.org/10.48550/arXiv.1904.12192).
  CNN detects narrow lines ~94%, ~10⁴× faster — closest ML analog to detecting
  individual arc lines.
- **Keown et al. (2019)**, *CLOVER: Convnet Line-fitting Of Velocities in
  Emission-line Regions.* arXiv:[1909.08727](https://arxiv.org/abs/1909.08727),
  DOI [10.48550/arXiv.1909.08727](https://doi.org/10.48550/arXiv.1909.08727).
  1D CNNs classify/fit emission-line profiles in noisy spectra.

### 13.4 Line lists, atomic data & arc-lamp atlases (the match targets)

- **NIST Atomic Spectra Database (ASD)**, Standard Reference Database 78.
  <https://www.nist.gov/pml/atomic-spectra-database>;
  query: <https://physics.nist.gov/PhysRefData/ASD/lines_form.html>.
  Authoritative observed/Ritz wavelengths for every element — the ground truth.
- **NIST — Spectrum of Th-Ar Hollow Cathode Lamps (line lists).**
  <https://www.nist.gov/pml/spectrum-th-ar-hollow-cathode-lamps/spectrum-th-ar-hollow-cathode-lamps-line-lists>.
- **Redman, Nave & Sansonetti (2014)**, *The Spectrum of Thorium from 250 nm to
  5500 nm.* ApJS 211, 4. arXiv:[1308.5229](https://arxiv.org/abs/1308.5229),
  DOI [10.1088/0067-0049/211/1/4](https://doi.org/10.1088/0067-0049/211/1/4).
  Modern high-accuracy ThAr standard (19,874 Th lines).
- **Lovis & Pepe (2007)**, *A new list of thorium and argon spectral lines in the
  visible.* A&A 468, 1115,
  DOI [10.1051/0004-6361:20077249](https://doi.org/10.1051/0004-6361:20077249).
  The LP07 HARPS-based ThAr atlas (>8400 lines). *(no arXiv preprint)*
- **Murphy et al. (2007)**, *Selection of ThAr lines for wavelength calibration
  of echelle spectra.* MNRAS 378, 221.
  arXiv:[astro-ph/0703623](https://arxiv.org/abs/astro-ph/0703623),
  DOI [10.1111/j.1365-2966.2007.11768.x](https://doi.org/10.1111/j.1365-2966.2007.11768.x).
  Page + downloads: <http://astronomy.swin.edu.au/~mmurphy/thar/index.html>.
  Algorithm for selecting "clean" ThAr lines for a given spectrograph.
- **NOIRLab / NOAO Spectral Atlas Central** (ThAr, HeNeAr, CuAr, FeAr atlases):
  <https://noirlab.edu/science/data-services/other/spectral-atlas>;
  legacy ThAr: <https://www.noao.edu/kpno/tharatlas/thar/thar.html>.
  *(legacy `iraf.noao.edu/specatlas/*` links may be dead)*
- **ING Technical Note TN070** — spectral atlas of INT IDS calibration lamps:
  <https://www.ing.iac.es/astronomy/observing/manuals/ps/tech_notes/tn070.pdf>.
  *(unverified)*

### 13.5 Precision calibration sources (combs, etalons)

- **Murphy et al. (2007)**, *High-precision wavelength calibration … with laser
  frequency combs.* MNRAS 380, 839.
  arXiv:[astro-ph/0703622](https://arxiv.org/abs/astro-ph/0703622),
  DOI [10.1111/j.1365-2966.2007.12147.x](https://doi.org/10.1111/j.1365-2966.2007.12147.x).
- **Steinmetz et al. (2008)**, *Laser Frequency Combs for Astronomical
  Observations.* Science 321, 1335.
  arXiv:[0809.1663](https://arxiv.org/abs/0809.1663),
  DOI [10.1126/science.1161030](https://doi.org/10.1126/science.1161030).
- **Bauer, Zechmeister & Reiners (2015)**, *Calibrating echelle spectrographs
  with Fabry-Perot etalons.* A&A 581, A117.
  arXiv:[1506.07887](https://arxiv.org/abs/1506.07887),
  DOI [10.1051/0004-6361/201526462](https://doi.org/10.1051/0004-6361/201526462).
  Fuses a dense FP grid with a ThAr spectrum for absolute anchoring.
- **Wilken et al. (2012)**, *A spectrograph for exoplanet observations calibrated
  at the centimetre-per-second level.* Nature 485, 611,
  DOI [10.1038/nature11092](https://doi.org/10.1038/nature11092). *(no arXiv)*

### 13.6 Spectroscopic reduction pipelines & methodology

- **Prochaska et al. (2020)**, *PypeIt: The Python Spectroscopic Data Reduction
  Pipeline.* JOSS 5, 2308. arXiv:[2005.06505](https://arxiv.org/abs/2005.06505),
  DOI [10.21105/joss.02308](https://doi.org/10.21105/joss.02308).
  The project this work builds on.
- **Perley (2019)**, *Fully-Automated Reduction of Longslit Spectroscopy with
  LRIS at Keck (LPipe).* PASP 131, 084503.
  arXiv:[1903.07629](https://arxiv.org/abs/1903.07629),
  DOI [10.1088/1538-3873/ab215d](https://doi.org/10.1088/1538-3873/ab215d).
  Hands-off pipeline incl. automated wavelength solution via bright-triplet
  pattern matching.
- **Lam, Smith & Steele (2023)**, *ASPIRED.* AJ 166, 13.
  arXiv:[1912.05885](https://arxiv.org/abs/1912.05885),
  DOI [10.3847/1538-3881/acd75c](https://doi.org/10.3847/1538-3881/acd75c).
  Automated long-slit toolkit; wavelength module powered by RASCAL.
- **Piskunov, Wehrhahn & Marquart (2021)**, *Optimal extraction of echelle
  spectra (PyReduce).* A&A 646, A32.
  arXiv:[2008.05827](https://arxiv.org/abs/2008.05827),
  DOI [10.1051/0004-6361/202038293](https://doi.org/10.1051/0004-6361/202038293).
  Docs: <https://pyreduce-astro.readthedocs.io/en/latest/wavecal_linelist.html>.
- **Labrie et al. (2023)**, *DRAGONS — A Quick Overview.*
  arXiv:[2310.03048](https://arxiv.org/abs/2310.03048),
  DOI [10.48550/arXiv.2310.03048](https://doi.org/10.48550/arXiv.2310.03048).
  Gemini's Python reduction platform.
- **IRAF `identify`/`reidentify`/`ecidentify`** — the canonical interactive/
  semi-automatic tools (incl. the `AUTOIDENTIFY` line-ratio pattern matcher):
  <https://iraf.readthedocs.io/en/latest/tasks/noao/onedspec/reidentify.html>.
- **specreduce** (Astropy): <https://specreduce.readthedocs.io/en/stable/>,
  code <https://github.com/astropy/specreduce>, line lists
  <https://github.com/astropy/specreduce-data>.
- **Learn Astropy** — *Spectroscopic Data Reduction Part 2: Wavelength
  Calibration*: <https://learn.astropy.org/tutorials/2_WavelengthCalibration.html>.
  Worked end-to-end example querying NIST for IDs.

---

## 14. In-depth reads of key prior-art papers

Full-text notes on papers the user supplied as PDFs in
[design/docs/](docs/) (added v0.3). Both are squarely the **calibration** half
of the project (step 2). **Neither attempts lamp identification (step 1)** —
both *assume the lamp/template is already known* — which directly corroborates
the §13 gap: blind lamp-ID is the genuinely novel piece.

### 14.1 RASCAL — Hough transform + RANSAC (Veitch-Michaelis & Lam 2019)

[design/docs/veitch2019.pdf](docs/veitch2019.pdf) · ADASS XXIX proceedings ·
arXiv:1912.05883. A Python library (the first public astronomy implementation of
the **Song et al. 2018**, *Appl. Opt.* 57, 6876 algorithm), developed for the
ASPIRED pipeline.

**Problem framing.** Given detected peak pixels `P` and an atlas of emission
lines `A` [λ], find for each peak its matching atlas line; then fit
`f(x, p) = xλ`. In the general case *any* peak could match *any* atlas line, with
spurious peaks, undetected atlas lines, blends, and centroid noise — so robust
fitting is essential.

**Required inputs (note — not fully blind).** An atlas of calibration lines (so
*the lamp must be known*), a peak list (e.g. `scipy.signal.find_peaks`), and
*"some information about the system"*: a wavelength range of interest (default
tolerance **±200 Å**) and a dispersion `D` constrained from the pixel count and
wavelength range. So RASCAL automates step 2 but presupposes step 1 and a rough
configuration.

**Algorithm.**
1. Filter the atlas to the range of interest → `A'`.
2. Enumerate the full Cartesian product `A' × P` (all peak↔line pairs).
3. **Hough transform** over the *linear* model `xλ = D·x + c`: every pair votes
   into a 2D accumulator in `(D, c)` (dispersion, intercept) space. Dense cells
   = "candidate sets" of mutually-consistent correspondences.
4. **Improvement over Song et al.:** rather than fit each candidate set
   separately and pick the best (which fails under strong curvature), they take
   the **top N = 20** candidate sets *simultaneously* and, for each peak, choose
   the most common best-fit atlas line across them — a piecewise-linear-like
   vote that recovers matches across both the red and blue ends.
5. **RANSAC** robustly fits a 4th–5th-order polynomial to the surviving
   correspondences; the result can seed a more sophisticated instrument model.

**Performance / status.** Pure-Python (numpy/scipy/matplotlib/astropy), < 10 s on
a laptop, demonstrated on a Xe arc from SPRAT (Liverpool Telescope).

**Relevance to the Holy Grail.** This is the **Hough + RANSAC** route, conceptually
close to PypeIt's own from-scratch matching but voting in linear `(D, c)` space
rather than scale-invariant pattern space. Key limitation for our goal: the
candidate generation is anchored on a *linear* dispersion approximation and a
±200 Å range prior, and it still needs the lamp identity. A blind algorithm
would have to drop both the range prior and the lamp prior.

### 14.2 DTW — sequence alignment to a template (Davenport et al. 2025)

[design/docs/davenport2025.pdf](docs/davenport2025.pdf) · arXiv:2508.05862 ·
introduces the **PyKOSMOS** toolkit. Applies **Dynamic Time Warping** (from
speech recognition; here the Giorgino 2009 R/Python implementation) to align a
query arc to a *calibrated template* arc, recovering even non-linear and
discontinuous dispersions with **no initial guess**.

**Two-step algorithm.**
1. **DTW alignment.** Boxcar-extract query and template spectra; normalize each
   by its median flux (so amplitudes are comparable regardless of exposure).
   Run DTW with `open_begin`/`open_end` (align the query to a *subsection* of a
   larger template) and `step_pattern='asymmetric'`. DTW returns the warp that
   maps query→reference using the **entire spectrum**, so even weak lines
   contribute.
2. **Line-based refinement.** Raw DTW can produce "jumpy"/non-physical
   pixel-level warps, so they then detect peaks (`scipy.find_peaks`, ≥ 5 px
   apart, Gaussian-centroided), transfer each line's wavelength from the
   template via the alignment, and fit a smooth model (polynomial, spline, or
   Gaussian Process) — exactly the IRAF `IDENTIFY` final step. They explicitly
   **warn against using raw DTW alone** for narrow-line arcs.

**Validation.** A deliberately hard synthetic arc (30 lines, *discontinuous*
piecewise log/linear dispersion, 25 % of lines missing, low S/N, extra reference
lines) solved in **1.6 s**. Real KOSMOS Ne/Ar/Kr across six grisms; and
cross-instrument transfer — KOSMOS Ne+Ar templates successfully calibrated DIS
HeNeAr at R≈7000 despite missing He and different optics.

**Limitations.** Because DTW matches the *whole* spectrum (amplitudes and
profiles, not just peak positions), it **fails when instruments differ strongly**
(e.g. DIS R300, dominated by scattered light and broadening) and when too few
lines are present ("Blue Low" grism). The authors recommend **per-instrument
templates**. Stated aim: replace IRAF `IDENTIFY`; not EPRV-precision. DTW could
also align each echelle order given a template.

**Relevance to the Holy Grail.** This is the **template-based** route — strictly
more demanding on prior knowledge than RASCAL: it needs a *calibrated reference
arc of (roughly) the same lamp combination*, i.e. it presupposes step 1 even
more directly. Its strength (robustness to non-linear/discontinuous dispersion,
differing resolution) and its weakness (amplitude/profile sensitivity from using
the whole spectrum) are both instructive: a Holy Grail solver likely wants
DTW-like tolerance to non-linearity **without** DTW's dependence on a matched
template or on line amplitudes.

### 14.3 Takeaways for the project

- Both leading automated methods are **step-2 only** and assume the lamp is
  known (RASCAL via the atlas + range prior; DTW via the template). The blind
  **lamp-identification** problem (step 1) remains open — the project's clearest
  novel contribution.
- Two complementary matching paradigms to draw on: **parameter-space voting**
  (RASCAL's Hough in `(D, c)`; PypeIt's `(wvcen, disp)` histogram) and
  **sequence alignment** (DTW). A blind solver may need to combine the
  scale/shape-invariance of the former with the non-linear tolerance of the
  latter.
- Recurring robustness tools across all prior art: RANSAC / robust polynomial
  fitting, redundant voting across many candidate correspondences, and a final
  peak-based smooth fit. Amplitude information is double-edged — Balona (2010)
  and DTW exploit it, but it hurts cross-instrument transfer.

---

## Version history

| Version | Date | Summary |
|---|---|---|
| 0.1 | 2026-06-20 | Initial draft. §§1–12 synthesized from the PypeIt, dev-suite, and `arclines` codebases (the in-repo state of the art). |
| 0.2 | 2026-06-20 | Added §0 (project goal: blind lamp-ID + calibration of an unlabeled arc, per user). Added §13 (external arXiv + web literature with URLs/DOIs). Added versioning + this history. Marked the prior Q&A as resolved. |
| 0.3 | 2026-06-20 | Added §14 — full-text reads of the two user-supplied PDFs (RASCAL/Hough+RANSAC; Davenport DTW), with cross-refs from §13.1. Confirmed both are step-2-only (lamp assumed known), reinforcing blind lamp-ID as the open problem. |
| 0.4 | 2026-06-20 | Added §0.1 (data corpus): per user, leverage dev-suite `RAW_DATA/` (labelled raw arcs, ~45 instruments), `reid_arxiv/` (242 solved reference arcs = calibration ground truth), and `arc_lines/lists/` (atomic data). Resolved Q3. |

---

## Q&A

*(Resolved questions retained for the record.)*

1. **Scope / next steps.** *(asked v0.1)* What should the next addition be —
   external technical documents, or a deeper algorithm dive?
   **→ Answered:** the user will direct next steps via prompts. (v0.2 added the
   external-literature survey, §13.)

2. **End goal.** *(asked v0.1)* Improve, replace, or document the current
   auto-ID?
   **→ Answered:** *replace* — build an entirely new algorithm that takes an
   unlabeled arc spectrum and (1) identifies the arc lamp(s) and (2) calibrates
   it, with no human input. Captured in §0.

3. **Corpus for blind lamp-ID.** *(asked v0.3)* Can the dev-suite `RAW_DATA/`
   and `reid_arxiv/` serve as the labelled corpus, with a preferred split?
   **→ Answered:** *yes — definitely leverage those.* Captured in §0.1. (A
   specific train/test split / held-out instruments remain to be decided.)

## Requests

*(Requests for additional material are logged here.)*

- **(Open)** The "Technical documents on wavelength calibration" listed in the
  project goals are not yet present in the repos. If you can drop relevant
  papers/notes into a folder (e.g. `design/refs/`), I will incorporate them
  alongside the §13 survey.
