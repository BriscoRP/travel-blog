---
project: Project Atlas
repository: travel-blog

document: SYSTEM_ARCHITECTURE.md
version: 1.0.0
status: Active

owner: Rik Powell

created: 2026-08-01
last_updated: 2026-08-04

review_frequency: Quarterly
codex_maintained: false
---

# System Architecture

## Purpose

This document describes the overall architecture of Project Atlas.

It explains how information flows through the system, how each component interacts with the others, and defines the responsibilities of every major part of the platform.

The architecture is intentionally designed to favour simplicity, maintainability, privacy, performance and long-term sustainability.

This document forms part of the Project Atlas Constitution.

Changes should be made deliberately and with consideration of their impact on architecture, workflow and maintainability.

## High-Level Architecture

Project Atlas follows a simple publishing pipeline.

Family
│
├── Photos
├── Audio recordings
├── Notes
├── WhatsApp messages
└── Google Drive
│
▼
AI Processing (Codex)
│
├── Transcription
├── AI Summary
├── SEO Validation
├── Metadata Generation
├── Image Optimisation
├── Accessibility Checks
├── Consistency Validation
├── Build Preparation
└── Draft Place Page
│
▼
Rik Editorial Review
│
├── Approve
├── Request Changes
└── Reject
│
▼
Static Website Generation
│
▼
Cloudflare Pages
│
├── Preview Deployment
└── Production Deployment
│
▼
Visitors
Google
Family

## Place and Visit Architecture

A Place represents one real physical location and has one stable canonical public page.

A Place may have one or more Visits over time. Each Visit records the dated family experience and evidence relating to that occasion.

Place
│
├── Stable identity and canonical public page
├── Approved editorial content
└── One or more Visits
    ├── Dated observations
    ├── Approved derivative publishing assets
    └── Opaque references to private original evidence

Later Visits should normally improve the existing Place page rather than create a duplicate page. They may verify or update observations, add approved photographs, expand editorial content and record significant changes.

Version 1 may support one Visit per Place in the implementation, provided the underlying design can support multiple Visits without requiring a redesign.

## Information and Asset Boundaries

Project Atlas separates information and assets into three categories.

### Private Original Evidence

Raw photographs, audio, video, messages, personal notes, full transcripts and private documents remain in a private editorial archive controlled by Rik.

Private original evidence must not be stored in the public Git repository by default.

### Approved Derivative Publishing Assets

Approved, privacy-reviewed assets derived from original evidence may be stored in Git when required to build the website. Examples include optimised web images, approved excerpts and approved publishing content.

Any repository reference back to private original evidence must use a stable, opaque identifier. Public repository data must not expose private storage URLs, personal filenames, local paths, contact details, unintended GPS metadata or private storage arrangements.

Only Rik's private editorial archive contains the mapping between opaque identifiers and original evidence.

### Generated Public Assets

The build process creates public website output from approved source content and approved derivative publishing assets. Generated public assets contain only information and media approved for publication.

The Git repository is the publishing repository, not the archival repository.

## Prototype Foundation

The existing repository is a prototype foundation. It is neither disposable nor approved architecture.

Python, Jinja, static generation, image optimisation and Cloudflare Pages are useful prototype choices that may be retained where they continue to satisfy the Constitution.

Decap CMS, the content format, any database choice, the current templates and all other prototype decisions may be reconsidered. No technology should be retained solely because it already exists.

## System Components

### Family Contributors

Provide the original source material, including photographs, audio recordings, notes and travel experiences.

### Rik (Editor)

Owns the project, reviews all generated content, makes editorial decisions and approves all published pages.

### Codex

Codex acts as an AI engineering and publishing assistant. It supports implementation, validation and documentation while Rik retains responsibility for all architectural, editorial and technical decisions.

Codex is responsible for:

- organising submitted content
- transcribing audio
- generating AI summaries
- validating data
- checking SEO
- checking accessibility
- optimising images
- generating metadata
- maintaining project documentation
- preparing the website for publication

Codex must never publish content without Rik's approval.

### Static Website

The public website is generated from approved content and contains no public editing functionality.

Each Place has one canonical public URL. Later Visits update that Place page rather than creating duplicate Place pages.

An archived Place normally retains its canonical URL with a clear archival notice, but is removed from normal listings and filters. If an archived Place is replaced by a genuinely equivalent canonical page, the old URL should permanently redirect to the replacement.

### Cloudflare Pages

Hosts the production website and preview deployments using a fully static architecture.

### GitHub

Stores the approved publishing source, approved derivative publishing assets, documentation, configuration and project history.

Git is the single source of truth for Project Atlas.

Git is not the source of truth for private original evidence. That evidence remains in Rik's private editorial archive.

## Architectural Principles

The architecture of Project Atlas is governed by the following principles:

- Static-first architecture wherever practical.
- Privacy by design.
- Mobile-first user experience.
- Accessibility is mandatory.
- SEO is built into the publishing workflow rather than added afterwards.
- AI assists with repetitive work but never replaces human editorial judgement.
- Every published page must originate from a genuine family visit.
- Simplicity is preferred over unnecessary complexity.
- Components should be loosely coupled and easy to replace in the future.
- Long-term maintainability takes priority over short-term convenience.
- Private original evidence, approved derivative publishing assets and generated public assets must remain clearly separated.
- Technology choices must be justified by the Constitution rather than by their presence in the prototype.
