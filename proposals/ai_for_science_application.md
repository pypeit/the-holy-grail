# AI for Science Program — Application Draft

*The Holy Grail: An automated approach to the fundamental calibration of astronomical spectra*

> **How to use this file.** Headings below are the **actual Google-Form fields**,
> in order, each annotated with its word limit. Paste each field's prose into the
> form. **Before pasting, strip the italic `*(Prompt N …)*` scaffolding lines and
> any `[TBD — user]` / `[confirm — user]` flags** — those are working notes, not
> answers. Fields still carrying a flag need PI input (see Q&A in
> `claude_prompts/ai_for_science_application_prompts.md`). A submission checklist
> is at the bottom.
>
> ⚠️ **CREDIT-CEILING CONTRADICTION (must resolve before submitting).** The
> application form PDF (p.1, "About our Process") states **up to $50,000**; the
> official help-center article states **up to $20,000** over a **6-month period**.
> The program's own materials disagree. This draft requests **$48k** on the form's
> $50k figure — **confirm the real ceiling first; if $20k is current, rescale the
> budget.** (Q&A 4 / Requests.)

---

## Plain-language pitch (seed — not a form field)

Every spectrograph records light as a pattern of pixels, but science needs
physical wavelengths; bridging the two requires a **wavelength solution**, and
producing one is one of the most time-consuming, expertise-dependent steps in
all of optical/infrared astronomy. The standard recipe leans on an "arc" frame —
an exposure of a calibration lamp whose emission lines sit at known
wavelengths — but it normally requires someone to tell the pipeline
*which combination of lamps* were used and roughly *how* the instrument disperses light. **The
Holy Grail project removes those assumptions entirely**: given a completely
*unlabeled* arc spectrum — no instrument, grating, dispersion, or even lamp
identity — it (1) **identifies the arc lamp(s)** from the spectrum alone, then
(2) **derives the full pixel→wavelength solution** with no human input and no
prior guess. Step 1, *blind lamp identification*, is essentially absent from the
published literature, making it a genuine open problem; step 2 pushes well
beyond the current state of the art, which still requires a lamp list and often
fails without an instrument-specific archived solution previously developed by 
an experienced spectroscopist. Solving both yields a single,
transferable, instrument-agnostic calibrator — *one solution to rule them all* —
that drops into PypeIt (the community-standard reduction pipeline, ~45
instrument arms) and unlocks high-throughput and archival spectroscopy.

---

## Contact information

### Email *(required)*
**[TBD — user]** Confirm submitting address: form is pre-filled with
`xavier@ucolick.org`; credits account noted as `jxp@ucsc.edu`. (Q&A 3)

### Name of primary contact *(required)*
J. Xavier Prochaska

### Name of organization/research institution *(required)*
University of California, Santa Cruz

### Position/title at organization *(required)*
Professor of Astronomy and Astrophysics

### Website of org / research group, Google Scholar, or GitHub *(required)*
- PypeIt: https://github.com/pypeit/PypeIt
- J. X. Prochaska (SciXplorer): https://scixplorer.org/search?p=1&q=prochaska%2C+j&sort=score+desc&sort=date+desc&d=general
- https://profxj.github.io/

### Where did you hear about this program?

From a colleague who now works at Anthropic (Brice Ménard).

---

## Project information

### Project title *(required)*
The Holy Grail: An automated approach to the fundamental calibration of astronomical spectra

### Scientific field(s) — select all that apply *(required)*
- [x] **Physics**
- [x] **Other:** Astronomy / astronomical instrumentation

### Organization ID (UUID, from console.anthropic.com/settings/organization) *(required)*
**[TBD — user]** (Q&A 3)

---

## Research Team

### Team description — expertise in science **and** AI/ML — **<300 words** *(required)*
*(Prompt 5 — ~210 words; finalize once Cooke/Hennawi AI/ML lines arrive, Q&A 6)*

The team pairs deep spectroscopy/instrumentation expertise with hands-on
machine-learning experience.

**J. Xavier Prochaska (PI)** — Professor of Astronomy & Astrophysics, UC Santa
Cruz; co-founder and core developer of PypeIt, the community-standard Python
pipeline for slit-based spectroscopy (~45 instrument arms). Decades of expertise
across optical/IR spectrographs and atomic-line analysis. Active deep-learning
practitioner since 2017, with published CNN applications to astronomical
spectra — the SPectral Image Typer (SPIT; Jankov & Prochaska 2018), which
classifies raw spectrograph frames at 98.7% accuracy, and deep learning to
detect and characterize damped Lyα systems in quasar spectra (Parks, Prochaska
et al. 2018) — direct precedents for the spectral pattern-identification at the
core of this project.

**Ryan Cooke (Co-I)** — Professor of Astronomy, Durham University; co-founder of
PypeIt; expert in high-precision spectroscopy and wavelength calibration, with over
20 years of experience. Brings a strong background in wavelength calibration,
combined with a track record of applying machine learning to astronomical data, including
the development of algorithms for spectral line identification and classification.
Recent works include the application of CNNs to identify rare galaxies and absorption
features (Cheng & Cooke 2025, 2026) and extract hundreds of absorption line identifications
in astronomical spectra (Cheng, Cooke & Rudie 2022), combined with the development of
machine learning models for spectroscopic data reduction.

**Joseph Hennawi (Co-I)** — Professor of Physics, UC Santa Barbara; co-developer
of PypeIt **[confirm role wording — user]**; expert in quasar and
intergalactic-medium spectroscopy and large spectroscopic surveys.
**[AI/ML experience — TBD, user to supply, Q&A 6.]**

**Kyle B. Westfall (Co-I)** - Researcher at UC Observatories, UC Santa Cruz.
Co-lead developer for PypeIt; funded by the Simons Foundation via their
Scientific Software Research Faculty Award to develop community-driven software
for astronomical spectroscopy; member of Astropy leadership, the core Python
package used by all astronomers.  Expert in processing and analysis of
spectroscopic, particularly for fiber-based instruments.

The team authored both PypeIt and the prior `arclines` "Holy Grail" prototype
this project builds on, and is an existing Anthropic customer (Team account
since 2025).

### Key team members using Claude (name, title, role) *(required)*
*(Prompt 5)*

- **J. Xavier Prochaska** — PI, Professor (UCSC). Leads the lamp-ID and
  calibration design; runs the Claude agentic experimentation loop over the
  corpus and the PypeIt integration.
- **Ryan Cooke** — Co-I, Professor (Durham). Wavelength-calibration validation
  and reference line-list curation; reviews Claude-vetted solutions.
- **Joseph Hennawi** — Co-I, Professor (UCSB). Cross-instrument evaluation and
  archival application of the resulting calibrator.
- **Kyle B. Westfall** - Co-I, Researcher (UCO/UCSC). Validation, testing, and
  PypeIt and Astropy integration

### Links to Google Scholar / professional profiles
- Prochaska: https://scixplorer.org/search?p=1&q=prochaska%2C+j&sort=score+desc&sort=date+desc&d=general
- Cooke: https://scixplorer.org/search?p=1&q=orcid%3A0000-0001-7653-5827&sort=date+desc&d=general
- Hennawi: https://scixplorer.org/search?p=1&q=hennawi%2C+j&sort=score+desc&sort=date+desc&d=general
- Westfall: https://tinyurl.com/5n6zzwr6

---

## Research Proposal

### Project description — **<500 words** *(required)*
*(Prompt 8 trim — ~395 words; covers question · methodology · outcomes · timeline.)*

**Scientific question.** Wavelength calibration — mapping detector pixels to
physical wavelengths, `λ = f(pixel)` — gates **every** optical/infrared spectroscopic
reduction: no redshift, abundance, or velocity is trustworthy without it. Its
bottleneck is *line identification*: assigning each detected arc-lamp peak to its
rest wavelength. This is a historically manual, expertise-intensive step, and
even modern "automated" solvers sidestep the hardest part: they must be **told
the lamp**, given an approximate dispersion or a **manually pre-calibrated
template**, and remain **brittle, per-instrument algorithms** with failure modes
that still need human patching — no general, fully automated solution exists. Our
question:
can one algorithm calibrate an *entirely unlabeled* arc — no instrument, grating,
dispersion, or lamp identity — by first **identifying the lamp(s) from the
spectrum alone** (for example, does the lamp contain thorium, argon, copper, mercury,
or hydroxide lines from Earth's sky, among others), then **deriving the full `λ = f(pixel)`
solution with no human input**? The first step, *blind lamp identification*, is
essentially **absent from the published literature** — the leading calibrators
(RASCAL, Davenport DTW, xwavecal) are step-2-only and assume the lamp is known;
the nearest ML precedent (SPIT - developed by the PI) classifies frame *type*, not lamp species —
making it our clearest novel contribution.

**Methodology.** Two chained stages, built and evaluated on the existing labeled
PypeIt corpus (~45 instrument arms of raw arcs; 242 solved reference arcs;
per-ion atomic line lists). **Stage 1 — blind lamp ID (novel):** classify the
lamp from the detected-peak pattern and coarse spectral features with an ML/LLM
classifier, trained on the labeled raw arcs plus *synthetic* arcs generated from
the line lists; its output narrows the line list for Stage 2. **Stage 2 — blind
calibration:** recombine two prior-art paradigms while dropping the priors each
requires — scale-invariant line-ratio **voting** for `(λ_cen, dispersion)`
(PypeIt cross-ratios; RASCAL's Hough) *without* a range/dispersion prior, seeded
by Stage 1 rather than a human; refined with DTW-style **sequence-alignment**
tolerance to non-linear dispersion *without* DTW's matched-template or amplitude
dependence; finished with a robust Legendre/RANSAC fit. **Evaluation** reuses
PypeIt's own gate: per-slit/order `RMS < 0.15 × FWHM` plus the PypeIt Development
Suite's instrument-specific thresholds, on setups held out by instrument.

**Outcomes & deliverables.** (1) an open-source, instrument-agnostic blind
calibrator integrated into PypeIt; (2) a benchmark report versus the PypeIt
Development suite gates
and the current `holy-grail` baseline; (3) a released labeled dataset +
train/test splits; (4) a methods paper.

**Timeline (~6 months).** M1: assemble corpus, split by instrument, generate
synthetic arcs. M1–2: lamp-ID prototype. M2–4: blind-calibration prototype +
Claude-as-judge vetting. M4–5: evaluate against the dev-suite thresholds on
held-out setups. M5–6: PypeIt integration + write-up.

### How specifically will Claude's capabilities be used? — **300 words max** *(required)*
*(Prompt 4 — ~230 words)*

Claude (via the Anthropic API) is the reasoning core of both research stages:

1. **Blind lamp identification** — Claude Opus 4.8 reasons over each arc's
   detected-peak pattern, line-spacing ratios, and FITS metadata — and, via
   high-resolution vision, the arc plot itself — to hypothesize the lamp
   species and rank candidate reference line lists.
2. **Calibration vetting (LLM-as-judge)** — Claude scores candidate
   pixel→wavelength solutions for physical plausibility (monotonic dispersion,
   line-ID self-consistency, RMS-vs-FWHM gate), pruning the voting/alignment
   search.
3. **Agentic experimentation** — a Claude tool-use loop runs the pipeline across
   dev-suite setups, reads the RMS/QA outputs, and proposes parameter and
   algorithm refinements, iterating against the labeled corpus.
4. **Code generation & PypeIt integration** — Claude writes and refactors the
   classifier, solver, and glue code into `pypeit/core/wavecal/`.
5. **Literature & line-list synthesis** — Claude distills atomic line lists and
   prior-art methods into structured features and training targets.

*Token/credit scale (feeds Prompt 6):* the dominant consumer is the agentic
corpus loop (long tool-use traces over ~224 setups × multiple rounds, with
prompt caching on the shared corpus context, reads ≈0.1× input). LLM-as-judge
vetting is high-volume but **batchable (50% via the Batch API)** and can tier
down to Sonnet 4.6 / Haiku 4.5; vision reasoning adds image tokens per arc.
Code generation through Claude Code is *incidental developer tooling, not funded
API use* — the credit request covers the API workloads above.

### How will Claude significantly accelerate/enhance vs. existing methods? — **200 words max** *(required)*
*(Prompt 4 — ~150 words)*

Today there is **no general, fully automated solution**. Existing "automated"
methods are partial and brittle: humans must hand-code algorithms per instrument
(or instrument group), the methods rely on **manually pre-calibrated templates**,
and they still hit failure modes requiring human intervention and patching. The
human cost scales with what is known: a few **minutes per spectrum** when the
lamps *and* their line lists are in hand; **days** of curating and scouring
atomic databases when the lamps (elements) are known but the line list is not;
**hours to days** when even the lamp identity is uncertain (usually known — but
not always). PypeIt is representative: its from-scratch `holy-grail` method must
be handed the lamp list and "can fail catastrophically," so production leans on
expert-built archive templates via the interactive `pypeit_identify` GUI. Claude
removes the human from both steps — reasoning over unlabeled spectra and metadata
to identify the lamp and vet solutions, a judgment task no matcher (RASCAL, DTW,
PypeIt's voting) performs — and its agentic loop replaces per-instrument
hand-tuning with automated iteration over the whole corpus. The payoff: one
calibrator that generalizes to unseen instruments.

---

## Impact Assessment

### Potential scientific impact if successful — **200 words max** *(required)*
*(Prompt 2 — ~150 words)*

Wavelength calibration is a universal prerequisite for spectroscopy, and its
line-identification step remains a per-instrument, expert-tuned chore that costs
astronomer and pipeline-developer time across the field. A solver that works on
an *unlabeled* arc — identifying the lamp and deriving the dispersion with no
human input or instrument-specific prior — would be **transferable and
instrument-agnostic by construction**: one calibrator that drops into PypeIt
(the community-standard open-source reduction pipeline, already validated across
~224 dev-suite setups) and generalizes to instruments it has never
seen, including future and archival data with missing or unreliable metadata.
This removes a recurring barrier to **high-throughput** reductions (modern
multi-object and IFU spectrographs produce hundreds-to-thousands of spectra per
exposure, each needing a solution) and to mining **heterogeneous archives** at
scale. It also closes a genuine methodological gap — blind lamp identification —
establishing a reusable template for blind pattern-identification-plus-
calibration problems beyond astronomy.

### Applications beyond pure discovery / societal benefit / paths to scale — **200 words max** *(required)*
*(Prompt 7 — ~180 words)*

**Open-source infrastructure, immediate reach.** The calibrator ships inside
PypeIt — the community-standard reduction pipeline used across dozens of
observatories and ~45 instrument arms — so a success reaches the entire
user base, not one group. Path to scale: every PypeIt reduction gains hands-off
calibration, and the same engine unlocks **archival mining** of the millions of
legacy spectra whose metadata are missing or unreliable.

**The method generalizes.** "Identify the source from an unlabeled signal, then
calibrate it against a reference library, with no human prior" is a template
that recurs far beyond astronomy — mass spectrometry, nuclear magnetic resonance,
Raman and other spectroscopic techniques utilized in laboratories, and sensor/instrument
calibration more generally. A working
demonstration is a reusable blueprint for blind pattern-identification +
calibration problems across the physical sciences (the program's own form lists
Physics as an eligible field).

**Reproducibility & public data.** All code is open-source and all benchmark
data are public (the PypeIt Development suite), so results are independently verifiable
and the labeled corpus + splits become a community resource.

### How will you measure success of using Claude? (specific metrics/objectives) — **200 words max** *(required)*
*(Prompt 6 — ~140 words)*

We use the PypeIt Development Suite's built-in, objective gates as the benchmark — no new
ground truth data are needed:

1. **Blind calibration success rate** — fraction of held-out dev-suite setups
   for which the solution passes the per-slit/order acceptance gate
   (`RMS < 0.15 × FWHM`, plus the instrument-specific thresholds) with *no*
   lamp, dispersion, or template prior supplied.
2. **Lamp-ID accuracy** — classification accuracy on instruments/configurations
   held out of training.
3. **Baseline delta** — both above vs. PypeIt's current `holy-grail` method and
   versus the archive-template workflow it replaces.
4. **Claude-integration metrics** — LLM-as-judge precision/recall at flagging
   wrong solutions, and credits (tokens) consumed per solved setup trending down
   as caching and model-tiering are tuned.

Target: match or beat the PypeIt Development Suite RMS gates on a majority of held-out setups
with zero human input.

---

## Resource Requirements

### Anticipated API credit amount + how it leads to impact *(required)*
*(Prompt 6 — **proposed $48,000**. ⚠️ Ceiling is contradictory: form says $50k,
help-center says $20k — confirm before submitting; if $20k, rescale. Q&A 4.)*

We anticipate **~$48,000** in API credits over the project, mapped to the
Prompt-4 workloads (Claude Opus 4.8 unless noted; prices $5/$25 per 1M
input/output; Batch API at 50%; prompt-cache reads ≈0.1× input):

| Workload | Est. credits | Notes |
|---|---|---|
| Agentic experimentation loop over the corpus | ~$32k | Dominant cost. Long tool-use traces over ~224 dev-suite setups × many refinement rounds, run at high effort; shared corpus context is prompt-cached (reads ≈0.1×), so most input is cheap. The primary lever for depth/quality — more rounds and higher reasoning effort directly improve the solver. |
| LLM-as-judge solution vetting | ~$6k | High volume but **batched (50% off)** and tiered to Sonnet 4.6 / Haiku 4.5. |
| Lamp-ID reasoning + high-res vision over arcs | ~$5k | Image tokens per arc across training/eval rounds. |
| Literature & line-list synthesis, misc. | ~$2k | |
| Contingency | ~$3k | |

**Order-of-magnitude check:** one full agentic pass over 224 setups at ~200k
(largely cached) input + ~50k output tokens each ≈ $0.3–0.4k/round; the ~$32k
line funds roughly **80–100 development rounds**, or fewer rounds run at higher
(`xhigh`/`max`) effort — the depth needed to push blind calibration past the
dev-suite gates across diverse instruments.

**How it leads to impact:** the credits directly fund the iteration that turns a
labeled corpus into a working blind calibrator — every dollar buys experiment
rounds against the PypeIt Development suite gates, and the larger agentic-loop allocation buys
the search depth that a from-scratch blind solver needs to generalize across
~45 instrument arms. Code generation via Claude Code is *not* funded here.

---

## Biosecurity assessment

### Does your research involve pathogen/virology, drug-resistance, toxicology, or synthetic biology? *(required)*
- [x] **None of the above** (astronomical instrumentation)

### Biosecurity safeguards
N/A — no boxes checked above.

---

## Additional information

### Anything else for the review committee?
*(Prompt 7 — optional; trim/keep in Prompt 8)*

**Why Claude specifically.** This problem is not a single ML classification — it
chains *judgment* over heterogeneous, unlabeled scientific data (spectra,
metadata, plots) with *code* (the solver and its PypeIt integration). Claude is
uniquely suited because one agent can reason about the spectrum, vet a candidate
solution, and write the integration — unifying tasks that would otherwise need
separate bespoke models.

**Program fit.** Astronomy/instrumentation sits under the form's **Physics**
field option, and the work is open-source scientific infrastructure with a
methodology that transfers to other physical science calibration problems.

**Track record with Anthropic.** The team is an existing Anthropic customer
(Team account since 2025) and has already used Claude Code in this project's
setup — we are ready to put API credits to work immediately.

### Terms of Service agreement *(required)*
- [ ] I agree *(check at submission)*

---

## Submission checklist (Prompt 8)

**Before pasting:** strip every italic `*(Prompt N …)*` scaffolding line and every
`[TBD — user]` / `[confirm — user]` flag from the field prose.

**Word limits — all verified within cap** (counts as of this draft):

| Field | Cap | Count |
|---|---|---|
| Team description | <300 | ~170 (grows when Cooke/Hennawi AI/ML lines are added — keep < 300) |
| Project description | <500 | **~395** (trimmed from 602) |
| How Claude is used | 300 | ~218 |
| Claude vs. existing methods | 200 | ~142 |
| Scientific impact | 200 | ~144 |
| Applications beyond / scale | 200 | ~159 |
| Measuring success | 200 | ~123 |

**Form mechanics:**
- [ ] Email: confirm `xavier@ucolick.org` vs `jxp@ucsc.edu` *(Q&A 3)*
- [ ] Organization ID (UUID from console.anthropic.com) *(Q&A 3 — required, blank)*
- [ ] Scientific field(s): **Physics** + **Other: Astronomy** ✓ set
- [ ] "Where did you hear about this program?" *(Q&A 5 — blank)*
- [ ] Biosecurity: **None of the above** ✓ (safeguards box → leave blank)
- [ ] Terms of Service: check **I agree** at submission

**Outstanding PI input (content):**
- [ ] Cooke & Hennawi AI/ML credentials *(Q&A 6)*
- [ ] Confirm Hennawi's PypeIt role wording ("co-developer")
- [ ] Confirm credit amount + **resolve the $50k-vs-$20k ceiling** *(Q&A 4 / ⚠️ top)*
- [ ] Confirm 6-month start date

**Claims spot-checked against `design/holygrail_context.md`:** blind lamp-ID gap
(§0, §13, §14.3) ✓; RASCAL/DTW/xwavecal are step-2-only (§14) ✓; SPIT = frame-type
CNN, 98.7% (§13.3) ✓; 242 reid_arxiv solved arcs + ~45-arm RAW_DATA corpus (§0.1) ✓;
RMS < 0.15×FWHM acceptance gate (§3, §11) ✓; dev-suite ~224 setups as benchmark
(§9) ✓. Instrument-arm figures standardized: **~45** (PypeIt/corpus breadth),
**~224 setups** (dev-suite benchmark); the standalone "~59 arms" was removed to
avoid an internal clash.
