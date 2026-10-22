# Shared Scripts

## 1. Purpose

This directory contains small, reusable helper scripts that support the DevSecOps Platform's GitHub Actions workflows.

Scripts should be introduced only when they simplify repeated tasks or provide functionality that is difficult to express clearly using native GitHub Actions steps.

## 2. Design Principles

- Keep scripts small and focused.
- Prefer native GitHub Actions functionality when practical.
- Reuse scripts across workflows rather than duplicating logic.
- Use predictable inputs, outputs, and exit codes.
- Avoid unnecessary external dependencies.
- Document usage and limitations.
- Never embed credentials or sensitive values.
- Keep execution safe for untrusted pull request content.

## 3. Planned Script Categories

Examples of future helper scripts include:

| Category | Purpose |
|---|---|
| Repository validation | Validate required project files and configuration |
| Report processing | Produce concise, safe workflow summaries |
| Policy validation | Check configuration against platform standards |
| Version validation | Validate version and release conventions |
| Workflow utilities | Provide shared, narrowly scoped automation |

These are planned categories, not implemented scripts.

## 4. Script Requirements

Every script should:

- Have a clearly defined responsibility.
- Validate required inputs.
- Handle errors explicitly.
- Return a meaningful exit code.
- Avoid printing credentials or sensitive information.
- Avoid modifying application repositories unless explicitly required.
- Include safe test cases.
- Document any dependencies.

## 5. Exit Code Standards

Use conventional exit codes:

| Exit code | Meaning |
|---|---|
| `0` | Operation completed successfully |
| Non-zero | Validation, execution, or processing failed |

Scripts must not return success when a required security operation fails.

Where practical, error messages should distinguish invalid input, execution errors, and detected policy violations.

## 6. Security Requirements

- Never hardcode API keys, passwords, or access tokens.
- Avoid logging environment variables or sensitive files.
- Validate inputs before using them in shell commands.
- Avoid unsafe evaluation of dynamically constructed commands.
- Do not execute untrusted downloaded scripts.
- Use minimal filesystem and network access.
- Treat repository content as untrusted input.
- Do not write unredacted secret-scanning results to persistent artifacts.

## 7. Testing

Test scripts against:

- Valid inputs.
- Missing required inputs.
- Invalid configuration.
- Unexpected file contents.
- Expected error conditions.
- Sensitive-data handling.

Use synthetic test data for security-related tests.

## 8. Documentation Template

Each script should include documentation covering:

- Name and purpose.
- Required inputs.
- Optional inputs.
- Dependencies.
- Expected outputs.
- Exit codes.
- Security considerations.
- Usage example.
- Test instructions.

## 9. Maintenance

Scripts should be reviewed whenever their associated workflows change.

Remove scripts that are no longer used, and update documentation when behavior or interfaces change.

## 10. Conclusion

Shared scripts should reduce complexity rather than create another framework to maintain.

Keep the platform workflow-first, introducing helper scripts only when they provide a clear benefit.