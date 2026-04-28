# Security Guide

This guide covers security considerations and best practices for using GitHub Commander safely.

## Token Security

### GitHub Personal Access Token

**What It Is:**
A token that authenticates you with GitHub API. It has the same access as your GitHub account.

**Risks:**
- If compromised, attacker can access all your repositories
- Can delete repositories
- Can modify code
- Can access private data

**Best Practices:**

1. **Never Share Your Token**
   - Don't paste in chat
   - Don't email it
   - Don't commit it to repositories
   - Don't store in plain text files

2. **Use Minimal Scopes**
   - Only grant necessary permissions
   - Review scopes regularly
   - Revoke unused tokens

3. **Short Expiration**
   - Set 30-90 day expiration
   - Rotate tokens regularly
   - Don't use permanent tokens

4. **Secure Storage**
   - Token stored in `~/.github-commander/config.json`
   - File permissions should be `600` (owner read/write only)
   - Consider using environment variables (advanced)

5. **Revocation**
   - Revoke immediately if compromised
   - Revoke when no longer needed
   - Revoke before changing machines

### Checking Token Permissions

1. Go to GitHub.com → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Review each token's:
   - Scopes
   - Expiration date
   - Last used date
   - Authorized applications

## Configuration Security

### Config File Location

**Path:** `~/.github-commander/config.json`

**Contains:**
- GitHub token
- Git configuration
- User preferences
- Repository settings

**Protection:**

1. **File Permissions**
   ```bash
   chmod 600 ~/.github-commander/config.json
   ```

2. **Backup Security**
   - Encrypt backups
   - Don't store in cloud without encryption
   - Keep offline copies secure

3. **Version Control**
   - Never commit config file
   - Add to `.gitignore`
   - Use template for shared settings

### Environment Variables (Advanced)

For enhanced security, use environment variables:

```bash
export GITHUB_TOKEN="your-token-here"
```

This requires code modification to read from environment.

## Repository Security

### Access Control

**Review Regularly:**
- Collaborators list
- Team memberships
- Organization permissions
- Third-party applications

**Least Privilege:**
- Grant minimum necessary access
- Use read-only when possible
- Remove access when no longer needed
- Review quarterly

### Branch Protection

**Enable for main branch:**
- Require pull request reviews
- Require status checks
- Restrict who can push
- Enable required reviewers

### Secrets Management

**Never Commit:**
- API keys
- Passwords
- Certificates
- Private keys
- Configuration secrets

**Use Instead:**
- GitHub Secrets (for Actions)
- Environment variables
- Secret management tools
- Encrypted secrets files
- `.env` files (in .gitignore)

## Network Security

### HTTPS

**Always Use HTTPS:**
- GitHub Commander uses HTTPS by default
- Don't disable certificate verification
- Use VPN on public networks
- Be cautious on public Wi-Fi

### Proxy Configuration

If using a proxy:
- Ensure proxy is trusted
- Use authenticated proxy
- Configure in system settings
- Verify proxy certificates

## Data Protection

### Sensitive Data in Repositories

**Scan for Secrets:**
- Use tools like `git-secrets`
- Scan history before pushing
- Review commits regularly
- Use pre-commit hooks

**If Secret Committed:**
1. Remove from current files
2. Rotate the secret immediately
3. Remove from git history
4. Consider repository rotation if severe

### Large Files

**Risks:**
- Can contain sensitive data
- Slow down operations
- Exceed GitHub limits

**Best Practices:**
- Use Git LFS for large files
- Scan before uploading
- Encrypt sensitive large files
- Use external storage when appropriate

## Authentication

### Two-Factor Authentication (2FA)

**Enable on GitHub:**
- Required for best security
- Protects against password theft
- Use authenticator app (not SMS)
- Backup recovery codes

**Impact on GitHub Commander:**
- Personal Access Tokens bypass 2FA
- No additional configuration needed
- Still recommended for overall security

### Session Management

**Best Practices:**
- Lock workstation when away
- Don't leave application unattended
- Log out when done (if available)
- Use screen timeout

## Application Security

### Updates

**Keep Updated:**
- Regularly check for updates
- Update dependencies
- Review changelog for security fixes
- Update promptly when security fixes released

### Verification

**Verify Downloads:**
- Download from official sources
- Verify checksums if available
- Check signatures
- Be cautious of modified versions

### Code Review

**If Modifying Code:**
- Review for security issues
- Don't hardcode secrets
- Validate inputs
- Handle errors securely
- Follow security best practices

## Incident Response

### If Token Compromised

**Immediate Actions:**
1. Revoke token on GitHub
2. Rotate all secrets that may have been accessed
3. Review repository access logs
4. Check for unauthorized changes
5. Enable 2FA if not already enabled
6. Review all connected applications

### If Repository Compromised

**Immediate Actions:**
1. Revoke collaborator access
2. Review all changes
3. Revert unauthorized commits
4. Rotate repository secrets
5. Check for added files
6. Review third-party integrations

### If Machine Compromised

**Immediate Actions:**
1. Revoke all GitHub tokens
2. Change all passwords
3. Review repository access
4. Scan for malware
5. Rebuild machine if necessary
6. Review other accounts

## Compliance

### Data Privacy

**Be Aware Of:**
- GDPR requirements
- Data retention policies
- User data handling
- Cross-border data transfer

### Auditing

**Regular Audits:**
- Review access logs
- Check token usage
- Review permissions
- Audit third-party access
- Document findings

## Security Checklist

### Daily
- [ ] Lock workstation when away
- [ ] Don't share credentials

### Weekly
- [ ] Review recent commits
- [ ] Check for unauthorized access
- [ ] Update application if available

### Monthly
- [ ] Review GitHub token scopes
- [ ] Review repository collaborators
- [ ] Check connected applications
- [ ] Review security settings

### Quarterly
- [ ] Rotate GitHub tokens
- [ ] Audit all repositories
- [ ] Review and update documentation
- [ ] Security training refresh

### Annually
- [ ] Full security audit
- [ ] Review all access controls
- [ ] Update security policies
- [ ] Incident response drill

## Resources

### Further Reading

- [GitHub Security Documentation](https://docs.github.com/en/security)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Git Security Best Practices](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

### Tools

- git-secrets - Prevent committing secrets
- truffleHog - Find secrets in git history
- GitGuardian - Monitor for secrets
- Snyk - Security scanning

### Reporting Security Issues

If you find a security vulnerability in GitHub Commander:
1. Don't publicize it
2. Report it privately
3. Allow time for fix
4. Follow responsible disclosure

## Disclaimer

This guide provides general security recommendations. Security is complex and evolving. Always:
- Stay informed about current threats
- Consult security professionals for critical systems
- Follow your organization's security policies
- Use professional judgment
