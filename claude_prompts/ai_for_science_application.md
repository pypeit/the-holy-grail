# Prompt document: Anthropic "AI for Science" Program application

## Purpose

This is a **prompt document**: a sequenced set of prompts that will guide Claude
(and the user) through drafting a strong application to **Anthropic's AI for
Science Program** for *The Holy Grail* project (automated, blind wavelength
calibration of arc-line spectra).

Execute the prompts **in order**. Each produces a section of the application,
written into a working draft at `design/ai_for_science_application.md`. Earlier
sections (summary, impact) should be revisited after later ones (methods,
budget) are written, so the final pass is a coherence/edit prompt.

Treat [holygrail_context.md](holygrail_context.md) → `design/holygrail_context.md`
as the **source of truth** for all technical and project facts. Do not invent
results; cite the context doc's sections (§0–§14) where relevant.

## Background — the program (verify before submitting)

Summary of the program as of June 2026 (confirm against the official pages
listed in *References* below — terms change):

- **What:** free Anthropic **API** credits (not the Claude web app) for
  researchers, to support high-impact scientific work.
- **Award:** up to **$20,000** in API credits, applied for a **6-month** period.
- **Eligibility:** researchers at **academic / nonprofit** institutions; not in
  countries under U.S. export restrictions.
- **Application:** a proposal covering **project goals, methodology, and how the
  API credits will be used**, plus **team/researcher details**.
- **Evaluation criteria:** **scientific merit · potential impact · technical
  feasibility · team credentials** (in both the subject area *and* AI).
- **Cadence:** applications reviewed on the **first Monday of each month**.
- **Focus:** biology / life sciences are called out as priorities, but the
  program covers topics Anthropic deems high priority broadly. → The application
  must make the impact + AI-methodology case explicitly, since astronomy is
  outside the headline focus (see Prompt 7).

## Inputs needed from the user (fill before/while drafting)

These are facts only the user can supply; the prompts will ask for them, but
collecting them up front helps:

- **PI / team:** names, roles, institutions, relevant credentials in (a)
  astronomy/spectroscopy and (b) AI/ML; links (ADS, GitHub, ORCID).
- **Institutional eligibility** confirmation (academic/nonprofit).
- **Credit budget:** desired amount (≤ $20k) and the rough split across uses.
- **Timeline:** intended 6-month start; any external deadlines.
- **Anthropic account** email the credits would attach to.
- Any **prior Anthropic** engagement (this project's logs already note Claude
  Code use).

## Claude / Skills

- Use the project context doc and the three codebases (PypeIt, dev-suite,
  arclines) for grounding.
- The `deep-research` skill may help sharpen the impact/landscape section;
  `critical-partner` is useful for the pre-submission red-team (Prompt 8).

## Prompts

1. **Set up the draft + extract the pitch.** Create
   `design/ai_for_science_application.md` with a section skeleton matching the
   application components (Summary, Scientific motivation & impact, Technical
   approach, Use of Claude / API credits, Team, Feasibility & milestones,
   Budget & credit usage, Broader impact / open science, References). Then,
   from `design/holygrail_context.md` §0–§0.1, write a 3–5 sentence **plain-language
   pitch**: the problem (turning an *unlabeled* arc spectrum into a wavelength
   solution with no human input), the two sub-goals (lamp-ID, then calibration),
   and why it matters.

2. **Scientific motivation & impact.** Using context §1 (the problem), §9
   (instrument/lamp diversity), and §13 (literature), write the motivation:
   how much astronomer/pipeline time wavelength calibration costs; that it
   gates every spectroscopic reduction across ~45 instruments; and the specific
   **gap** — blind *lamp identification* is essentially absent from the
   literature (§13, §14.3). State the impact if solved: a transferable,
   instrument-agnostic calibration that drops into PypeIt and beyond, enabling
   high-throughput and archival spectroscopy. Quantify where possible.

3. **Technical approach.** From context §3–§8 (current PypeIt methods, the
   baseline to beat), §5 (scale-invariant pattern matching), and §14 (RASCAL
   Hough+RANSAC; DTW), lay out the proposed method: (a) lamp-ID step — how an
   LLM/ML + statistical approach could classify the lamp from raw spectral
   features; (b) calibration step — combining parameter-space voting and
   sequence-alignment ideas without the priors those methods require. Be
   explicit about what is novel vs. what reuses prior art. Reference the
   evaluation metric (RMS vs. FWHM-scaled threshold, context §3, §9).

4. **Use of Claude / the API credits.** Concretely describe *how Claude is used
   in the research* (this is central to the program). E.g.: Claude as a
   reasoning agent over spectra/metadata; code generation and pipeline
   integration; literature/line-list synthesis; agentic experimentation over
   the corpus; LLM-as-judge for solution vetting. Tie each use to an estimated
   token/credit consumption to feed Prompt 6. Distinguish API use (funded) from
   incidental tooling.

5. **Team & credentials.** Using the user-supplied inputs, write the team
   section establishing credibility in **both** spectroscopy/astronomy (PypeIt
   authorship, instrument expertise) and AI/ML. Keep it factual; request any
   missing CV/links via the Q&A.

6. **Feasibility, milestones & budget.** Using context §0.1 (the ready-made
   labelled corpus: `RAW_DATA/`, the 242 `reid_arxiv/` solved arcs, the atomic
   line lists) and §9 (the dev-suite RMS gates as a built-in benchmark), write a
   6-month plan with milestones (data assembly + split-by-instrument; lamp-ID
   prototype; calibration prototype; evaluation against dev-suite thresholds;
   write-up). Then build the **credit budget**: map the Prompt-4 uses to a
   dollar estimate ≤ $20k. Argue feasibility from the existing data + baseline.

7. **Broader impact & program fit.** Make the explicit case for funding an
   *astronomy/instrumentation* project under a bio-focused program: it is
   **open-source scientific infrastructure** (PypeIt is community-standard); the
   **AI-for-science methodology generalizes** (blind pattern identification +
   calibration is a template for other domains); reproducibility and public
   data. Address why Claude specifically (reasoning over heterogeneous
   scientific data + code).

8. **Red-team & finalize.** Run a critical pass (consider the `critical-partner`
   skill): check every claim against `design/holygrail_context.md`; verify the
   program facts against the official pages (References); tighten the Summary
   and Impact in light of the full draft; confirm length/format match the
   application form's fields; flag anything still needing user input. Produce a
   clean final draft and a short submission checklist.

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
2. **PI/team & budget.** Who is the PI/team (credentials/links), and what credit
   amount (≤ $20k) and 6-month start should the budget/timeline assume? (See
   *Inputs needed from the user*.)

## Requests

*(Requests for additional material are logged here.)*

- If available, a **copy of the actual application form / its exact questions**
  would let the prompts map 1:1 to the required fields rather than the inferred
  structure above.

## Logging

The "Logs" section records Claude's work, newest last, using:

### <Date> (Short summary of the work)

<Detailed description of the work and what was learned>

## Logs
