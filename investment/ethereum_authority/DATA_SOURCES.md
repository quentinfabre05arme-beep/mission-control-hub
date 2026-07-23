# Ethereum Authority — Data Sources & Verification

## Primary Data Sources

### Market Data
| Source | Use | Frequency | Limitations |
|--------|-----|-----------|-------------|
| **Twelve Data** | Price, volume, technicals | Real-time | 8 req/min free tier |
| **CoinGecko** | Crypto prices, market cap | 5 min delay | Rate limits |
| **Yahoo Finance** | Stock prices (MSTR, COIN, etc.) | 15 min delay | 429 errors common |
| **DeFi Llama** | DeFi TVL, protocol metrics | ~1 hour delay | API stability |

### Institutional Flows
| Source | Use | Frequency | Verification |
|--------|-----|-----------|--------------|
| **Farside Investors** | ETF flows | Daily, end-of-day | Primary source, cross-ref with Bloomberg |
| **Bloomberg Terminal** | Institutional data | Real-time | Gold standard, but requires access |
| **SEC EDGAR** | Filings, disclosures | Daily | Official, lagged |
| **Coinbase Prime** | On-chain custody flows | Real-time | On-chain verification possible |

### On-Chain
| Source | Use | Frequency | Notes |
|--------|-----|-----------|-------|
| **Dune Analytics** | Custom dashboards | Hourly | Community queries, verify SQL |
| **Glassnode** | Network metrics | Hourly | Paid tiers for real-time |
| **Nansen** | Smart money tracking | Daily | Premium required for full data |
| **Etherscan** | Direct on-chain | Real-time | Raw data, manual interpretation |

### DeFi/Ecosystem
| Source | Use | Frequency | Limitations |
|--------|-----|-----------|-------------|
| **DeFi Llama** | Protocol TVL | Hourly | Aggregation delays |
| **Token Terminal** | Revenue metrics | Daily | Data accuracy varies by protocol |
| **Lido/AAVE/Uniswap** | Direct protocol data | Real-time | Each has own API/UI |
| **EigenLayer** | Restaking data | Daily | New, limited history |

## Verification Process

### Cross-Reference Rule
**Never rely on single source for critical data.**

| Data Point | Primary | Secondary | Tertiary |
|------------|---------|-----------|----------|
| ETH Price | Twelve Data | CoinGecko | Yahoo Finance |
| ETF Flows | Farside | Bloomberg | On-chain |
| Staking Yield | Lido | Token Terminal | Calculated |
| DeFi TVL | DeFi Llama | Dune | Protocol direct |

### Confidence Levels
| Level | Criteria | Action |
|-------|----------|--------|
| **High** | 3+ sources align, official data | Use in posts |
| **Medium** | 2 sources align, some discrepancy | Flag uncertainty |
| **Low** | Single source, unverified | Don't use / research further |
| **Stale** | Data > 24h old | Refresh before posting |

## Data Refresh Schedule

| Data Type | Refresh Frequency | Auto-Update |
|-----------|-------------------|-------------|
| Prices | Every 5 min | ✅ Yes |
| ETF Flows | Daily (after market close) | ⚠️ Manual trigger |
| On-Chain | Hourly | ✅ Yes |
| DeFi Metrics | Every 2 hours | ✅ Yes |
| News/Sentiment | Continuous | ⚠️ Manual curation |

## Known Limitations

### Current Issues
1. **Twelve Data rate limits**: 8/min, causes SPY/QQQ/GLD/TLT failures
   - **Workaround**: Cache fallback, stagger requests
   - **Impact**: Core crypto assets (BTC/ETH/MSTR) unaffected

2. **Farside data delay**: End-of-day aggregation
   - **Workaround**: Use prior day flows for morning posts
   - **Impact**: Intraday flow changes not captured

3. **Yahoo Finance blocking**: 429 "Too Many Requests"
   - **Workaround**: Fallback to cache, reduce request frequency
   - **Impact**: Stock correlations less current

4. **DeFi data accuracy**: Self-reported by protocols
   - **Workaround**: Cross-protocol comparison, outlier detection
   - **Impact**: TVL figures may have 5-10% variance

## Quality Assurance

### Pre-Post Checklist
- [ ] Price data &lt; 1 hour old
- [ ] Flow data verified against 2+ sources
- [ ] On-chain metrics cross-checked
- [ ] No major discrepancies (&gt;5%) between sources
- [ ] Breaking news fact-checked

### When Data Conflicts
1. **Check timestamps**: Which is most recent?
2. **Check methodology**: Are they measuring same thing?
3. **Check source credibility**: Official > aggregators > social
4. **Flag uncertainty**: "Preliminary data suggests..."
5. **Research further**: Don't post if unresolved

## Data Source Hierarchy

### Most Reliable (Tier 1)
- SEC filings (official)
- Protocol direct APIs (Lido, Aave)
- Bloomberg Terminal (institutional)
- On-chain direct (Etherscan)

### Reliable with Caveats (Tier 2)
- Farside Investors (aggregated, but verified)
- DeFi Llama (aggregated, community maintained)
- Glassnode (paid tiers more reliable)
- CoinGecko (widely used, some delays)

### Use with Caution (Tier 3)
- Social media sentiment (LunarCrush, etc.)
- News aggregators (The Block, CoinDesk)
- Community dashboards (Dune — verify SQL)
- Predictive models (own calculations)

## Transparency Commitments

### In Posts
- **Date-stamp data**: "As of July 23, 2026..."
- **Source attribution**: "Per Farside Investors..."
- **Confidence qualifiers**: "Preliminary data suggests..."
- **Correction policy**: Update if wrong, explain why

### In Research
- **Save raw data**: Preserve source snapshots
- **Document methodology**: How calculations made
- **Track errors**: Log discrepancies, learn patterns
- **Update encyclopedia**: Refresh stale chapters

## Red Flags (Don't Post)

- Single unverified source claiming major event
- Data > 48 hours old for time-sensitive metrics
- Price discrepancies &gt; 2% between sources
- Breaking news without secondary confirmation
- "Anonymous sources" for institutional flows

## Improvement Priorities

### Immediate
- [ ] Add Bloomberg API (institutional data)
- [ ] Implement real-time websocket feeds
- [ ] Build data quality alerts (stale data detection)

### Medium-term
- [ ] On-chain data pipeline (direct node access)
- [ ] Institutional contact network (verify flows)
- [ ] Academic research integration ( SSRN papers)

### Long-term
- [ ] Proprietary data collection
- [ ] Predictive models (flow forecasting)
- [ ] Real-time sentiment analysis

---

**Last Updated**: 2026-07-23
**Next Review**: Weekly (Sundays with deep dive)
