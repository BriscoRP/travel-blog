---
project: Project Atlas
repository: travel-blog

document: CODEX_RULES.md
version: 1.0.0
status: Active

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-04

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
11. Publish only first-hand family observations and approved editorial content, never copied third-party facts.
12. Treat publication as deny-by-default.
13. Protect private original evidence and personal information.
14. Bind editorial approval to an exact content version.

## Prohibited Behaviour

When working on Project Atlas, Codex must never:

- Invent facts or fabricate information.
- Delete or overwrite user content without explicit approval.
- Introduce breaking architectural changes without approval.
- Commit API keys, passwords, secrets or personal information.
- Modify Constitution documents unless specifically requested.
- Ignore build failures, validation errors or accessibility issues.
- Publish content without human editorial approval.
- Copy external facts into Project Atlas merely to complete missing information.
- Publish an external link without Rik's explicit approval.
- Store private original evidence in the public Git repository by default.
- Expose private storage URLs, personal filenames, local paths, contact details, unintended GPS metadata or private storage arrangements.
- Publish family member identities unless Rik has explicitly approved identification and the person is comfortable being named.
- Infer publication approval from completeness, location, filename or previous publication.

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
- Distinguish prototype choices from approved architecture.
- Retain an existing technology only when it remains the simplest correct choice under the Constitution.
- Keep private original evidence, approved derivative publishing assets and generated public assets clearly separated.
- Use stable opaque identifiers for references to private evidence.
- Treat time-sensitive observations as dated evidence rather than permanently current facts.

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
- Distinguish first-hand observation from official information and editorial interpretation.

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
- Design Places to support one or more Visits, even if Version 1 initially implements one Visit per Place.
- Exclude Draft and Review records from production.
- Include Published records only when their approval metadata is valid for the exact content version.
- Treat missing, unknown and malformed publication states as not approved.
- Fail clearly when content appears intended for production but lacks required approval metadata.
- Keep Archived Places out of normal listings while preserving previously published canonical URLs by default.
- Ensure preview content is protected from indexing and clearly identified as unpublished.

## Evidence and Privacy Rules

The public Git repository is the publishing repository, not the archival repository.

Codex must:

- keep raw photographs, audio, video, messages, personal notes, full transcripts and private documents in Rik's private editorial archive by default
- place only approved publishing content and approved derivative publishing assets in Git
- use only stable opaque identifiers when repository content must refer to private evidence
- ensure only Rik's private editorial archive maps those identifiers to original evidence
- remove unintended metadata from approved derivative assets before publication
- exclude internal visitor identities from public output unless explicit approval has been given

Approval metadata should contain approval status, approval date and approved content version. An opaque internal approver identifier may be stored only if required. Unnecessary public personal information must not be recorded.

## External Information Rules

Codex must not copy official or frequently changing information into Project Atlas merely because it is available.

Where visitors need opening times, prices, booking information, temporary closure details or similar official information, Codex should propose a clearly labelled authoritative link for editorial review.

External links must not be published until Rik has explicitly approved them.

## Place and Visit Rules

A Place represents one physical location and owns one canonical public page.

A Visit represents a dated family visit and contains Visit-specific observations, evidence references and approved derivative assets.

Later Visits should normally improve the existing Place page. Material updates require renewed editorial approval and should display an appropriate Public Last Updated date. Time-sensitive observations should display a Visit or Last Verified date using wording approved by Rik.

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
