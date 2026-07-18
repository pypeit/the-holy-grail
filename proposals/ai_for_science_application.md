# AI for Science Program — Application Draft

*The Holy Grail: An automated approach to the fundamental calibration of astronomical spectra*

> **How to use this file.** Headings below are the **actual Google-Form fields**,
> in order, each annotated with its word limit. Paste each field's prose into the
> form. **Before pasting, strip the italic `*(Prompt N …)*` scaffolding lines and
> any `[TBD — user]` / `[confirm — user]` flags** — those are working notes, not
> answers. Fields still carrying a flag need PI input (see Q&A 3–6 in
> `claude_prompts/ai_for_science_application.md`). A submission checklist is at the
> bottom.
>
> ✅ **CREDIT CEILING RESOLVED: $50,000.** The current live form
> (`proposals/application_form.pdf`, captured 2026-07-17) states: *"The maximum
> award for the AI for Science program is $50,000 in credits."* The earlier
> help-center $20k figure is superseded; the **$48k request stands**. The form
> also encourages **~6-month timelines** (matching our plan) and adds: *"if your
> project requires Claude Science credits, please indicate how much money in
> credits is needed across Claude Science and Claude Code"* — PI may optionally
> add a Claude Code line to the budget answer (currently declared not-funded).
>
> ⚠️ **1–2 SENTENCE LIMITS.** Six form questions specify **"(1–2 sentences,
> N words max)"**: Claude-use (300 w), Claude-vs-existing (200 w), scientific
> impact (200 w), applications beyond (200 w), measuring success (200 w), and
> biosecurity safeguards (N/A). Those answers below are each condensed to
> **two sentences** (Prompt 11) — do not paste multi-paragraph text into them.

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
instrument arms) and unlocks high-throughput and archival spectroscopy. Claude
is the engine we use to *discover and write* this calibrator; the delivered
algorithm is standalone Python inside PypeIt and runs on its own — no API call at
reduction time — so it applies to any future arc, from a seen or an entirely
unseen spectrograph.

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
`aa19f221-1347-4bf1-9078-c0508e3e4ce3` *(as entered in the in-progress form
draft, `proposals/application_form.pdf` p.3 — confirm it matches the org the
credits should attach to, Q&A 3)*

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

**Joseph Hennawi (Co-I)** — Professor of Physics, UC Santa Barbara and Astronomy at Leiden University; co-founder of PypeIt; expert in quasar and intergalactic-medium spectroscopy, large spectroscopic surveys, with a decades-long record of developing statistical and machine-learning methods for astronomical data. His group pioneered extreme-deconvolution density estimation for probabilistic quasar target selection (Bovy, Hennawi et al. 2011; Nanni, Hennawi et al. 2022) and generalized
it to conditional density estimation with neural-network Gaussian mixtures (Kang, Hennawi et al. 2025), and has built differentiable neural surrogate models for the mean and covariance of the Lyα forest power spectrum (González-Hernández, Hennawi et al. 2025) and generative machine-learning models of IGM damping wings in quasar spectra (Hennawi et al. 2025).  His work provides direct precedents for the probabilistic spectral pattern-identification at the core of this project.


**Kyle B. Westfall (Co-I)** - Researcher at UC Observatories, UC Santa Cruz.
Current PypeIt project manager and lead developer; funded by the Simons Foundation via their
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
- **Joseph Hennawi** — Co-I, Professor (UCSB/Leiden). Cross-instrument evaluation and
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
even modern automated solvers sidestep the hardest part — they must be **told the
lamp** and given an approximate dispersion or a matching template. Our question:
can one algorithm calibrate an *entirely unlabeled* arc — no instrument, grating,
dispersion, or lamp identity — by first **identifying the lamp(s) from the
spectrum alone** (for example, does the lamp contain thorium, argon, copper, mercury,
or hydroxide lines from Earth's sky, among others), then **deriving the full `λ = f(pixel)`
solution with no human input**? The first step, *blind lamp identification*, is
essentially **absent from the published literature** — the leading calibrators
(RASCAL, Davenport DTW, xwavecal) are step-2-only and assume the lamp is known;
the nearest ML precedent (SPIT - developed by the PI) classifies frame *type*, not lamp species —
making it our clearest novel contribution.

**Methodology.** We use Claude as the research engine to *design, prototype, and
write* a two-stage algorithm, delivered as standalone Python in PypeIt that runs
with no LLM or API call at reduction time. Both stages are built and evaluated on
the existing labeled PypeIt corpus (~45 instrument arms of raw arcs; 242 solved
reference arcs; per-ion atomic line lists). **Stage 1 — blind lamp ID (novel):** a
self-contained classifier assigns the lamp(s) from the detected-peak pattern and
coarse spectral features, trained on the labeled raw arcs plus *synthetic* arcs
generated from the line lists; its output narrows the line list for Stage 2. **Stage 2 — blind
calibration:** recombine two prior-art paradigms while dropping the priors each
requires — scale-invariant line-ratio **voting** for `(λ_cen, dispersion)`
(PypeIt cross-ratios; RASCAL's Hough) *without* a range/dispersion prior, seeded
by Stage 1 rather than a human; refined with DTW-style **sequence-alignment**
tolerance to non-linear dispersion *without* DTW's matched-template or amplitude
dependence; finished with a robust Legendre/RANSAC fit. **Evaluation** reuses
PypeIt's own gate: per-slit/order `RMS < 0.15 × FWHM` plus the PypeIt Development
Suite's instrument-specific thresholds, on setups held out by instrument.

**Outcomes & deliverables.** (1) a standalone, open-source, instrument-agnostic
blind-calibration algorithm integrated into PypeIt (no LLM at inference); (2) a
benchmark report versus the PypeIt
Development suite gates
and the current `holy-grail` baseline; (3) a released labeled dataset +
train/test splits; (4) a methods paper.

**Timeline (~6 months).** M1: assemble corpus, split by instrument, generate
synthetic arcs. M1–2: lamp-ID prototype. M2–4: blind-calibration prototype +
Claude-as-judge vetting. M4–5: evaluate against the dev-suite thresholds on
held-out setups. M5–6: PypeIt integration + write-up.

### How specifically will Claude's capabilities be used? — **1–2 sentences, 300 words max** *(required)*
*(Prompt 11 — condensed to 2 sentences, ~168 words)*

Claude (via the Anthropic API) is the research-and-development engine we will
use to *design, prototype, and write* a standalone two-stage blind
wavelength-calibration algorithm for PypeIt: Claude will reason over our labeled
arc corpus (detected-peak patterns, line-spacing ratios, FITS metadata, and —
via high-resolution vision — the arc plots) to design a self-contained
lamp-identification classifier; prototype and refine the
voting/sequence-alignment/robust-fit calibration solver; drive an agentic
tool-use loop that runs the evolving algorithm across ~224 PypeIt Development
Suite setups, reads the RMS/QA outputs, and folds diagnosed failures back into
the code; screen candidate pixel→wavelength solutions for physical plausibility
as an LLM judge (batched via the Batch API and tiered to smaller models); and
synthesize atomic line lists and prior-art methods into structured features and
training targets. The delivered product is standalone Python integrated into
PypeIt's wavelength-calibration module with **no LLM or API call at reduction
time**, so the credits fund these discovery-and-engineering workloads — the
prompt-cached agentic development loop being the dominant consumer — rather
than a runtime dependency.

### How will Claude significantly accelerate/enhance vs. existing methods? — **1–2 sentences, 200 words max** *(required)*
*(Prompt 11 — condensed to 2 sentences, ~157 words)*

No general, fully automated wavelength-calibration solution exists today:
"automated" methods are partial and brittle — humans hand-code algorithms per
instrument (or group of instruments), production reductions rely on manually
pre-calibrated templates built per setup through PypeIt's interactive
`pypeit_identify` GUI, remaining failure modes need human patching, and even
with the lamps and line lists known an expert spends minutes per spectrum, days
curating atomic databases when the line list is missing, and hours-to-days when
the lamp identity itself is uncertain. Claude removes the human from every one
of those steps — reasoning over heterogeneous, unlabeled spectral and metadata
inputs to identify the lamp and screen candidate solutions, a judgment task no
existing matcher (RASCAL's Hough/RANSAC, Davenport DTW, PypeIt's
parameter-space voting) encodes — and its agentic loop compresses today's
substantial per-instrument expert tuning into rapid automated iteration over
the entire labeled corpus, distilled into a **standalone algorithm** that ships
in PypeIt and calibrates unseen instruments on its own.

---

## Impact Assessment

### Potential scientific impact if successful — **1–2 sentences, 200 words max** *(required)*
*(Prompt 11 — condensed to 2 sentences, ~123 words)*

A solver that calibrates a fully *unlabeled* arc — identifying the lamp and
deriving the dispersion solution with no human input or instrument-specific
prior — would be **transferable and instrument-agnostic by construction**: one
calibrator that drops into PypeIt (the community-standard open-source reduction
pipeline, already validated across ~224 dev-suite setups) and generalizes to
instruments it has never seen, including future spectrographs and archival data
with missing or unreliable metadata. Success removes a recurring expert
bottleneck to **high-throughput** reduction (modern multi-object and IFU
spectrographs produce hundreds-to-thousands of spectra per exposure, each
needing a wavelength solution) and to mining **heterogeneous archives** at
scale, while closing a genuine methodological gap — blind lamp identification —
as a reusable template for blind pattern-identification-plus-calibration
problems beyond astronomy.

### Applications beyond pure discovery / societal benefit / paths to scale — **1–2 sentences, 200 words max** *(required)*
*(Prompt 11 — condensed to 2 sentences, ~117 words)*

Yes — the calibrator ships inside PypeIt, open-source infrastructure used
across dozens of observatories and ~45 instrument arms, so every PypeIt
reduction gains hands-off calibration, the same engine unlocks **archival
mining** of the millions of legacy spectra whose metadata are missing or
unreliable, and all code and benchmark data (the PypeIt Development Suite)
remain public and independently verifiable, with the labeled corpus and splits
released as a community resource. The underlying method — identify the source
from an unlabeled signal, then calibrate it against a reference library with no
human prior — is a reusable blueprint that recurs far beyond astronomy, in mass
spectrometry, nuclear magnetic resonance, Raman and other laboratory
spectroscopies, and sensor/instrument calibration generally.

### How will you measure success of using Claude? (specific metrics/objectives) — **1–2 sentences, 200 words max** *(required)*
*(Prompt 11 — condensed to 2 sentences, ~118 words)*

We will benchmark against the PypeIt Development Suite's built-in, objective
gates — no new ground truth needed — with two primary metrics: the **blind
calibration success rate** (fraction of held-out setups whose solution passes
the per-slit/order acceptance gate, `RMS < 0.15 × FWHM` plus the
instrument-specific thresholds, with *no* lamp, dispersion, or template prior
supplied) and **lamp-ID accuracy** on instruments/configurations held out of
training, each compared against PypeIt's current `holy-grail` method and the
archive-template workflow it replaces. Secondary development-efficiency metrics
are the precision/recall of Claude's solution-screening (does it correctly
discard bad candidates?) and credits consumed per solved setup, with the
overall objective of matching or beating the dev-suite RMS gates on a majority
of held-out setups with zero human input.

---

## Resource Requirements

### Anticipated API credit amount + how it leads to impact *(required — no sentence limit on this field)*
*(Prompt 6 — **proposed $48,000**. ✅ Ceiling resolved: the live form states the
maximum award is **$50,000**. Note the form adds: if the project requires
**Claude Science** credits, indicate the split across Claude Science and
**Claude Code** — the answer below currently declares Claude Code not-funded;
PI may choose to request a Claude Code line instead. Prompt 12: budget table
converted to plain text — the form field cannot render a table; the answer below
is paste-safe as-is.)*

We anticipate ~$48,000 in API credits over the project (Claude Opus 4.8 unless
noted; prices $5/$25 per 1M input/output tokens; Batch API at 50%; prompt-cache
reads ≈0.1× input), allocated across five workloads:

- ~$32k — the agentic development loop over the corpus, the dominant cost: long
  tool-use traces over ~224 dev-suite setups across many refinement rounds, run
  at high effort, with the shared corpus context prompt-cached (reads ≈0.1×) so
  most input is cheap. This line is the primary lever for depth and quality —
  more rounds and higher reasoning effort directly improve the algorithm Claude
  writes.
- ~$6k — solution-screening during development (Claude-as-judge): high volume,
  but batched (50% off) and tiered to Sonnet 4.6 / Haiku 4.5.
- ~$5k — lamp-ID feature discovery with high-resolution vision over the arcs:
  image tokens per arc studied while designing the standalone classifier.
- ~$2k — literature and line-list synthesis, plus miscellaneous use.
- ~$3k — contingency.

Order-of-magnitude check: one full agentic pass over 224 setups at ~200k
(largely cached) input + ~50k output tokens each ≈ $0.3–0.4k/round, so the ~$32k
line funds roughly 80–100 development rounds, or fewer rounds run at higher
effort — the depth needed to push blind calibration past the dev-suite gates
across diverse instruments.

How it leads to impact: the credits directly fund the iteration that turns a
labeled corpus into a working, standalone blind-calibration algorithm — every
dollar buys experiment rounds against the PypeIt Development Suite gates, and
the larger agentic-loop allocation buys the search depth that a from-scratch
blind solver needs to generalize across ~45 instrument arms and to arms it has
never seen. The delivered algorithm runs inside PypeIt with no API dependency;
code generation via Claude Code is not funded here.

---

## Biosecurity assessment

### Does your research involve pathogen/virology, drug-resistance, toxicology, or synthetic biology? *(required)*
- [x] **None of the above** (astronomical instrumentation)

### Biosecurity safeguards — **1–2 sentences, 200 words max** *(only if a box above is checked)*
N/A — no boxes checked above; leave blank on the form.

---

## Additional information

### Anything else for the review committee?
*(Prompt 7 — optional; trim/keep in Prompt 8)*

**Why Claude specifically.** This problem is not a single ML classification — it
chains *judgment* over heterogeneous, unlabeled scientific data (spectra,
metadata, plots) with *code* (the solver and its PypeIt integration). Claude is
uniquely suited because one agent can reason about the spectra, work out and
screen candidate solutions, and write the resulting algorithm — unifying
development tasks that would otherwise need separate bespoke models, and yielding
a standalone tool rather than an ongoing runtime LLM dependency.

**Program fit.** Astronomy/instrumentation sits under the form's **Physics**
field option, and the work is open-source scientific infrastructure with a
methodology that transfers to other physical science calibration problems.

**Track record with Anthropic.** The team is an existing Anthropic customer
(Team account since 2025) and has already used Claude Code in this project's
setup — we are ready to put API credits to work immediately.

### Terms of Service agreement *(required)*
- [ ] I agree *(check at submission)*

---

## Submission checklist (updated at Prompt 11)

**Before pasting:** strip every italic `*(Prompt N …)*` scaffolding line and every
`[TBD — user]` / `[confirm — user]` flag from the field prose.

**Sentence limits (Prompt 11):** the form marks six questions
"**(1–2 sentences, N words max)**" — Claude-use, Claude-vs-existing, scientific
impact, applications beyond, measuring success, biosecurity safeguards. All are
now **exactly 2 sentences** (safeguards = N/A, left blank). The team, project
description, key-members, and credit-amount fields carry **no** sentence limit.

**Word limits** (counted at Prompt 11):

| Field | Cap | Count | Sentences |
|---|---|---|---|
| Team description | <300 | ⚠️ **~428 — OVER CAP** (grew with Hennawi/Westfall additions; PI must trim ~130 words) | n/a |
| Project description | <500 | ~449 ✓ | n/a |
| How Claude is used | 300 | ~167 ✓ | 2 ✓ |
| Claude vs. existing methods | 200 | ~156 ✓ | 2 ✓ |
| Scientific impact | 200 | ~121 ✓ | 2 ✓ |
| Applications beyond / scale | 200 | ~116 ✓ | 2 ✓ |
| Measuring success | 200 | ~120 ✓ | 2 ✓ |

**Form mechanics** (checked against the in-progress form draft,
`proposals/application_form.pdf`, captured 2026-07-17):
- [x] Email: form draft is under **xavier@ucolick.org** — confirm credits attach
      to the right org regardless *(Q&A 3)*
- [x] Organization ID: `aa19f221-1347-4bf1-9078-c0508e3e4ce3` entered ✓
- [x] Scientific field(s): **Physics** + **Other: Astronomy** ✓ (checked in form)
- [ ] "Where did you hear…": form draft says **"In Anthropic's website"**, but
      Q&A 5 answer was **Brice Ménard** — reconcile (a personal referral may
      serve the application better)
- [x] Credit ceiling: **$50,000 confirmed on the live form** — $48k request stands
- [ ] Biosecurity: check **None of the above** (safeguards box → leave blank)
- [ ] Terms of Service: check **I agree** at submission

**Outstanding PI input (content):**
- [ ] ⚠️ **Trim team description below 300 words** (currently ~428)
- [ ] Decide whether to state a **Claude Science / Claude Code credit split**
      (new form language) or keep "Claude Code not funded"
- [ ] Confirm 6-month start date (form encourages ~6-month timelines ✓)
- [ ] Project title in form draft is truncated ("…An automated approach to the") —
      make sure the full title pasted

**Claims spot-checked against `design/holygrail_context.md`:** blind lamp-ID gap
(§0, §13, §14.3) ✓; RASCAL/DTW/xwavecal are step-2-only (§14) ✓; SPIT = frame-type
CNN, 98.7% (§13.3) ✓; 242 reid_arxiv solved arcs + ~45-arm RAW_DATA corpus (§0.1) ✓;
RMS < 0.15×FWHM acceptance gate (§3, §11) ✓; dev-suite ~224 setups as benchmark
(§9) ✓. Instrument-arm figures standardized: **~45** (PypeIt/corpus breadth),
**~224 setups** (dev-suite benchmark); the standalone "~59 arms" was removed to
avoid an internal clash.
