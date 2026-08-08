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
now created with the opaque Place association explicitly verified. Rik's
selected genuine photograph has been applied as public-safe responsive hero
derivatives and Rik has visually approved the result as the V1 Place-page
direction. The genuine end-to-end content/media path is proven. Publication
remains explicitly unapproved and the private original remains outside Git and
unchanged.

All three 7 August goals reached 100% of their intended daily scope. This does
not mean Atlas is complete; estimated overall V1 live readiness is approximately
75%.

No admin web UI, AI, staging, publication or Google Drive API milestone is
authorised.

On 8 August, the next genuine operational test successfully reached Form
submission, Google's built-in email notification, Atlas read-only discovery and
the hardened importer dry-run. Rik classified all five upload references as
photos. The dry-run proposed a new `Open` Visit with one response note and five
photo evidence items. Rik then explicitly selected new Place plus new Visit and
approved private persistence. Atlas created exactly one private `Open` Visit
and mapping, marked the response processed and proved repeat retrieval
idempotent. Rik then approved a public-safe Hadleigh Country Park review record.
Atlas privately verified its Visit-to-Place association and created the
protected review without media. Publication and media processing remain
unauthorised.

Rik visually and editorially approved the Hadleigh review as accurate
public-safe content and an acceptable V1 presentation direction. This is not
publication approval. Detailed design and layout remain deferred.

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
- Google Forms built-in email notifications for new responses are enabled.
  V1 does not require Rik's PC or Python to run continuously: the intended loop
  is notification, Rik opens local Atlas tooling or the future local Admin UX,
  then explicitly checks and processes pending submissions. Cloud polling is
  outside current V1 scope.
- The 8 August genuine submission proved the notification and read-only
  discovery loop. Rik's practical private batch download from the Form upload
  folder means no Drive API or additional Google scope is currently needed for
  V1.
- Rik has genuine local originals available for later curated intake. He should
  not manually resize or compress them; Atlas should validate them and generate
  public-safe derivatives after the Place association and presentation profile
  are explicitly approved.
- Hadleigh Country Park now has a genuine public-safe review source containing
  only the approved Place, broad-location, Visit and practical-observation
  categories. It is unapproved, canonical-free, `noindex, nofollow`, excluded
  from the sitemap and has no hero, gallery or other media association.

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

## Approved deferred media direction

- A publishable Place ultimately has one Rik-selected primary asset reused as
  its hero and default listing-card image through context-appropriate
  derivatives; Atlas never infers or rotates it.
- The future operator UX should support several local originals, thumbnails,
  include/exclude, primary selection, explicit ordering, reviewed alt text,
  optional independently editable captions and preview before apply or
  publication. EXIF order is not editorial order.
- A future accessible gallery/lightbox should support mobile and occasional
  large-screen family viewing without depending solely on touch. A future
  approved-photo discovery wall is possible but outside current V1 scope.
- Public media should support stable identity, owning Place, primary status,
  order, responsive derivatives, alt text, optional caption and public-safe
  credit/provenance. Private Visit IDs and provenance remain private.
- The current widths and WebP quality are provisional. Final profiles follow
  approved hero/card/gallery layouts and representative performance testing.

## Three-way incoming response decision

Rik explicitly chooses one operation for every genuine submission:

1. New Place plus new Visit.
2. New Visit associated with an existing Place and its stable Place identity.
3. Append later material to an existing Visit.

Contributors do not handle Atlas IDs or database relationships. Atlas never
matches or merges from names, locations, text similarity, photographs or AI.
Operations 1 and 3 have genuine workflow evidence. Operation 2 is implemented
through an explicitly supplied existing Place ID and is covered by fictional
importer tests, but has not yet been proven with a genuine live submission.

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
- Valid embedded ICC profiles are colour-transformed to standard sRGB before
  profile removal; invalid or unusable profiles fail safely during dry-run.
- The current 480, 800 and 1200 candidates demonstrate delivery for the present
  72rem Place shell. They are not an SEO rule or permanent Atlas width count;
  final candidates follow approval of the final Place layout and device tests.
- Further size and quality comparisons are paused. Quality 82 and the current
  candidates remain provisional until template measurement, representative
  photographs, Lighthouse and Core Web Vitals review.
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

- All 91 automated tests pass.
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
- Baseline commit: `a5a5dd1` (`docs: close 7 August Atlas session`).
- Functional source, generated output, tests and the 7 August handover are
  committed and pushed.
- The 8 August genuine Hadleigh review source, generated review output,
  protection-test update and operational/roadmap documentation are uncommitted.
- No Constitution files changed.
- No publication, deployment or admin UI work is present.

## Handover boundaries

### Committed and pushed

- The 7 August closeout checkpoint `a5a5dd1` and everything before it.

### Uncommitted

- Protected Hadleigh Country Park source and generated review output.
- Review-page protection-test updates.
- The 8 August updates to `docs/PROJECT_STATUS.md` and `NEXT_SESSION.md`.

### Proven live

- Real Atlas Test V1 Form to private Sheet to Atlas read-only connection.
- One genuine private Bluebell Wood `Open` Visit and verified opaque Place
  association outside Git.
- Genuine response through private persistence, public-safe Place review,
  explicit hero selection, private dry-run and preview, colour-managed apply,
  static build and Rik's local visual approval.
- A second genuine response through Form submission, email notification,
  Sheets-readonly discovery and hardened-importer dry-run with five
  Rik-classified photo references, followed by explicitly approved new-Place
  and new-Visit private persistence and an idempotent repeat retrieval.
- The matching genuine Hadleigh Country Park public-safe review source after
  private Visit-to-Place verification, with no private Visit identity or media
  association in publishing source or generated output.

### Not yet done

- Any processing of the privately downloaded photographs for the newly
  persisted Visit.
- Reuse of the selected primary image on Place listing cards; the current
  listing renders no card images, so this remains a deferred policy gap.
- Detailed Place layout and styling, breadcrumbs, tags and filtering, and final
  responsive-image tuning after template measurement, representative images,
  Lighthouse and Core Web Vitals review.
- Any private media admin web UI.
- Any approved Place refinements following Rik's visual review.
- Any real or public Place publication.

## Next objective

Complete Rik's review and approval of the smallest sensible commit grouping for
today's genuine operational and Hadleigh review checkpoint. After that, keep
photograph intake and Admin design behind separate approval boundaries. Rik's
content and presentation approval is not publication approval.

## Next session plan

1. Review and approve the focused commit grouping for today's checkpoint.
2. Keep the new genuine Visit, mapping and photographs private until Rik
   separately approves the next exact checkpoint.
3. From today's genuine evidence, design the smallest useful local Admin UX for:
   checking submissions; reviewing/selecting a response; Visit create/append;
   Place association; selected-photo intake; Rik-selected hero; Rik-reviewed
   alt text; preview; and explicit apply.
4. Present the explicit three-way operator decision without exposing internal
   relationship decisions to contributors.
5. Keep gallery, lightbox, photo wall and Drive integration deferred.
6. Keep publication and deployment as a separate approval boundary.
7. Defer final visual, image-policy and SEO refinement until the operational
   workflow is comfortable.

## Deferred before public V1

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

Do not begin the local Admin implementation before reviewing the real incoming
workflow evidence and obtaining explicit approval for that focused slice. AI
drafting, staging and publication remain separately unapproved.
