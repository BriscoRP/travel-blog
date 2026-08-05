# Project Atlas — Session Handover

## Project goal

- Preserve and share genuine family travel experiences.
- Build a simple, static and privacy-first website.
- Make it easy for family members to contribute from their iPhones.
- Use AI to assist with drafting while Rik retains editorial control.
- Optimise for long-term maintainability rather than rapid feature growth.

## Current position

- The Project Atlas Constitution is frozen as Version 1.0.
- The public website shell is implemented; its final copy, visual direction and
  accessibility acceptance remain separate outstanding work.
- The Visit Capture Workflow is approved as the working design.
- Milestone 2 Visit Capture Foundation Tasks 1–4 are implemented, approved,
  committed and pushed.
- `Atlas Test V1` has completed two end-to-end manual submissions.
- `Atlas Test V1` is frozen for the first family pilot.

## Atlas Test V1 outcome

The manual Google Forms prototype demonstrated that:

- The contributor workflow is simple and suitable for the first family pilot.
- The form captures the Place name, location context, private visitor identity,
  Visit date, first-hand observations, advice and optional facility details.
- Photos and videos can be uploaded privately to Google Drive.
- The response spreadsheet contains private links to uploaded evidence.
- Contributors are not asked for internal identifiers, approval metadata,
  publication settings or technical publishing information.

`Atlas Test V1` remains an exploratory contributor prototype. It is not part of
the implemented Visit Capture Foundation and is not an approved final
contributor interface.

## Completed implementation

- Minimum Version 1 Visit record contract.
- Storage-independent Visit operations behind the `VisitStore` interface.
- Local YAML storage adapter.
- Maintainer commands to create, show, validate and add evidence references.
- Automated tests using fictional data and temporary storage.
- Living `Open` Visit behaviour with incremental opaque evidence references.

## Decisions now approved

- Constitution Version 1.0.
- Static Python/Jinja architecture with Cloudflare Pages as the intended hosting
  platform.
- One canonical public page per Place with one or more Visit records.
- Privacy, evidence separation, exact-version approval and deny-by-default
  publishing rules.
- Visit Capture Workflow as the working lifecycle design.
- Milestone 2 Tasks 1–4 implementation.
- `VisitStore` as the structured Visit-record storage boundary.
- A Visit remains `Open` until a future explicitly authorised readiness
  transition is implemented.
- `Atlas Test V1` question set is frozen for the first family pilot.

## Next objective

Design and implement the Google Forms Importer that converts a completed
`Atlas Test V1` submission into an `Open` Visit using the existing Visit Capture
Foundation.

The importer should:

- Translate the completed response into the minimum Visit contract.
- Assign or use opaque Visit, Place, contributor and evidence identifiers.
- Register the form response and uploaded media as opaque evidence references.
- Keep Google account details, spreadsheet links, Drive identifiers, filenames
  and private evidence outside public Git.
- Be idempotent so the same submission cannot create duplicate Visits or
  evidence references.
- Stop with a clear error when required information is absent or ambiguous.
- Create only an `Open` Visit.

Google authentication, private evidence retrieval and provider-specific file
handling must remain behind explicit private boundaries. AI drafting,
Ready for Review, staging and publication remain out of scope.

## Decisions still outstanding

- The exact importer input boundary: exported row, spreadsheet access or
  another authorised source.
- How private Google response and file identifiers are mapped to opaque Project
  Atlas identifiers.
- How private visitor names are mapped to opaque contributor identifiers.
- How a submitted location is matched to an existing Place or assigned a new
  opaque Place identity.
- Whether structured Visit persistence and Drive evidence access require
  separate adapters.
- Credential storage and least-privilege access.
- Retry, duplicate and partial-failure behaviour.
- The future `Ready for Review` transition and evidence-snapshot behaviour.
- AI-assisted draft creation and its evidence-access boundary.
- Final review of the public website shell, final public copy, canonical domain,
  public contact routes and `dist/` policy.

## Current repository status

- Branch: `main`.
- The Visit Capture Foundation is committed and present on `origin/main`.
- `docs/PROJECT_STATUS.md` and `NEXT_SESSION.md` contain the current uncommitted
  documentation update.
- No Constitution, public website or implementation files were changed.
- No commit or push has been made for this documentation update.

## Next session plan

1. Read `AGENTS.md`, the bootstrap, project status, Constitution and this
   handover.
2. Confirm Git status and review the documentation diff.
3. Inspect the authorised `Atlas Test V1` response structure without copying
   private evidence into Git.
4. Produce the minimum Google Forms Importer design and implementation plan.
5. Resolve importer-boundary and identifier-mapping decisions with Rik.
6. Wait for approval before implementation.
7. Implement only the approved importer slice using fictional automated test
   data.
8. Verify that the result is an `Open` Visit with private provider details kept
   outside public Git.
