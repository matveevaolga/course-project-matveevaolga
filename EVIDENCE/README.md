# Evidence Directory Structure

This directory contains security evidence for the project.

## P09 - SBOM & SCA Evidence

### Structure
- `P09/sbom-*.json` - Software Bill of Materials (CycloneDX format)
- `P09/sca-report-*.json` - Software Composition Analysis reports
- `P09/sca_summary.md` - Human-readable vulnerability summary
- `P09/policy_report.md` - Policy compliance report

### Usage
- SBOM files are timestamped and linked to specific commits
- Latest reports are symlinked as `*-latest.json`
- Reports are uploaded as GitHub Actions artifacts
- Used for compliance and vulnerability management

### Integration
- Generated automatically on code changes
- Part of CI/CD pipeline
- Referenced in security reviews
