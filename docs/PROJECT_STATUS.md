---
project: Project Atlas
repository: travel-blog

document: PROJECT_STATUS.md
version: 1.1.0
status: Active

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-06

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
| Phase | Read-only Google Sheets Connection Checkpoint |
| Status | Live connection proven; awaiting Rik's review |
| Objective | Verify secure read-only access to the private Atlas Test V1 response Sheet without importing a response. |

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
- Repository governance updated for milestone-based startup and session
  completion.
- One-row Atlas Test V1 CSV importer implemented.
- Correct and legacy private visitor headings supported explicitly.
- Opaque Visit, Place, contributor and evidence identifier generation
  implemented.
- Dry-run, idempotency and recoverable private mapping journal implemented.
- Uploaded media registered through opaque evidence references with explicit
  photo/video typing.
- Google Forms Importer automated tests implemented using fictional data.
- Explicit append to an existing `Open` Visit implemented.
- Later submissions preserve all earlier evidence and increment the Visit record
  version once.
- Existing private Place and contributor mappings recovered for append
  validation.
- Place, location, Visit date and visitor differences reported clearly.
- Reordered columns, UTF-8 BOM, quoted commas, multiline cells, empty optional
  cells and multiple upload links covered.
- Full automated suite passing with 45 tests.
- Importer Hardening committed and pushed as `a1819fb`.
- Official desktop OAuth connection implemented with the
  `spreadsheets.readonly` scope.
- Real Atlas Test V1 spreadsheet and response worksheet reached successfully.
- All 13 response headings recognised and the response-row count observed
  changing from 2 to 3 after a deliberately fictional Form submission, without
  printing private response values.

---

## Current Position

- The Visit Capture Foundation supports creating one living `Open` Visit and adding opaque evidence references over time.
- The foundation contains no Google Drive integration, AI drafting, staging, publication or contributor interface.
- The importer accepts an exported CSV containing exactly one Atlas Test V1
  submission.
- Without an explicit existing Visit ID, it creates a proposed new `Open`
  Visit and never attempts an automatic merge.
- With `--existing-visit-id`, it appends one distinct submission to that exact
  existing `Open` Visit.
- Create uses `VisitStore.create`; append uses one optimistic
  `VisitStore.save`.
- Raw form values, private visitor labels and Google provider references remain
  in a separate explicitly private mapping output.
- There is no Google API, authentication, live connectivity, AI, staging,
  publication or website behaviour.
- The hardened importer is committed and present on `origin/main`.
- The Google Sheets checkpoint authenticates Rik through a private local
  desktop OAuth flow and performs structural read-only checks only.
- OAuth client configuration, tokens and Sheet identifiers remain outside Git.
- The real Sheet is read-only to Atlas; no response has been imported.

---

## Next Tasks

1. Review the read-only Google Sheets connection checkpoint.
2. Confirm the OAuth, private-configuration and safe-output boundaries.
3. Commit and push the checkpoint only after Rik's separate approvals.
4. Design the larger Google-to-importer workflow only after separate approval.

No subsequent implementation milestone is authorised.

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
- Updated `AGENTS.md` with the current startup, milestone and session-completion
  governance.
- Implemented the CSV-only Google Forms Importer using the existing
  storage-independent Visit foundation.
- Added private mapping output, dry-run, idempotent retry and safe failure
  behaviour.
- Preserved the current misspelled Google Sheet visitor heading as an explicitly
  supported input.
- Implemented the focused Importer Hardening milestone.
- Added explicit append to an existing `Open` Visit without automatic matching.
- Added private Place/contributor recovery, difference reporting, optimistic
  versioning and recoverable append failure handling.
- Verified the complete implementation with 45 passing tests.

### 2026-08-06

- Committed and pushed the approved Importer Hardening milestone as `a1819fb`.
- Added isolated Google Sheets desktop OAuth scaffolding using only
  `https://www.googleapis.com/auth/spreadsheets.readonly`.
- Stored OAuth configuration, tokens and Sheet identifiers outside the
  repository.
- Successfully authenticated Rik and read the structure of the real Atlas Test
  V1 response Sheet.
- Confirmed 13 recognised headings and observed the response count change from
  2 to 3 after a deliberately fictional Form submission, without printing
  private response content.
- Decided that automated and integration tests will simulate Google Sheet
  responses using fictional data outside the real Sheet.
- The real Sheet remains read-only to Atlas; artificial test rows must never be
  written to it.
- A future real-world validation will use a new submission made through the
  actual Atlas Test V1 Google Form.

---

## Version

Constitution Version: 1.0

Implementation Status: Public website shell, Visit Capture Foundation and hardened importer approved; read-only Google Sheets connection proven and awaiting review

Current Milestone: Read-only Google Sheets Connection Checkpoint
