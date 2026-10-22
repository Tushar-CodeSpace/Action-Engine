# Action Engine

A centralized, GitHub-native DevSecOps platform for managing the Software Development Life Cycle (SDLC) across multiple projects and repositories.

The goal is to provide reusable CI/CD automation, security scanning, code quality checks, and release controls without requiring separately managed servers such as Jenkins or SonarQube.

## Objectives

- Centralize DevSecOps workflows for multiple repositories.
- Automate security checks throughout the SDLC.
- Use GitHub Actions and free/open-source tools wherever practical.
- Avoid dedicated CI/CD infrastructure and unnecessary server configuration.
- Standardize security policies and quality gates across projects.
- Provide consistent results, reports, and pull request checks.
- Enable easy onboarding of new repositories.
- Keep the platform modular and extensible.

## Core Principles

- **Free-first:** Prefer free and open-source tools.
- **Serverless CI/CD:** Use GitHub-hosted runners where available and appropriate.
- **Reusable workflows:** Maintain common pipeline logic centrally.
- **Security by default:** Apply least privilege and secure workflow practices.
- **Production safety:** Validate changes before enforcing blocking checks.
- **Scalability:** Support multiple repositories and technology stacks.
- **Maintainability:** Keep configuration minimal in application repositories.

## Planned Capabilities

### 1. Runners and Agents

- GitHub-hosted runner integration.
- Optional self-hosted runner support for specialized workloads.

### 2. Security Checks

- Secret detection with Gitleaks.
- Dependency vulnerability scanning.
- Static Application Security Testing (SAST).
- Container image scanning.
- Infrastructure-as-Code (IaC) scanning.
- Software Bill of Materials (SBOM) generation.

### 3. Code Quality

- Linting and formatting checks.
- Test execution.
- Code coverage reporting.
- Quality gates using suitable free/open-source tooling.

### 4. CI/CD Automation

- Standardized build pipelines.
- Automated test execution.
- Container build and validation.
- Release and deployment workflows.
- Deployment verification and rollback guidance.

### 5. Reporting and Governance

- Pull request status checks.
- Security scan summaries.
- Central workflow version management.
- Repository onboarding documentation.
- Security exception tracking.

## Architecture

The platform maintains reusable workflows in a central repository. Application repositories invoke these workflows through small GitHub Actions caller workflows.

```text
devsecops-platform
        |
        | Reusable Workflows
        |
        +-------------------+
        |                   |
   Project A            Project B
   Repository           Repository
        |                   |
        +---------+---------+
                  |
          GitHub Actions
          Hosted Runners
                  |
          Automated SDLC Checks
                  |
        Pass / Fail / Reports
```

## Technology Stack

| Component | Technology |
|---|---|
| Workflow orchestration | GitHub Actions |
| Execution environment | GitHub-hosted runners |
| Secret scanning | Gitleaks |
| Dependency and container scanning | Trivy |
| Static analysis | Semgrep or other suitable tools |
| Source control | GitHub |
| Workflow configuration | YAML |
| Documentation | Markdown |

Tool selection and licensing will be reviewed before production adoption.

## Repository Structure

```text
devsecops-platform/
├── .github/
│   └── workflows/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY-MODEL.md
│   ├── ONBOARDING.md
│   ├── WORKFLOW-CATALOG.md
│   ├── OPERATING-GUIDE.md
│   ├── ROADMAP.md
│   ├── CONTRIBUTING.md
│   └── DECISIONS.md
├── scripts/
├── README.md
└── .gitignore
```

## Implementation Roadmap

- [ ] Establish the central platform repository.
- [ ] Implement reusable secret scanning.
- [ ] Integrate and validate a pilot repository.
- [ ] Configure required pull request checks.
- [ ] Add dependency and static analysis checks.
- [ ] Add container and IaC security scanning.
- [ ] Introduce build, test, and release workflows.
- [ ] Expand adoption across multiple repositories.
- [ ] Standardize reporting and governance.

## Cost Model

The platform is designed to minimize recurring infrastructure costs by avoiding dedicated CI/CD servers and prioritizing free/open-source tools.

GitHub Actions usage, artifact storage, concurrency, and GitHub security features remain subject to applicable plan limits and eligibility. Therefore, unlimited zero-cost execution is not guaranteed.

## Security Considerations

- Never commit real credentials or secrets.
- Use least-privilege workflow permissions.
- Pin third-party actions to reviewed commit SHAs for production.
- Avoid exposing sensitive scan output in logs or artifacts.
- Do not execute untrusted pull request code with privileged credentials.
- Rotate credentials immediately when exposure is suspected.

## Project Status

**Current phase:** Foundation and security automation.

Secret scanning is the initial implementation priority. Additional capabilities will be introduced incrementally after validation.

## Contribution

All workflow and policy changes should be reviewed, tested, and documented before being rolled out to application repositories.