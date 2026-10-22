# Architecture Decision Records (ADRs)

## Purpose

This document records the major architectural and technical decisions made during the development of the DevSecOps Platform.

The objective is to preserve the reasoning behind important decisions, document trade-offs, and maintain consistency as the platform evolves.

---

## ADR-001: Use GitHub Actions as the Primary Workflow Engine

**Status:** Accepted

### Context

Traditional CI/CD systems such as Jenkins require installation, configuration, maintenance, upgrades, and infrastructure resources.

The platform needs to support multiple repositories while minimizing operational overhead and recurring costs.

### Decision

Use GitHub Actions as the primary workflow orchestration and execution platform.

### Rationale

- Native integration with GitHub repositories and pull requests.
- Support for reusable workflows.
- Hosted execution environments.
- No dedicated CI server required for standard workloads.
- Built-in workflow status reporting.

### Trade-offs

- Usage is subject to GitHub Actions quotas and plan limits.
- Execution depends on GitHub platform availability.
- Specialized workloads may require self-hosted runners.
- Private reusable workflow access requires appropriate configuration.

---

## ADR-002: Centralize Reusable Workflows

**Status:** Accepted

### Context

Maintaining separate implementations of the same security pipeline across many repositories creates duplication and inconsistent policies.

### Decision

Maintain shared workflow implementations in the central `Action-Engine` repository.

Application repositories will invoke these workflows through small caller workflows.

### Rationale

- One centrally maintained implementation.
- Consistent security checks across projects.
- Easier maintenance and upgrades.
- Less duplicated YAML.
- Simplified repository onboarding.

### Trade-offs

- A workflow defect can affect multiple repositories.
- Workflow changes require compatibility testing.
- Access permissions must be configured for private platform repositories.
- Version pinning and rollback procedures are necessary.

---

## ADR-003: Prefer Free and Open-Source Tools

**Status:** Accepted

### Context

The platform is intended to minimize infrastructure and licensing costs while providing useful security coverage.

### Decision

Prefer tools with free or open-source execution options when they satisfy the security requirement.

Initial examples include:

- Gitleaks for secret detection.
- Trivy for vulnerability and configuration scanning.
- Semgrep for suitable static analysis use cases.
- Syft for SBOM generation.

### Rationale

- Lower initial operating costs.
- Broad ecosystem support.
- Reduced dependence on paid hosted scanning services.
- Ability to run tools directly in CI workflows.

### Trade-offs

- Some features may require paid plans or have additional restrictions.
- Tool configuration and maintenance remain necessary.
- Open-source tools may not provide every enterprise reporting or governance feature.

Tool licenses and usage terms must be reviewed before adoption.

---

## ADR-004: Implement Secret Scanning First

**Status:** Accepted

### Context

The platform needs a focused initial capability that can be integrated into multiple repositories and validated without substantial infrastructure.

### Decision

Implement reusable Gitleaks secret scanning as the first security workflow.

### Rationale

- Addresses accidental credential exposure.
- Requires no dedicated scanning server.
- Can run