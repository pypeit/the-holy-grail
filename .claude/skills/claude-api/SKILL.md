---
name: claude-api
description: >-
  Reference for the Claude API / Anthropic SDK — model ids, pricing, params,
  streaming, tool use, MCP, agents, caching, token counting, model migration.
  TRIGGER — read BEFORE opening the target file; don't skip because it "looks
  like a one-liner" — whenever: the prompt names Claude/Anthropic in any form
  (Claude, Anthropic, Fable, Opus, Sonnet, Haiku, `anthropic`, `@anthropic-ai`,
  `claude-*`, `us.anthropic.*`, `[1m]`); the user asks about an LLM
  (pricing/model choice/limits/caching) — never answer from memory; OR the task
  is LLM-shaped with provider unstated (agent/MCP/tool-definition/multi-agent/
  RAG/LLM-judge/computer-use; generate/summarize/extract/classify/rewrite/
  converse over NL; debugging refusals/cutoffs/streaming/tool-calls/tokens).
  SKIP only when another provider is being worked on (overrides all triggers):
  OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama named in the query; OR
  `grep -rE 'openai|langchain_openai|google.generativeai|genai|mistralai|cohere|ollama'`
  over the project hits (run this grep FIRST if no provider named — don't Read
  the file).
metadata:
  type: reference
  source: "Anthropic bundled skill `claude-api` (Claude Code 2.1.183), vendored into this repo on 2026-06-20."
---

> **Project-local copy.** This is a vendored copy of Anthropic's bundled
> `claude-api` skill, placed in this repo so the project carries its own pinned
> reference (model ids, pricing, SDK patterns). The per-language reference
> material lives in the sibling folders (`python/`, `typescript/`, `go/`,
> `java/`, `ruby/`, `csharp/`, `php/`, `curl/`, `shared/`) — read the relevant
> `{lang}/claude-api/README.md` and the `shared/*.md` files for full detail.
> Cached values (model table dated below) can drift; verify against
> `shared/live-sources.md` before quoting pricing in anything that ships.

# Building LLM-Powered Applications with Claude

This skill helps you build LLM-powered applications with Claude. Choose the
right surface based on your needs, detect the project language, then read the
relevant language-specific documentation in the sibling folders.

## Before You Start

Scan the target file (or, if no target file, the prompt and project) for
non-Anthropic provider markers — `import openai`, `from openai`,
`langchain_openai`, `OpenAI(`, `gpt-4`, `gpt-5`, file names like
`agent-openai.py` or `*-generic.py`, or any explicit instruction to keep the
code provider-neutral. If you find any, stop and tell the user that this skill
produces Claude/Anthropic SDK code; ask whether they want to switch the file to
Claude or want a non-Claude implementation.

## Output Requirement

When the user asks you to add, modify, or implement a Claude feature, your code
must call Claude through one of:

1. **The official Anthropic SDK** for the project's language (`anthropic`,
   `@anthropic-ai/sdk`, `com.anthropic.*`, etc.). Default whenever a supported
   SDK exists.
2. **Raw HTTP** (`curl`, `requests`, `fetch`, `httpx`) — only when the user
   explicitly asks for cURL/REST/raw HTTP, the project is a shell/cURL project,
   or the language has no official SDK.

Never mix the two. Never fall back to OpenAI-compatible shims. **Never guess SDK
usage** — function/class/namespace/method names must come from the `{lang}/`
files here or the official SDK repos/docs in `shared/live-sources.md`.

## Defaults

Unless the user requests otherwise: use **Claude Opus 4.8** (`claude-opus-4-8`);
default to adaptive thinking (`thinking: {type: "adaptive"}`) for anything
remotely complicated; default to streaming for any request with long input/
output or high `max_tokens` (use `.get_final_message()` / `.finalMessage()`).

## ⚠️ API Drift — Your Training Prior May Be Stale

| Area | Stale prior | Current API |
|---|---|---|
| Extended thinking | `thinking: {type: "enabled", budget_tokens: N}` | On 4.6+ models: `thinking: {type: "adaptive"}`. `budget_tokens` deprecated on Opus 4.6 / Sonnet 4.6, **400** on Fable 5 / Opus 4.8 / 4.7. |
| Web search / fetch tool type | `web_search_20250305`, `web_fetch_20250910` | `web_search_20260209`, `web_fetch_20260209` (dynamic filtering) on Opus 4.8/4.7/4.6 + Sonnet 4.6. |
| PHP parameter names | snake_case wire names | Top-level named args are camelCase (`maxTokens`). Copy nested keys verbatim from examples. |

The `{lang}/` files are authoritative over recalled patterns.

---

## Current Models (cached: 2026-06-04)

| Model             | Model ID            | Context | Input $/1M | Output $/1M |
| ----------------- | ------------------- | ------- | ---------- | ----------- |
| Claude Fable 5    | `claude-fable-5`    | 1M      | $10.00     | $50.00      |
| Claude Opus 4.8   | `claude-opus-4-8`   | 1M      | $5.00      | $25.00      |
| Claude Opus 4.7   | `claude-opus-4-7`   | 1M      | $5.00      | $25.00      |
| Claude Opus 4.6   | `claude-opus-4-6`   | 1M      | $5.00      | $25.00      |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M      | $3.00      | $15.00      |
| Claude Haiku 4.5  | `claude-haiku-4-5`  | 200K    | $1.00      | $5.00       |

**ALWAYS use `claude-opus-4-8` unless the user explicitly names a different
model.** Never downgrade for cost — that's the user's decision. Use exact model
ID strings as-is; do not append date suffixes. Full catalog, capability lookup,
and request-resolution table: `shared/models.md`.

**Pricing levers:** Batch API = **50%** of standard prices (`shared/*/batches.md`).
Prompt-cache reads ≈ **0.1×** input price; cache writes **1.25×** (5-min TTL) /
**2×** (1-h TTL) — break-even at ~2 requests (5-min) or ~3 (1-h). Details:
`shared/prompt-caching.md`.

---

## Quick-Reference Topics (read the named file for detail)

- **Thinking & effort** — adaptive thinking + `output_config.effort`
  (`low|medium|high|xhigh|max`). `shared/model-migration.md`.
- **Prompt caching** — prefix-match invariant, breakpoint placement, silent
  invalidators, pre-warming. `shared/prompt-caching.md`.
- **Tool use** — runner vs manual loop, strict tools, parallel tool results,
  server tools (web search/fetch, code execution, tool search).
  `shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`.
- **Structured outputs** — `output_config.format` / `messages.parse()`;
  `output_format` is deprecated.
- **Managed Agents** — server-managed stateful agents; Agent (once) → Session
  (every run). `shared/managed-agents-*.md` + `{lang}/managed-agents/README.md`.
- **Errors** — typed exception chains per language. `shared/error-codes.md`.
- **Token counting** — use `messages.count_tokens`, never `tiktoken`.
  `shared/token-counting.md`.
- **Model migration** — breaking changes per target model, retired-model
  replacements. `shared/model-migration.md`.
- **Provider platforms** — per-feature availability across first-party / AWS /
  Bedrock / Vertex / Foundry. `shared/platform-availability.md`.
- **Latest docs** — WebFetch URLs in `shared/live-sources.md`.

## Language Detection

Infer from project files, then read that folder: `*.py`→`python/`,
`*.ts`/`*.js`→`typescript/`, `*.java`/`*.kt`/`*.scala`→`java/`, `*.go`→`go/`,
`*.rb`→`ruby/`, `*.cs`→`csharp/`, `*.php`→`php/`; raw HTTP→`curl/`. If
ambiguous, ask. If unsupported (Rust/Swift/C++/…), use `curl/` and offer
Python/TypeScript as reference.
