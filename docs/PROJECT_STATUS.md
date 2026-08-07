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
| Phase | Local Operator Workflow Preparation |
| Status | 7 August goals completed; genuine contribution-to-review path proven and committed |
| Objective | Use the next genuine response to observe operator friction before designing the smallest useful local Admin UX. |

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
- The real Sheet remains read-only to Atlas. One Rik-selected response has been
  persisted through the hardened importer to private storage outside Git.
- Discovery reports only total, processed and pending counts plus opaque Atlas
  response IDs.
- Importing one response requires explicit selection. Append still requires an
  explicit existing Visit ID; similar or identical rows are never merged
  automatically.
- Rik explicitly selected the later genuine Bluebell Wood response and
  classified its single uploaded-media reference as `photo`.
- That response passed hardened-importer dry-run validation and was then
  persisted with separate explicit approval as one genuine private `Open`
  Visit, its private mapping and processed-response state.
- The fictional Place pages are committed review prototypes, remain
  `noindex, nofollow`, have no canonical URLs and are excluded from the
  sitemap.
- The private Media Intake Foundation accepts explicitly selected JPEG, PNG or
  prepared WebP still images from outside the repository.
- Rik must explicitly select the Place source record, Visit ID, `hero` role and
  accessibility-focused alt text. V1 does not infer association or final alt
  text and does not yet implement galleries.
- The engine loads the selected Visit from an explicitly private Visit store
  and requires its opaque Place ID to match the selected Place record; it never
  guesses the association from filenames, folders, metadata or image content.
- Dry-run plans the complete operation without changing public source. An
  optional processed preview can be written only to an explicitly private
  directory outside the repository. Apply is a separate explicit action.
- Apply writes metadata-stripped WebP derivatives to the static site's source
  assets and associates responsive metadata with the selected Place. It does
  not commit, push, deploy, approve the Place or publish anything.
- The provisional hero delivery profile uses candidate widths of 480, 800 and
  1200 pixels, capped at the source width; small sources receive only useful
  non-upscaled variants. This is a current-layout demonstration policy, not an
  SEO rule or a fixed Atlas architecture. Final candidates will be selected
  after Rik approves the final Place image slot and representative-device tests.
- The current `sizes` value describes the actual shell slot: viewport width
  minus the two 1rem gutters until the 72rem cap is reached at a 74rem viewport.
  Width descriptors then let the browser account for device pixel density.
- The likely LCP hero is discovered directly in HTML, is not lazy-loaded and
  uses `fetchpriority="high"`; no preload or `<picture>` complexity is added.
- ICC-profiled sources are validated and colour-transformed to standard sRGB
  before derivative output. Invalid or unusable profiles fail safely. Public
  WebPs deliberately omit ICC, EXIF and other private metadata; sources without
  profiles retain the existing safe RGB or RGBA normalisation path.
- Public filenames use the controlled pattern
  `<place-slug>-<role>-<width>.webp` and never use the private source filename.
- One generated fictional image demonstrates a Glasshouse Gardens hero with
  complete `src`, `srcset`, `sizes`, `width`, `height` and approved test alt
  text while retaining every review-only indexing protection.
- The first genuine private `Open` Visit is persisted outside Git with its
  private importer mapping and processed-response state.
- A genuine Bluebell Wood Place source now uses the Visit's exact opaque Place
  association and only Rik-approved public-safe categories. Its local page is
  review-only, `noindex, nofollow`, canonical-free, sitemap-excluded and not
  approved for publication.
- Rik explicitly approved one genuine Bluebell Wood photograph as the primary
  hero after dry-run, private-preview and colour-management validation. The
  public-safe responsive WebPs are associated with the protected review Place;
  the private original remains outside Git and unchanged.
- Hero metadata contains only public delivery fields and Rik-approved alt text.
  The private Visit ID is used for operator-side association validation but is
  not persisted in publishing source or generated HTML.
- The genuine end-to-end content and media path is now proven: private Visit
  association, public-safe Place review, explicit hero selection, private
  validation, public-safe apply, static build and local visual review.
- Rik visually approved the resulting Bluebell Wood page as the V1 Place-page
  direction. Detailed layout and styling, breadcrumbs, tags and filtering, and
  final responsive-image tuning remain deferred until the final template can be
  measured with representative images, Lighthouse and Core Web Vitals.
- The Places listing currently renders no card images, so it does not yet reuse
  the approved primary image. This Primary Place Image Policy gap is recorded
  for the deferred final Place/listing template work.
- The private Visit-ID publishing regression discovered during apply is fixed
  with regression coverage. Opaque identifiers provide identity, never
  authorisation.
- No private media administration UI has been implemented.
- Google Forms built-in email notifications for new responses were enabled by
  Rik at the end of the session.
- V1 does not require Rik's PC or a Python process to run continuously. The
  intended operating loop is notification, Rik opens local Atlas tooling or a
  future local Admin UX, then explicitly checks and processes pending
  submissions. Cloud polling and automation are outside current V1 scope.

## End-of-Day Assessment — 7 August 2026

These are planning estimates, not calculated metrics. Completing today's goals
does not mean Project Atlas itself is complete.

- Goal 1 — Project records accurate: **100% of today's intended scope**.
- Goal 2 — Form to Atlas evidence and media path: **100% of today's intended scope**.
- Goal 3 — Place visual review: **100% of today's intended scope**.
- Estimated overall V1 live readiness: **approximately 75%**.

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

## Primary Place Image Policy

- Every publishable Place will have one explicitly selected primary or hero
  image.
- Rik selects the primary image. Atlas must not randomly choose, rotate, infer
  or automatically replace it.
- The primary image is the Place-page hero and, by default, the image that
  represents the Place on Places listings and cards.
- The same approved underlying image may be reused in different layouts through
  appropriately sized derivatives. It should not be displayed unnecessarily as
  separate duplicate content on the same Place page.
- Additional approved photographs will later receive deliberate editorial
  placement and ordering. Gallery behaviour remains outside the current V1
  media-foundation checkpoint.
- Alt text remains contextual, accessibility-first and Rik-reviewed.
- Responsive candidate widths, candidate count and WebP quality remain
  provisional until the final Place template and representative real
  photographs have been assessed.
- Further image-size and quality optimisation is paused. Final delivery policy
  will be reviewed against the approved Place template, representative images,
  Lighthouse and Core Web Vitals.

## Deferred Place Review Requirements

- Rik's first impression of the Place-page direction is positive.
- Add a visible `HOME > PLACES > [PLACE]` breadcrumb hierarchy.
- Implement correct `BreadcrumbList` structured data.
- Give Places useful tags for search and filtering.
- Keep search and filter result pages `noindex`.
- These are recorded requirements and placeholders only; implementation awaits
  a separately approved refinement task.

## Deferred Before Public V1

- Final Place and site UX.
- Breadcrumb UI and `BreadcrumbList` structured data.
- Tags, filtering and listing/card imagery.
- Final responsive-image candidate and quality policy.
- Accessibility finishing review.
- SEO titles, descriptions, canonicals and structured-data review.
- Lighthouse and Core Web Vitals validation.
- Cloudflare production and deployment validation.
- Controlled publication and indexation policy.
- Final domain and live checks.

---

## Next Tasks

1. Begin the next session with Rik's Daily Stand-Up and explicitly declare the
   new Project Atlas session.
2. If M & G submit a genuine new outing response, use it as the next operational
   test instead of manufacturing another submission where practical.
3. Confirm Rik receives the Google notification and Atlas discovers the new
   response through the existing read-only Sheet connection.
4. Observe operator friction, then design the smallest useful local Admin UX
   for explicit response review, Visit create/append, Place association,
   selected-photo intake, hero and alt-text approval, preview and apply.
5. Keep publication/deployment separately approved and defer final visual and
   SEO refinement until the operational workflow is comfortable.

No further feature implementation is authorised in the 7 August session. The
next session begins with real operational evidence and a fresh approval boundary.

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
- Implemented the engine-first Private Media Intake Foundation with an explicit
  local CLI and no admin web interface.
- Added actual-data validation for JPEG, PNG and prepared WebP inputs, EXIF
  orientation correction, metadata stripping, safe colour-mode conversion and
  decompression-bomb protection.
- Added deterministic responsive WebP planning and explicit dry-run, private
  preview and apply boundaries with collision and partial-output protection.
- Integrated a programmatically generated fictional hero into Glasshouse
  Gardens to prove static responsive image output without using contributor
  media.
- Kept Google Sheets read-only, added no Drive API or scope, and preserved the
  rule that image approval does not approve or publish its Place.
- Persisted the first genuine private Bluebell Wood `Open` Visit and created
  its matching public-safe review-only Place without exposing private Visit
  data in publishing content.
- Applied one explicitly Rik-selected genuine primary hero through the verified
  private Place/Visit boundary, sRGB transformation and metadata-safe WebP
  pipeline; the original remained private and unchanged.
- Fixed the discovered private Visit-ID publishing regression and added
  regression coverage while preserving operator-side association validation.
- Proved the genuine end-to-end content/media path and recorded Rik's visual
  approval of the V1 Place-page direction. Detailed refinement and the admin UI
  remain deferred.
- Verified repeat retrieval was idempotent and could not create a duplicate
  Visit.
- Confirmed the genuine source contained private metadata categories including
  GPS and device metadata without recording their values; the public WebPs
  contained none of those categories.
- Enabled Google Forms built-in email notification for new responses as the V1
  trigger for Rik's explicit local operator workflow; no continuously running
  PC process or cloud polling is required.
- Closed all three 7 August goals at 100% of their intended daily scope and set
  the planning estimate for overall V1 live readiness to approximately 75%.

---

## Version

Constitution Version: 1.0

Implementation Status: Genuine Form-to-private-Visit-to-public-safe-review path proven and committed; local Admin UX not yet implemented and publication remains unapproved

Current Milestone: Local Operator Workflow Preparation
