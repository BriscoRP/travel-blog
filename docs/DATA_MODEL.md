---
project: Project Atlas
repository: travel-blog

document: DATA_MODEL.md
version: 1.1.0
status: Draft

owner: Rik Powell

created: 2026-08-01
last_updated: 2026-08-02

review_frequency: Quarterly
codex_maintained: false
---

# Data Model

## Purpose

This document defines the canonical data model for Places, Visits and their publishing lifecycle within Project Atlas.

It is the single source of truth for the information stored about each place and ensures consistency throughout the website, AI workflow, SEO, filtering and future database.

This document forms part of the Project Atlas Constitution.

Changes should be made deliberately and with consideration of their impact on architecture, workflow and maintainability.

## Core Relationship

Every Place represents one real physical location personally visited by the family.

A Place may have one or more Visits. Each Visit represents a separate family visit to that Place.

The public website has one canonical page per Place. Later Visits normally improve that page instead of creating a new Place page.

Version 1 may support one Visit per Place, but the stored relationship must support multiple Visits without redesign.

## Place

### Identity

| Property | Required | Description |
|--------|:--------:|-------------|
| Place ID | ✅ | Permanent opaque internal identifier for the physical location. |
| Name | ✅ | Public display name of the Place. |
| Alternative Name(s) | Optional | Historic or commonly used names. |
| Place Type | ✅ | The type of Place, using an approved vocabulary. |
| URL Slug | ✅ | Stable, SEO-friendly URL slug. |

### Location

| Property | Required | Description |
|--------|:--------:|-------------|
| Address | Optional | Approved public address if applicable. |
| Town / City | Optional | Nearest town or city. |
| Administrative Area | Optional | Appropriate regional division, such as county, council area, province, state, region, department, canton or municipality. |
| Country | ✅ | Country in which the Place is located. |
| Postcode | Optional | Approved public postcode if applicable. |
| Latitude | Optional | GPS latitude approved for publication. |
| Longitude | Optional | GPS longitude approved for publication. |
| What3Words | Optional | What3Words reference approved for publication. |
| Map Link | Optional | Approved public map link. |

The public website should display an Administrative Area naturally and must not force UK-specific terminology onto international locations.

### Editorial Experience

| Property | Required | Description |
|--------|:--------:|-------------|
| AI Summary | ✅ | Short factual overview based only on genuine family evidence as provided by one or more visits and gets approved by Rik. |
| Personal Experience | Optional | Approved first-hand editorial account built from one or more Visits. |
| Recommended | Optional | Whether the family would recommend visiting. |
| Favourite Features | Optional | Approved highlights from family Visits. |
| Things to Know | Optional | Approved first-hand advice discovered during Visits. |
| Material Update Note | Optional | Brief public explanation when a later Visit materially verifies or expands the page. |

### Approved External Links

| Property | Required | Description |
|--------|:--------:|-------------|
| Official Website | Optional | Authoritative website explicitly approved by Rik. |
| Other Approved Links | Optional | Additional external URLs explicitly approved by Rik. |
| Link Approval Status | Required when a link is proposed | Internal approval state for the external URL. |

Project Atlas must not copy official or frequently changing information merely because it is available elsewhere. Opening times, prices, booking information and temporary closures should normally be obtained by visitors through a clearly labelled approved authoritative link.

Proposed external URLs may be stored for editorial review but must not be published before approval.

### SEO

| Property | Required | Description |
|--------|:--------:|-------------|
| SEO Title | ✅ | Search engine page title. |
| Meta Description | ✅ | Search engine description. |
| Canonical URL | ✅ | Stable canonical URL for the Place page. |
| Open Graph Image | Optional | Approved social sharing image. |
| Robots Directive | ✅ | Indexing directive appropriate to publication and preview state. |
| Tags | ✅ | Approved consistent tags used for filtering and search. |

## Visit

### Visit Record

| Property | Required | Description |
|--------|:--------:|-------------|
| Visit ID | ✅ | Permanent opaque identifier for the Visit. |
| Place ID | ✅ | Identifier of the Place visited. |
| Visit Date | ✅ | Date of the Visit, stored at an appropriate approved level of precision. |
| Time Visited | Optional | Morning, afternoon, evening, night or another approved representation. |
| Visit Duration | Optional | Approximate length of the Visit. |
| Weather | Optional | Weather observed during the Visit. |
| Visited By | ✅ | Internal family-member identifiers used for provenance and editorial follow-up. Private by default. |

Month, day of the week and similar filter values should be derived from Visit Date rather than maintained as duplicate facts where practical.

Visitor identities must not appear publicly unless Rik has explicitly approved the person being named and the person is comfortable being identified. Version 1 assumes names are not public.

### Visit Observations

Time-sensitive information is stored as first-hand observation rather than permanent fact.

| Property | Required | Description |
|--------|:--------:|-------------|
| Parking | Optional | Parking observed during the Visit. |
| Toilets | Optional | Toilet facilities observed during the Visit. |
| Accessibility | Optional | Accessibility conditions personally observed during the Visit. |
| Dog Access | Optional | Dog access observed during the Visit. |
| Entry Arrangements | Optional | Entry arrangements personally encountered during the Visit. |
| Facilities | Optional | Facilities personally observed during the Visit. |
| Path / Ground Conditions | Optional | Conditions observed during the Visit. |
| Other Observations | Optional | Additional first-hand observations. |
| Last Verified | Required for a published time-sensitive observation | Date on which the observation was made or confirmed by a family Visit. |

Public presentation must make clear that time-sensitive details were observed during a dated Visit and may have changed. Wording such as “Observed during our visit in June 2026” or “Last verified by us: June 2026” may be used subject to Rik's editorial approval.

A later Visit may confirm or replace an observation and update its Last Verified date.

### Visit Media and Evidence

| Property | Required | Description |
|--------|:--------:|-------------|
| Featured Photo | Optional | Approved derivative image used on listings and social sharing. |
| Gallery | Optional | Approved derivative web images. |
| Photo Captions | Optional | Approved public captions. |
| Photo Credits | Optional | Approved attribution where required. |
| Evidence References | Optional | Opaque identifiers that trace the Visit to private original evidence. |

Raw photographs, audio, video, messages, personal notes, full transcripts and private documents are private original evidence and must not be stored in the public Git repository by default.

Approved derivative publishing assets may be stored in Git after privacy and editorial review. Generated public assets are created from approved content and approved derivatives during the website build.

Evidence references must be stable but meaningless outside Rik's private editorial archive. They must not expose private storage URLs, personal filenames, local paths, contact information, unintended GPS metadata or private storage arrangements.

## Publishing

### Publication States

Every Place and Visit has an explicit publication state:

| State | Production Behaviour |
|--------|----------------------|
| Draft | Never included in production. |
| Review | Never included in production. |
| Published | Included only when all required approval metadata is valid. |
| Archived | Excluded from active production output. A previously published Place retains its existing public URL under the Archived Places rules below. |

Missing, unknown or malformed publication states are treated as not approved.

### Approval Metadata

| Property | Required for Published | Description |
|----------|:----------------------:|-------------|
| Approval Status | ✅ | Explicit editorial approval state. |
| Approval Date | ✅ | Date the content version was approved. |
| Approved Content Version | ✅ | Exact record or content version covered by the approval. |
| Approver ID | Optional | Opaque internal approver identifier, stored only if required. |

Approval metadata must avoid unnecessary public personal information. Completeness never implies approval, and a material update requires approval of the new content version.

### Publication and Review Dates

| Property | Required | Description |
|----------|:--------:|-------------|
| Publish Date | Required when first published | Date the Place first entered production. |
| Public Last Updated | Required for a published material update | Date the public page was materially updated. |
| Last Reviewed | Optional | Editorial review date. |
| Archived Date | Required when archived | Date the Place entered the Archived state. |
| Notes for Editor | Optional | Internal workflow notes excluded from public website output and containing no personal or private information. |

## Archived Places

A previously published archived Place normally retains its canonical URL and historical content.

The page must:

- display a clear archival notice
- explain that it is no longer actively maintained
- explain that some information may be outdated
- direct visitors to an approved official source where appropriate
- avoid presenting old observations as currently verified

Archived Places must be removed from normal listings and filters and must not be treated as newly active content.

A URL should be removed only for a strong legal, privacy, safety or factual reason. If an archived Place is replaced by a genuinely equivalent canonical page, the old URL should use a permanent redirect.

## System

| Property | Required | Description |
|----------|:--------:|-------------|
| Record Version | ✅ | Version identifier used to bind editorial approval to exact content. |
| Date Created | ✅ | Record creation date. |
| Record Last Modified | ✅ | Internal record modification date. |

Internal identifiers must be stable, opaque and free of unnecessary personal information.
