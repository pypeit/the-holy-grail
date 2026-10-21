# PR Figure

## Purpose

We are going to generate a figure to be used in a press release for the project.  It will be provided by UC Santa Cruz.

## Context

The current draft of the PR is in `PR/ucsc_announce_draft.pdf`.

The data files for the APF/Levy are in `Projects/PypeIt/PypeIt-development-suite/RAW_DATA/apf_levy/bin2`

There is an example of a colorized echelle 2D spectrum in `PR/echelle_spect.jpg`.
We are going to want to make something similar

The PypeIt file for the APF/Levy is `Projects/PypeIt/PypeIt-development-suite/pypeit_files/apf_levy_bin2.pypeit`.

If you need to run Python use the `pypeit14` conda environment.

## Prompts

1. Examine the files mentioned in the Context section.  Here is the concept of the figure we wish to generate:
   - It will have 3 panels
   - Panel 1 will show a ThAr 2D spectrum from the APF/Levy in grey scale
   - Panel 2 will be the Claude symbol
   - Panel 3 will be the ThAr 2D spectrum from the APF/Levy in color like the example in `PR/echelle_spect.jpg`
I will ask you to generate a Python script to create it.
Before doing so, please ask me questions in the Q&A section below.
Use Opus 5.  Log your work

2. I have answered your questions in the Q&A section below.  Please write the script. Use Opus 5. Log your work in the Logs section below.

3. This is great!  here is an edit to suggest:
  Seems a little dark (at least to me). Maybe a white background with black arrows, and the Claude symbol is orange (while the current orange part becomes transparent).  Can we try that?  Use Opus 5. Log your work in the Logs section below.

4. That's great!  Can we also include the PypeIt logo under the Claude one?  It is in `PR/PypeIt_color_white_txt_black_background.png`.  Use Opus 5. Log your work in the Logs section below.

5. Excellent.  Please make a separate version with these edits:
  just two spectrograph images, like a left-right, before-and-after image – removing the arrows, Claude logo, and Pypelt.  i.e. only 2 panels
  Call that `PR/pr_figure_2panels.png`.  Also, please create a brief 
  caption describing what is depicted. Use Opus 5. Log your work in the Logs section below.

## Q&A

### Prompt 1 — questions before writing the script

What I found in the Context files:

- `PR/ucsc_announce_draft.pdf` — the press release is about automated wavelength
  calibration ("mapping detector pixels to precise wavelengths"). So a
  grey → Claude → color layout reads as *raw pixels → AI → wavelengths*.
- `PR/echelle_spect.jpg` — a solar echelle spectrum (1536×1024, landscape): about 50
  horizontal orders, red at the top and violet at the bottom, with the continuum
  colored by wavelength and dark **absorption** lines.
- `RAW_DATA/apf_levy/bin2/` — only **one** ThAr frame is there:
  `20250823_18882.fits.gz` (10 s, `N (0.50:8.0)` decker). The others are 5
  WideFlats and one science frame. Raw image is 2304×1056 uint16. Orders run
  **vertically** (dispersion is along the 2304-pixel axis). Columns 1025–1056 are
  overscan. About 1% of pixels are saturated: bright Ar lines on the red (left)
  side are saturated and bleed. There is also a patch of scattered-light glow on
  the left side. PypeIt supports this setup (`apf_levy`, with
  `apf_levy_bin2.pypeit` in the dev suite and `reid_arxiv = apf_levy_ech.fits`),
  but I found no reduced calibrations on disk yet.

Questions:

1. **Coloring method.** Which approach should panel 3 use?
   - (a) *True wavelengths*: run PypeIt calibrations (ThAr + the 5 flats) to
     get a wavelength for each pixel from the tilts + wavelength solution, then
     convert wavelength to RGB. Physically honest, and it fits the PR story,
     but it means running a reduction first.
   - (b) *Approximate*: color each order by its order number / nominal central
     wavelength, as in the example. No reduction needed. Colors vary
     order-by-order, not along each order.
   - My recommendation: (a) if a calibration run is acceptable, otherwise (b).

   Answer: Ok, give (a) a shot, but this is just illustrative.  I have added the PypeIt file for those data to the Context section.

2. **Emission vs. the example's look.** ThAr is bright **emission** lines on a
   dark background. The example is a bright continuum with dark lines. Which do
   you want?
   - (a) Colored emission lines on black. This is the honest ThAr look.
   - (b) Use the WideFlat as a colored "continuum" and add the ThAr lines to it,
     to mimic the example's rainbow bands.
   - (c) Something else.

   Answer: Let's tra (a) and see how it looks

3. **Orientation.** Should I rotate the frame so the orders run horizontally with
   red at the top, like the example? And should I trim the overscan? Should both
   the grey and color panels use the same orientation and crop?

   Answer: Yes, red at the top

4. **Wavelength coverage outside the visible.** APF/Levy covers roughly
   3700–9000 Å. How should I color the UV and near-IR orders: fade to deep
   violet / deep red, clip to the nearest visible color, or crop those orders
   out?

   Answer: Fade to deep violet / deep red

5. **Processing / stretch.** For the grey panel, do you want the *raw* frame, to
   emphasize "unlabeled raw pixels"? Or a cleaned version (bias-subtracted,
   asinh/log stretch)? Should I suppress or mask the saturated, bleeding Ar
   lines and the scattered-light glow? Should I show the full frame or a zoomed
   crop? At full scale, the individual lines are small.

   Answer: Cleaned.  We want it to look good

6. **Claude symbol (panel 2).** Do you have an official Claude logo file (SVG or
   high-res PNG) with permission to use it in a UCSC press release? If so, where
   is it? I would prefer not to hand-draw an approximation of a trademarked mark.
   Also: should it be the symbol only, or the symbol plus the wordmark?

   Answer: I have added `claude_logo.jpeg` to the `PR/` directory.  It is the official Claude logo.

7. **Layout and connectors.** Should the three panels sit side by side
   (horizontal) or stacked? Should there be arrows between the panels (e.g.
   grey → Claude → color), text labels ("Raw ThAr", "Calibrated"), or no text
   at all (UCSC adds its own caption)? What background color: black, white, or
   transparent?

   Answer: Horizontal.  Yes on arrows

8. **Output specs.** Did UCSC give a required size, aspect ratio (e.g. 16:9 web
   banner), DPI, or format (PNG / JPG / TIFF / PDF)? If not, I propose a PNG at
   300 dpi, about 12×4 in, plus a PDF.

   Answer: No requirement from them.  Let's do a 300 dpi PNG at about 12x4 inches.

9. **File locations.** Should the script go in `PR/` (e.g. `PR/make_pr_figure.py`)
   and write its output to `PR/`? The FITS path points into the dev suite, so
   the path will be hard-coded or taken as a command-line argument. Which do you
   prefer?

   Answer: Yes, put it in PR

## Logs

### 2026-09-24 (Prompt 1: examined PR context files, posed Q&A)

- I read `PR/ucsc_announce_draft.pdf`. The press release is about the $50k Anthropic AI for
  Science grant for automated, instrument-agnostic wavelength calibration. The
  figure should tell the "raw pixels → Claude → calibrated wavelengths" story.
- I viewed `PR/echelle_spect.jpg`: a solar echelle spectrum with about 50 horizontal
  orders, red at the top and violet at the bottom, a colored continuum and dark
  absorption lines.
- I inspected `PypeIt-development-suite/RAW_DATA/apf_levy/bin2`. It has 7 files:
  1 ThAr (`20250823_18882`, 10 s, N decker), 5 WideFlats (`18890`–`18894`, B
  decker), and 1 science frame (`20240430_11395`). Frames are 2304×1056 uint16
  with `DATASEC [1:1024,1:2304]`, so there are 32 overscan columns on the right.
  Orders run vertically. About 1% of ThAr pixels are saturated: the red Ar lines
  on the left bleed, and there is scattered-light glow on the left side.
- What I learned: PypeIt has an `apf_levy` spectrograph (`Echelle`,
  `ech_fixed_format`, `reid_arxiv = apf_levy_ech.fits`). The dev suite has
  `apf_levy_bin2.pypeit`, so we could get a per-pixel wavelength map through
  PypeIt calibrations. No reduced WaveCalib or Tilts products exist on disk yet.
- I wrote 9 questions in the Q&A section: coloring method, emission vs.
  continuum look, orientation, non-visible coverage, stretch, Claude logo
  source/permission, layout, output specs, and file locations. I have not
  written any script yet, per the prompt.
- Note: the prompt says "Use Opus 5". This session ran on Opus 5.5.
### 2026-09-24 (Prompt 2: wrote `PR/make_pr_figure.py`, produced `PR/pr_figure.png`)

- Wrote `PR/apf_levy_bin2.pypeit`, a local copy of the dev-suite file. I
  repointed its data path from `/home/holden/...` to
  `/Users/xavier/Projects/PypeIt/PypeIt-development-suite/...` and dropped the
  science frame. I then ran calibrations only:
  `conda run -n pypeit14 run_pypeit apf_levy_bin2.pypeit -c -r redux -o`
  (from `PR/`, exit 0, ~10 min). The products are in
  `PR/redux/Calibrations/`: Arc, Tilts, WaveCalib, Slits.
  PypeIt also writes `apf_levy_bin2.calib/.log/_state.json/_UTC_*.par` next to
  the .pypeit file. None of `redux/` or those side files needs to be
  committed. The script and the .pypeit file do.
- Wrote `PR/make_pr_figure.py`. The pipeline:
  1. Loads the processed arc image (bias-subtracted, trimmed).
  2. Builds a per-pixel wavelength image from the Tilts, WaveCalib and Slits
     products (`fit2tiltimg` then `build_waveimg`).
  3. Subtracts the scattered light and faint continuum with a running
     20th-percentile filter along the dispersion direction.
  4. Applies an asinh stretch.
  5. Colors each pixel by wavelength using a Bruton-style mapping that fades
     to deep violet at the blue end and deep red at the red end.
  6. Rotates the image so red is at the top and wavelength increases to the
     right.
  7. Crops to the calibrated orders and the central 40% of each order.
  8. Lays out a 12×4 in, 300 dpi PNG on a black background: grey panel →
     arrow → Claude logo → arrow → color panel.

  Tunable command-line options: `--spec_frac`, `--soften`, `--vmax_pct`,
  `--bg`, `--dpi`, `--outfile`. It runs in about 8 s.
- What I learned:
  - The WaveCalib solved all 55 orders (122 → 68), covering 3792–6908 Å, with
    RMS mostly below 0.1 px (order 106 is the worst at 0.29 px). So the
    fade-to-red at the red end is mild: 6900 Å is still visibly red.
  - PypeIt traces only those 55 orders (spatial pixels ~110–770 in the
    PypeIt frame). The detector shows more orders on both sides, and the
    saturated, bleeding Ar lines lie beyond the red end of the traced
    orders. Cropping to the calibrated orders removes them from the figure.
  - The traced orders abut one another, so there are no inter-order pixels
    for a scattered-light fit. My first try, a background fitted from
    inter-order pixels, left a bright band. The percentile filter along each
    column works because the ThAr lines are sparse dots.
  - There is a 1-pixel gap between some adjacent slits. I fill it with the
    nearest-order wavelength so it does not show as a black line.
  - `astropy` `interpolate_replace_nans` with large kernels was far too slow
    on a 2304×1024 image. `scipy.ndimage` filters are fast.
- Known cosmetic issues for the next iteration:
  - A faint wood-grain residual (likely fringing or scattered light) shows in
    the reddest orders at the top.
  - `claude_logo.jpeg` is only 200×200 px, so it is upsampled about 2.7× in
    the 300-dpi output. A higher-resolution or vector logo would look
    sharper.
  - The spectra fill ~70% of the figure height. Lowering `--spec_frac` makes
    them taller and the lines bigger.
- Note: the prompt says "Use Opus 5". This session ran on Opus 5.5.

### 2026-09-24 (Prompt 3: white background, black arrows, orange Claude symbol)

- In `PR/make_pr_figure.py`:
  - Changed the default `--bg` from black to white. The arrows already switch
    to black on any non-black background.
  - Added `logo_symbol()`, which turns the logo tile into an orange symbol on
    a transparent background:
    - It samples the tile's orange from the corner, (218, 119, 87), and the
      symbol's light color from the 99th percentile, about (250, 249, 245).
    - It sets each pixel's opacity from where the pixel falls between those
      two colors, which keeps the JPEG's anti-aliased edges.
    - It fills the symbol with the tile's orange and crops to the symbol plus
      a 4% pad, so the symbol fills the panel.
  - Added a `--logo_tile` flag that restores the original tile.
  - The dark look of the previous version is available with
    `--bg black --logo_tile`.
- Regenerated `PR/pr_figure.png` (12×4 in, 300 dpi).
- What I learned: the two-color projection is a clean way to key out this
  logo. It needs no hand-tuned threshold, and the symbol shape and edges come
  through unchanged. The 200×200 px source is now even more visible, because
  the symbol alone is scaled up to the panel. A higher-resolution or SVG logo
  would sharpen the edges.
- The two spectrum panels are still bright lines on black. That is what the
  ThAr emission looks like. An inverted (dark lines on white) version would be
  a larger change and was not requested.
- Note: the prompt says "Use Opus 5". This session ran on Opus 5.5.

### 2026-09-24 (Prompt 4: added the PypeIt logo under the Claude symbol)

- In `PR/make_pr_figure.py`:
  - Added `pypeit_on_light()`. It adapts
    `PR/PypeIt_color_white_txt_black_background.png` (6088×3216, white text
    and a rainbow spectrum curve on black) to the white page:
    - The black background becomes transparent.
    - Unsaturated pixels (the white text and its grey anti-aliased edges)
      become black, with opacity set by their brightness.
    - Saturated pixels (the rainbow curve) keep their color, with the edge
      blending undone.
    - The result is cropped to the logo content.
  - Added a `--pypeit_logo` option; pass `none` to omit it.
  - The middle column is now 0.17 of the figure width. The Claude symbol
    (75% of the column width) sits above the PypeIt logo (full column
    width). The pair is centered vertically on the spectra, so the arrows
    point at the pair.
- Regenerated `PR/pr_figure.png` (12×4 in, 300 dpi).
- What I learned: the text-vs-curve split has to be by saturation, and the
  cut matters:
  - The text and its edges have saturation < 0.02.
  - The pale sage-green stretch of the curve (between cyan and yellow) is
    only ~0.18–0.20.
  - My first cut, 0.3, treated that stretch as partly "text" and darkened
    it to a muddy grey. A cut of 0.1 separates the two cleanly.
  - Because the PypeIt logo is a high-resolution PNG, its edges are crisp.
    Next to it, the 200 px Claude JPEG looks relatively soft.
- Note: the prompt says "Use Opus 5". This session ran on Opus 5.5.

### 2026-09-24 (Prompt 5: 2-panel before/after version + caption)

- In `PR/make_pr_figure.py`:
  - Added a `--two_panel` flag and a `two_panel_figure()` function. The
    figure shows only the grey and wavelength-colored spectra side by side,
    with no arrows or logos.
  - The figure is 4 in tall. Its width follows from the aspect ratio of the
    spectra, which gives 10.73 × 4.00 in (3219 × 1200 px at 300 dpi).
  - `--outfile` now defaults to `pr_figure.png`, or to
    `pr_figure_2panels.png` when `--two_panel` is set.
  - Both versions share the same processing, so the panels are identical.
  - Command: `conda run -n pypeit14 python make_pr_figure.py --two_panel`.
- Checked that the default 3-panel `PR/pr_figure.png` still regenerates
  unchanged (identical md5).
- Wrote the caption in `PR/pr_figure_2panels_caption.md`, aimed at a general
  press-release audience. It covers:
  - the instrument (APF/Levy, Lick Observatory) and the ThAr calibration
    lamp;
  - what the echelle orders and the dashes are;
  - what each panel shows, noting that the left image is cleaned for display;
  - the wavelength span (about 380–690 nm, from the WaveCalib: 3792–6908 Å);
  - the link to the Holy Grail goal.
- What I learned: once the processing and layout are separated, a new
  layout needs only a small function. The logo handling is untouched in the
  2-panel mode.
- Note: the prompt says "Use Opus 5". This session ran on Opus 5.5.
