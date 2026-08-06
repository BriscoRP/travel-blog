# Project Atlas Agent Instructions

## Purpose

This file is the primary entry point for AI coding agents working in the Project Atlas repository.

Project Atlas is an AI-assisted, static-first travel publishing platform based on genuine family visits and experiences.

## Mandatory Startup

Before making recommendations, editing files or running commands:

1. Read `docs/CODEX_BOOTSTRAP.md`.
2. Read `docs/PROJECT_STATUS.md`.
3. Read `NEXT_SESSION.md`.
4. Read the Constitution documents in this order:
   1. `docs/PROJECT_VISION.md`
   2. `docs/SYSTEM_ARCHITECTURE.md`
   3. `docs/DATA_MODEL.md`
   4. `docs/CONTENT_WORKFLOW.md`
   5. `docs/CODEX_RULES.md`
5. Identify the current implementation milestone from the status and handover
   before proposing work.
6. Review the current repository and Git status.
7. Compare the implementation against the documentation.
8. Ask one clarification question at a time where requirements are unclear.
9. Wait for approval before making significant changes.

## Core Repository Rules

- Git is the single source of truth.
- Never invent facts or travel information.
- Never publish content without Rik's approval.
- Never delete or overwrite user content without explicit approval.
- Never commit secrets, passwords, API keys or personal information.
- Do not modify Constitution documents unless explicitly requested.
- Prefer the simplest correct solution.
- Build static-first, mobile-first and privacy-first.
- Prioritise accessibility, performance and visitor experience.
- Avoid unnecessary JavaScript and dependencies.
- Keep code and documentation synchronised.
- Keep each commit focused on one logical change.
- Verify work before claiming it is complete.

## Incremental Development

Project Atlas is developed through small, explicitly approved milestones.

- Build the smallest safe working slice that advances the current milestone.
- Keep exploratory prototypes separate from approved implementation.
- Validate each slice with realistic workflow evidence and automated tests
  before expanding it.
- Do not begin the next implementation milestone until Rik approves the current
  result.
- Treat future capabilities described in plans as out of scope until separately
  authorised.

## Standard Session Completion

At the end of each significant development session:

1. Update `docs/PROJECT_STATUS.md`.
2. Update `NEXT_SESSION.md`.
3. Run appropriate verification and review the complete Git diff.
4. Verify and report Git status.
5. Recommend a focused commit message.
6. Wait for Rik's explicit approval before committing.
7. Wait for Rik's explicit approval before pushing.

## First Review

During the first Project Atlas session:

- Do not modify files.
- Do not write code.
- Do not run destructive commands.
- Produce a concise repository and Constitution review.
- Identify inconsistencies, ambiguity, technical debt and missing decisions.
- Ask exactly one clarification question and wait for Rik's reply.
