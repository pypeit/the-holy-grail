# AI for Science Program — Application Draft

*The Holy Grail: blind, instrument-agnostic wavelength calibration of arc-line spectra*

> **How to use this file.** Headings below are the **actual Google-Form fields**,
> in order, each annotated with its word limit. Answers drop straight into the
> form. Fields marked **[TBD — user]** need input from the PI (see Q&A 3–6 in
> `claude_prompts/ai_for_science_application.md`); fields marked
> **[Prompt N]** are written/expanded by that prompt in the sequence. This
> Prompt-1 pass sets the skeleton and the plain-language pitch (bottom).

---

## Plain-language pitch (seed — not a form field)

Every spectrograph records light as a pattern of pixels, but science needs
physical wavelengths; bridging the two requires a **wavelength solution**, and
producing one is one of the most time-consuming, expertise-dependent steps in
all of optical/infrared astronomy. The standard recipe leans on an "arc" frame —
an exposure of a calibration lamp whose emission lines sit at known
wavelengths — but it normally assumes someone has already told the pipeline
*which lamp* was used and roughly *how* the instrument disperses light. **The
Holy Grail project removes those assumptions entirely**: given a completely
*unlabeled* arc spectrum — no instrument, grating, dispersion, or even lamp
identity — it (1) **identifies the arc lamp(s)** from the spectrum alone, then
(2) **derives the full pixel→wavelength solution** with no human input and no
prior guess. Step 1, *blind lamp identification*, is essentially absent from the
published literature, making it a genuine open problem; step 2 pushes well
beyond the current state of the art, which still requires a lamp list and often
fails without an instrument-specific archive. Solving both yields a single,
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

### Where did you hear about this program?
**[TBD — user]** (Q&A 5)

---

## Project information

### Project title *(required)*
*The Holy Grail: Blind, Instrument-Agnostic Wavelength Calibration of
Astronomical Arc Spectra* *(working title — refine in Prompt 8)*

### Scientific field(s) — select all that apply *(required)*
- [x] **Physics**
- [x] **Other:** Astronomy / astronomical instrumentation

### Organization ID (UUID, from console.anthropic.com/settings/organization) *(required)*
**[TBD — user]** (Q&A 3)

---

## Research Team

### Team description — expertise in science **and** AI/ML — **<300 words** *(required)*
**[Prompt 5]** Draft establishing credibility in both spectroscopy/astronomy
(PypeIt authorship, instrument expertise) and AI/ML.

Seed facts:
- **J. Xavier Prochaska** — UC Santa Cruz; Professor of Astronomy & Astrophysics;
  co-founder of PypeIt; decades of spectroscopy/astronomy expertise; active deep-
  learning user since 2017.
- **Ryan Cooke** — Durham University; Professor of Astronomy; co-founder of
  PypeIt. **[TBD — user: AI/ML credentials]** (Q&A 6)
- **Joseph Hennawi** — UC Santa Barbara; Professor of Physics. **[TBD — user:
  AI/ML credentials]** (Q&A 6)

### Key team members using Claude (name, title, role) *(required)*
**[Prompt 5]** Concise list mapping each PI to their project role.

### Links to Google Scholar / professional profiles
- Prochaska: https://scixplorer.org/search?p=1&q=prochaska%2C+j&sort=score+desc&sort=date+desc&d=general
- Cooke: https://scixplorer.org/search?p=1&q=cooke%2C+r&sort=score+desc&sort=date+desc&d=general
- Hennawi: https://scixplorer.org/search?p=1&q=hennawi%2C+j&sort=score+desc&sort=date+desc&d=general

---

## Research Proposal

### Project description — **<500 words** *(required)*
Cover: scientific question/problem · methodology & approach · expected outcomes
& deliverables · timeline for completion.

**[Prompts 2, 3, 6]** — motivation (Prompt 2), technical approach (Prompt 3),
milestones/timeline (Prompt 6). Open with the pitch above.

### How specifically will Claude's capabilities be used? — **300 words max** *(required)*
**[Prompt 4]** Tasks Claude performs + how it integrates with the research
workflow (reasoning agent over spectra/metadata; code generation & pipeline
integration; line-list synthesis; agentic experimentation; LLM-as-judge for
solution vetting). API use only.

### How will Claude significantly accelerate/enhance vs. existing methods? — **200 words max** *(required)*
**[Prompt 4]** Contrast against the baseline: current PypeIt requires expert
hand-tuning and an instrument-specific archive per setup.

---

## Impact Assessment

### Potential scientific impact if successful — **200 words max** *(required)*
**[Prompt 2]** Distilled impact statement (≤200 words).

### Applications beyond pure discovery / societal benefit / paths to scale — **200 words max** *(required)*
**[Prompt 7]** Open-source scientific infrastructure; methodology generalizes to
other blind pattern-ID + calibration problems; reproducibility, public data.

### How will you measure success of using Claude? (specific metrics/objectives) — **200 words max** *(required)*
**[Prompt 6]** e.g. fraction of dev-suite setups passing the RMS gate *blind*;
lamp-ID classification accuracy on held-out instruments.

---

## Resource Requirements

### Anticipated API credit amount + how it leads to impact *(required, ≤ $50k)*
**[Prompt 6 + TBD — user]** Justified figure ≤ $50k mapped to the Prompt-4 uses.
(Q&A 4)

---

## Biosecurity assessment

### Does your research involve pathogen/virology, drug-resistance, toxicology, or synthetic biology? *(required)*
- [x] **None of the above** (astronomical instrumentation)

### Biosecurity safeguards
N/A — no boxes checked above.

---

## Additional information

### Anything else for the review committee?
**[Prompt 7/8]** Optional. Candidate points: PypeIt is community-standard
open-source infrastructure; the team is an active Anthropic Team customer
(since 2025) and has used Claude Code in this project's setup.

### Terms of Service agreement *(required)*
- [ ] I agree *(check at submission)*
