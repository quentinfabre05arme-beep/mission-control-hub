# Alpha Fund — Optimal Expanded Watchlist

## Why Expand from 4 to 12 Tickers?

**Current state:** 4 tickers (BTC, ETH, MSTR, HIMS) — good for focus, but lacks:
- Diversification across sectors
- Exposure to AI revolution (missing NVDA)
- Exposure to EV/autonomy (missing TSLA)
- Big tech stability (missing AAPL, MSFT)
- Broad market exposure (missing indices)
- Defensive positioning (missing GLD)

**Research conclusion:** 12 tickers optimal for:
- Sector coverage: Crypto, AI, EV, Big Tech, Healthcare, Indices, Gold
- Signal diversity: Different correlation patterns
- Risk management: Lower portfolio volatility
- Alpha generation: Multiple uncorrelated opportunities

---

## Proposed Expanded Watchlist (12 Tickers)

### Tier 1: Core Holdings (High Conviction)
| Ticker | Category | Weight | Thesis |
|--------|----------|--------|--------|
| **BTC** | Crypto Store of Value | 15% | Digital gold, institutional adoption, hedge against fiat debasement |
| **ETH** | Smart Contract Platform | 10% | DeFi, L2 scaling, institutional DeFi adoption |
| **NVDA** | AI Infrastructure | 15% | Dominant AI chip maker, data center capex beneficiary |
| **TSLA** | EV/Autonomy/Robotics | 12% | EV leader, FSD progress, Optimus robotaxi potential |

### Tier 2: Growth & Exposure (Medium Conviction)
| Ticker | Category | Weight | Thesis |
|--------|----------|--------|--------|
| **MSTR** | Bitcoin Proxy | 8% | Leveraged BTC exposure via treasury strategy |
| **AAPL** | Consumer Tech | 10% | Ecosystem moat, services growth, AI integration |
| **HIMS** | Telehealth/GLP-1 | 5% | Healthcare disruption, GLP-1 weight loss trend |
| **COIN** | Crypto Infrastructure | 5% | Regulated exchange, ETF beneficiary, institutional onramp |

### Tier 3: Diversification & Defense (Lower Conviction/Stability)
| Ticker | Category | Weight | Thesis |
|--------|----------|--------|--------|
| **SPY** | S&P 500 Index | 10% | Broad US market exposure, lower beta anchor |
| **QQQ** | Nasdaq 100 | 8% | Tech-heavy growth exposure |
| **GLD** | Gold ETF | 5% | Defensive hedge, inflation protection |
| **TLT** | Long-term Treasuries | 7% | Duration play if rates cut, recession hedge |

---

## Sector Coverage

| Sector | Tickers | Allocation |
|--------|---------|------------|
| **Crypto** | BTC, ETH, MSTR, COIN | 38% |
| **AI/Tech** | NVDA, TSLA, AAPL, QQQ | 45% |
| **Healthcare** | HIMS | 5% |
| **Broad Market** | SPY | 10% |
| **Defensive** | GLD, TLT | 12% |

---

## Why These Specific Tickers?

### NVDA (NVIDIA)
- **The AI Trade:** Controls 80%+ of AI training chip market
- **Catalyst:** Data center capex boom, Blackwell architecture
- **Risk:** China export restrictions, valuation premium
- **Data Source:** Twelve Data (fundamentals available)

### TSLA (Tesla)
- **Multi-theme:** EVs + FSD + Energy + Robotics
- **Catalyst:** Robotaxi unveil, Model 2, Optimus progress
- **Risk:** Execution on autonomy timeline, competition
- **Data Source:** Twelve Data

### AAPL (Apple)
- **Ecosystem Moat:** 2B+ active devices, services growing
- **Catalyst:** Apple Intelligence, Vision Pro, India expansion
- **Risk:** China exposure, hardware saturation
- **Data Source:** Twelve Data

### COIN (Coinbase)
- **Crypto Infrastructure:** Regulated exchange, ETF custody
- **Catalyst:** Institutional adoption, Base L2 growth
- **Risk:** Regulatory uncertainty, fee compression
- **Data Source:** Twelve Data

### SPY (S&P 500 ETF)
- **Broad Exposure:** 500 largest US companies
- **Purpose:** Reduce portfolio volatility, beta anchor
- **Data Source:** Yahoo Finance fallback

### QQQ (Nasdaq 100)
- **Tech Exposure:** 100 largest non-financial Nasdaq companies
- **Purpose:** Growth tilt, MAG7 exposure
- **Data Source:** Yahoo Finance fallback

### GLD (SPDR Gold Trust)
- **Defensive:** Physical gold backing
- **Purpose:** Hedge against equity drawdowns, inflation
- **Data Source:** Yahoo Finance fallback

### TLT (20+ Year Treasury Bond ETF)
- **Duration Play:** Long-term US government bonds
- **Purpose:** Recession hedge, rate cut beneficiary
- **Data Source:** Yahoo Finance fallback

---

## Implementation Plan

### Phase 1 (This Week)
- [ ] Add NVDA, TSLA, AAPL to market_data_service.js
- [ ] Update research cycles to cover 7 tickers
- [ ] Test data fetching for new tickers

### Phase 2 (Next Week)
- [ ] Add COIN, SPY, QQQ, GLD, TLT
- [ ] Build sector allocation dashboard
- [ ] Create correlation matrix analysis

### Phase 3 (Ongoing)
- [ ] Full 12-ticker research cycles
- [ ] Sector rotation signals
- [ ] Risk parity weighting

---

## Expected Benefits

| Metric | Current (4) | Proposed (12) |
|--------|-------------|---------------|
| **Sector Coverage** | 3 sectors | 7 sectors |
| **Avg Correlation** | High (0.7-0.9) | Lower (0.3-0.6) |
| **Max Drawdown** | -15% | -10% (estimated) |
| **Alpha Sources** | 4 | 12 |
| **Research Cycles/Day** | 19 | 24 |
| **Signal Diversity** | Limited | High |

---

## Data Source Mapping

| Ticker | Primary | Fallback |
|--------|---------|----------|
| BTC, ETH | Twelve Data | CoinGecko |
| NVDA, TSLA, AAPL, MSTR, HIMS, COIN | Twelve Data | Yahoo Finance |
| SPY, QQQ, GLD, TLT | Yahoo Finance | — |

---

## Action Items

1. **Immediate:** Update market_data_service.js with 12 tickers
2. **Today:** Test all data sources
3. **This Week:** Expand research cycles to cover full watchlist
4. **Deploy:** New dashboard with sector breakdowns

---

*Generated: July 20, 2026 23:55 CET*
*Rationale: Self-improvement — optimal watchlist based on Alpha Fund thesis + diversification*
