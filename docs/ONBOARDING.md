# Repository Onboarding Guide

## 1. Purpose

This guide explains how to integrate an application repository with the centralized DevSecOps Platform.

The goal is to enable consistent security checks across multiple repositories with minimal configuration and without requiring a dedicated Jenkins or SonarQube server.

## 2. Prerequisites

Before onboarding a repository, ensure that:

- The application repository is hosted on GitHub.
- GitHub Actions is enabled.
- The central `Action-Engine` platform repository exists.
- The reusable security workflow has been reviewed and committed.
- The application repository is permitted to access the reusable workflow.
- The person configuring the integration has the required repository permissions.

## 3. Integration Architecture

```text id="x7k5vf"
Application Repository
        |
        | Caller Workflow
        |
        v
DevSecOps Platform
        |
        | Reusable Workflow
        |
        v
GitHub-Hosted Runner
        |
        v
Security Scan
        |
        v
Pass / Fail Result
```

## 4. Step 1 — Configure Platform Access

If the platform repository is private, configure GitHub's Actions access settings so authorized application repositories can use its reusable workflows.

Do not make the platform public solely to simplify integration without first reviewing the security implications.

## 5. Step 2 — Add the Caller Workflow

Inside the application repository, create:

`.github/workflows/security.yml`

Add the following workflow:

```yaml
name: Security Checks

on:
  pull_request:
  push:
    branches:
      - main
      - master
  workflow_dispatch:

permissions:
  contents: read

jobs:
  secret-scan:
    uses: ORGANIZATION/Action-Engine/.github/workflows/secret-scan-reusable.yml@VERSION
```

Replace:

- `ORGANIZATION` with the GitHub organization or username that owns the platform.
- `VERSION` with a reviewed release tag or full commit SHA.

The referenced workflow must exist at that exact path and revision.

## 6. Step 3 — Validate the Integration

Test the integration in a pilot repository before enabling it across production repositories.

1. Create a temporary test branch.
2. Use a deliberately fake test string that Gitleaks recognizes.
3. Open a pull request.
4. Confirm that the security workflow starts.
5. Verify that the scan fails when the test finding is detected.
6. Check that logs and artifacts do not expose real credentials.
7. Remove the test string and confirm the workflow passes.

Never use a real API key, access token, password, or production credential for testing.

## 7. Step 4 — Enable Merge Protection

Once the workflow behaves correctly:

1. Open the application repository's Settings.
2. Navigate to Rules → Rulesets or the applicable branch protection settings.
3. Configure a required status check for the secret-scanning job.
4. Save the rules.
5. Open a test pull request.
6. Verify that a failed required check prevents merging.

Use the actual check name reported by GitHub Actions. Test the configuration before applying it to critical production branches.

## 8. Step 5 — Onboard Additional Repositories

Repeat the integration process for each repository.

Maintain a simple inventory:

| Repository | Secret Scan | Required Check | Owner |
|---|---|---|---|
| Project A | Pending | Pending | Team A |
| Project B | Pending | Pending | Team B |
| Project C | Pending | Pending | Team C |

Replace these examples with actual repositories and ownership details.

## 9. Configuration Standards

Keep application-side configuration minimal.

- Use reusable workflows for shared logic.
- Use workflow inputs for project-specific options.
- Use repository variables for non-sensitive configuration.
- Use GitHub Actions secrets only when credentials are necessary.
- Pin workflow references to approved versions.
- Avoid duplicating scanners and security policies across application repositories.

## 10. Troubleshooting

### Reusable workflow not found

Check the organization or username, repository name, workflow path, and referenced version.

### Access denied

Verify the private repository's Actions access policy and the permissions of the user configuring the integration.

### Workflow does not start

Check the workflow triggers, YAML syntax, branch names, and whether GitHub Actions is enabled.

### Required status check cannot be selected

Run the workflow first and verify the exact check name reported by GitHub.

### Scan fails

Determine whether the failure is caused by a detected secret, an invalid workflow configuration, or a scanner execution error.

Do not suppress a genuine finding to force a successful result.

## 11. Rollback Procedure

If a platform workflow update disrupts an application repository:

1. Identify the last known-good workflow revision.
2. Update the caller to reference that revision.
3. Re-run the workflow.
4. Verify the expected security behavior.
5. Investigate and correct the platform change before attempting another rollout.

Avoid removing required security checks without an approved temporary exception.

## 12. Onboarding Checklist

- [ ] Platform access configured.
- [ ] Caller workflow added.
- [ ] Workflow reference pinned to an approved version.
- [ ] Secret scanning tested.
- [ ] Logs reviewed for sensitive information.
- [ ] Required check enabled.
- [ ] Repository owner assigned.
- [ ] Onboarding inventory updated.

## 13. Conclusion

The onboarding process allows repositories to adopt centralized security automation without copying complete pipeline implementations or maintaining their own CI servers.

New repositories should use the approved reusable workflow version and follow the same validation and enforcement process.