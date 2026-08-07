---
project: Project Atlas
repository: travel-blog

document: PROJECT_STATUS.md
version: 1.1.0
status: Active

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-07

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
| Phase | Sheets-to-Importer Integration and Place Visual Review |
| Status | Implemented and verified locally; awaiting Rik's review |
| Objective | Review the private Google response bridge and fictional Place-page prototypes without importing or publishing real content. |

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
- Read-only Google Sheets Connection checkpoint committed and pushed as
  `8081208`.
- Private response discovery implemented with opaque Atlas response IDs and
  private pending/processed state.
- Explicit one-response dry-run, create and append bridge implemented through
  the existing hardened importer.
- Google response identity bound to importer idempotency so separate identical
  rows cannot be merged as retries.
- Sixteen dedicated fictional bridge scenarios implemented without writing to
  the real Sheet.
- Three fictional, review-only Place-page prototypes implemented for visual
  review.
- Complete automated suite passing with 69 tests.

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
- Google Sheets access is private, owner-operated and read-only. There is no
  Google Drive access, AI drafting, staging or publication behaviour.
- The hardened importer is committed and present on `origin/main`.
- The Google Sheets checkpoint authenticates Rik through a private local
  desktop OAuth flow and performs structural read-only checks only.
- OAuth client configuration, tokens and Sheet identifiers remain outside Git.
- The real Sheet is read-only to Atlas; no response has been imported.
- Discovery reports only total, processed and pending counts plus opaque Atlas
  response IDs.
- Importing one response requires explicit selection. Append still requires an
  explicit existing Visit ID; similar or identical rows are never merged
  automatically.
- Rik explicitly classified response #3's deliberately fictional uploaded
  evidence as `photo`.
- Live response #3 passed hardened importer validation in dry-run mode and
  proposed one `Open` Visit with exactly one form-response note and one photo.
- Response #3 remains pending. No real response has been persisted to a Visit
  store or private importer mapping.
- The fictional Place pages are uncommitted review prototypes, remain
  `noindex, nofollow`, have no canonical URLs and are excluded from the
  sitemap.

## Approved V1 Media Boundary

- Atlas will not receive broad Google Drive API access merely to automate Form
  upload retrieval. No additional Google OAuth scope is approved.
- Google Sheets remains read-only using the already-approved
  `spreadsheets.readonly` scope.
- Contributors may continue supplying private original photos, video or audio
  through convenient private channels, including the existing Google Form,
  WhatsApp, email and private Google Drive. They do not need to understand
  Atlas filenames, SEO, identifiers, backend systems or publication workflow.
- Rik remains the human curation boundary. For V1, Rik manually reviews and
  selects evidence, then supplies only selected media to a future private Atlas
  media-intake or administration workflow.
- That future workflow should select the intended Place and Visit; accept a
  Rik-selected source image or prepared WebP; validate the file; strip private
  metadata and EXIF where applicable; generate or validate a web-ready WebP;
  produce a clean SEO-friendly filename; and place the publishing derivative
  in the correct project location.
- Original and private contributor files remain outside public Git. Only a
  public-safe derivative that Rik has reviewed and approved may enter the
  website publishing pipeline. Publication is never automatic.
- Alt text is primarily an accessibility description, not a keyword-stuffing
  field. Future AI may propose alt text, but Rik must review and approve it.

## Deferred Place Review Requirements

- Rik's first impression of the Place-page direction is positive.
- Add a visible `HOME > PLACES > [PLACE]` breadcrumb hierarchy.
- Implement correct `BreadcrumbList` structured data.
- Give Places useful tags for search and filtering.
- Keep search and filter result pages `noindex`.
- These are recorded requirements and placeholders only; implementation awaits
  a separately approved refinement task.

---

## Next Tasks

1. Continue Rik's visual review of the three fictional Place prototypes.
2. Decide whether any Place-page refinements should be authorised.
3. Review the uncommitted Sheets-to-importer bridge and its fictional tests.
4. Decide whether response #3 should be imported permanently; it remains
   pending until Rik explicitly approves persistence.
5. Plan the private media-intake workflow only as a separately approved task;
   do not add Google Drive API access or additional Google OAuth scopes.
6. Commit and push later phases only after separate approvals.

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
- Committed and pushed the approved Google Read-Only Connection checkpoint as
  `8081208`.
- Implemented private opaque response discovery and explicit selected-response
  bridging into the hardened importer.
- Kept pending/processed state outside Google and outside public Git.
- Verified that standalone CSV and Google-origin idempotency remain distinct,
  including separate identical Google rows.
- Exercised 16 fictional bridge scenarios and 12-response discovery using only
  simulated sources and temporary private stores.
- Rik explicitly classified response #3's deliberately fictional uploaded
  evidence as `photo`.
- Completed the approved live response #3 dry-run through the hardened
  importer. It proposed one `Open` Visit containing one form-response note and
  one photo.
- Persisted nothing from the dry-run; response #3 remains pending.
- Proved the live Form to Sheet to Atlas to hardened-importer dry-run path
  end-to-end.
- Kept Google Sheets read-only and deliberately deferred Drive metadata,
  download and automated evidence retrieval pending permission-model review.
- Created three explicitly fictional Place-page review prototypes for standard,
  richer and practical/accessibility-focused layouts.
- Preserved `noindex, nofollow`, sitemap exclusion and the human publication
  boundary.
- Verified the complete work with 69 passing tests.

### 2026-08-07

- Locked the day's planning estimates at Goal 1 90%, Goal 2 85%, Goal 3 75%
  and approximately 61% overall V1 live readiness; estimates increase only
  when real capability or an agreed milestone advances.
- Rik's first visual impression of the fictional Place-page direction was
  positive.
- Recorded breadcrumbs, `BreadcrumbList` structured data, Place tags and
  `noindex` search/filter results as deferred requirements, without
  implementation.
- Decided that V1 will not grant broad Google Drive API access merely to
  automate Form-upload retrieval and will request no additional OAuth scopes.
- Retained read-only Google Sheets access and the deliberately simple
  contributor experience across private channels.
- Established Rik as the manual media-curation boundary before any selected,
  validated, metadata-safe and approved derivative can enter publishing.
- Recorded the intended future private image-intake requirements, including
  Place/Visit selection, validation, metadata stripping, WebP preparation,
  clean naming and Rik-approved accessibility-focused alt text.

---

## Version

Constitution Version: 1.0

Implementation Status: Read-only Google connection committed and pushed; uncommitted Sheets-to-importer bridge and fictional Place prototypes implemented and awaiting review

Current Milestone: Sheets-to-Importer Integration and Fictional Place Visual Review
