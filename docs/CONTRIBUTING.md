# Contributing to DevSecOps Platform

## 1. Purpose

This document defines the contribution standards for developing, testing, reviewing, and releasing workflows in the DevSecOps Platform.

The objective is to maintain secure, reusable, reliable, and cost-efficient automation across multiple repositories.

## 2. Contribution Principles

All contributions should:

- Improve security, automation, reliability, or maintainability.
- Prefer reusable workflows over duplicated pipeline logic.
- Use free/open-source tools where practical.
- Follow least-privilege security practices.
- Include appropriate documentation.
- Be tested before production rollout.
- Avoid unnecessary infrastructure and configuration.
- Preserve compatibility with supported application repositories.

## 3. Contribution Workflow

### Step 1 — Create a Branch

Use a descriptive branch name.

Examples:

```text
feature/add-trivy-scan
fix/gitleaks-workflow
docs/update-onboarding
```

### Step 2 — Implement the Change

Keep the change focused and avoid modifying unrelated workflows.

Document:

- The problem being solved.
- The intended behavior.
- The repositories or technologies affected.
- Any new permissions or dependencies.
- Expected cost or execution-time implications.

### Step 3 — Validate the Change

Before opening a pull request:

- Validate YAML syntax.
- Review workflow triggers.
- Check permissions.
- Confirm tool versions.
- Test successful execution.
- Test failure behavior.
- Inspect logs and artifacts for sensitive data.
- Verify that scanner errors do not silently produce success.

Use fake test credentials when validating secret detection. Never include real credentials in test fixtures.

### Step 4 — Open a Pull Request

The pull request should include:

- Summary of the change.
- Reason for the change.
- Security implications.
- Testing performed.
- Compatibility considerations.
- Rollback approach.

### Step 5 — Review and Merge

Reviewers should verify:

- Workflow permissions are minimal.
- External actions are pinned to reviewed commit SHAs.
- No secrets or sensitive data have been committed.
- Failure conditions are correct.
- Documentation is updated.
- Existing workflows remain compatible.

Merge only after the required checks and approvals succeed.

## 4. Workflow Development Standards

### Naming Conventions

Use descriptive workflow filenames.

Examples:

```text
secret-scan-reusable.yml
dependency-scan-reusable.yml
sast-reusable.yml
container-scan-reusable.yml
build-reusable.yml
test-reusable.yml
release-reusable.yml
```

### Reusable