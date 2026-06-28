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
- **Award:** ⚠️ **SOURCES CONTRADICT.** The application **form PDF** (p.1, "About
  our Process") says up to **$50,000**; the **help-center article** (verified
  2026-06-20, Prompt 8) says up to **$20,000**. Unresolved — the PI must confirm
  the true ceiling before submitting. The draft requests **$48k** on the form's
  figure. The specific amount is decided during evaluation; the form asks the
  applicant to state how much they anticipate and why.
- **Grant period:** ⚠️ also contradictory. The **help-center** states a
  **6-month period**; the **form** mentions no fixed window and asks only for a
  project "timeline for completion." Our ~6-month plan is consistent with the
  help-center either way — present it as the plan, but it is *not* contradicted.
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

2. *(Done — see Logs.)* **Scientific motivation & impact.** *(Feeds the project-description opening and
   the "potential scientific impact" field — 200 words max.)* Using context §1
   (the problem), §9 (instrument/lamp diversity), and §13 (literature), write the
   motivation: how much astronomer/pipeline time wavelength calibration costs;
   that it gates every spectroscopic reduction across ~45 instruments; and the
   specific **gap** — blind *lamp identification* is essentially absent from the
   literature (§13, §14.3). State the impact if solved: a transferable,
   instrument-agnostic calibration that drops into PypeIt and beyond, enabling
   high-throughput and archival spectroscopy. Quantify where possible. Keep the
   distilled impact statement to ≤200 words.

3. *(Done — see Logs.)* **Technical approach.** From context §3–§8 (current PypeIt methods, the
   baseline to beat), §5 (scale-invariant pattern matching), and §14 (RASCAL
   Hough+RANSAC; DTW), lay out the proposed method: (a) lamp-ID step — how an
   LLM/ML + statistical approach could classify the lamp from raw spectral
   features; (b) calibration step — combining parameter-space voting and
   sequence-alignment ideas without the priors those methods require. Be
   explicit about what is novel vs. what reuses prior art. Reference the
   evaluation metric (RMS vs. FWHM-scaled threshold, context §3, §9).

4. *(Done — see Logs.)* **Use of Claude / the API credits.** *(Feeds two fields: "How specifically
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

5. *(Done — see Logs.)* **Team & credentials.** *(Feeds the <300-word team description, the "key team
   members using Claude" list, and the Scholar-links field.)* Using the
   user-supplied inputs, write the team section establishing credibility in
   **both** spectroscopy/astronomy (PypeIt authorship, instrument expertise) and
   AI/ML — the form explicitly weights both. Keep it factual and **under 300
   words**; the SciXplorer links above serve as the profile links. Request any
   missing AI/ML credentials (Cooke, Hennawi) via the Q&A.

6. *(Done — see Logs.)* **Feasibility, milestones & budget.** *(The timeline + outcomes feed the
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

7. *(Done — see Logs.)* **Broader impact & program fit.** *(Feeds "applications beyond pure discovery /
   paths to scale" — 200 words max — and informs the "anything else" field.)*
   Make the explicit case for funding an *astronomy/instrumentation* project: it
   is **open-source scientific infrastructure** (PypeIt is community-standard);
   the **AI-for-science methodology generalizes** (blind pattern identification +
   calibration is a template for other domains — note the form lists Physics as
   an eligible field); reproducibility and public data. Address why Claude
   specifically (reasoning over heterogeneous scientific data + code).

8. *(Done — see Logs.)* **Red-team & finalize.** Run a critical pass (consider the `critical-partner`
   skill): check every claim against `design/holygrail_context.md`; verify the
   program facts against the official pages (References); tighten the impact
   statements in light of the full draft. **Enforce every form word limit**
   (300/200-word caps; <300 team; <500 project) — count words per field and trim.
   Confirm the biosecurity answer is "None of the above," the Organization ID and
   submitting email are filled, Physics + Other:Astronomy are selected, and the
   ToS box is acknowledged. Flag anything still needing user input. Produce a
   clean final draft and a short submission checklist keyed to the form fields.


9. *(Done — see Logs; one question at Q&A 7.)* **Hennawi comments.** Hennawi says "I would make it more clear that partial automated solutions require humans to code up specific algorithms for each instrument or a group of instruments, that these methods rely on pre-calibrated templates, and that there are still significant failure modes, that require human intervention and patching. Make it clear that this task requires a human a few minutes per spectrum if the lines and lamps are known. With knowledge of the lamps (elements), but without the list of lines, humans have to spend days curating and scouring atomic databases. Without knowledge of the lamps (which we typically have, but not always) the problem would take a human hours or days. And there is no known general solution to this problem that is fully automated and does not require some human intervention, either to curate line lists, identify lines manually, or write brittle algorithms that exploit pre-calibrated  (manually) templates."  Please address these comments in the draft.  If you have any questions, please log them in the Q&A section below and I will answer them.  Log your work.

10. **Final draft.** The draft is now complete.  Please review it and make any necessary changes.  Then, please generate a short submission checklist keyed to the form fields.

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
   the budget request, and over what project timeline?

   → PI direction (2026-06-20): request **near the $50k ceiling**. Budget now set
   to **$48k** (agentic-iteration line scaled up). Timeline still ~6 months (TBD
   per Q2 — confirm start date).

   → ⚠️ Prompt-8 red-team finding: the **help-center article says $20k / 6-month**,
   while the **form PDF says $50k**. The $48k request is only valid if the form's
   $50k is current — **PI must resolve this before submitting**; if the cap is
   $20k, rescale the budget.

5. **"Where did you hear about this program?"** What should this field say?

6. **AI/ML credentials for Cooke & Hennawi.** The team description must establish
   AI/ML experience for all listed PIs; their entries in *Inputs* still read
   "ADD YOUR ML HERE." Please supply.

   → Cooke's AI/ML lines supplied (in draft, 2026-06-27). **Hennawi's still
   read "[AI/ML experience — TBD]"** — please supply. (Westfall was also added
   as a 4th Co-I.)

7. **Hennawi's human-time figures + lamp framing (Prompt 9).** I folded Hennawi's
   tiered human-time costs into the "Claude vs. existing" field as the **team's
   expert characterization** (minutes/spectrum with lamps+lines; days curating
   atomic databases with lamps-but-no-line-list; hours–days when the lamp is
   unknown). Two checks: (a) OK to state these as expert estimate without a
   citation? (b) Hennawi notes the lamp is *usually* known — I kept the headline
   ambition as the *fully* unlabeled case (per context §0) and framed the value
   as removing **all** the human steps (even minutes-per-spectrum when the lamp
   *is* known), not only the rare lamp-unknown case. Confirm that framing, or say
   if you want lamp-unknown foregrounded differently.
   A. (a) yes that is fine and (b) yes, confirm that framing.

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

### 2026-06-20 (Prompt 2 — scientific motivation & impact)

Drew on context §1 (the problem), §9 (instrument/lamp diversity + RMS gates),
§13 (literature gap) and §14.3 (lamp-ID is the open problem). Wrote two pieces of
the draft:

- **Project-description → "Scientific question / problem"** sub-block: framed
  wavelength calibration as gating every spectroscopic reduction; the
  line-identification bottleneck; the two assumptions modern solvers still
  require (known lamp; instrument-specific prior/archive); and the literature
  gap — blind *lamp ID* is absent (RASCAL, DTW, xwavecal are step-2-only;
  SPIT classifies frame type, not lamp species). Also restructured that field
  into four labelled sub-blocks (question / methodology / outcomes / timeline)
  so Prompts 3 and 6 slot in.
- **"Potential scientific impact if successful"** field (~150 words, under the
  200-word cap): transferable, instrument-agnostic calibrator dropping into
  PypeIt (~59 arms / ~224 setups), enabling high-throughput + archival
  spectroscopy and closing the blind-lamp-ID gap as a reusable template.

Quantification used: ~59 instrument arms / ~224 dev-suite setups; per-slit/order
RMS as the sole success gate; hundreds–thousands of spectra per exposure for
multi-object/IFU. Next: Prompt 3 (technical approach).

### 2026-06-20 (Prompt 3 — technical approach)

Filled the project-description **"Methodology & approach"** sub-block from §3–§8
(PypeIt baseline), §5 (scale-invariant patterns), and §14.1/§14.2 (RASCAL
Hough+RANSAC; Davenport DTW). Laid out two chained stages and was explicit about
novel vs. reused:

- **Stage 1 — blind lamp ID = novel** (ML/LLM classifier on detected-peak
  pattern + features; trained on labelled raw arcs + synthetic arcs from the
  atomic line lists). Output narrows the line list for Stage 2.
- **Stage 2 — blind calibration = recombination of prior art minus its priors:**
  parameter-space voting (PypeIt §5 cross-ratios + RASCAL Hough in `(D,c)`)
  *without* range/dispersion prior, seeded by Stage 1 not a human; refined with
  DTW-style non-linear tolerance *without* DTW's matched-template / amplitude
  dependence; robust Legendre/RANSAC final fit with line-growth (§7).
- **Evaluation metric** wired to PypeIt's own gate: per-slit/order
  `RMS < rms_thresh_frac_fwhm × FWHM` (0.15×FWHM px) + dev-suite instrument Å
  thresholds (§3, §9), on instrument/config-held-out setups.

The project-description field is now long across its sub-blocks; Prompt 8 will
trim it to <500 words. Next: Prompt 4 (use of Claude / API credits).

### 2026-06-20 (Prompt 4 — use of Claude / API credits, grounded in current pricing)

Loaded the `claude-api` skill to ground model choice + pricing rather than guess.
Current facts used: Opus 4.8 = $5/$25 per 1M in/out; Sonnet 4.6 = $3/$15; Haiku
4.5 = $1/$5; **Batch API = 50% off**; prompt-cache reads ≈0.1× input, writes
1.25× (5-min) / 2× (1-h). Per user request, **vendored the skill into
`.claude/skills/claude-api/`** (copied the 884K language/`shared/` reference
folders from the bundle and authored a `SKILL.md` with frontmatter — the bundle
ships no top-level SKILL.md, and the `<doc>` blocks are appended by the loader
from the folders, so the vendored copy carries the folders + a body that points
at them).

Filled two draft fields:
- **"How specifically will Claude be used"** (~230 w, ≤300): five API workloads —
  (1) blind lamp ID via Opus 4.8 reasoning + high-res vision over peaks/metadata/
  plots; (2) LLM-as-judge solution vetting; (3) agentic experimentation loop over
  the dev-suite corpus; (4) code-gen + PypeIt integration; (5) literature/line-
  list synthesis. Tagged per-use token scale for Prompt 6 (agentic loop dominant
  + cacheable; judging high-volume but batchable/tier-able; vision adds image
  tokens) and flagged Claude Code as incidental, *non-funded* tooling.
- **"How Claude accelerates vs. existing"** (~150 w, ≤200): baseline is
  human-gated (`holy-grail` needs the lamp list + "can fail catastrophically";
  production leans on per-setup expert templates via `pypeit_identify`); Claude
  removes the human from lamp-ID + vetting (a judgment task no matcher does) and
  collapses weeks of per-instrument tuning into corpus-wide iteration.

Next: Prompt 5 (team & credentials) — still needs Cooke/Hennawi AI/ML lines
(Q&A 6).

### 2026-06-20 (Prompt 5 — team & credentials)

Filled the **team description** (~210 w, ≤300) and the **key-members-using-Claude**
list. Established AI/ML credibility for the PI from grounded facts in context
§13.3: Prochaska's SPIT (Jankov & Prochaska 2018, CNN frame classifier, 98.7%)
and the DLA CNN (Parks, Prochaska et al. 2018) — both direct precedents for
spectral pattern ID. Domain credentials given for all three (PypeIt authorship,
high-precision spectroscopy, quasar/IGM + surveys). The profile-links field was
already populated in Prompt 1 (SciXplorer + GitHub).

Flagged, not invented: **Cooke and Hennawi AI/ML experience remain [TBD — user]
(Q&A 6)**; also flagged **Hennawi's PypeIt role wording for user confirmation** —
the Inputs section lists "Co-founder" only for Prochaska and Cooke, so I wrote
Hennawi as "co-developer [confirm]" rather than asserting co-founder.

Next: Prompt 6 (feasibility, milestones, budget) — fills the project-description
outcomes/timeline sub-blocks, the success-metrics field, and the credit budget
(≤ $50k); the dollar figure still needs the user's target (Q&A 4).

### 2026-06-20 (Prompt 6 — feasibility, milestones & budget)

Filled four pieces from context §0.1 (corpus) and §9 (RMS gates):

- **Project-description "Expected outcomes & deliverables"** — open-source blind
  calibrator in PypeIt, benchmark report vs. dev-suite gates + `holy-grail`
  baseline, released labelled dataset/splits, methods paper.
- **Project-description "Timeline"** — ~6-month milestone plan (M1 corpus +
  split; M1–2 lamp-ID; M2–4 calibration; M4–5 dev-suite eval; M5–6 integration +
  write-up), framed explicitly as a proposal choice, not a program window.
- **"How you'll measure success"** (~140 w, ≤200) — blind RMS-gate pass rate on
  held-out setups, lamp-ID accuracy, delta vs. baseline, and Claude-integration
  metrics (judge precision/recall, credits-per-solved-setup).
- **Credit budget** — per-workload table grounded in the Prompt-4 uses and
  current pricing (Opus $5/$25, Batch −50%, cache reads ≈0.1×). **Per PI
  request (2026-06-20), set near the $50k ceiling: $48k** — agentic loop ~$32k
  (dominant, cached, run at high effort), judging ~$6k (batched/tiered), vision
  ~$5k, synthesis ~$2k, contingency ~$3k. Order-of-magnitude check: ~80–100
  rounds (or fewer at `xhigh`/`max` effort). (Initial draft was $35k; raised to
  $48k at the PI's direction, scaling the agentic-iteration line.)

**Flagged:** the $48k figure still benefits from a final PI confirmation
(Q&A 4); the user has directed it toward the ceiling.

Next: Prompt 7 (broader impact & program fit) — the "applications beyond pure
discovery / paths to scale" field (≤200 w) + the "anything else" field.

### 2026-06-20 (Prompt 7 — broader impact & program fit)

Filled two fields:

- **"Applications beyond pure discovery / paths to scale"** (~180 w, ≤200): three
  beats — (1) open-source infrastructure with immediate reach (ships in PypeIt,
  ~45 arms; scales to hands-off calibration for every user + archival mining of
  legacy spectra); (2) the method generalizes (blind source-ID + reference-library
  calibration is a template for mass spec / NMR / Raman / sensor calibration —
  Physics is a listed form field); (3) reproducibility + public data (open code,
  public dev-suite benchmark, released corpus).
- **"Anything else for the committee"** (optional): why Claude specifically (one
  agent chains judgment over heterogeneous data + code/integration, vs. separate
  bespoke models + glue); program fit (astronomy under the Physics field option);
  track record (Anthropic Team customer since 2025, Claude Code already in use →
  ready to deploy credits immediately).

Next: Prompt 8 (red-team & finalize) — verify claims vs context doc, enforce all
word limits, confirm form-field completeness (biosecurity, Org ID, email,
Physics+Other, ToS), produce a clean draft + submission checklist. Outstanding
user inputs before submission: Q&A 3 (email + Org ID), Q&A 5 (where-heard),
Q&A 6 (Cooke/Hennawi AI/ML); budget confirmed near ceiling at $48k (Q&A 4).

### 2026-06-20 (Prompt 8 — red-team & finalize)

Ran the finalize pass. Findings + fixes:

- **⚠️ CRITICAL — credit-ceiling contradiction.** WebFetched the official
  help-center article: it states **up to $20,000** over a **6-month period**.
  The application **form PDF says $50,000**. The program's own materials
  disagree. Flagged prominently at the top of the draft, on the budget field, in
  Background, and in Q&A 4 — PI must resolve before submitting. (The help-center
  *does* confirm a 6-month period, so our ~6-month plan is fine; it also lists
  "biosecurity screening" as a criterion, validating our biosecurity section.)
- **Word limits — counted every capped field.** Only the **project description
  was over** (602 → trimmed to ~395, <500). All others within cap (team ~170,
  Claude-use ~218/300, vs-existing ~142/200, impact ~144/200, applications
  ~159/200, success ~123/200). Added a word-count table to the checklist.
- **Internal number inconsistency fixed:** the draft mixed "~45" and "~59"
  instrument arms. Standardized: **~45** = PypeIt/RAW_DATA corpus breadth;
  **~224 setups** = dev-suite benchmark; removed the standalone "~59 arms."
- **Soft claim grounded:** "weeks of per-instrument tuning" → "substantial,
  per-instrument tuning" (the "weeks" figure isn't in the context doc).
- **Finalized** the project title (dropped the working-title note).
- **Claims spot-checked** against context doc (gap §13/§14.3; RASCAL/DTW step-2
  §14; SPIT 98.7% §13.3; 242 arcs §0.1; RMS<0.15×FWHM §3/§11) — all hold.
- **Added a submission checklist** keyed to the form fields (de-scaffolding step,
  word-count table, form mechanics, outstanding PI inputs, claim spot-check).

Draft is content-complete and within all limits. **Blocking before submission:**
resolve the $20k/$50k ceiling (Q&A 4); fill email + Org ID (Q&A 3); "where heard"
(Q&A 5); Cooke/Hennawi AI/ML (Q&A 6); confirm Hennawi's PypeIt role + start date.

### 2026-06-27 (Prompt 9 — addressed Hennawi's comments)

Folded Hennawi's review points into the draft, respecting word caps (re-counted
after editing):

- **"How Claude accelerates vs. existing"** field (rewritten, now **182/200 words**):
  led with **"no general, fully automated solution exists"**; characterized
  existing "automated" methods as **partial and brittle** — humans hand-code
  algorithms per instrument/group, methods rely on **manually pre-calibrated
  templates**, and failure modes still need human patching. Added Hennawi's
  **tiered human-time cost**: ~minutes/spectrum (lamps + line lists known); days
  curating atomic databases (lamps known, line list not); hours–days (lamp
  identity uncertain — "usually known, but not always"). Kept the PypeIt-specific
  baseline and the "Claude removes the human from both steps" payoff.
- **Project-description "Scientific question"** block: sharpened the
  state-of-the-art clause to call modern solvers **brittle, per-instrument
  algorithms** reliant on **manually pre-calibrated templates** with failure
  modes needing human patching, and to state **no general fully automated
  solution exists**. Project description now **426/500 words** (still under).
- Impact field left as-is to avoid triple-repeating the time figures.

These are consistent with the context doc (§5 "can fail catastrophically"; §6
template-reliant production methods; §8 the human `pypeit_identify` path; §12
NotImplementedError/"too unstable" paths) — Hennawi's framing matches the code
state, so nothing was invented.

Also fixed a **stale pointer** in the draft header (the prompts file was renamed
to `..._prompts.md`) and recorded that **Cooke's AI/ML lines + Westfall (4th
Co-I)** are now in the draft (user edits), leaving **Hennawi's AI/ML still TBD**.

**Questions logged at Q&A 7** (citation for the time figures; confirm the
fully-blind headline framing). Next: Prompt 10 (final review + submission
checklist) — still blocked on Q&A 3 (email/Org ID), 4 (ceiling), 6 (Hennawi
AI/ML), and the Hennawi role/start-date confirmations.
