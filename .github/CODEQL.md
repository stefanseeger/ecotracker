# CodeQL Security Analysis

This project uses GitHub CodeQL for automated security and code quality analysis.

## What is CodeQL?

CodeQL is a semantic analysis engine that helps find security vulnerabilities, bugs, and code quality issues in your code. It provides:

- **Security Analysis**: Detects potential security vulnerabilities (SQL injection, path traversal, etc.)
- **Code Quality Analysis**: Identifies code smells and quality improvements
- **Custom Queries**: Support for writing custom analyses specific to your codebase
- **Continuous Monitoring**: Runs on every push and pull request

## Workflow Configuration

### File: `.github/workflows/codeql.yml`

The CodeQL workflow runs:
- On every push to `main` and `develop` branches
- On every pull request to `main` and `develop` branches
- Daily at 2 AM UTC (scheduled scan)

### Language Analysis

Currently analyzing:
- **Python** - Home Assistant integration code in `custom_components/ecotracker/`

### Results

CodeQL results are available in the **Security** tab of your repository:
- GitHub repository → Security → Code scanning

## Custom Configuration

The `.github/codeql-config.yml` file specifies:

```yaml
paths:
  - custom_components/ecotracker  # Analyze integration code

paths-ignore:
  - tests/                         # Skip test files
  - .devcontainer/                 # Skip dev container
  - docs/                          # Skip documentation
```

## Interpreting Results

CodeQL findings include:

1. **Rule**: Name of the security rule or quality check
2. **Severity**: Critical, High, Medium, Low, Note
3. **Location**: File and line number
4. **Recommendation**: Best practices to fix the issue

## Integration with Pull Requests

When CodeQL findings are detected:
- PR checks will show analysis results
- Status checks help enforce security standards
- All findings must be reviewed or dismissed before merge

## Running CodeQL Locally

To run CodeQL analysis locally (requires CodeQL CLI installation):

```bash
# Initialize database
codeql database create --language=python ecotracker-db

# Run analysis
codeql database analyze ecotracker-db --format=sarif-latest --output=results.sarif

# View results
codeql database analyze ecotracker-db github/codeql-queries/python --format=text
```

## Next Steps

1. Monitor the **Security** tab for findings
2. Address high and critical severity issues
3. Evaluate medium/low issues for improvement
4. Keep CodeQL database updated with latest queries

## Resources

- [GitHub CodeQL Documentation](https://codeql.github.com/docs/)
- [CodeQL for Python](https://codeql.github.com/docs/codeql-language-guides/codeql-for-python/)
- [Security best practices for Home Assistant](https://github.com/home-assistant/core/blob/dev/SECURITY.md)
