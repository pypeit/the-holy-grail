# Prompt document: Anthropic "AI for Science" Program application

## Purpose

This is a **prompt document**: a sequenced set of prompts that will guide Claude
(and the user) through drafting a strong application to **Anthropic's AI for
Science Program** for *The Holy Grail* project (automated, blind wavelength
calibration of arc-line spectra).

Execute the prompts **in order**. Each produces a section of the application,
written into a working draft at `proposals/ai_for_science_application.md`. Earlier
sections (summary, impact) should be revisited after later ones (methods,
budget) are written, so the final pass is a coherence/edit prompt.

The actual application form is now in hand
(`proposals/Application Form - Anthropic's AI for Science Program.pdf`). The
draft must map **1:1 to the real form fields** (see Prompt 1), each respecting
its word limit, rather than the inferred structure originally sketched here.

Treat [holygrail_context.md](holygrail_context.md) → `design/holygrail_context.md`
as the **source of truth** for all technical and project facts. Do not invent
results; cite the context doc's sections (§0–§14) where relevant.

## Background — the program (verified against the application form, June 2026)

Confirmed against the official application form PDF in `proposals/`
(re-verify the official pages in *References* before submitting — terms change):

- **What:** free Anthropic **API** credits (the *standard model suite*; not the
  Claude web app) for nonprofit/academic researchers on high-impact projects.
- **Award:** up to **$50,000** in API credits (not $20k — the doc's earlier
  figure is superseded). The **specific amount is decided during evaluation**;
  the form asks the applicant to state how much they anticipate needing and why.
- **No fixed grant period.** The program does **not** state a 6-month window.
  The form asks only for a project **"timeline for completion"** (open-ended)
  and the anticipated credit amount. Any 6-month plan in this doc is a *proposal
  choice*, not a program constraint — present it that way.
- **Eligibility:** researchers at **academic / nonprofit** institutions.
- **No Usage-Policy exemption:** standard Trust & Safety enforcement applies.
- **Application:** a Google Form (see field map in Prompt 1) covering contact +
  org info, team credentials (science **and** AI/ML), a <500-word project
  description, several short capability/impact questions (200–300-word caps), a
  credit-budget justification, and a **biosecurity** declaration.
- **Required:** an **Anthropic Organization ID** (UUID from
  `console.anthropic.com/settings/organization`) — set up an account first.
- **Evaluation criteria:** **scientific credentials · potential impact of the
  proposed research · AI's ability to meaningfully accelerate the work.**
- **Process:** reviewed on the **first Monday of each month**; if successful,
  credits are applied after a **30-minute video call**. (Not approved →
  generally no individual response.)
- **Focus:** biology / life sciences are the stated priority, **but "Physics" is
  an explicit field option** on the form — astronomy/instrumentation fits there
  (select Physics, and add "Astronomy" under *Other*). The impact +
  AI-methodology case must still be made explicitly (see Prompt 7), but the
  project is *not* off-topic for the form's own taxonomy.

## Inputs needed from the user (fill before/while drafting)

These are facts only the user can supply; the prompts will ask for them, but
collecting them up front helps:

- **PI / team:** 
    - J. Xavier Prochaska
      - University of California, Santa Cruz
      - Professor of Astronomy and Astrophysics
      - Co-founder of the PypeIt project
      - Decades of expertise in spectroscopy and astronomy
      - Active user of deep learning since 2017
      - https://scixplorer.org/search?p=1&q=prochaska%2C+j&sort=score+desc&sort=date+desc&d=general
    - Ryan Cooke
      - Durham University
      - Professor of Astronomy 
      - Co-founder of the PypeIt project
      - ADD YOUR ML HERE
      - https://scixplorer.org/search?p=1&q=cooke%2C+r&sort=score+desc&sort=date+desc&d=general
    - Joseph Hennawi
      - University of California, Santa Barbara
      - Professor of Physics
      - ADD YOUR ML HERE
      - https://scixplorer.org/search?p=1&q=hennawi%2C+j&sort=score+desc&sort=date+desc&d=general

- **Institutional eligibility** confirmation (academic/nonprofit).
    - Our institutions are all eligible
- **Credit budget:** desired amount (**≤ $50k** — the program's stated ceiling)
  and the rough split across uses.
    - TBD
- **Project timeline:** the form asks for a "timeline for completion" (no fixed
  6-month grant window); state intended start and any external deadlines.
    - TBD
- **Anthropic Organization ID** (required form field): the UUID from
  `console.anthropic.com/settings/organization`. An account must exist before
  submitting.
    - TBD — JXP to retrieve from the console
- **Form email / account:** the form PDF is pre-filled with **xavier@ucolick.org**,
  but the credits-account email noted below is **jxp@ucsc.edu**. Confirm which
  email submits the form and which Organization ID the credits attach to.
    - jxp@ucsc.edu (credits account) — confirm vs. the xavier@ucolick.org login
- **Where did you hear about this program?** (form field) — to fill in.
    - TBD
- **Org website / Google Scholar / GitHub link** (required form field).
    - PypeIt GitHub + the SciXplorer profile links below
- Any **prior Anthropic** engagement (this project's logs already note Claude
  Code use).
    - JXP has had a Team account since 2025

## Claude / Skills

- Use the project context doc and the three codebases (PypeIt, dev-suite,
  arclines) for grounding.
- The `deep-research` skill may help sharpen the impact/landscape section;
  `critical-partner` is useful for the pre-submission red-team (Prompt 8).

## Prompts

0. **More prep** Read this doc, my edits, and the application form PDF in the proposals/ folder.  Modify this doc as needed to reflect them. *(Done — see Logs.)*

1. *(Done — see Logs.)* **Set up the draft as a 1:1 form map + extract the pitch.** Create
   `proposals/ai_for_science_application.md` whose headings are the **actual form
   fields** (in order), each annotated with its word limit, so answers drop
   straight into the Google Form:

   **Contact information**
   - Email *(required)* — confirm xavier@ucolick.org vs jxp@ucsc.edu
   - Name of primary contact *(required)*
   - Name of organization/research institution *(required)*
   - Position/title at organization *(required)*
   - Website of org/research group, Google Scholar, or GitHub *(required)*
   - Where did you hear about this program?

   **Project information**
   - Project title *(required)*
   - Scientific field(s) — checkboxes; select **Physics**, add **Other: Astronomy /
     astronomical instrumentation** *(required)*
   - Organization ID (UUID from the Anthropic console) *(required)*

   **Research Team**
   - Team description, expertise in **science *and* AI/ML** — **<300 words** *(required)*
   - Key team members using Claude (name, title, role) *(required)*
   - Links to Google Scholar / professional profiles

   **Research Proposal**
   - Project description — **<500 words**, covering: scientific question/problem ·
     methodology & approach · expected outcomes & deliverables · timeline for
     completion *(required)*
   - How specifically Claude's capabilities will be used (tasks + workflow
     integration) — **300 words max** *(required)*
   - How Claude significantly accelerates/enhances vs. existing methods —
     **200 words max** *(required)*

   **Impact Assessment**
   - Potential scientific impact if successful — **200 words max** *(required)*
   - Applications beyond pure discovery / societal benefit / paths to scale —
     **200 words max** *(required)*
   - How you'll measure success of using Claude (specific metrics/objectives) —
     **200 words max** *(required)*

   **Resource Requirements**
   - Anticipated API credit amount + how it leads to impact *(required)*

   **Biosecurity assessment**
   - Does your research involve pathogen/virology, drug-resistance, toxicology,
     synthetic biology? → **None of the above** (astronomy) *(required)*
   - Biosecurity safeguards — only if any box checked (N/A here)

   **Additional information**
   - Anything else for the review committee
   - Terms of Service agreement *(required)*

   Then, from `design/holygrail_context.md` §0–§0.1, write a 3–5 sentence
   **plain-language pitch** (it seeds the Project title + the opening of the
   <500-word project description): the problem (turning an *unlabeled* arc
   spectrum into a wavelength solution with no human input), the two sub-goals
   (lamp-ID, then calibration), and why it matters.

2. **Scientific motivation & impact.** *(Feeds the project-description opening and
   the "potential scientific impact" field — 200 words max.)* Using context §1
   (the problem), §9 (instrument/lamp diversity), and §13 (literature), write the
   motivation: how much astronomer/pipeline time wavelength calibration costs;
   that it gates every spectroscopic reduction across ~45 instruments; and the
   specific **gap** — blind *lamp identification* is essentially absent from the
   literature (§13, §14.3). State the impact if solved: a transferable,
   instrument-agnostic calibration that drops into PypeIt and beyond, enabling
   high-throughput and archival spectroscopy. Quantify where possible. Keep the
   distilled impact statement to ≤200 words.

3. **Technical approach.** From context §3–§8 (current PypeIt methods, the
   baseline to beat), §5 (scale-invariant pattern matching), and §14 (RASCAL
   Hough+RANSAC; DTW), lay out the proposed method: (a) lamp-ID step — how an
   LLM/ML + statistical approach could classify the lamp from raw spectral
   features; (b) calibration step — combining parameter-space voting and
   sequence-alignment ideas without the priors those methods require. Be
   explicit about what is novel vs. what reuses prior art. Reference the
   evaluation metric (RMS vs. FWHM-scaled threshold, context §3, §9).

4. **Use of Claude / the API credits.** *(Feeds two fields: "How specifically
   will Claude's capabilities be used" — 300 words max — and "How will Claude
   significantly accelerate/enhance vs. existing methods" — 200 words max.)*
   Concretely describe *how Claude is used in the research* (central to the
   program): e.g. Claude as a reasoning agent over spectra/metadata; code
   generation and pipeline integration; literature/line-list synthesis; agentic
   experimentation over the corpus; LLM-as-judge for solution vetting. Make the
   acceleration-vs-baseline contrast explicit (current PypeIt requires expert
   hand-tuning per setup). Tie each use to an estimated token/credit consumption
   to feed Prompt 6. Distinguish funded **API** use from incidental tooling
   (Claude Code, web app), since the program funds API credits only.

5. **Team & credentials.** *(Feeds the <300-word team description, the "key team
   members using Claude" list, and the Scholar-links field.)* Using the
   user-supplied inputs, write the team section establishing credibility in
   **both** spectroscopy/astronomy (PypeIt authorship, instrument expertise) and
   AI/ML — the form explicitly weights both. Keep it factual and **under 300
   words**; the SciXplorer links above serve as the profile links. Request any
   missing AI/ML credentials (Cooke, Hennawi) via the Q&A.

6. **Feasibility, milestones & budget.** *(The timeline + outcomes feed the
   <500-word project description; the budget feeds "anticipated API credit
   amount … how it leads to impact"; the metrics feed "how you'll measure
   success of using Claude" — 200 words max.)* Using context §0.1 (the ready-made
   labelled corpus: `RAW_DATA/`, the 242 `reid_arxiv/` solved arcs, the atomic
   line lists) and §9 (the dev-suite RMS gates as a built-in benchmark), write a
   milestone plan (data assembly + split-by-instrument; lamp-ID prototype;
   calibration prototype; evaluation against dev-suite thresholds; write-up). A
   ~6-month timeline is a reasonable *proposal choice* — present it as ours, not
   as a program requirement (no fixed grant window exists). Then build the
   **credit budget**: map the Prompt-4 uses to a dollar estimate **≤ $50k**, with
   a justified figure and the impact it buys. Define the **success metrics** for
   Claude integration (e.g. fraction of dev-suite setups passing the RMS gate
   blind; lamp-ID accuracy). Argue feasibility from the existing data + baseline.

7. **Broader impact & program fit.** *(Feeds "applications beyond pure discovery /
   paths to scale" — 200 words max — and informs the "anything else" field.)*
   Make the explicit case for funding an *astronomy/instrumentation* project: it
   is **open-source scientific infrastructure** (PypeIt is community-standard);
   the **AI-for-science methodology generalizes** (blind pattern identification +
   calibration is a template for other domains — note the form lists Physics as
   an eligible field); reproducibility and public data. Address why Claude
   specifically (reasoning over heterogeneous scientific data + code).

8. **Red-team & finalize.** Run a critical pass (consider the `critical-partner`
   skill): check every claim against `design/holygrail_context.md`; verify the
   program facts against the official pages (References); tighten the impact
   statements in light of the full draft. **Enforce every form word limit**
   (300/200-word caps; <300 team; <500 project) — count words per field and trim.
   Confirm the biosecurity answer is "None of the above," the Organization ID and
   submitting email are filled, Physics + Other:Astronomy are selected, and the
   ToS box is acknowledged. Flag anything still needing user input. Produce a
   clean final draft and a short submission checklist keyed to the form fields.

## References (verify program terms here)

- Anthropic — AI for Science Program (announcement):
  <https://www.anthropic.com/news/ai-for-science-program>
- Claude Help Center — Anthropic's AI for Science Program:
  <https://support.claude.com/en/articles/11199177-anthropic-s-ai-for-science-program>
- Claude Help Center — External Researcher Access Program:
  <https://support.claude.com/en/articles/9125743-what-is-the-external-researcher-access-program>

## Q&A

*(Questions for the user are logged here.)*

1. **Program target.** Is the intended program specifically the **AI for Science
   Program** (API credits, the focus of this doc), or the related **External
   Researcher Access Program**? The prompts target the former; confirm so the
   application fields match.

Yes, the API credits.

2. **PI/team & budget.** Who is the PI/team (credentials/links), and what credit
   amount (≤ $20k) and 6-month start should the budget/timeline assume? (See
   *Inputs needed from the user*.)

The PI/team are as listed in the Inputs needed from the user section.  The budget is TBD.  The timeline is TBD.

3. **Submitting email & Organization ID.** The form PDF is pre-filled with
   **xavier@ucolick.org**, while the credits account noted is **jxp@ucsc.edu**.
   Which email submits the form, and what is the **Anthropic Organization ID**
   (UUID at `console.anthropic.com/settings/organization`) the credits should
   attach to? *(Required form field — needed before submission.)*

4. **Credit amount.** The ceiling is now **$50k** (not $20k). What figure should
   the budget request, and over what project timeline? *(Still TBD per Q2.)*

5. **"Where did you hear about this program?"** What should this field say?

6. **AI/ML credentials for Cooke & Hennawi.** The team description must establish
   AI/ML experience for all listed PIs; their entries in *Inputs* still read
   "ADD YOUR ML HERE." Please supply.

## Requests

*(Requests for additional material are logged here.)*

- If available, a **copy of the actual application form / its exact questions**
  would let the prompts map 1:1 to the required fields rather than the inferred
  structure above.

I have added a PDF of the form in the proposals/ folder.

  → **Resolved.** Form read; Prompt 1 now maps 1:1 to the real fields and the
  Background section is corrected (award **≤ $50k**, no fixed 6-month window,
  Org-ID required, biosecurity declaration). Outstanding user inputs are now
  tracked as Q&A items 3–5 below.

## Logging

The "Logs" section records Claude's work, newest last, using:

### <Date> (Short summary of the work)

<Detailed description of the work and what was learned>

## Logs

### 2026-06-20 (Prompt 0 — reconciled the prompt doc with the real application form)

Read the application form PDF (`proposals/Application Form - Anthropic's AI for
Science Program.pdf`) and the user's inline edits, then revised this prompt doc
to match. Corrections the form forced:

- **Award is up to $50,000**, not $20k — fixed in Background, Inputs, and Prompts
  6 & 8. The exact amount is set during evaluation; the applicant states what
  they anticipate.
- **No fixed 6-month grant period** exists. The form asks only for a project
  "timeline for completion" and the anticipated credit amount. Reframed the
  6-month plan as a proposal choice, not a program constraint.
- **Organization ID (UUID)** is a required field; added to Inputs/Q&A.
- **Email discrepancy:** form pre-filled with xavier@ucolick.org vs. the
  jxp@ucsc.edu credits account — flagged as Q&A 3.
- **Biosecurity declaration** (new section) → "None of the above" for astronomy.
- **"Physics" is an explicit field checkbox**, so the project fits the form's own
  taxonomy (Physics + Other: Astronomy); softened the "outside the focus" framing.
- Rewrote **Prompt 1** from the inferred skeleton into a **1:1 map of the actual
  form fields** with their word limits (300/200 caps, <300 team, <500 project),
  and annotated Prompts 2–7 with which field each one feeds. Marked the form
  Request resolved; added Q&A items 3–6 for outstanding user inputs.

No draft created yet — that is Prompt 1.

### 2026-06-20 (Prompt 1 — created the draft skeleton + plain-language pitch)

Created `proposals/ai_for_science_application.md` with headings that are a **1:1
map of the real Google-Form fields** (in order, each annotated with its word
limit). Pre-filled everything already known from the Inputs section:

- Contact/Project info: primary contact (Prochaska, UCSC, Professor of Astronomy
  & Astrophysics), website/GitHub + SciXplorer links, project title, field
  selection (Physics + Other: Astronomy), biosecurity = "None of the above".
- Seeded the Team and profile-links fields with the three PIs.
- Marked **[TBD — user]** the fields needing input (submitting email, Org ID,
  credit amount, "where did you hear," Cooke/Hennawi AI/ML credentials) and
  **[Prompt N]** the fields written by later prompts.

Wrote the **plain-language pitch** from `design/holygrail_context.md` §0–§0.1:
the unlabeled-arc problem, the two sub-goals (blind lamp-ID, then calibration),
the literature gap (lamp-ID), and why it matters (transferable, instrument-
agnostic calibrator for PypeIt, ~45 instrument arms). It seeds the project title
and the opening of the <500-word project description.

Next: Prompt 2 (scientific motivation & impact). Several user inputs (Q&A 3–6)
should be supplied before the draft can be finalized.
