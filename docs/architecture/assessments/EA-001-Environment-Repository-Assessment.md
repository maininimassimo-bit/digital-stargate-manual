# EA-001 — Environment & Repository Assessment

**Project:** Digital StarGate  
**Document Version:** 1.0  
**Status:** BASELINE APPROVED  
**Owner:** Massimo Mainini  
**Execution Environment:** PC Principale  
**Assessment Date:** 24 July 2026  

---

## 1. Purpose

This document defines the current baseline of the Digital StarGate development environment on the PC Principale.

Its purpose is to:

- establish the actual structure already present on the workstation;
- avoid creating duplicate repositories, folders, documentation, or technical flows;
- align the existing environment with the agreed roadmap;
- define the role of the PC Principale and of the EAGLE;
- identify the authoritative locations for source code, documentation, data, releases, and operational components;
- provide a stable reference before starting the Data Warehouse phase.

This document does not replace the roadmap. It is a preliminary alignment step required to execute the roadmap coherently.

---

## 2. Agreed Roadmap

The project roadmap remains:

1. Data Warehouse
2. Analytics
3. Observatory Automation
4. Dashboard
5. AI Observatory Assistant

The execution workflow remains:

1. Analysis
2. ADR, when required
3. Design
4. Implementation
5. Tests
6. Documentation
7. Roadmap update
8. Release Candidate
9. Installation
10. Field verification
11. Release

No roadmap phase is considered complete until its documentation and validation artifacts are available.

---

## 3. Assessed Computer

### 3.1 Computer Role

**Computer:** PC Principale  
**Primary root:** `C:\DigitalStarGate`

The PC Principale is the development, integration, documentation, validation, and release-management workstation.

It is the authoritative environment for:

- source code development;
- Git repositories;
- architecture documentation;
- release preparation;
- test execution not requiring observatory hardware;
- Data Warehouse design and implementation;
- Analytics;
- Dashboard;
- AI components;
- packaging for EAGLE deployment.

Direct development on the EAGLE is not part of the standard workflow.

---

## 4. Current Root Structure

The assessment identified the following first-level folders under `C:\DigitalStarGate`:

```text
C:\DigitalStarGate
├── digital-stargate-manual
├── DSG-Analytics-v0.1.0
├── DSG_Analytics_v0.1.1_patch
├── DSG_Full_Automation_v2.0A
├── observatory-status-4.1
├── portal-4.0
└── reporting-workflow
```

This structure shows that Digital StarGate is already composed of multiple working components, prototypes, release packages, and documentation areas.

The environment must therefore be consolidated incrementally. It must not be replaced with a second parallel structure.

---

## 5. Current Git Baseline

The assessment identified one Git repository under the inspected depth:

```text
C:\DigitalStarGate\digital-stargate-manual
```

This repository currently acts as the primary integrated project repository on the PC Principale.

It contains:

- the technical manual;
- architecture documentation;
- operational documentation;
- analytics components;
- session data;
- reports;
- release material;
- scripts;
- templates;
- generated site content.

The repository `DigitalStarGate.Reporting`, published separately on GitHub as release `v1.0.4`, is not currently cloned under `C:\DigitalStarGate` on the PC Principale.

No local folder for that repository shall be created until the repository integration strategy is formally approved.

---

## 6. Existing Integrated Repository

### 6.1 Authoritative Path

```text
C:\DigitalStarGate\digital-stargate-manual
```

### 6.2 Main Existing Areas

```text
digital-stargate-manual
├── .git
├── .github
├── .venv
├── assets
├── backup-analytics-v0.1.0
├── build
├── data
├── docs
├── dsg-analytics
├── release
├── reports
├── scripts
├── site
└── templates
```

### 6.3 Current Role

Until a later architectural decision changes it, this repository is the authoritative integrated workspace for:

- system documentation;
- architecture decisions;
- observatory manuals;
- procedures;
- validation registers;
- integrated analytics documentation;
- session reporting;
- platform-level release notes.

---

## 7. Existing Architecture Documentation

The following ADRs already exist:

```text
docs\architecture\ADR-001-Session-Layer.md
docs\architecture\ADR-002-Analytics-Quality-Gates.md
docs\architecture\ADR-003-Warehouse-Engine.md
```

This is a critical finding.

Before creating any new Data Warehouse architecture document, the existing ADR-003 must be reviewed to determine:

- what has already been decided;
- which assumptions are still valid;
- whether the Warehouse design is already partially implemented;
- whether a new ADR is needed;
- whether DW-001 should be an analysis document, an implementation specification, or should not be created at all.

No duplicate architectural document shall be introduced before this review.

---

## 8. Existing Functional Components

### 8.1 Analytics

Existing analytics-related areas include:

```text
C:\DigitalStarGate\DSG-Analytics-v0.1.0
C:\DigitalStarGate\DSG_Analytics_v0.1.1_patch
C:\DigitalStarGate\digital-stargate-manual\dsg-analytics
C:\DigitalStarGate\digital-stargate-manual\data\analytics
C:\DigitalStarGate\digital-stargate-manual\docs\analytics
```

These locations indicate that Analytics work already exists in multiple forms:

- release package;
- patch package;
- integrated code;
- generated or retained data;
- documentation.

Before the Analytics roadmap phase, these areas will require consolidation and classification.

### 8.2 Automation

Existing automation-related area:

```text
C:\DigitalStarGate\DSG_Full_Automation_v2.0A
```

It contains:

```text
.github
dsg-analytics
eagle
```

The presence of an `eagle` folder confirms that EAGLE deployment material already exists and must be assessed before new automation code is designed.

### 8.3 Dashboard and Portal

Existing dashboard or portal-related areas include:

```text
C:\DigitalStarGate\observatory-status-4.1
C:\DigitalStarGate\portal-4.0
```

These are to be treated as existing prototypes or release packages until their exact lifecycle state is formally classified.

### 8.4 Reporting

Existing reporting-related areas include:

```text
C:\DigitalStarGate\reporting-workflow
C:\DigitalStarGate\digital-stargate-manual\templates\reporting
```

A separate GitHub repository also exists:

```text
https://github.com/maininimassimo-bit/DigitalStarGate.Reporting.git
```

Its certified release is:

```text
v1.0.4
```

The local integration strategy between the GitHub repository and the existing manual repository remains to be defined.

---

## 9. Existing Documentation Baseline

The manual repository already contains a broad documentation structure, including:

- 44 numbered chapters;
- architecture ADRs;
- analytics documentation;
- operational procedures;
- session reports;
- release notes;
- installation guides;
- validation records;
- templates;
- appendices;
- system status documentation.

This repository must therefore remain the authoritative source for platform-level documentation unless a future ADR explicitly changes that responsibility.

Module-specific repositories may contain technical documentation required to build, test, install, and release the module, but they shall not duplicate the complete platform manual.

---

## 10. Existing Development Tooling

### 10.1 Python Virtual Environment

```text
C:\DigitalStarGate\digital-stargate-manual\.venv
```

The active PowerShell prompt also showed the virtual environment enabled during the assessment.

### 10.2 MkDocs Environment

The repository contains:

```text
site
build
docs
```

and Python packages associated with Markdown and MkDocs.

This confirms that documentation generation is already part of the current platform workflow.

### 10.3 PowerShell Configuration Files

The following PowerShell data files were identified:

```text
C:\DigitalStarGate\digital-stargate-manual\templates\reporting\reporting.config.psd1
C:\DigitalStarGate\DSG_Full_Automation_v2.0A\eagle\automation.config.psd1
C:\DigitalStarGate\reporting-workflow\templates\reporting.config.psd1
```

No `.psm1` module files were identified by the assessment command under the inspected root.

This does not prove that no PowerShell modules exist elsewhere; it only records the result of the executed assessment.

---

## 11. Role of the EAGLE

The EAGLE is the operational observatory computer.

Its expected responsibilities are:

- execution of observatory-side software;
- NINA session execution;
- PHD2 guiding;
- CPWI and ASCOM integration;
- collection of logs;
- collection of weather and safety data;
- local session packaging;
- scheduled upload or synchronization;
- execution of approved automation packages;
- field validation.

The EAGLE is not the authoritative source-code development workstation.

Changes intended for the EAGLE must be:

1. developed on the PC Principale;
2. tested where possible on the PC Principale;
3. packaged as complete release files;
4. installed on the EAGLE using documented steps;
5. field-verified;
6. recorded in release documentation.

---

## 12. Environment Responsibility Matrix

| Area | PC Principale | EAGLE |
|---|---:|---:|
| Architecture | Authoritative | Consumer |
| Source development | Yes | No |
| Git operations | Yes | Only if explicitly required |
| Documentation | Authoritative | Operational copy only |
| Release preparation | Yes | No |
| NINA execution | No | Yes |
| PHD2 execution | No | Yes |
| CPWI / ASCOM | No | Yes |
| Weather acquisition | No | Yes |
| Session upload | Receives / processes | Produces / sends |
| Warehouse | Primary | Source only |
| Analytics | Primary | No |
| Dashboard | Primary | Optional display only |
| AI Assistant | Primary | No |
| Field validation | Supports | Primary execution |

---

## 13. File Delivery Rule

For all future project activities:

- every delivered source file must be complete;
- no partial replacement shall be provided unless explicitly requested;
- no undocumented patch shall be used as the standard delivery format;
- every instruction must specify the target computer;
- every instruction must specify the exact working directory;
- every command block must be complete and copy/paste ready;
- PowerShell commands must state whether they run on the PC Principale or EAGLE;
- Git publication must occur only after implementation, tests, documentation, and release validation are complete.

---

## 14. Repository Governance

The current environment contains both:

- an integrated platform repository;
- independent packages and prototypes;
- a separate published Reporting repository.

The project shall not immediately convert all components into separate repositories.

Repository separation will occur only when justified by:

- independent release lifecycle;
- independent deployment;
- clear ownership boundary;
- stable interface;
- reduced coupling;
- explicit architectural approval.

Until then, the platform shall evolve from the existing integrated repository without creating unnecessary duplicates.

---

## 15. Consolidation Principles

The following principles are approved:

1. Existing folders are assessed before new folders are created.
2. Existing ADRs are reviewed before new ADRs are written.
3. Existing code is classified before being replaced.
4. Existing release packages are preserved until formally superseded.
5. The PC Principale remains the integration authority.
6. The EAGLE remains the observatory execution node.
7. The manual repository remains the platform documentation authority.
8. The agreed roadmap remains unchanged.
9. The current environment is consolidated incrementally.
10. No destructive cleanup is performed without a validated inventory and backup.

---

## 16. Identified Risks

### 16.1 Duplication Risk

Multiple Analytics, Reporting, Portal, and Automation folders may contain overlapping versions.

### 16.2 Version Ambiguity

Folder names include release numbers and patches, but their current authoritative status is not yet formally recorded.

### 16.3 Repository Fragmentation

Only one local Git repository was identified, while other components appear to be unversioned packages or extracted releases.

### 16.4 Documentation Duplication

New Warehouse or architecture documents could duplicate existing ADRs and manual chapters.

### 16.5 Deployment Drift

EAGLE packages may diverge from PC Principale source material unless release installation and verification are controlled.

### 16.6 Data Placement Ambiguity

Session data, analytics history, reports, and future Warehouse data may overlap unless authoritative storage paths are defined.

---

## 17. Required Next Assessment

Before implementing the Data Warehouse, the next activity is:

**EA-002 — Integrated Repository and Warehouse Assessment**

It must review, at minimum:

```text
C:\DigitalStarGate\digital-stargate-manual\docs\architecture\ADR-003-Warehouse-Engine.md
C:\DigitalStarGate\digital-stargate-manual\data
C:\DigitalStarGate\digital-stargate-manual\dsg-analytics
C:\DigitalStarGate\digital-stargate-manual\scripts
C:\DigitalStarGate\digital-stargate-manual\release
C:\DigitalStarGate\reporting-workflow
```

The purpose will be to determine:

- the actual Warehouse architecture already defined;
- the current data model;
- the ingestion workflow;
- the relationship with Reporting;
- the current Analytics dependency;
- gaps against the roadmap;
- the correct location for future implementation.

No Data Warehouse implementation shall begin before EA-002 is complete.

---

## 18. Current Decisions

### DEC-EA-001-01

`C:\DigitalStarGate` remains the root directory on the PC Principale.

### DEC-EA-001-02

`C:\DigitalStarGate\digital-stargate-manual` remains the authoritative integrated repository for platform documentation and current integrated project material.

### DEC-EA-001-03

No duplicate `DigitalStarGate.Reporting_v1.0.4_WORK` folder shall be created on the PC Principale.

### DEC-EA-001-04

The separate Reporting repository shall not be cloned or integrated locally until its role is assessed against the existing platform structure.

### DEC-EA-001-05

The roadmap proceeds with Data Warehouse only after reviewing the existing Warehouse ADR and implementation material.

### DEC-EA-001-06

All future instructions must identify the execution computer and exact working path.

### DEC-EA-001-07

All future delivered files must be complete release-ready files.

---

## 19. Baseline Status

**Assessment result:** PASS WITH CONSOLIDATION ACTIONS

The PC Principale is suitable as the central Digital StarGate development and integration environment.

The environment is already operational and mature, but it contains multiple historical packages and partially overlapping components.

The correct next step is not to create a new project structure. The correct next step is to assess and consolidate the existing Warehouse, Reporting, and Analytics components in alignment with the agreed roadmap.

---

## 20. Approval

This document establishes the current environment baseline for the Digital StarGate roadmap.

**Approved status:** BASELINE APPROVED  
**Next document:** EA-002 — Integrated Repository and Warehouse Assessment

---

**END OF DOCUMENT**
