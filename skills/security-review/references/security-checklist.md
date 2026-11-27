# Defensive Security Review Checklist

## Review areas

| Area | Review focus |
| --- | --- |
| Authentication | Identity validation, session lifecycle, and credential handling. |
| Authorization | Resource ownership, tenant isolation, and privilege checks. |
| Untrusted input | Validation, safe parsing, parameterized operations, and output encoding. |
| Sensitive data | Storage, transport, logging, retention, and accidental disclosure. |
| Dependencies | Relevant advisory applicability, affected versions, and reachable behavior. |
| Configuration | Default privileges, exposed interfaces, and security-sensitive settings. |

## Evidence and remediation

- Identify the affected asset, actor, prerequisite, reachable path, and impact.
- Use synthetic data and authorized isolated tests; avoid destructive or external probing.
- Redact secrets and personal data from findings, logs, and examples.
- Distinguish scanner alerts from confirmed vulnerabilities; verify advisory applicability.
- Recommend proportionate corrections and tests that establish the protection boundary.
- Record residual risk and missing evidence without claiming comprehensive security assurance.

## Official guidance

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
