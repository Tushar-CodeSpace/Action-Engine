# DevSecOps Platform Operating Guide

## 1. Purpose

This guide defines how to operate, troubleshoot, maintain, and improve the DevSecOps Platform across multiple application repositories.

The platform uses GitHub Actions and reusable workflows to run security and SDLC checks without requiring a dedicated CI/CD server.

## 2. Operating Principles

- Keep shared workflows centrally maintained.
- Validate changes against a pilot repository before rollout.
- Apply least-privilege permissions.
- Treat scanner findings and workflow execution errors separately.
- Never expose credentials in logs or reports.
- Keep a known-good workflow version available for rollback.
- Document exceptions and assign clear ownership.

## 3. Standard Pull Request Lifecycle

1. A developer opens a pull request.
2. The application repository invokes the approved reusable workflows.
3. GitHub Actions provisions the required runner.
4. Security and quality checks execute.
5. GitHub reports the result to the pull request.
6. Required checks determine whether merging is permitted.
7. The repository owner resolves findings before approval.

## 4. Handling Security Findings

### 4.1 Secret Detection

When Gitleaks identifies a potential secret:

1. Treat the finding as sensitive.
2. Determine whether the value represents a real credential without copying it into public comments or logs.
3. Revoke or rotate the credential if it is real and potentially exposed.
4. Remove it from active source code.
5. Investigate whether it remains in Git history.
6. Re-run the scan to verify remediation.

Do not merge a pull request merely because the developer has removed the finding from the latest file.

### 4.2 Dependency Vulnerabilities

When a dependency scanner reports a vulnerability:

1. Identify the affected package and version.
2. Review the vulnerability severity and available fixes.
3. Upgrade or replace the package where practical.
4. Re-run the dependency scan and relevant tests.
5. Document an approved exception if immediate remediation is not possible.

### 4.3 Static Analysis Findings

When SAST identifies a potential code vulnerability:

1. Review the affected code path.
2. Confirm whether the issue is exploitable or a false positive.
3. Fix the issue or document a narrowly scoped exception.
4. Re-run the relevant checks.
5. Obtain the required review before merging.

## 5. Troubleshooting

### 5.1 Workflow Does Not Start

Check:

- Workflow YAML syntax.
- Event triggers and branch filters.
- GitHub Actions availability and repository settings.
- Workflow file location.
- Caller workflow reference and permissions.

### 5.2 Reusable Workflow Cannot Be Found

Verify:

- Platform repository owner and name.
- Reusable workflow path.
- Referenced tag or commit SHA.
- Access permissions when the platform repository is private.

### 5.3 Scanner Reports a Finding

Determine whether the result is a genuine security issue or a false positive.

Do not disable the scanner simply to obtain