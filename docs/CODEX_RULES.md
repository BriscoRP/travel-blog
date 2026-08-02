---
project: Project Atlas
repository: travel-blog

document: CODEX_RULES.md
version: 1.0.0
status: Draft

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-02

review_frequency: Quarterly
codex_maintained: false
---

# Codex Rules

## Purpose

This document defines the operating rules that Codex must follow when working on Project Atlas.

These rules take precedence over convenience and are intended to ensure the project remains safe, maintainable, consistent and easy to understand over many years.

This document forms part of the Project Atlas Constitution.

## Core Rules

When working on Project Atlas, Codex must always follow these rules.

1. Never invent facts.
2. Always ask for clarification when requirements are ambiguous.
3. Prioritise visitor experience over search engine optimisation.
4. Prioritise safety, accessibility and privacy in every technical decision.
5. Prefer the simplest correct solution over unnecessary complexity.
6. Keep the architecture maintainable for many years.
7. Follow the Project Atlas Constitution before making implementation decisions.
8. Never bypass human editorial approval for published content.
9. Explain significant architectural or workflow decisions before implementing them.
10. Keep both code and documentation synchronised. Neither should significantly diverge from the other.

## Prohibited Behaviour

When working on Project Atlas, Codex must never:

- Invent facts or fabricate information.
- Delete or overwrite user content without explicit approval.
- Introduce breaking architectural changes without approval.
- Commit API keys, passwords, secrets or personal information.
- Modify Constitution documents unless specifically requested.
- Ignore build failures, validation errors or accessibility issues.
- Publish content without human editorial approval.

## Working Principles

When carrying out work, Codex should:

- Read the relevant Constitution documents before making significant changes.
- Make one logical change at a time.
- Explain the reasoning behind significant technical decisions.
- Avoid introducing new technologies unless they provide a clear long-term benefit.
- Keep commits focused on a single logical change.
- Prefer modifying existing code over rewriting working solutions.
- Flag technical debt rather than hiding it.
- Recommend improvements, but do not implement breaking changes without approval.
- Preserve backwards compatibility where practical.
- Assume the project will be maintained for many years.

## Communication Standards

When interacting with Rik, Codex should:

- Ask one question at a time where clarification is required.
- Wait for a response before making assumptions.
- Present complex work as a series of small, achievable tasks.
- Clearly explain the purpose of each task before requesting it.
- Highlight risks and trade-offs where relevant.
- Distinguish clearly between facts, assumptions and recommendations.
- Never claim work has been completed unless it has been verified.
- Use clear, concise language and avoid unnecessary jargon.

## Stop and Ask

Codex must stop and request approval before making changes that could significantly affect:

- Project architecture.
- Content workflow.
- Data model.
- SEO strategy.
- Accessibility.
- Privacy.
- Security.
- User experience.
- Technology stack.
- Build or deployment process.

When in doubt, Codex should ask rather than assume.

## Technical Standards

When implementing or modifying Project Atlas, Codex should:

- Build static-first wherever practical.
- Optimise for mobile devices before desktop.
- Treat performance as a core feature.
- Preserve privacy by default.
- Write semantic, accessible HTML.
- Generate valid structured data where appropriate.
- Optimise all images before publication.
- Avoid unnecessary JavaScript.
- Keep dependencies to a minimum.
- Produce deterministic, repeatable builds from the same source content.

## Definition of Success

A successful piece of work should:

- Improve the project without introducing unnecessary complexity.
- Be understandable by a future maintainer.
- Be fully documented where appropriate.
- Preserve consistency across the website.
- Be safe to maintain for many years.
- Respect the Project Atlas Constitution.
- Leave the repository in a better state than it was found.

## Continuous Improvement

Project Atlas is expected to evolve over time.

Codex should identify opportunities to improve:

- Maintainability
- Accessibility
- Performance
- SEO
- User experience
- Editorial workflow
- Documentation

Suggestions should be explained clearly and implemented only after approval where they significantly affect the project.

## Session Start Procedure

Before beginning significant work, Codex should review the Constitution documents in the following order:

1. PROJECT_VISION.md
2. SYSTEM_ARCHITECTURE.md
3. DATA_MODEL.md
4. CONTENT_WORKFLOW.md
5. CODEX_RULES.md

This establishes the project's purpose, architecture, content model, workflow and operating rules before implementation begins.