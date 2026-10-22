# Shared Scripts

## 1. Purpose

This directory contains reusable helper scripts that support Action-Engine's GitHub Actions workflows.

Scripts are introduced only when they simplify repeated tasks, generate complex formatted artifacts (such as multi-tab Excel reports), or provide functionality difficult to express clearly in pure YAML.

---

## 2. Implemented Scripts

### 2.1 `generate_security_report.py`

**Purpose:**
Parses raw JSON scan reports from **Gitleaks** and **Trivy**, compiling them into a standardized, styled multi-tab Excel workbook (`.xlsx`) with an executive summary dashboard. It also dynamically writes scanner metric counts to GitHub Actions step outputs (`$GITHUB_OUTPUT`).

**Supported Sheets in Excel Report:**
1. **Executive Summary**:
   - Repository name, scan timestamp, workflow run URL, and interpretation guide.
   - Status cards for Gitleaks and Trivy.
   - High-level findings breakdown.
   - Trivy vulnerability severity breakdown (CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN).
2. **Gitleaks Findings**:
   - Columns: `Rule ID`, `Description`, `File`, `Start Line`, `Commit`, `Author`, `Date`.
3. **Trivy Findings**:
   - Columns: `Finding Type`, `ID`, `Package / Type`, `Installed Version`, `Fixed Version`, `Severity`, `Target File`, `Title`.
4. **Trivy Packages**:
   - Columns: `Package`, `Version`, `Type`, `Target File` (full SBOM / dependency inventory).

**Dependencies:**
- Python 3.8+
- `openpyxl` (`pip install openpyxl`)

**CLI Arguments:**

| Flag | Required | Description |
|---|---|---|
| `--gitleaks` | Yes | Path to Gitleaks JSON report (e.g. `reports/gitleaks-report.json`) |
| `--trivy` | Yes | Path to Trivy JSON report (e.g. `reports/trivy-report.json`) |
| `--output` | Yes | Path for output Excel file (e.g. `reports/security-report.xlsx`) |
| `--repository` | No | Target repository identifier (e.g. `owner/repo`) |
| `--gitleaks-status` | No | Reported status of Gitleaks (`success`, `failure`, etc.) |
| `--trivy-status` | No | Reported status of Trivy (`success`, `failure`, etc.) |
| `--workflow-url` | No | Direct URL to the GitHub Actions workflow run |
| `--github-output` | No | Path to `$GITHUB_OUTPUT` file for exporting environment variables |

**Exported GitHub Output Metrics:**
When `--github-output "$GITHUB_OUTPUT"` is provided, the script appends:
- `gitleaks_count`: Number of leaked secrets found.
- `trivy_count`: Number of vulnerabilities and misconfigurations found.
- `trivy_packages_count`: Number of analyzed dependencies/packages scanned.
- `total_count`: Combined sum of Gitleaks and Trivy findings.

**Usage Example:**
```bash
python3 -m venv .venv
.venv/bin/pip install openpyxl
.venv/bin/python scripts/generate_security_report.py \
  --gitleaks reports/gitleaks-report.json \
  --trivy reports/trivy-report.json \
  --output reports/security-report.xlsx \
  --repository "NIDO-MACHINERIES/nidoworkz-backend" \
  --gitleaks-status "failure" \
  --trivy-status "success" \
  --workflow-url "https://github.com/Tushar-CodeSpace/Action-Engine/actions/runs/12345" \
  --github-output "$GITHUB_OUTPUT"
```

---

## 3. Design Principles

- Keep scripts small, predictable, and focused.
- Prefer native GitHub Actions functionality when practical.
- Use predictable inputs, outputs, and exit codes.
- Never embed credentials or sensitive values.
- Keep execution safe for untrusted pull request content.

---

## 4. Exit Code Standards

| Exit code | Meaning |
|---|---|
| `0` | Operation completed successfully |
| Non-zero | Validation, execution, or processing failed |

Scripts must not return success when a required security operation fails.
