# SCA Vulnerability Summary
Generated: Wed Dec 10 19:22:32 UTC 2025
Commit: [233fdc88f75edef1d0f2129ad4185e49e036f3ac](https://github.com/matveevaolga/course-project-matveevaolga/commit/233fdc88f75edef1d0f2129ad4185e49e036f3ac)

## Critical Findings

### pip-audit discovered vulnerabilities:



### Starlette Vulnerability Analysis

**Package:** starlette 0.38.6

**Vulnerabilities:**
1. **GHSA-f96h-pmfr-66vw** (High) - Open redirect in StaticFiles
2. **GHSA-2c2j-9gv5-cj73** (Medium) - Directory traversal in StaticFiles

**Our Risk Exposure:** LOW
- StaticFiles middleware not used
-  API-only service (no static files)
-  No user file upload functionality

### Additional Grype Findings

[]

## Action Plan

### Completed Actions
1.  Identified vulnerabilities via pip-audit
2.  Conducted risk assessment
3. Created waivers with justification
4.  Opened tracking issue

### Pending Actions
1.  Monitor FastAPI releases for starlette dependency update
2.  Schedule update to FastAPI >=0.115.0 (Q1 2025)
3.  Implement additional security monitoring

### Risk Acceptance Criteria
- Vulnerabilities not in attack surface
- Waivers expire 2025-03-31
- Regular reassessment scheduled
