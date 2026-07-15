---
name: "fact-checker"
description: "Multi-source fact verification and cross-reference validation for research reliability"
---

# Fact Checker

Use this skill when making claims in research, briefings, or reports. Verifies information against multiple authoritative sources before stating as fact.

## Workflow

1. **Identify Claims** — Extract factual assertions from text
2. **Source Verification** — Check minimum 2 independent sources
3. **Confidence Scoring** — Rate: high/medium/low/unverified
4. **Flag Discrepancies** — Note conflicting information
5. **Annotate Output** — Mark verified claims with sources

## Source Hierarchy

1. **Primary:** Official data, direct measurements, raw APIs
2. **Secondary:** Established platforms (TradingView, CoinGecko)
3. **Tertiary:** Verified news (Reuters, Bloomberg)
4. **Quaternary:** Expert analysis with track record
5. **Avoid:** Unverified social media, anonymous sources

## Verification Patterns

### Financial Data
- Cross-check prices: CoinGecko + Yahoo Finance
- Verify with timestamp
- Flag if >1% discrepancy

### News Claims
- Minimum 2 independent sources
- Check publication dates
- Verify author credibility

### Statistics
- Seek original study/report
- Check methodology
- Look for peer review

## Output Format

```
[✓] BTC price $62,490 — Source: CoinGecko, Yahoo Finance (high confidence)
[?] "Study shows 40% efficacy" — Source: single outlet, needs verification
[✗] Claim contradicted by Reuters report — Flagged for review
```

## Configuration

```json
{
  "minSources": 2,
  "maxSourceAgeHours": 24,
  "confidenceThreshold": "medium"
}
```

## Safety

- Never state unverified claims as fact
- Always include confidence level
- Flag when sources conflict
- Log all fact-checks for audit

## Integration

Apply to:
- Daily briefings before sending
- Social media posts
- Research reports
- Dashboard data displays
