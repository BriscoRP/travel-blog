# Project Atlas — Session Handover

## Project goal

- Preserve and share genuine family travel experiences.
- Build a simple, static and privacy-first website.
- Make it easy for family members to contribute from their iPhones.
- Use AI to assist with drafting while Rik retains editorial control.
- Optimise for long-term maintainability rather than rapid feature growth.

## Current milestone

The read-only Google Sheets Connection checkpoint is committed and pushed.
The uncommitted Sheets-to-importer bridge and fictional Place-page visual
prototypes are implemented. Rik's first visual impression is positive, with
specific refinements recorded for later approval.

No AI, staging, publication or Google Drive API milestone is authorised.

## Current position

- The Constitution is frozen as Version 1.0.
- The public website shell and Visit Capture Foundation are approved.
- `Atlas Test V1` is frozen for the first family pilot.
- The Google Form and linked Google Sheet remain private operational tools.
- The approved importer is committed and pushed as `a1819fb`.
- The isolated Google Sheets checkpoint uses official desktop OAuth and only
  the `spreadsheets.readonly` scope.
- OAuth files, tokens, Sheet identifiers and private responses remain outside
  the repository.
- Atlas successfully authenticated Rik and reached the real Atlas Test V1
  response worksheet.
- The structural proof recognised all 13 headings and observed the response
  count change from 2 to 3 after a deliberately fictional Form submission,
  without printing response values.
- V1 will not receive broad Google Drive API access merely to automate Form
  upload retrieval. No additional Google OAuth scope is approved.
- No private family submission has been imported by this implementation.
- Opaque response discovery now reports pending and processed state without
  displaying response contents.
- One explicitly selected response can be dry-run, created as a new Visit or
  appended to an explicitly supplied existing Visit through the hardened
  importer.
- Similar and even identical Google rows never trigger automatic merging.
- Rik explicitly classified response #3's deliberately fictional upload as a
  photo.
- Response #3 passed the hardened importer dry-run and proposed one `Open`
  Visit containing one form-response note and one photo.
- Nothing from that dry-run was persisted; response #3 remains pending.
- The live Form to Sheet to Atlas to hardened-importer dry-run path is proven
  end-to-end.
- Three fictional Place prototypes are available for visual review and cannot
  qualify as approved production content. Rik's first impression is positive.
- Visible breadcrumbs, correct `BreadcrumbList` structured data, useful Place
  tags and `noindex` search/filter results are deferred requirements only.

## Approved V1 private media boundary

- Contributors may send private original media through the existing Google
  Form, WhatsApp, email or private Google Drive without learning Atlas backend
  or publication concepts.
- Rik manually reviews and selects evidence before supplying it to a future
  private Atlas media-intake or administration workflow.
- That future workflow should associate the intended Place and Visit, validate
  selected files, remove private metadata where applicable, prepare a
  web-ready WebP with a clean filename, and keep originals outside public Git.
- Alt text is an accessibility description. AI may eventually propose it, but
  Rik must review and approve it.
- Only Rik-approved public-safe derivatives may enter publishing, and
  publication is never automatic.

## What was implemented

- Updated `AGENTS.md` to include `NEXT_SESSION.md` in startup, identify the
  current milestone before work, record incremental development and require
  Rik's separate commit and push approval.
- Added strict CSV parsing for exactly one Atlas Test V1 response.
- Supported both:
  - `Who went on the visit? (private)`
  - `Who went on the vist? (private)`
- Preserved the exact visitor heading used by the source in the private mapping.
- Generated opaque Visit, Place, contributor, evidence and import identifiers.
- Allowed an existing opaque Place ID to be supplied instead of generating one.
- Built and validated one complete `Open` Visit before persistence.
- Registered the complete form response as opaque note evidence.
- Registered photo, video and audio uploads as opaque evidence references.
- Required explicit photo/video types when the CSV link alone is ambiguous.
- Added a separate private YAML mapping output for raw form values and provider
  references.
- Added dry-run mode, source fingerprinting, idempotent re-import and
  recoverable pending/complete journal states.
- Required Visit storage and private mapping output to be outside the public
  repository when using the CLI.
- Added `--existing-visit-id` for an explicit append to one existing `Open`
  Visit.
- Recovered the existing private Place and contributor mappings before append.
- Compared submitted Place name, location, Visit date and private visitor set
  with the existing mapping and reported every difference.
- Preserved all earlier evidence and appended the new form response and media
  in one record update.
- Incremented `record_version` once per distinct appended submission.
- Used optimistic version checking for the append save.
- Kept identical first and later submissions idempotent after the Visit evolves.

## Privacy boundary

The Open Visit contains only:

- Opaque identifiers.
- Visit date and precision.
- `Open` state.
- Safe generic evidence descriptions.
- Record timestamps and version.

The separate private mapping contains:

- Raw form headings and values.
- Private visitor labels.
- Place name and submitted location.
- Google or other provider references.
- The mapping from private values to opaque identifiers.
- The exact planned Visit used for recovery and idempotency.

The private mapping must remain outside public Git.

## Verification

- All 69 automated tests pass.
- Tests use fictional submissions and temporary directories.
- Dry-run writes neither a Visit nor a mapping.
- Re-importing either source fingerprint returns the current existing Visit.
- A distinct later submission appends only when Rik explicitly supplies the
  existing Visit ID.
- Omitting the existing Visit ID creates a separate proposed Visit and never
  merges automatically.
- Closed or unknown states, mapping conflicts and stale versions are rejected.
- Reordered columns, a UTF-8 BOM, quoted commas, multiline paragraphs, empty
  optional cells and multiple uploaded-file links are supported or tested.
- Ambiguous media typing fails before any output is written.
- Normal create or append storage failures remove their new pending mappings.
- Pending create or append mappings can recover interrupted imports on retry.
- Existing Visit Capture Foundation behaviour remains covered.

## Implementation decisions

- Input is a CSV export, not a live Sheet.
- Exactly one response row is imported at a time.
- CSV headings are strict so unexpected private fields are not ignored.
- The raw response is private evidence rather than approved public content.
- Google timestamps are retained as local source timestamps without inventing a
  timezone.
- Visit dates are normalised from `DD/MM/YYYY` to ISO `YYYY-MM-DD`.
- Visitor labels are split on commas, semicolons or new lines and mapped to
  random opaque contributor IDs.
- Photo/video types must be provided explicitly in source-link order because
  Drive URLs do not safely identify media type.
- The importer calls `VisitStore.create` once with a fully validated Visit.
- A later submission is appended only through an explicit
  `--existing-visit-id`; text similarity is never used.
- Append requires the original private create mapping and reuses its Place and
  contributor IDs.
- Append calls `VisitStore.save` once with the expected prior record version.

## Provider adapter boundaries

The implemented private Google Sheets bridge supplies one explicitly selected
response to the hardened importer. V1 will not add broad Google Drive API access
to resolve Form-upload references. Rik instead remains the manual curation
boundary for media selected from contributors' private channels.

Provider adapters must not change:

- Visit validation.
- Opaque public-repository references.
- `Open` state behaviour.
- Editorial approval boundaries.
- The separation between private evidence and publishing Git.

Automated and integration tests must simulate Google Sheet responses with
fictional data outside the real Sheet. Atlas must never write artificial test
rows to the real Form response Sheet. Final real-world validation will use a
new submission through the actual Atlas Test V1 Google Form.

Google Drive metadata access, downloads and automated evidence retrieval are
not part of the approved V1 approach. No additional Google permission or OAuth
scope is authorised.

## Current repository status

- Branch: `main`.
- Baseline commit: `8081208`.
- The Sheets-to-importer bridge, tests, operational documentation and
  fictional Place visual prototypes are modified or untracked.
- No Constitution files changed.
- No Phase 2 or Phase 3 work has been committed or pushed.

## Handover boundaries

### Committed and pushed

- Google Read-Only Connection checkpoint `8081208` and everything before it.

### Uncommitted

- Google Sheet to hardened-importer bridge and new-response discovery.
- Fictional Place-page visual-review work.
- Associated tests, documentation, source and generated build changes.

### Proven live

- Real Atlas Test V1 Form to private Sheet to Atlas read-only connection.
- Explicitly selected response #3 to hardened-importer dry-run, using Rik's
  explicit `photo` classification.

### Not yet done

- Permanent import of response #3.
- A separately approved private media-intake or administration workflow.
- Any approved Place refinements following Rik's visual review.
- Any real or public Place publication.

## Next objective

Continue Rik's visual review of the fictional Place-page prototypes, then
decide whether any recorded refinements should be authorised.

## Next session plan

1. Begin with Rik's daily stand-up.
2. Review the current project position and agree the day's goals.
3. Confirm the current milestone and Git status.
4. Continue reviewing the three fictional Place prototypes visually.
5. Decide whether the deferred breadcrumb, structured-data, tag and search
   requirements should become an approved implementation task.
6. Do not add Google Drive API access or request additional Google OAuth scopes.
7. Continue from the proven response #3 dry-run; do not repeat completed Google
   Sheets setup.
8. Review discovery, explicit selection, idempotency and non-merging behaviour.
9. Apply only corrections explicitly approved by Rik.
10. Recommend focused commit boundaries and wait for Rik before committing or
    pushing.

Do not begin private media-intake implementation, AI drafting, staging or
publication without separate approval.
