#!/usr/bin/env python3
"""Reusable Excel report generator for Gitleaks, Trivy, Semgrep, and SonarQube."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def parse_gitleaks(data):
    if not isinstance(data, list):
        return []
    return [[
        item.get("RuleID", ""), item.get("Description", ""),
        item.get("File", ""), item.get("StartLine", ""),
        item.get("Commit", ""), item.get("Author", ""),
        item.get("Date", ""),
    ] for item in data if isinstance(item, dict)]


def parse_trivy(data):
    rows = []
    packages = []
    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "UNKNOWN": 0
    }
    
    if not isinstance(data, dict):
        return rows, counts, packages 

    for result in data.get("Results", []) or []:
        if not isinstance(result, dict):
            continue
        
        target = result.get("Target", "")
        
        for package in result.get("Packages", []) or []:
            if not isinstance(package, dict):
                continue
            
            packages.append([
                package.get("Name",  ""),
                package.get("Version", ""),
                result.get("Type", ""),
                target,
            ])
        
        for vuln in result.get("Vulnerabilities", []) or []:
            if not isinstance(vuln, dict):
                continue
            severity = str(vuln.get("Severity") or "UNKNOWN").upper()
            counts[severity] = counts.get(severity, 0) + 1
            rows.append([
                "Vulnerability", vuln.get("VulnerabilityID", ""),
                vuln.get("PkgName", ""), vuln.get("InstalledVersion", ""),
                vuln.get("FixedVersion", ""), severity, target,
                vuln.get("Title", ""),
            ])
        for issue in result.get("Misconfigurations", []) or []:
            if not isinstance(issue, dict):
                continue
            severity = str(issue.get("Severity") or "UNKNOWN").upper()
            counts[severity] = counts.get(severity, 0) + 1
            rows.append([
                "Misconfiguration", issue.get("ID", ""), issue.get("Type", ""),
                "", "", severity, target, issue.get("Title", ""),
            ])
    return rows, counts, packages


def parse_semgrep(data):
    if not isinstance(data, dict):
        return []
    rows = []
    for item in data.get("results", []) or []:
        if not isinstance(item, dict):
            continue
        check_id = item.get("check_id", "")
        path = item.get("path", "")
        start_line = item.get("start", {}).get("line", "")
        extra = item.get("extra", {})
        message = extra.get("message", "")
        severity = str(extra.get("severity", "WARNING")).upper()
        metadata = extra.get("metadata", {})
        cwe = metadata.get("cwe", [])
        cwe_str = ", ".join(cwe) if isinstance(cwe, list) else str(cwe)
        owasp = metadata.get("owasp", [])
        owasp_str = ", ".join(owasp) if isinstance(owasp, list) else str(owasp)
        rows.append([
            check_id, severity, path, start_line, cwe_str, owasp_str, message
        ])
    return rows


def parse_sonarqube(data):
    if not isinstance(data, dict):
        return [], {
            "quality_gate": "N/A",
            "bugs": "N/A",
            "vulnerabilities": "N/A",
            "code_smells": "N/A",
            "security_hotspots": "N/A",
            "coverage": "N/A",
            "dashboard_url": "",
        }
    metrics = {
        "quality_gate": str(data.get("qualityGate", "N/A")),
        "bugs": str(data.get("bugs", 0)),
        "vulnerabilities": str(data.get("vulnerabilities", 0)),
        "code_smells": str(data.get("codeSmells", 0)),
        "security_hotspots": str(data.get("securityHotspots", 0)),
        "coverage": str(data.get("coverage", "N/A")),
        "dashboard_url": str(data.get("dashboardUrl", "")),
    }
    rows = []
    for it in data.get("issues", []) or []:
        if not isinstance(it, dict):
            continue
        rows.append([
            it.get("key", ""),
            it.get("type", ""),
            it.get("severity", ""),
            it.get("rule", ""),
            it.get("component", "").split(":")[-1],
            it.get("line", ""),
            it.get("effort", ""),
            it.get("status", ""),
            it.get("message", ""),
        ])
    return rows, metrics


def add_sheet(wb, title, headers, rows):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for row in rows:
        ws.append(row)
    ws.freeze_panes = "A2"
    if ws.max_row > 1:
        ws.auto_filter.ref = ws.dimensions
    return ws


def style_workbook(wb):
    header_fill = PatternFill("solid", fgColor="17365D")
    header_font = Font(bold=True, color="FFFFFF")
    thin_gray = Side(style="thin", color="D9E2F3")

    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[1].height = 28

        for row in ws.iter_rows():
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                cell.border = Border(bottom=thin_gray)

        for col in ws.columns:
            letter = get_column_letter(col[0].column)
            width = max((len(str(c.value or "")) for c in col), default=0) + 2
            ws.column_dimensions[letter].width = min(max(width, 14), 55)

    summary = wb["Executive Summary"]
    summary.column_dimensions["A"].width = 30
    summary.column_dimensions["B"].width = 85
    summary.conditional_formatting.add(
        "B14:B18",
        CellIsRule(
            operator="greaterThan",
            formula=["0"],
            fill=PatternFill("solid", fgColor="FCE4D6"),
            font=Font(bold=True, color="9C0006"),
        ),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gitleaks", default="reports/gitleaks-report.json")
    parser.add_argument("--trivy", default="reports/trivy-report.json")
    parser.add_argument("--semgrep", default="reports/semgrep-report.json")
    parser.add_argument("--sonarqube-report", default="reports/sonarqube-report.json")
    parser.add_argument("--output", default="reports/security-report.xlsx")
    parser.add_argument("--repository", default="unknown/unknown")
    parser.add_argument("--gitleaks-status", default="unknown")
    parser.add_argument("--trivy-status", default="unknown")
    parser.add_argument("--semgrep-status", default="unknown")
    parser.add_argument("--sonarqube-status", default="unknown")
    parser.add_argument("--workflow-url", default="")
    parser.add_argument("--github-output", default="")
    args = parser.parse_args()

    gitleaks = load_json(args.gitleaks, [])
    trivy = load_json(args.trivy, {})
    semgrep = load_json(args.semgrep, {})
    sonarqube = load_json(args.sonarqube_report, {})
    if not isinstance(gitleaks, list):
        gitleaks = []

    gitleaks_rows = parse_gitleaks(gitleaks)
    trivy_rows, severity_counts, package_rows = parse_trivy(trivy)
    semgrep_rows = parse_semgrep(semgrep)
    sonarqube_rows, sonarqube_metrics = parse_sonarqube(sonarqube)
    total = len(gitleaks_rows) + len(trivy_rows) + len(semgrep_rows)

    wb = Workbook()
    summary = wb.active
    summary.title = "Executive Summary"
    rows = [
        ["SECURITY SCAN REPORT"],
        ["Repository", args.repository],
        ["Generated (UTC)", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")],
        ["Gitleaks status", args.gitleaks_status],
        ["Gitleaks findings", len(gitleaks_rows)],
        ["Trivy status", args.trivy_status],
        ["Trivy findings", len(trivy_rows)],
        ["Trivy packages analyzed", len(package_rows)],
        ["Semgrep SAST status", args.semgrep_status],
        ["Semgrep SAST findings", len(semgrep_rows)],
        ["SonarQube status", args.sonarqube_status],
        ["SonarQube quality gate", sonarqube_metrics["quality_gate"]],
        ["SonarQube bugs", sonarqube_metrics["bugs"]],
        ["SonarQube vulnerabilities", sonarqube_metrics["vulnerabilities"]],
        ["SonarQube code smells", sonarqube_metrics["code_smells"]],
        ["SonarQube security hotspots", sonarqube_metrics["security_hotspots"]],
        ["SonarQube dashboard", sonarqube_metrics["dashboard_url"]],
        ["Total security findings", total],
        ["", ""],
        ["TRIVY SEVERITY BREAKDOWN", "Count"],
        ["CRITICAL", severity_counts.get("CRITICAL", 0)],
        ["HIGH", severity_counts.get("HIGH", 0)],
        ["MEDIUM", severity_counts.get("MEDIUM", 0)],
        ["LOW", severity_counts.get("LOW", 0)],
        ["UNKNOWN", severity_counts.get("UNKNOWN", 0)],
        ["", ""],
        ["Interpretation", "A failed scanner can indicate findings or a scanner error. Review workflow logs."],
        ["Workflow run", args.workflow_url],
    ]
    for row in rows:
        summary.append(row)
    summary.freeze_panes = "A2"

    add_sheet(wb, "Gitleaks Findings",
              ["Rule ID", "Description", "File", "Start Line", "Commit", "Author", "Date"],
              gitleaks_rows)
    add_sheet(wb, "Trivy Findings",
              ["Finding Type", "ID", "Package / Type", "Installed Version",
               "Fixed Version", "Severity", "Target File", "Title"],
              trivy_rows)
    add_sheet(
        wb,
        "Trivy Packages",
        ["Package", "Version", "Type", "Target File"],
        package_rows,
    )
    add_sheet(
        wb,
        "Semgrep SAST Findings",
        ["Rule ID", "Severity", "File", "Line", "CWE", "OWASP", "Message"],
        semgrep_rows,
    )
    add_sheet(
        wb,
        "SonarQube Issues",
        ["Issue Key", "Type", "Severity", "Rule", "Component", "Line", "Effort", "Status", "Message"],
        sonarqube_rows,
    )
    style_workbook(wb)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)

    print(f"Excel report: {output}")
    print(f"Gitleaks findings: {len(gitleaks_rows)}")
    print(f"Trivy findings: {len(trivy_rows)}")
    print(f"Trivy packages analyzed: {len(package_rows)}")
    print(f"Semgrep SAST findings: {len(semgrep_rows)}")
    print(f"SonarQube quality gate: {sonarqube_metrics['quality_gate']}")
    print(f"SonarQube bugs: {sonarqube_metrics['bugs']}")
    print(f"SonarQube vulnerabilities: {sonarqube_metrics['vulnerabilities']}")
    print(f"SonarQube code smells: {sonarqube_metrics['code_smells']}")
    print(f"Total findings: {total}")

    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as f:
            f.write(f"gitleaks_count={len(gitleaks_rows)}\n")
            f.write(f"trivy_count={len(trivy_rows)}\n")
            f.write(f"trivy_packages_count={len(package_rows)}\n")
            f.write(f"semgrep_count={len(semgrep_rows)}\n")
            f.write(f"sonarqube_gate={sonarqube_metrics['quality_gate']}\n")
            f.write(f"sonarqube_bugs={sonarqube_metrics['bugs']}\n")
            f.write(f"sonarqube_vulnerabilities={sonarqube_metrics['vulnerabilities']}\n")
            f.write(f"sonarqube_code_smells={sonarqube_metrics['code_smells']}\n")
            f.write(f"sonarqube_hotspots={sonarqube_metrics['security_hotspots']}\n")
            f.write(f"sonarqube_dashboard_url={sonarqube_metrics['dashboard_url']}\n")
            f.write(f"total_count={total}\n")


if __name__ == "__main__":
    main()
