# Enterprise Glossary

**Document ID:** DSG-KF-GLO-001  
**Status:** Controlled Draft  
**Owner:** Chief Enterprise Architect / Knowledge Architect  
**Governance level:** Knowledge Framework  
**Roadmap authority:** DSG-MR-001  
**Traceability:** DSRA -> Enterprise Architecture -> ADR -> SOP -> Manuals -> Runbooks

## Purpose

This glossary is the controlled terminology reference for the Digital StarGate knowledge repository. It normalizes recurring terms used by the Master Roadmap, DSRA, Enterprise Architecture, Enterprise Solution Blueprint, ADRs, SOPs, manuals and runbooks.

Definitions do not introduce implementation decisions. Where a term depends on an unresolved architecture decision, the applicable decision remains open in the architecture decision catalog or in the Knowledge Framework open decision sections.

## Glossary

| Term | Definition | Architecture reference |
| --- | --- | --- |
| ADR | Architecture Decision Record used to document approved or open architecture decisions under the governance hierarchy. | `docs/enterprise-architecture/architecture-decision-catalog.md` |
| AI Assistant | Application capability that supports analysis, interpretation, documentation assistance and recommendations using governed observatory knowledge. | `docs/enterprise-architecture/application-architecture.md` |
| AI Recommendation | Governed output of the AI Assistant that proposes actions, findings or documentation improvements without bypassing human or roadmap governance. | `docs/knowledge/domain-model.md` |
| Alert | Operational signal generated from weather, safety, automation, session, processing or platform monitoring conditions. | `docs/enterprise-architecture/observability-architecture.md` |
| AllSky | External observatory visual context source used for sky-state awareness and operational evidence. | `docs/enterprise-architecture/integration-architecture.md` |
| Alpaca | ASCOM network protocol option for equipment integration where repository architecture recognizes ASCOM Alpaca integration. | `docs/enterprise-solution-blueprint/integration-catalog.md` |
| Analytics | Capability for dashboards, indicators, quality reporting and trend analysis over observation, processing, maintenance and documentation data. | `docs/enterprise-architecture/application-architecture.md` |
| Archive | Long-term governed preservation area for observation data, scientific products, manifests, metadata and documentation evidence. | `docs/enterprise-architecture/data-architecture.md` |
| ASCOM | Astronomy device interoperability layer used by Digital StarGate to connect control software to observatory equipment. | `docs/enterprise-architecture/technology-architecture.md` |
| Assessment | Controlled evaluation artefact positioned after ADRs and before SOPs in the governance hierarchy. | `docs/enterprise-architecture/repository-map.md` |
| ASTAP | External plate solving and astronomy processing integration referenced by the architecture. | `docs/enterprise-solution-blueprint/integration-catalog.md` |
| AAVSO | External scientific submission or reference organization integration for variable star and observation workflows when applicable. | `docs/enterprise-solution-blueprint/integration-catalog.md` |
| Backup | Controlled preservation mechanism for repository, observation data, configuration and operational evidence. | `docs/enterprise-architecture/technology-architecture.md` |
| Calibration | Process of creating or applying calibration assets to reduce sensor and optical artefacts in astronomical images. | `docs/enterprise-architecture/data-architecture.md` |
| Calibration Asset | Bias, dark, flat or master calibration data used by calibration and image processing workflows. | `docs/knowledge/domain-model.md` |
| Calibration Library | Application service that governs calibration frames, master calibrations and their reuse conditions. | `docs/enterprise-architecture/application-architecture.md` |
| Capability | Stable business ability required by Digital StarGate, traceable to roadmap and enterprise architecture. | `docs/enterprise-architecture/business-architecture.md` |
| Capability Map | Structured view of the business capabilities needed to operate, improve and govern Digital StarGate. | `docs/enterprise-architecture/business-architecture.md` |
| Cloud Storage | External or remote storage capability used for backup, archive or publication according to governed architecture decisions. | `docs/enterprise-architecture/technology-architecture.md` |
| Configuration | Controlled operational setting for equipment, automation, software components, processing or documentation tooling. | `docs/knowledge/domain-model.md` |
| CPWI | Celestron mount control integration referenced in the observatory control architecture. | `docs/enterprise-architecture/integration-architecture.md` |
| Data Platform | Logical capability that organizes observation data, metadata, catalogs, archive, publication flow and data lifecycle governance. | `docs/enterprise-architecture/data-architecture.md` |
| Documentation Asset | Governed repository artefact such as roadmap, DSRA, architecture document, ADR, SOP, manual, runbook or release note. | `docs/knowledge/domain-model.md` |
| DSRA | Digital StarGate Risk Assessment layer that derives from the Master Roadmap and informs enterprise architecture. | `docs/enterprise-architecture/repository-map.md` |
| EAGLE | Observatory-side execution node referenced by the technology architecture for local control and remote operation. | `docs/enterprise-architecture/technology-architecture.md` |
| Engineering Asset | Technical or operational asset used to support the observatory, including equipment, configuration, software component or manual evidence. | `docs/knowledge/domain-model.md` |
| Engineering Handbook | Governed contributor and maintainer guidance layer after SOPs in the documentation hierarchy. | `docs/enterprise-architecture/repository-map.md` |
| Engineering Portal | Portal capability for engineering status, configuration awareness, maintenance evidence and operational support. | `docs/enterprise-architecture/application-architecture.md` |
| Equipment | Physical observatory device or subsystem used in acquisition, guiding, weather safety, network access or operations. | `docs/enterprise-architecture/technology-architecture.md` |
| Equipment Registry | Canonical inventory of equipment, capabilities, configuration references and operational state metadata. | `docs/knowledge/domain-model.md` |
| GitHub | Authoritative repository platform for documentation, governance artefacts, ADRs and release records. | `docs/enterprise-architecture/repository-map.md` |
| Governance | Controlled decision, review and lifecycle framework that preserves the roadmap-first hierarchy. | `docs/knowledge/architecture-governance.md` |
| Image Acquisition | Process by which N.I.N.A. and equipment produce raw astronomical images during an observation session. | `docs/enterprise-solution-blueprint/logical-architecture.md` |
| Image Processing | Processing capability that transforms calibrated or registered inputs into integrated and processed images or scientific products. | `docs/enterprise-architecture/application-architecture.md` |
| Integrated Image | Combined image product produced after registration and stacking/integration of compatible frames. | `docs/knowledge/domain-model.md` |
| Knowledge Asset | Any governed concept, term, requirement, architecture element, decision, procedure or evidence record. | `docs/knowledge/repository-taxonomy.md` |
| Knowledge Framework | Semantic backbone that organizes domain model, information model, glossary, requirements, traceability, taxonomy, governance and quality. | `docs/knowledge/repository-taxonomy.md` |
| Knowledge Graph | Conceptual semantic model linking observations, targets, equipment, sessions, data products, decisions, procedures and evidence. | `docs/knowledge/knowledge-graph-model.md` |
| Manual | Technical manual layer used to describe durable operating or engineering knowledge after the Engineering Handbook. | `docs/enterprise-architecture/repository-map.md` |
| Maintenance Activity | Planned or corrective activity affecting equipment, configuration, operational readiness or repository knowledge. | `docs/knowledge/domain-model.md` |
| Master Roadmap | Frozen highest authority for Digital StarGate scope, sequencing and governance constraints. | `docs/enterprise-architecture/repository-map.md` |
| N.I.N.A. | Observatory automation and imaging application integration used for observation execution. | `docs/enterprise-architecture/integration-architecture.md` |
| Observation | Governed scientific or engineering activity that targets astronomical data acquisition or operational validation. | `docs/enterprise-architecture/business-architecture.md` |
| Observation Archive | Governed long-term store for observation data, manifests, products and metadata. | `docs/enterprise-architecture/data-architecture.md` |
| Observation Catalog | Curated index of observation sessions, targets, metadata, products and traceability references. | `docs/knowledge/domain-model.md` |
| Observation Request | Canonical request to observe a target or perform an observing activity under scheduling and operational constraints. | `docs/knowledge/domain-model.md` |
| Observation Session | Bounded execution instance in which equipment, target, plan, weather state and acquisition outputs are linked. | `docs/knowledge/domain-model.md` |
| Observatory | Physical and operational environment for automated astronomical observations. | `docs/enterprise-architecture/business-architecture.md` |
| Observatory Safety | Capability that protects equipment, data integrity and remote operations through weather and operational state awareness. | `docs/enterprise-architecture/observability-architecture.md` |
| Open Architectural Decision | Architecture question that cannot be finalized from repository evidence and must remain explicitly open. | `docs/enterprise-architecture/architecture-decision-catalog.md` |
| Open Knowledge Decision | Knowledge-modeling question that cannot be finalized from repository evidence and is recorded without invented resolution. | `docs/knowledge/knowledge-graph-model.md` |
| PHD2 | Guiding integration used in observation execution and session evidence. | `docs/enterprise-architecture/integration-architecture.md` |
| PixInsight | Image processing integration referenced by architecture for astronomical processing workflows. | `docs/enterprise-architecture/integration-architecture.md` |
| Plate Solving | Process that determines the astronomical position and orientation of an image by matching stars to known references. | `docs/enterprise-solution-blueprint/integration-catalog.md` |
| Processed Image | Image product after processing steps such as calibration, registration, integration and enhancement as governed by processing workflow. | `docs/knowledge/domain-model.md` |
| Publication | Controlled release or sharing of scientific products, metadata, documentation or results. | `docs/enterprise-architecture/data-architecture.md` |
| Registered Image | Image aligned to a reference frame or astrometric solution for integration or analysis. | `docs/knowledge/domain-model.md` |
| Release Notes | Final documentation layer recording released changes, readiness and traceability. | `docs/enterprise-architecture/repository-map.md` |
| Remote Access | Operational capability for accessing observatory nodes through governed network and security controls. | `docs/enterprise-architecture/technology-architecture.md` |
| Roadmap | See Master Roadmap. | `docs/enterprise-architecture/repository-map.md` |
| Runbook | Executable operational recovery or support procedure derived from SOPs and manuals. | `docs/enterprise-architecture/repository-map.md` |
| Safety Event | Event affecting observatory safety, equipment protection, weather safety or remote operating state. | `docs/knowledge/domain-model.md` |
| Science Portal | Portal capability for observation products, catalogs, scientific evidence and publication-facing views. | `docs/enterprise-architecture/application-architecture.md` |
| Scientific Metadata | Structured metadata describing targets, sessions, image products, calibration lineage, quality and scientific context. | `docs/enterprise-architecture/data-architecture.md` |
| Scientific Product | Validated observation result suitable for analysis, publication or archive preservation. | `docs/knowledge/domain-model.md` |
| Session Manifest | Canonical record that binds request, target, equipment, weather, configuration, acquisition files, processing lineage and outputs. | `docs/knowledge/domain-model.md` |
| SOP | Standard Operating Procedure derived from assessments and architecture, used to govern repeatable operations. | `docs/enterprise-architecture/repository-map.md` |
| Target | Astronomical object or sky region selected for observation, scheduling, acquisition or analysis. | `docs/knowledge/domain-model.md` |
| Target Registry | Canonical register of targets, identifiers, coordinates, priorities and observation history. | `docs/knowledge/domain-model.md` |
| Teltonika | Network component referenced by technology and integration architecture for observatory connectivity. | `docs/enterprise-architecture/technology-architecture.md` |
| TNS | Transient Name Server integration for transient object reference or reporting workflows when applicable. | `docs/enterprise-solution-blueprint/integration-catalog.md` |
| Traceability | Required relationship from roadmap authority through DSRA, architecture, ADR, assessments, SOPs, manuals, runbooks and release notes. | `docs/knowledge/traceability-matrix.md` |
| VPN | Secure remote connectivity capability referenced by security and technology architecture. | `docs/enterprise-architecture/security-architecture.md` |
| Weather Event | Weather-related condition or transition that affects observation eligibility and observatory safety. | `docs/knowledge/domain-model.md` |
| Weather Safe | Governed state indicating that weather conditions permit safe observation or continued operations according to approved procedures. | `docs/enterprise-architecture/observability-architecture.md` |
| Weather Station | External observatory weather data source used for safety and session decisions. | `docs/enterprise-architecture/integration-architecture.md` |

## Governance Rules

- New terms shall be added only when they recur in controlled documentation or are required for traceability.
- Definitions shall reference an architecture or governance document whenever applicable.
- Terms that require unresolved technology, data, security or operating decisions shall remain linked to open decisions.
- The glossary does not replace ADRs, SOPs or manuals; it stabilizes language across them.

## Open Knowledge Decisions

| Decision | Reason | Impact | Owner | Required input |
| --- | --- | --- | --- | --- |
| OKD-GLO-001 - Multilingual glossary policy | Repository evidence does not define whether glossary terms must be bilingual. | Affects terminology reuse in manuals and portals. | Knowledge Architect | Governance decision on language policy. |
| OKD-GLO-002 - Formal synonym management | Repository evidence does not define whether synonyms and aliases require separate registry entries. | Affects search, Knowledge Graph and documentation consistency. | Knowledge Architect | Taxonomy decision and repository tooling constraints. |
