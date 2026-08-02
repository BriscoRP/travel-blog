---
project: Project Atlas
repository: travel-blog

document: CODEX_BOOTSTRAP.md
version: 1.1.0
status: Active

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-02
---

# Codex Bootstrap

## Purpose

This document defines how Codex should begin and complete work on Project Atlas.

The repository-level `AGENTS.md` file is the primary entry point. This document provides the detailed session procedure it references.

This document is operational guidance and is not part of the Project Atlas Constitution.

## Guiding Principles

Project Atlas prioritises:

- Mobile-first design.
- Excellent visitor experience.
- Accessibility for all users.
- Privacy by default.
- Fast page performance.
- Simple and maintainable solutions.
- Modern, well-supported web standards.
- Consistency throughout the website.
- Human editorial control.
- Factual accuracy.

Where several valid solutions exist, Codex should recommend the simplest solution that satisfies these principles.

## Session Startup Procedure

Before making recommendations, editing files or running commands, Codex must:

1. Read the repository-level `AGENTS.md`.
2. Read `docs/PROJECT_STATUS.md`.
3. Read the Constitution documents in the order stated in `AGENTS.md`.
4. Review the repository structure and relevant source files.
5. Review the current Git status.
6. Compare the implementation with the Constitution.
7. Identify inconsistencies, ambiguity, risks and technical debt.
8. Ask one clarification question at a time where required.
9. Wait for approval before making significant implementation changes.

Codex must understand the project and the requested outcome before attempting to improve it.

## Work Procedure

For each implementation task, Codex should establish:

- **Goal:** What should change?
- **Context:** Which files and requirements matter?
- **Constraints:** Which Constitution rules and technical limits apply?
- **Done when:** How will successful completion be verified?

Codex should then:

1. Propose a concise approach when the task is significant.
2. Ask for clarification where needed.
3. Make one logical change at a time.
4. Run appropriate checks or tests.
5. Review the resulting diff.
6. Report what changed and how it was verified.

## First Session Only

During Codex's first Project Atlas session, Codex must:

1. Read `AGENTS.md`.
2. Read this Bootstrap document.
3. Read `PROJECT_STATUS.md`.
4. Read the complete Project Atlas Constitution.
5. Review the entire repository.
6. Compare the repository against the Constitution.
7. Make no file changes.
8. Write no implementation code.
9. Produce a structured review.
10. Ask exactly one clarification question.
11. Wait for Rik's answer before continuing.

## Session Completion

At the end of each significant session, Codex should:

- Summarise the work completed.
- State how the work was verified.
- Identify any unresolved risks or questions.
- Recommend the next logical task.
- Update `docs/PROJECT_STATUS.md` when authorised and appropriate.
- Recommend Constitution changes only where genuinely necessary.
- Leave the repository in a clear and reviewable state.