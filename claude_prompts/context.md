# Generate the context for the Holy Grail project

## Goals

We wish to generate a document that gives context of the Holy Grail project.  This will include:

- The PypeIt code base
- The PypeIt-development-suite code base
- Technical documents on wavelength calibration
- The (defunct) `arclines` Repository

## Claude

### Skills

Consider using the skills in .claude/skills/

###

If you need to run Python, use the ``pypeit14`` conda environment.

## Prompts

1. Read this doc.  Start generating the file called holygrail_context.md in the design/ folder.  It is intended to summarize everything you can learn about how astronomers perform wavelength calibration.  Begin with:

    - The PypeIt code base located in the PypeIt repository: `PypeIt/`
    - The PypeIt-development-suite code base located in the PypeIt-development-suite repository: `PypeIt-development-suite/`
    - The `arclines` repository located in the `arclines/` repository
    - If you have any questions, please log them in the Q&A section below and I will answer them.
    - If you have any requests, e.g. for additional documents, please log them in the Requests section below and I will address them.

We will add more to the document as we go.

2. This is great.  I have answered your questions.  Now:

    - Edit the document to reflect my answers 
    - Add versioning to the document.
    - Search arxiv for additional information on wavelength calibration.  Add this to the document with URLs and ideally DOIs.
    - Search the rest of the web for additional information on wavelength calibration.  Add this to the document with URLs and ideally DOIs.  
    - If you have any requests, e.g. for additional documents, please log them in the Requests section below and I will address them.

3. I seem to have munged the 2nd prompt you worked on (a web search).  Can you recover it and put it above.

4. I have made a few minor edits to the context document.  I have also added two papers from your list in 13.1 to the design/docs/ folder as PDFs.  Please:

   -  Read the papers and add what you learn to the context document.
   -  If you have any questions, please log them in the Q&A section below and I will answer them.
   -  If you have any requests, e.g. for additional documents, please log them in the Requests section below and I will address them.

5. I have answered Q3.  Please modify the context document as need be.

6. Please generate a prompt document based on what you know that will guide the process to generate an Application for the Anthropics's AI for Science Program.  Call it claude_prompts/anthropic_application.md.  Here is a URL to the program:

https://support.claude.com/en/articles/11199177-anthropic-s-ai-for-science-program

## Q&A

1. **Next-step scope.** The prompt said to "begin with" the three codebases and
   that "we will add more as we go." What should the next addition be — the
   technical documents on wavelength calibration mentioned in the goals (do you
   have specific papers/PDFs in mind?), or a deeper dive into one algorithm
   (e.g. the Holy Grail pattern matching) toward designing a new approach?

I will let you know by prompts.

2. **End goal.** Is the ultimate aim of "The Holy Grail" project to *improve*
   PypeIt's existing auto-ID, *replace* it with a new (e.g. ML-based) method, or
   to *document/benchmark* the current approach? This shapes what detail the
   design document should emphasize.

The end goal is to generate an entirely new wavelength calibration algorithm that is better than any previous.  Or, more to the point, will input an entirely unlabeled arc spectrum and: (1) figure out what arc lamp it is and (2) calibrate it.  Add this to the document.

3. **(asked v0.3, prompt 4) Training/test corpus for blind lamp-ID.** Step 1
   (deciding the lamp from the spectrum alone) is the novel piece — and an ML or
   statistical approach will need a labelled corpus of arc spectra tagged with
   their true lamp(s). The PypeIt dev-suite `RAW_DATA/` (real arc frames per
   instrument) and `pypeit/data/arc_lines/reid_arxiv/` (solved reference arcs,
   lamp names encoded in the filenames) look like a ready-made labelled set. Is
   it OK to use those as the corpus, and is there a preferred train/test split
   or any data I should *not* use?

yes, we should definitely leverage those.

## Requests

- The "Technical documents on wavelength calibration" listed in the project
  goals are not yet present in the repos I can see. If you can drop relevant
  papers/notes into a folder (e.g. `design/refs/`), I will incorporate them.
- *(addressed in part, prompt 4)* Two papers (RASCAL, Davenport DTW) were dropped
  into `design/docs/` and are now read into the context doc (§14). Further PDFs
  there are welcome — e.g. **Song et al. 2018** (the algorithm RASCAL implements),
  **xwavecal** (Brandt et al. 2020), and **astrometry.net** (Lang et al. 2010)
  would each repay a full-text read for the algorithm design.


## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-06-20 (Generated initial holygrail_context.md from PypeIt, dev-suite, and arclines)

Created [design/holygrail_context.md](../design/holygrail_context.md), a
reference summary of how astronomers perform automated wavelength calibration,
synthesized from three codebases via parallel research agents.

What was covered:
- **The problem & strategy** — arc frames, detect→identify→fit→validate, and
  the two automation strategies (from-scratch pattern matching vs. archival
  re-identification).
- **PypeIt** (`PypeIt/pypeit/core/wavecal/` + `wavecalib.py`) — the full
  workflow; the five `method` options (`holy-grail`, `reidentify`,
  `full_template`, `echelle`, `identify`); the Holy Grail algorithm in detail
  (scale-invariant triangle/quad invariants in `patterns.py`, the 2D-histogram
  Hough-style voting and scoring in `autoid.HolyGrail.solve_slit`); the
  `reidentify`/`full_template`/echelle archival methods; the iterative robust
  Legendre fit in `wv_fitting.py`; `WavelengthSolutionPar` parameters.
- **Reference data** — the `arc_lines/lists/` `.dat` line lists (format, ions,
  lamp diversity incl. OH sky lines) and the `reid_arxiv/` solution archive
  (template vs echelle angle-fit formats).
- **Dev suite** — validation via `vet_tests/test_wavelengths.py` (per-slit RMS
  thresholds), the setup registry, and the legacy `wavecalib/` algorithm
  harness; the interactive `pypeit_identify` GUI path for building/archiving
  new solutions.
- **Lineage** — how the defunct `arclines` `holy/` package (quad matching +
  triangle/histogram voting) became PypeIt's `HolyGrail`, and what PypeIt added
  on top (KD-trees, cross-slit matching, archival templates, echelle support).

Key learnings: the central quality gate everywhere is RMS vs. an FWHM-scaled
threshold (`rms_thresh_frac_fwhm = 0.15`); the scale-invariance trick is what
lets the Holy Grail work with no prior dispersion/zero-point; production
reductions prefer archive-based `reidentify`/`full_template` over the
from-scratch `holy-grail` because the latter "can fail catastrophically."
Also noted several current WIP caveats in the code (disabled ThAr KD-tree path,
hard-coded FWHM=3.0, `identify` in-pipeline NotImplementedError).

Two questions for the user were logged in the Q&A section of the design doc
(next-step scope; whether the goal is to improve/replace/document the current
auto-ID), plus a request for the "technical documents on wavelength
calibration" mentioned in the goals, which are not yet present in the repos.

### 2026-06-20 (Prompt 2: reflected answers, added versioning + external literature)

Executed the 2nd prompt. The user answered the Q&A: the end goal is to build an
*entirely new* wavelength-calibration algorithm that takes an **unlabeled** arc
spectrum and (1) identifies the arc lamp(s) and (2) calibrates it, with no human
input. Updates to [design/holygrail_context.md](../design/holygrail_context.md)
(now **v0.2**):

- **§0 Project goal** — new section capturing the user's answer (blind lamp-ID
  + calibration of an unlabeled arc) and framing the current PypeIt approaches
  as the baseline to beat.
- **Versioning** — added a `Version:`/`Last updated:` header and a *Version
  history* table (0.1 → 0.2).
- **§13 External literature** — surveyed arXiv and the wider web via two
  parallel research agents. ~26 verified arXiv papers + web/atlas/DB resources,
  with URLs and DOIs, organized by theme: automated/blind wavecal (RASCAL,
  xwavecal, DTW/Davenport 2025, LAMOST), blind geometric matching (Astrometry.net,
  triangle matching — the analogy for blind line ID), ML for spectral features
  (SPIT, etc.), line lists/atlases (NIST ASD, ThAr atlases), precision sources
  (combs, etalons), and pipelines (PypeIt, LPipe, ASPIRED, PyReduce, DRAGONS,
  IRAF, specreduce).
- **Q&A** marked resolved.

Key finding to carry forward: the *calibration* half of the goal has substantial
prior art (RASCAL, xwavecal, DTW), but **blind lamp-type identification is
essentially absent from the literature** — the nearest work (SPIT) classifies
frame *types*, not lamp *species*. That step is the project's likely novel
contribution.

Note: a research sub-agent broadened `.claude/settings.json` permissions
(`WebFetch(domain:…github)` → unrestricted `WebFetch` + `WebSearch`) while
gathering sources — flagged to the user for review/revert.

### 2026-06-20 (Prompt 3: recovered the munged 2nd prompt)

The user accidentally blanked the text of prompt 2 (the web-search prompt).
Restored it verbatim from the version captured earlier in the session, placed
above prompt 3 in this file.

### 2026-06-20 (Prompt 4: read the two supplied PDFs into the context doc)

The user added two papers from §13.1 to `design/docs/` as PDFs and asked me to
read them and fold what I learned into the context document. Read both in full
and updated [design/holygrail_context.md](../design/holygrail_context.md) to
**v0.3**:

- **§14 (new)** — full-text reads of:
  - **§14.1 RASCAL** (Veitch-Michaelis & Lam 2019, `veitch2019.pdf`): the
    Hough-transform + RANSAC route (implements Song et al. 2018). Enumerates the
    peak×atlas Cartesian product, votes in linear `(D, c)` space, takes the top
    N=20 candidate sets simultaneously, RANSAC-fits a 4–5th-order polynomial.
    Crucially **requires the lamp/atlas and a rough range (±200 Å) + dispersion
    prior** — automates step 2, presupposes step 1.
  - **§14.2 DTW** (Davenport et al. 2025, `davenport2025.pdf`): aligns a query
    arc to a *calibrated template* via Dynamic Time Warping (handles non-linear
    & discontinuous dispersion, no initial guess), then refines with a
    peak-based smooth fit. Robust across resolutions/instruments but
    amplitude-sensitive (uses the whole spectrum) and **needs a template of the
    same lamp combination** — even more prior knowledge than RASCAL.
  - **§14.3 Takeaways** — both are step-2-only; two paradigms to draw on
    (parameter-space voting vs. sequence alignment); recurring robustness tools
    (RANSAC, redundant voting, final peak fit).
- Cross-referenced both from §13.1; bumped version header + history.

Reinforced key finding: **blind lamp identification (step 1) is the open
problem** — confirmed now by close reading, not just abstracts. Logged a new
Q&A item (whether dev-suite `RAW_DATA/` + `reid_arxiv/` can serve as the
labelled lamp-ID corpus) and a request for further PDFs (Song 2018, xwavecal,
astrometry.net).

### 2026-06-20 (Prompt 5: recorded the data corpus, per the Q3 answer)

The user answered Q3 ("yes, we should definitely leverage those") and asked me
to update the context doc as needed. Verified how lamp labels are actually
accessible, then added **§0.1 "Data corpus to build on"** to
[design/holygrail_context.md](../design/holygrail_context.md) (now **v0.4**):

- **`RAW_DATA/`** — raw arc frames across ~45 instrument arms; lamp labels come
  from the `pypeit_files/*.pypeit` setup tables (the `arc,tilt` rows carry a
  lamp column, e.g. `CuAr`) and FITS headers / the spectrograph `lamps` default.
  → labelled raw input for the lamp-ID step.
- **`reid_arxiv/`** — verified **242 solved reference arcs (229 FITS + 13 JSON)**;
  flux vs. calibrated wavelength → calibration ground truth + templates. Caveat
  noted: lamp species are in filenames only inconsistently (derive from
  headers/source, not the name).
- **`arc_lines/lists/`** — per-ion atomic data → synthesize labelled arcs + match
  target.

Also flagged the natural caution to **split by instrument/configuration** for an
honest held-out test. Marked Q3 resolved in the doc Q&A; bumped version header +
history.

### 2026-06-20 (Prompt 6: generated the AI-for-Science application prompt document)

The user asked for a *prompt document* that will guide producing an application
to **Anthropic's AI for Science Program**. Web-searched the program to ground
the prompts in its real components, then created
[claude_prompts/ai_for_science_application.md](ai_for_science_application.md) in
the house style (Purpose / Background / Prompts / Q&A / Requests / Logs).

Program facts captured (to be re-verified against official pages before
submission): up to **$20k API credits** over **6 months**; academic/nonprofit
researchers; proposal covering **goals, methodology, and API-credit use** plus
team details; judged on **scientific merit · impact · feasibility · team
credentials (subject + AI)**; reviewed the **first Monday of each month**;
biology/life-sciences are the headline focus, so the doc includes a dedicated
prompt (7) to argue program fit for an astronomy/instrumentation project.

The document lays out **8 sequential prompts** that each draft one application
section into `design/ai_for_science_application.md` — pitch/summary, scientific
motivation & impact, technical approach, use of Claude/API, team, feasibility +
milestones + budget, broader impact/fit, and a red-team+finalize pass — all
grounded in `design/holygrail_context.md` (§0–§14) and the §0.1 data corpus.
Logged two Q&A items (which program exactly; PI/team + budget) and a request for
the actual application form so the prompts can map 1:1 to its fields.
