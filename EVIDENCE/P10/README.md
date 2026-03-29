# P10 - SAST & Secrets Scan Evidence

## Directory Purpose
This directory contains evidence from Static Application Security Testing (SAST) and secrets scanning performed as part of P10 requirements.

## File Structure

EVIDENCE/P10/ :
semgrep.sarif # SAST scan results (SARIF format)
semgrep-custom.sarif # Custom rules scan results
gitleaks.json # Secrets detection results (JSON)
sast_summary.md # Human-readable summary of findings
README.md # This documentation file

## Tools Used
1. **Semgrep** - Static Application Security Testing
   - Version: Latest (docker)
   - Config: `p/ci` profile + custom rules
   - Output: SARIF format for tool interoperability

2. **Gitleaks** - Secrets detection
   - Version: Latest (docker)
   - Config: `security/.gitleaks.toml` with allowlist
   - Output: JSON format for automated processing

## Scan Frequency
- **Automatic:** On every push to security-relevant files
- **Manual:** Via workflow_dispatch
- **Pre-commit:** Optional local scanning (configured in .pre-commit-config.yaml)

## Integration Points
1. **CI/CD Pipeline:** Automated scanning in GitHub Actions
2. **Code Review:** Findings referenced in pull requests
3. **Security Dashboard:** SARIF integration potential
4. **Developer Workflow:** Pre-commit hooks for early detection

## Usage in Security Process
1. **Immediate:** Review Critical/High severity findings
2. **Short-term:** Address confirmed security issues
3. **Long-term:** Use findings for security training and process improvement

## Retention Policy
- Evidence files are stored as GitHub Actions artifacts (90 days)
- Summary reports are referenced in documentation
- Critical findings are tracked in issue management system

