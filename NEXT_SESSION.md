# Project Atlas — Session Handover

## Project goal

- Preserve and share genuine family travel experiences.
- Build a simple, static and privacy-first website.
- Make it easy for family members to contribute from their iPhones.
- Use AI to assist with drafting while Rik retains editorial control.
- Optimise for long-term maintainability rather than rapid feature growth.

## Current milestone

The Google response bridge, fictional Place prototypes and Private Media Intake
Foundation V1 are committed and pushed. One genuine private Open Visit is
persisted outside Git, and its matching genuine Bluebell Wood review record is
now created with the opaque Place association explicitly verified. Publication
remains unapproved and the photograph remains private and unprocessed.

No admin web UI, AI, staging, publication or Google Drive API milestone is
authorised.

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
- One Rik-selected genuine Bluebell Wood submission has been imported to
  approved private storage outside Git.
- Opaque response discovery now reports pending and processed state without
  displaying response contents.
- One explicitly selected response can be dry-run, created as a new Visit or
  appended to an explicitly supplied existing Visit through the hardened
  importer.
- Similar and even identical Google rows never trigger automatic merging.
- Rik explicitly classified the selected response's single uploaded-media
  reference as a photo without Atlas inspecting or downloading it.
- The response passed dry-run validation and was separately approved for
  persistence as one private `Open` Visit with its private mapping and
  processed-response state.
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

## Primary Place image policy

- Every publishable Place has one Rik-selected primary or hero image. Atlas
  never randomly chooses, rotates, infers or automatically replaces it.
- The primary image is the Place-page hero and, by default, represents the
  Place on listing cards through layout-appropriate derivatives of the same
  approved underlying image.
- The primary image should not be repeated unnecessarily as separate content on
  the same Place page.
- Additional photographs will later have deliberate editorial placement and
  order; gallery behaviour remains out of scope.
- Alt text remains contextual, accessibility-first and Rik-reviewed.
- Responsive candidate widths and count, plus WebP quality, remain provisional
  until the final Place template and representative real photographs are
  assessed.

## Private Media Intake Foundation V1

- A reusable engine and local maintainer CLI accept a Rik-selected JPEG, PNG
  or prepared WebP source from outside the repository.
- The command requires an explicit Place source record, Visit ID, `hero` role
  and Rik-reviewed informative alt text. It never infers association from a
  filename, metadata, image content or AI.
- The selected Visit is loaded from an explicitly private Visit store and its
  opaque Place ID must match the selected Place record before processing.
- Dry-run reports the controlled filename, responsive widths and dimensions,
  alt text and project-relative destination without writing publishing source.
- An optional visual preview writes processed WebPs only to an explicitly
  private directory outside the repository.
- Explicit apply corrects EXIF orientation, strips metadata, safely normalises
  colour mode and uses a central provisional hero profile, never exceeding the
  source width.
- The current 480, 800 and 1200 candidates demonstrate delivery for the present
  72rem Place shell. They are not an SEO rule or permanent Atlas width count;
  final candidates follow approval of the final Place layout and device tests.
- The `sizes` value matches the actual capped shell and gutters. Browser source
  selection accounts for viewport slot, DPR, zoom and available candidates.
- The hero is not lazy-loaded and uses `fetchpriority="high"` as the likely LCP
  image. No preload or `<picture>` element is introduced.
- Public filenames are deterministic:
  `<place-slug>-<role>-<width>.webp`.
- Apply updates the selected Place's responsive image metadata only after a
  complete derivative set is prepared. Collisions fail; the source original is
  never deleted; apply does not approve or publish the Place.
- A generated fictional Glasshouse Gardens hero proves the complete static
  image markup while the page remains visibly fictional, `noindex, nofollow`,
  canonical-free and sitemap-excluded.
- The web-admin UI, gallery/replacement workflows, video, audio, HEIC, AI and
  publication integration remain future work.

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
- Processing or associating the still-private Bluebell Wood photograph.
- Any private media admin web UI.
- Any approved Place refinements following Rik's visual review.
- Any real or public Place publication.

## Next objective

Begin one controlled Bluebell Wood hero-photo validation from the verified
Place and private Visit association, starting with dry-run only. Keep the
original outside Git and chat and persist no publishing media without a
separate approval.

## Next session plan

1. Begin with Rik's daily stand-up.
2. Review the current project position and agree the day's goals.
3. Confirm the current milestone and Git status.
4. Keep Rik's selected original outside Git and chat and begin with dry-run
   only against the already verified Bluebell Wood Place/Visit association.
5. Use a private preview outside the repository before any separately approved
   apply step.
6. Do not add an admin UI, galleries, Drive access or unrelated frontend work.
7. Wait for Rik's explicit approval before apply, commit or push.

Do not begin private media-intake implementation, AI drafting, staging or
publication without separate approval.
