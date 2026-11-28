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

## High-risk input boundaries

- For authorization, verify access on every request and resource operation, including tenant/object ownership and alternate API paths. Deny by default when no rule grants access; a client-side check is not a server-side control.
- For server-side URL fetching, constrain allowed schemes, hosts, ports, and redirect behavior to the business requirement. Revalidate the destination after resolution and redirects, and use network egress controls where available; a hostname allowlist alone may not constrain the actual connected address.
- For user-influenced file paths and archive extraction, prefer an identifier-to-known-file mapping over accepting arbitrary path fragments. If paths are unavoidable, normalize and enforce containment under the intended root while accounting for platform separators, encoding, and symlinks. Test traversal and encoded variants using isolated synthetic files.
- Review logs, exception responses, traces, and validation errors for secrets, credentials, personal data, and internal topology. Redaction should occur at the boundary and be tested against representative sensitive values.

## Evidence and remediation

- Identify the affected asset, actor, prerequisite, reachable path, and impact.
- Use synthetic data and authorized isolated tests; avoid destructive or external probing.
- Redact secrets and personal data from findings, logs, and examples.
- Distinguish scanner alerts from confirmed vulnerabilities; verify advisory applicability.
- Recommend proportionate corrections and tests that establish the protection boundary.
- Record residual risk and missing evidence without claiming comprehensive security assurance.
- State the threat boundary and tested behavior; a static checklist or scanner result is not a comprehensive security assessment.

## Official guidance

- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP Path Traversal Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Path_Traversal_Prevention_Cheat_Sheet.html)
