# Project Atlas — Session Handover

## Project goal

- Preserve and share genuine family travel experiences.
- Build a simple, static and privacy-first website.
- Make it easy for family members to contribute from their iPhones.
- Use AI to assist with drafting while Rik retains editorial control.
- Optimise for long-term maintainability rather than rapid feature growth.

## What was completed today

- Froze the five Constitution documents as Version 1.0 and pushed that focused commit.
- Approved the Version 1 Architecture Proposal, Phase 1 Implementation Plan, UX proposal and Version 1 Wireframe Specification.
- Implemented the public website shell: Home, Places empty state, About, How We Create Our Guides, Privacy and Accessibility.
- Added the shared semantic header, primary navigation, footer and mobile-first stylesheet.
- Restored the prototype content loader, fallback vocabularies and image-processing capability after scope review.
- Rebuilt the static output and verified all shell routes and assets returned HTTP 200.
- Applied the review corrections: all representative pages are `noindex, nofollow`, crawling is blocked, the sitemap is empty, canonical base configuration is optional, and smooth scrolling was removed.

## Decisions now approved

- Constitution Version 1.0.
- Static Python/Jinja architecture with Cloudflare Pages as the intended hosting platform.
- One canonical public page per Place with one or more Visit records.
- Privacy, evidence separation, exact-version approval and deny-by-default publishing rules.
- Version 1 page structure, navigation, trust pages, empty states and Page Actions policy.
- Entirely AI-generated public assets require the disclosure “Asset made by AI”.
- Representative review copy must remain non-indexable.
- No permanent canonical domain is assumed; the base URL must be explicitly configured.

## Decisions still outstanding

- Final review and approval of the implemented website shell and representative copy.
- Final public copy to replace representative review content.
- Approved permanent canonical domain and production value for `ATLAS_SITE_URL`.
- Whether a public privacy or accessibility contact route will be provided.
- Whether generated `dist/` output should remain committed to Git.
- Final visual and accessibility acceptance after review.

## Current repository status

- Constitution freeze is committed and present on `origin/main`.
- Public website shell source and generated output are built but uncommitted.
- No schemas, Phase 1 validation or Place pages have been implemented.
- Decap CMS files remain present and unused.

## Current Git branch

`main`

## Working tree

Not clean. It contains modified and untracked website-shell source and generated files.

## Immediate next objective

Review the public website shell, resolve any requested corrections, and obtain Rik’s approval before preparing a focused commit.

## Next session plan

1. Read `AGENTS.md`, the bootstrap, project status, Constitution and this handover.
2. Confirm Git status and review the complete uncommitted diff.
3. Start the local `dist/` preview without rebuilding unless needed.
4. Review all six routes at mobile and desktop widths.
5. Check keyboard navigation, focus, zoom/reflow, landmarks and heading order.
6. Review representative copy, Privacy and Accessibility wording with Rik.
7. Apply only approved corrections and rebuild.
8. Verify all pages remain `noindex, nofollow`, robots blocks crawling, and the sitemap stays empty.
9. Present the final diff and verification results for approval.
10. Commit only after Rik explicitly authorises it.
