# Project Atlas — Session Handover

## Project goal

- Preserve and share genuine family travel experiences.
- Build a simple, static and privacy-first website.
- Make it easy for family members to contribute from their iPhones.
- Use AI to assist with drafting while Rik retains editorial control.
- Optimise for long-term maintainability rather than rapid feature growth.

## Current milestone

The read-only Google Sheets Connection Checkpoint is implemented and awaiting
Rik's review.

No later implementation milestone is authorised.

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
- No Google-to-importer automation or Drive integration has begun.
- No private family submission has been imported by this implementation.

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

- All 45 automated tests pass.
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

## Future adapter connection

A future Google Sheets adapter can supply one response with the same logical
headings to the importer parser boundary. A future Google Drive evidence
adapter can resolve provider references held in the private mapping.

Those adapters must not change:

- Visit validation.
- Opaque public-repository references.
- `Open` state behaviour.
- Editorial approval boundaries.
- The separation between private evidence and publishing Git.

Automated and integration tests must simulate Google Sheet responses with
fictional data outside the real Sheet. Atlas must never write artificial test
rows to the real Form response Sheet. Final real-world validation will use a
new submission through the actual Atlas Test V1 Google Form.

Importer wiring, provider retries and Drive access remain future work and
require separate approval.

## Current repository status

- Branch: `main`.
- Baseline commit: `a1819fb`.
- The read-only Google Sheets checkpoint is modified or untracked.
- No Constitution, importer behaviour or public website files were changed.
- The checkpoint has not been committed or pushed.

## Next objective

Obtain Rik's review of the read-only OAuth and structural Sheet connection
checkpoint.

## Next session plan

1. Read the mandatory startup documents in `AGENTS.md` order.
2. Confirm the current milestone and Git status.
3. Review the read-only OAuth scope, private paths and safe structural output.
4. Apply only corrections explicitly approved by Rik.
5. Run the full automated suite and whitespace checks.
6. Update the operational documents if review changes the result.
7. Recommend a focused commit message.
8. Wait for Rik before committing.
9. Wait for Rik before pushing.

Do not begin Google-to-importer automation or Google Drive integration without
separate approval.
