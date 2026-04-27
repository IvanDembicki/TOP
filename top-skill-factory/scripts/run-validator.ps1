param(
  [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
  [string]$ReportPath = ""
)

$scriptPath = Join-Path $PSScriptRoot 'validate_top_skill_factory.py'
if (-not $ReportPath) {
  $ReportPath = Join-Path $RepoRoot 'onboarding\schema-validation-report.md'
}

py -3 $scriptPath $RepoRoot --report $ReportPath
