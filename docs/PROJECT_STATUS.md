---
project: Project Atlas
repository: travel-blog

document: PROJECT_STATUS.md
version: 1.1.0
status: Active

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-05

updated_every_session: true
codex_maintained: true

---

# Project Status

## Purpose

This document records the current state of Project Atlas.

Unlike the Constitution documents, this file is expected to change regularly and should be updated at the end of each significant development session.

It provides a single source of truth for current progress, active work and the next planned tasks.

## Current Phase

| Property | Value |
|----------|-------|
| Phase | Google Forms Importer |
| Status | Atlas Test V1 completed and frozen; importer design next |
| Objective | Design and implement an importer that converts a completed Google Form submission into an `Open` Visit using the existing Visit Capture Foundation. |

---

## Completed

- Project Vision completed.
- System Architecture completed.
- Data Model completed.
- Content Workflow completed.
- Codex Rules completed.
- Git repository configured.
- Initial Constitution committed to GitHub.
- Project documentation structure established.
- First read-only repository and Constitution review completed.
- Existing implementation classified as a prototype foundation rather than approved architecture.
- Initial editorial, privacy, data and publication decisions agreed with Rik.
- Constitution frozen as Version 1.0.
- Version 1 Architecture Proposal approved.
- Phase 1 Implementation Plan approved.
- Version 1 UX and Wireframe Specification approved.
- Public website shell implemented for Home, Places, About, How We Create Our Guides, Privacy and Accessibility.
- Shared header, navigation, footer and mobile-first styling implemented.
- Representative Project Atlas review content added.
- Representative shell content protected from indexing.
- Visit Capture Workflow approved as the working design.
- Milestone 2 Visit Capture Foundation implementation plan approved.
- Minimum Visit record contract implemented.
- Storage-independent Visit operations and local YAML adapter implemented.
- Minimal maintainer command interface implemented.
- Visit Capture Foundation automated tests implemented and passing.
- Milestone 2 Tasks 1–4 reviewed and approved by Rik.
- Visit Capture Foundation committed and pushed to `origin/main`.
- `Atlas Test V1` completed as an exploratory contributor prototype.
- Two end-to-end manual submissions used to inspect the contributor experience
  and captured data.
- Required location context and private visitor identity added after the first
  test.
- `Atlas Test V1` frozen for the first family pilot.

---

## Current Position

- The Visit Capture Foundation supports creating one living `Open` Visit and adding opaque evidence references over time.
- The foundation contains no Google Drive integration, AI drafting, staging, publication or contributor interface.
- `Atlas Test V1` is sufficiently aligned with the Constitution, Version 1
  Architecture, Visit Capture Workflow and Visit Capture Foundation for the
  first family pilot.
- The manual prototype remains separate from the implemented foundation.
- The next implementation milestone is the Google Forms Importer.

---

## Next Tasks

1. Define the minimum Google Forms Importer contract and privacy boundaries.
2. Map a completed form response to one `Open` Visit and opaque evidence
   references.
3. Define how private Google identifiers, spreadsheet links, filenames and
   contributor identities remain outside public Git.
4. Design idempotency, duplicate handling, ambiguous-record handling and clear
   failure behaviour.
5. Obtain Rik's approval for the importer implementation plan.
6. Implement and test the smallest working importer slice using fictional data.

The importer must create only an `Open` Visit. AI drafting, readiness,
editorial approval, staging and publication remain out of scope.

---

## Current Repository

travel-blog/
├── AGENTS.md
├── docs/
│   ├── PROJECT_VISION.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── DATA_MODEL.md
│   ├── CONTENT_WORKFLOW.md
│   ├── CODEX_RULES.md
│   ├── CODEX_BOOTSTRAP.md
│   └── PROJECT_STATUS.md
├── dist/
├── public/
├── schemas/
├── src/
├── tests/
├── visit_capture/
├── build.py
└── requirements.txt

---

## Session Notes

This file should be updated at the end of every significant development session with:

- Progress made.
- Decisions taken.
- Outstanding questions.
- Next planned actions.

---

## Latest Update

### 2026-08-05

- Approved the Visit Capture Workflow as the working design.
- Approved the Milestone 2 Visit Capture Foundation implementation plan.
- Implemented and verified Tasks 1–4: the minimum Visit contract,
  storage-independent operations, the maintainer command interface and
  automated tests.
- Confirmed that a Visit remains a living `Open` record while opaque evidence
  references are added over time.
- Kept private evidence files, Google Drive, AI drafting, staging, publication,
  Place pages and contributor interfaces outside the implementation.
- Rik approved Milestone 2 Tasks 1–4.
- Set the next planned activity as the manual `Atlas Test V1` Google Forms
  prototype to validate the family contributor workflow.
- Completed two end-to-end `Atlas Test V1` submissions.
- Confirmed that the form is simple enough for the first family pilot and
  captures the minimum destination, location, private visitor, date,
  observation and optional-media context.
- Froze `Atlas Test V1` for the first family pilot.
- Set the next objective as designing and implementing the Google Forms
  Importer using the existing Visit Capture Foundation.

---

## Version

Constitution Version: 1.0

Implementation Status: Public website shell and Visit Capture Foundation implemented; Atlas Test V1 exploratory prototype completed and frozen; Google Forms Importer not yet implemented

Current Milestone: Google Forms Importer design and implementation
