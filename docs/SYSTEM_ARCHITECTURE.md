---
project: Project Atlas
repository: travel-blog

document: SYSTEM_ARCHITECTURE.md
version: 1.0.0
status: Draft

owner: Rik Powell

created: 2026-08-01
last_updated: 2026-08-01

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

## System Components

### Family Contributors

Provide the original source material, including photographs, audio recordings, notes and travel experiences.

### Rik (Editor)

Owns the project, reviews all generated content, makes editorial decisions and approves all published pages.

### Codex

Acts as the project's technical lead and publishing assistant.

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

### Cloudflare Pages

Hosts the production website and preview deployments using a fully static architecture.

### GitHub

Stores the complete source code, documentation and project history.

Git is the single source of truth for Project Atlas.

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