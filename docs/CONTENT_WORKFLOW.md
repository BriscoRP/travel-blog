---
project: Project Atlas
repository: travel-blog

document: CONTENT_WORKFLOW.md
version: 1.1.0
status: Draft

owner: Rik Powell

created: 2026-08-02
last_updated: 2026-08-02

review_frequency: Quarterly
codex_maintained: false
---

# Content Workflow

## Purpose

This document defines the complete publishing workflow used by Project Atlas.

Every published page should follow this workflow to ensure consistency, quality, accessibility, SEO and factual accuracy.

This document forms part of the Project Atlas Constitution.

Changes should be made deliberately and with consideration of their impact on long-term maintainability.

## High-Level Workflow

Project Atlas follows a simple editorial workflow.

Collect
    ↓
Organise
    ↓
AI Processing
    ↓
Editorial Review
    ↓
Website Build
    ↓
Preview
    ↓
Publish
    ↓
Monitor & Improve

Every published page must pass through each stage before reaching the public website.

## Stage 1 — Collect

The objective of this stage is to gather all original source material relating to a visit.

Typical inputs include:

- Photographs
- Audio recordings
- Written notes
- WhatsApp messages
- Google Drive folders
- Maps or location links

Only genuine information from family members should enter the publishing workflow.

No AI-generated facts should ever be introduced during this stage.

Original source material belongs in Rik's private editorial archive, not in the public Git repository. This includes raw photographs, audio, video, messages, personal notes, full transcripts and private documents.

Each original item required for provenance should receive a stable, opaque identifier. Only the private editorial archive should map that identifier to the original evidence.

## Stage 2 — Organise

The objective of this stage is to organise the collected material into a complete visit record.

Activities during this stage include:

- Grouping all files for a single visit.
- Confirming the location visited.
- Removing duplicate photographs.
- Checking that photographs, audio and notes belong to the same visit.
- Identifying any missing information that should be requested before AI processing begins.
- Separating Place information from Visit-specific evidence and observations.
- Assigning opaque references to relevant private original evidence.
- Identifying approved derivative publishing assets that may enter Git after editorial and privacy review.

No content should be generated during this stage.

The objective is simply to ensure that the source material is complete, organised and ready for processing.

Private storage URLs, personal filenames, local paths, contact details, unintended GPS metadata and private storage arrangements must not enter the public repository.

## Stage 3 — AI Processing

The objective of this stage is to transform organised source material into a high-quality draft ready for editorial review.

Codex may assist by:

- Transcribing audio recordings.
- Generating a draft summary based solely on first-hand family evidence.
- Suggesting SEO metadata.
- Creating image alt text.
- Optimising photographs for the website.
- Checking accessibility.
- Validating consistency with the Project Atlas Content Model.
- Identifying missing or conflicting information.
- Proposing authoritative external URLs for editorial review.

Codex must never invent facts.

Where information is uncertain or unavailable, Codex must flag the issue for editorial review rather than guessing.

Codex must not copy third-party facts into Project Atlas to complete missing fields. Official or frequently changing information should normally be represented by a proposed authoritative link for Rik to review.

AI processing may prepare proposed derivative publishing assets, but they must not be treated as approved merely because they have been generated. If used and public facing they need to have a UX friendly disclaimer which is consistent site-wide "Asset made by AI".

## Stage 4 — Editorial Review

Every draft produced by Codex must be reviewed by Rik before publication.

The editorial review includes:

- Fact checking.
- Reviewing AI-generated summaries.
- Checking image quality.
- Reviewing SEO metadata.
- Ensuring accessibility requirements are met.
- Confirming consistency with the Project Atlas Content Model.
- Confirming that published claims are supported by genuine first-hand family evidence.
- Confirming that time-sensitive observations carry an appropriate Visit or Last Verified date.
- Confirming that private family identities and private evidence details are excluded from public output.
- Reviewing and explicitly approving any external link.
- Approving each derivative publishing asset that will be stored in Git or published.
- Confirming the publication state, approval date and approved content version.

Only approved content may proceed to a production website build. Draft or Review content may proceed only to a protected preview build under the rules defined below.

Human editorial approval is mandatory for every published page.

Approval applies to an exact content version. A material update following a later Visit requires renewed approval before it can replace the production version.

## Stage 5 — Website Build

Once approved, the content is prepared for publication.

During this stage Codex may:

- Generate the static page.
- Generate navigation and internal links.
- Generate structured data (Schema.org).
- Generate the XML sitemap.
- Generate robots.txt where required.
- Optimise images.
- Validate internal links.
- Validate page performance.
- Prepare the complete website for deployment.

The website build must be fully repeatable and produce consistent results from the same approved content.

Production publishing is deny-by-default.

- Draft and Review records must never enter production.
- Published records may enter production only when their required approval metadata is valid.
- Missing, unknown or malformed publication states are treated as not approved.
- Archived Places retain their existing public pages where applicable but are excluded from normal listings and filters.
- A record that appears intended for production but lacks required approval metadata must cause a clear build failure rather than silent publication.

The build must keep three asset classes distinct:

1. Private original evidence held outside Git.
2. Approved derivative publishing assets stored in Git.
3. Generated public assets written by the build.

## Stage 6 — Preview

Before publication, every build must be reviewed in a preview environment.

The preview review includes:

- Checking page layout.
- Testing mobile responsiveness.
- Verifying internal links.
- Checking image quality.
- Validating SEO metadata.
- Confirming accessibility.
- Performing a final visual review.

No changes should be made directly to the production website.
Any required corrections should be made to the source content before rebuilding.

Preview builds may include Draft or Review records only when the preview environment:

- is protected from search indexing
- clearly labels unpublished content
- is appropriately access-controlled
- remains separate from normal production discovery

## Stage 7 — Publish

Once the preview has been approved, the website may be published.

Publishing includes:

- Deploying the latest approved build.
- Confirming the deployment completed successfully.
- Verifying that the live website is functioning correctly.
- Confirming that the new page is accessible.
- Checking that search engine files (such as the sitemap) have been updated.

Only approved builds may be published.

Publishing checks must confirm that the deployed content version matches the version approved by Rik.

## Stage 8 — Monitor & Improve

Publication is not the end of the workflow.

After publishing, Project Atlas should continue to improve over time through ongoing review.

Activities include:

- Monitoring for broken links.
- Reviewing page performance.
- Reviewing search engine performance.
- Updating information when places change.
- Improving accessibility where appropriate.
- Enhancing content based on genuine new information.
- Correcting factual errors if identified.
- Adding later Visits to an existing Place.
- Updating time-sensitive observations and their Last Verified dates.
- Displaying a Public Last Updated date after a material revision.
- Explaining, where useful, that information has been verified or expanded following a later family Visit.

Improvements must always be made to the source content rather than directly to generated output.

## Later Visit Workflow

When the family revisits an existing Place:

1. Create a new Visit linked to the existing Place.
2. Compare the new evidence with the current approved page.
3. Confirm or update time-sensitive observations.
4. Add or replace approved derivative publishing assets where appropriate.
5. Improve the existing Place content rather than create a duplicate Place page.
6. Add a concise material update explanation where it helps visitors.
7. Record the relevant Last Verified and Public Last Updated dates.
8. Obtain Rik's approval for the new content version.
9. Publish the updated canonical Place page.

Exact public wording for verification dates and material updates remains under Rik's editorial control.

## Archived Place Workflow

When a previously published Place is archived:

- retain its canonical URL by default
- remove it from normal listings and filters
- display an archival notice
- explain that the page is no longer actively maintained
- warn that observations may be outdated
- link to an approved official source where appropriate

The URL should be removed only for a strong legal, privacy, safety or factual reason. If a genuinely equivalent replacement page exists, use a permanent redirect instead of a 404 response.
