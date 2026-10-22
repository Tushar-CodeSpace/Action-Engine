# DevSecOps Workflow Catalog

## 1. Purpose

This document defines the workflows planned for the DevSecOps Platform.

The platform centralizes SDLC automation across multiple repositories using reusable GitHub Actions workflows and free/open-source tools wherever practical.

This catalog distinguishes the initial implementation from future capabilities.

## 2. Workflow Categories

- Security checks
- Code quality
- Build and testing
- Container security
- Infrastructure security
- Release management
- Reporting and governance

## 3. Security Workflows

### 3.1 Secret Scanning

**Workflow:** `secret-scan-reusable.yml`

**Tool:** Gitleaks

**Purpose:** Detect potentially exposed credentials in source code and Git history.

**Triggers:**
- Pull requests
- Pushes to configured branches
- Manual execution

**Expected behavior:**
- Pass when no actionable findings are detected.
- Fail when secrets are detected.
- Avoid exposing raw secret values in logs and artifacts.

**Priority:** Phase 1 — Initial implementation.

### 3.2 Dependency Vulnerability Scanning

**Planned workflow:** `dependency-scan-reusable.yml`

**Candidate tools:** Trivy and ecosystem-native dependency audit tools.

**Purpose:** Identify known vulnerabilities in application dependencies.

**Triggers:**
- Pull requests
- Pushes to configured branches
- Scheduled scans

**Expected behavior:**
- Report vulnerable dependencies and affected versions.
- Provide remediation guidance.
- Apply documented severity thresholds.

**Priority:** Phase 2.

### 3.3 Dependency Review

**Planned workflow:** `dependency-review-reusable.yml`

**Candidate tool:** GitHub Dependency Review Action, where available.

**Purpose:** Review dependency changes introduced by pull requests.

**Expected behavior:**
- Identify newly introduced vulnerable dependencies.
- Apply approved vulnerability thresholds.
- Report findings before merging.

**Priority:** Phase 2.

Availability of GitHub security features depends on repository eligibility and plan.

### 3.4 Static Application Security Testing

**Planned workflow:** `sast-reusable.yml`

**Candidate tool:** Semgrep or another suitable static analysis tool.

**Purpose:** Detect potentially insecure coding patterns.

**Triggers:**
- Pull requests
- Pushes to configured branches
- Scheduled scans

**Expected behavior:**
- Identify security findings in supported languages.
- Report severity and affected code.
- Support reviewed exceptions.
- Enforce blocking rules after validation.

**Priority:** Phase 2.

Tool licensing and usage terms must be reviewed before adoption.

### 3.5 Container Image Scanning

**Planned workflow:** `container-scan-reusable.yml`

**Tool:** Trivy

**Purpose:** Identify vulnerabilities in container images and relevant image configuration.

**Triggers:**
- Pull requests affecting container build files
- Image build workflows
- Release workflows

**Expected behavior:**
- Scan the image that will actually be published.
- Report vulnerable packages and severity.
- Apply documented release thresholds.

**Priority:** Phase 3.

### 3.6 Infrastructure-as-Code Scanning

**Planned workflow:** `iac-scan-reusable.yml`

**Tool:** Trivy or another suitable IaC scanner.

**Purpose:** Detect insecure infrastructure configuration.

**Supported areas may include:**
- Dockerfiles
- Kubernetes manifests
- Terraform configurations
- Other supported infrastructure definitions

**Triggers:**
- Pull requests
- Pushes affecting infrastructure files

**Expected behavior:**
- Identify insecure configuration.
- Provide remediation guidance.
- Fail according to the configured policy.

**Priority:** Phase 2.

### 3.7 Software Bill of Materials

**Planned workflow:** `sbom-reusable.yml`

**Tool:** Syft

**Purpose:** Generate an inventory of software components included in an application or release.

**Triggers:**
- Release builds
- Approved manual execution

**Expected behavior:**
- Generate an SBOM in a supported format.
- Associate it with the relevant build or release.
- Store it with appropriate access and retention controls.

**Priority:** Phase 3.

## 4. Code Quality Workflows

### 4.1 Linting and Formatting

**Planned workflow:** `lint-reusable.yml`

**Purpose:** Enforce project-specific coding standards and formatting.

**Examples:**
- ESLint for JavaScript and TypeScript.
- Ruff for Python.
- Other language-specific tools as required.

**Triggers:** Pull requests and pushes.

**Priority:** Phase 2.

### 4.2 Automated Testing

**Planned workflow:** `test-reusable.yml`

**Purpose:** Run application tests to detect regressions.

**Examples:**
- Unit tests
- Integration tests
- API tests

**Triggers:** Pull requests and pushes.

**Priority:** Phase 2.

### 4.3 Code Coverage

**Planned workflow:** `coverage-reusable.yml`

**Purpose:** Measure test coverage and optionally enforce minimum coverage thresholds.

**Triggers:** Pull requests and pushes.

**Priority:** Phase 2.

Coverage thresholds should reflect the project's testing maturity rather than being selected arbitrarily.

## 5. Build and Delivery Workflows

### 5.1 Application Build

**Planned workflow:** `build-reusable.yml`

**Purpose:** Build applications consistently across repositories.

**Expected behavior:**
- Install dependencies.
- Validate build configuration.
- Compile or package the application.
- Return a clear pass/fail result.

**Priority:** Phase 3.

### 5.2 Container Build

**Planned workflow:** `container-build-reusable.yml`

**Purpose:** Build and validate container images.

**Expected behavior:**
- Build the image.
- Apply consistent image tagging.
- Support scanning before publishing.
- Avoid exposing credentials during builds.

**Priority:** Phase 3.

### 5.3 Release Management

**Planned workflow:** `release-reusable.yml`

**Purpose:** Standardize release creation and artifact publication.

**Expected behavior:**
- Run required validation.
- Produce release artifacts.
- Associate artifacts with a version.
- Apply release permissions and approval requirements.

**Priority:** Phase 4.

### 5.4 Deployment

**Planned workflow:** `deploy-reusable.yml`

**Purpose:** Deploy applications to approved environments.

**Expected behavior:**
- Restrict deployment to approved branches or release events.
- Use environment protections where supported.
- Prefer short-lived credentials through OIDC when the cloud provider supports it.
- Verify deployment health.
- Document rollback procedures.

**Priority:** Phase 4.

Deployment credentials should never be exposed to untrusted pull request workflows.

## 6. Reporting and Governance

### 6.1 Workflow Summaries

**Planned capability:** Standardized GitHub Actions job summaries.

Purpose:
- Present pass/fail status.
- Summarize actionable findings.
- Link to safe remediation guidance.

### 6.2 Repository Coverage Inventory

**Planned capability:** Track which repositories have adopted the platform and which checks are enabled.

### 6.3 Exception Management

**Planned capability:** Document approved security exceptions, their owners, rationale, and expiry dates.

### 6.4 Scheduled Security Reviews

**Planned capability:** Run periodic checks for dependency vulnerabilities and other controls that benefit from fresh vulnerability data.

## 7. Recommended Implementation Order

| Phase | Workflows |
|---|---|
| Phase 1 | Secret scanning |
| Phase 2 | Dependency scanning, dependency review, SAST, IaC scanning, linting, testing |
| Phase 3 | Container scanning, builds, SBOM generation |
| Phase 4 | Releases, deployments, artifact provenance |
| Phase 5 | Coverage reporting, governance, and broader visibility |

## 8. Standard Workflow Requirements

Every reusable workflow should document:

- Purpose and supported project types.
- Triggering mechanism.
- Inputs and outputs.
- Required permissions.
- Tools and versions.
- Expected execution time.
- Failure conditions.
- Logging and artifact handling.
- Exceptions and troubleshooting.
- Rollback or version-pinning procedure.

## 9. Enforcement Policy

Not every scanner should block merges immediately.

Recommended approach:

1. Introduce the workflow in a pilot repository.
2. Observe findings and execution reliability.
3. Tune rules and investigate false positives.
4. Agree on severity thresholds.
5. Enable required checks or blocking behavior.
6. Roll out to other repositories.

Scanner execution errors must not be silently treated as successful security checks.

## 10. Cost and Licensing

The platform prioritizes free/open-source tooling, but actual cost depends on:

- GitHub Actions usage allowances.
- Artifact storage and retention.
- Repository visibility and plan.
- Tool licensing and usage restrictions.
- Optional hosted security services.

Review current terms before adopting a tool or relying on a GitHub security feature.

## 11. Conclusion

This catalog provides a phased plan for standardizing DevSecOps across multiple repositories.

Secret scanning is the first implementation target. Additional security, quality, build, and release workflows will be introduced incrementally, with clear ownership and production-safe enforcement.