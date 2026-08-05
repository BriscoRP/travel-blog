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
- Milestone 2 Visit Capture Foundation Tasks 1–4 are implemented and approved.
- No further implementation milestone is authorised.

## What was completed

- Defined the minimum Version 1 Visit record contract.
- Implemented storage-independent Visit operations behind the `VisitStore`
  interface.
- Implemented the local YAML storage adapter.
- Implemented the minimal maintainer commands to create, show, validate and add
  evidence references to one Visit.
- Verified that a Visit remains a living `Open` record as evidence is added over
  time.
- Added automated coverage using fictional data and temporary storage.
- Passed all 12 automated tests and the new-file whitespace checks.
- Kept Google Drive, evidence-file handling, AI drafting, staging, publishing,
  Place pages, contributor interfaces and web forms out of the implementation.

## Decisions now approved

- Constitution Version 1.0.
- Static Python/Jinja architecture with Cloudflare Pages as the intended hosting
  platform.
- One canonical public page per Place with one or more Visit records.
- Privacy, evidence separation, exact-version approval and deny-by-default
  publishing rules.
- Visit Capture Workflow as the working lifecycle design.
- Milestone 2 Tasks 1–4 implementation.
- `VisitStore` as the storage boundary for structured Visit records.
- A Visit remains `Open` until a future explicitly authorised readiness
  transition is implemented.

## Next planned activity

Create a manual Google Forms prototype named `Atlas Test V1` to validate the
family contributor workflow, particularly the experience on iPhones.

`Atlas Test V1` is exploratory. It is not part of the implemented Visit Capture
Foundation, is not a Google Drive adapter, and must not be treated as an
approved production contributor interface.

The prototype should be used to learn:

- Whether family contributors understand the questions.
- Whether the amount of required information is reasonable.
- Whether photos, videos, notes and audio can be contributed naturally at
  different times.
- Which questions should be mandatory or optional.
- Where contributors hesitate, abandon or provide ambiguous information.
- What should change before any contributor workflow is integrated with the
  repository or Visit Capture Foundation.

## Decisions still outstanding

- The exact questions and structure for `Atlas Test V1`.
- Who will participate in the prototype and what fictional or genuine test
  material is appropriate.
- How repeated submissions or later additions should be represented during the
  manual experiment.
- Whether and how a future Google Drive adapter should be implemented.
- The future `Ready for Review` transition and evidence-snapshot behaviour.
- AI-assisted draft creation and its evidence-access boundary.
- Final review and approval of the public website shell and representative copy.
- Final public copy, canonical domain, public contact routes and `dist/` policy.

## Current repository status

- Branch: `main`.
- `main` matches `origin/main`.
- The approved Visit Capture Foundation is present as untracked files.
- `docs/PROJECT_STATUS.md` and `NEXT_SESSION.md` contain uncommitted
  documentation updates.
- No Constitution or public website files were changed in this milestone.
- No commit or push has been made.

## Immediate next objective

Obtain Rik's review of the complete Visit Capture Foundation and documentation
diff. After any explicitly authorised commit, prepare the manual `Atlas Test V1`
prototype without extending the repository implementation.

## Next session plan

1. Read `AGENTS.md`, the bootstrap, project status, Constitution and this
   handover.
2. Confirm the branch and review the complete uncommitted diff.
3. Commit only if Rik explicitly authorises it.
4. Agree the minimum learning goals and questions for `Atlas Test V1`.
5. Build the prototype manually in Google Forms rather than in the repository.
6. Test the contributor experience on an iPhone.
7. Record findings without treating the prototype as approved architecture.
8. Ask Rik whether the working design or Visit contract should change.
9. Propose further implementation only after separate approval.
