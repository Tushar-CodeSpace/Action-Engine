# DevSecOps Platform Roadmap

## 1. Vision

Build a centralized, reusable, and free-first DevSecOps platform that manages SDLC automation across multiple application repositories using GitHub Actions and open-source tooling.

The platform should minimize infrastructure management, standardize security controls, and make onboarding additional repositories straightforward.

## 2. Development Principles

- Prioritize production safety over feature count.
- Implement one capability at a time.
- Validate each workflow against a pilot repository.
- Prefer free and open-source tools.
- Avoid dedicated CI/CD servers wherever possible.
- Centralize reusable workflow logic.
- Enforce security checks only after validating their reliability.
- Keep costs, permissions, and maintenance requirements visible.

## 3. Phase 0 — Foundation

**Objective:** Establish the platform repository and its governance model.

Tasks:

- [x] Create the `Action-Engine` platform repository.
- [x] Add the project README.
- [x] Document the system architecture.
- [x] Define the security model.
- [x] Document repository onboarding.
- [x] Define workflow naming and versioning standards.
- [x] Establish contribution and review requirements.
- [x] Confirm repository visibility and access controls.

**Completion criteria:**

- Documentation is available.
- Ownership is defined.
- Workflow changes follow a review process.
- The platform is ready for its first security workflow.

## 4. Phase 1 — Secret Scanning

**Objective:** Detect exposed credentials across application repositories.

**Tool:** Gitleaks

Tasks:

- [x] Implement parallel secret-scanning jobs using Gitleaks.
- [x] Configure pull request triggers.
- [x] Configure pushes to the relevant branches.
- [x] Add manual workflow execution (`workflow_dispatch`).
- [x] Test and verify leak detection across Git history.
- [x] Verify that scan results redact raw secrets.
- [x] Validate quality gate failure behavior.
- [x] Integrate pilot repositories (`Action-Engine`, `nidoworkz-backend`).
- [x] Implement automated Excel reporting and email alerting.
- [x] Roll out to additional repositories.

**Completion criteria:**

- The workflow detects test and real leaked secrets.
- The workflow passes when leaks are remediated or ignored via allowlist.
- Scanner execution failures are not silently ignored.
- The gatekeeper step blocks merging or marks runs failed when findings are detected.
- Repository owners receive detailed Excel and HTML email reports with remediation guidance.

## 5. Phase 2 — Core SDLC Security

**Objective:** Expand automated security checks and establish basic code validation.

### Dependency Security

- [x] Integrate dependency vulnerability & misconfiguration scanning with Trivy.
- [x] Implement package/SBOM inventory counting and reporting.
- [x] Define vulnerability severity thresholds (`HIGH,CRITICAL`).
- [x] Document dependency remediation procedures and package metrics.

### Static Application Security Testing

- [ ] Select and validate a suitable SAST tool.
- [ ] Support the languages used by pilot repositories.
- [ ] Configure pull request scanning.
- [ ] Establish false-positive management.
- [ ] Introduce blocking rules after validation.

### Infrastructure Security

- [ ] Integrate IaC scanning.
- [ ] Identify supported infrastructure file types.
- [ ] Validate findings against representative projects.

### Code Quality and Testing

- [ ] Add reusable linting workflows.
- [ ] Add reusable test workflows.
- [ ] Introduce code coverage reporting where useful.
- [ ] Support project-specific configuration through workflow inputs.

**Completion criteria:**

- Core checks run reliably on supported repositories.
- Findings are actionable.
- Tool failures and security findings are distinguishable.
- Required checks are enforced only after successful validation.

## 6. Phase 3 — Build and Container Security

**Objective:** Standardize application builds and container validation.

Tasks:

- [ ] Implement reusable application build workflows.
- [ ] Add container image build workflows.
- [ ] Integrate container vulnerability scanning.
- [ ] Add SBOM generation.
- [ ] Define artifact naming and retention policies.
- [ ] Establish consistent build metadata.
- [ ] Validate image scanning before publishing.

**Completion criteria:**

- Supported applications can build using reusable workflows.
- Container images can be scanned before release.
- SBOM artifacts are associated with the relevant build.
- Credentials are not exposed during builds.

## 7. Phase 4 — Release and Deployment Automation

**Objective:** Introduce controlled release and deployment workflows.

Tasks:

- [ ] Implement reusable release workflows.
- [ ] Standardize version and tag conventions.
- [ ] Add artifact publication.
- [ ] Configure protected deployment environments where supported.
- [ ] Use short-lived credentials through OIDC where appropriate.
- [ ] Add deployment verification.
- [ ] Document rollback procedures.
- [ ] Restrict production deployment to approved events and identities.

**Completion criteria:**

- Releases follow a documented process.
- Production credentials are not exposed to untrusted pull requests.
- Deployment permissions are limited.
- Rollback procedures have been tested.

## 8. Phase 5 — Reporting and Governance

**Objective:** Improve visibility across the repository portfolio.

Tasks:

- [ ] Standardize workflow summaries.
- [ ] Maintain a repository onboarding inventory.
- [ ] Track enabled security controls.
- [ ] Document approved exceptions and expiry dates.
- [ ] Review recurring workflow failures.
- [ ] Track remediation progress.
- [ ] Review usage quotas and execution costs.
- [ ] Establish periodic security coverage reviews.

**Completion criteria:**

- Repository owners can identify their enabled checks.
- Platform