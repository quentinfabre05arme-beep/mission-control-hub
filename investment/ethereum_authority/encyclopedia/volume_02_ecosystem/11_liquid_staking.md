# Liquid Staking: Ethereum's Yield Revolution

## Overview
Liquid staking allows ETH holders to earn staking rewards while maintaining liquidity. This creates a capital-efficient yield layer that underpins DeFi.

## The Staking Landscape

### Total ETH Staked
- **Total**: ~33M ETH (~28% of supply)
- **Validator Count**: ~1M validators
- **Network Yield**: ~3.2% APR (variable based on total stake)

### Staking Options Comparison
| Method | Custody | Liquidity | Minimum | Yield | Complexity |
|--------|---------|-----------|---------|-------|------------|
| **Solo Staking** | Self | Illiquid | 32 ETH | ~3.2% | High |
| **Lido** | Protocol | Liquid | Any | ~3.0% | Low |
| **Coinbase** | Exchange | Locked | Any | ~3.0% | Low |
| **Rocket Pool** | Protocol | Liquid | 0.01 ETH | ~3.0% | Medium |
| **EigenLayer** | Protocol | Liquid | Any | 3% + restaking | High |

## Liquid Staking Tokens (LSTs)

### Major LSTs
| Token | Issuer | Market Cap | DeFi Integration |
|-------|--------|------------|------------------|
| **stETH** | Lido | ~$25B | Aave, Curve, MakerDAO |
| **cbETH** | Coinbase | ~$8B | Aave, Compound |
| **rETH** | Rocket Pool | ~$5B | Aave, Balancer |
| **wstETH** | Lido (wrapped) | ~$20B | All major DeFi |

### How They Work
1. **Deposit ETH** → Receive LST (e.g., stETH)
2. **LST accrues value** → Exchange rate to ETH increases
3. **Use LST in DeFi** → Collateral, liquidity, yield farming
4. **Redeem** → Burn LST, receive ETH + accumulated yield

## Restaking: The Next Evolution

### EigenLayer
- **Concept**: Re-use staked ETH to secure other protocols
- **Additional Yield**: 2-10% on top of base staking
- **Risk**: Slashable for protocol failures
- **Airdrops**: AVS tokens distributed to restakers

### Liquid Restaking Tokens (LRTs)
| Token | Protocol | Backing | Yield |
|-------|----------|---------|-------|
| **ezETH** | Renzo | stETH + EigenLayer | ~5-8% |
| **rsETH** | Kelp | Multiple LSTs + EigenLayer | ~5-8% |
| **weETH** | Ether.fi | ETH + EigenLayer + decentralization | ~5-8% |

## DeFi Integration

### Collateral Use Cases
1. **Aave**: Borrow against LSTs at 80% LTV
2. **MakerDAO**: Mint DAI with LST collateral
3. **Curve**: LST/ETH liquidity pools earn trading fees
4. **Pendle**: Split yield from principal, trade separately

### Yield Stacking Strategies
| Strategy | Base Yield | Additional | Total | Risk |
|----------|------------|------------|-------|------|
| Simple Staking | 3.2% | — | 3.2% | Low |
| Lido + Aave | 3.0% | 2% borrowing | 5.0% | Medium |
| Restaking | 3.2% | 3% restaking | 6.2% | Medium-High |
| LRT + Pendle | 5.0% | YT leverage | 8-15% | High |

## Institutional Perspective

### Why Institutions Care
1. **Yield**: 3%+ risk-free rate (in ETH terms)
2. **Liquidity**: LSTs trade like ETH
3. **Composability**: Integrate with DeFi strategies
4. **Tax efficiency**: No taxable event until sale

### Barriers
1. **Slashing risk**: Validator penalties
2. **Smart contract risk**: LST contract exploits
3. **Regulatory**: Unclear treatment in some jurisdictions
4. **Custody**: Qualified custody solutions limited

### Institutional Solutions
- **Coinbase Prime**: cbETH with institutional custody
- **Figment**: Institutional staking with insurance
- **Fireblocks**: Multi-sig custody for LSTs

## Risks

### Protocol Risks
- **Smart contract bugs**: Lido, Rocket Pool exploits
- **Governance capture**: Centralized decision making
- **Slashing events**: Major validator failures

### Market Risks
- **Depegging**: LST trading below ETH (Luna/UST scenario fear)
- **Liquidity crunch**: Unable to redeem for ETH
- **Regulatory**: Staking as securities classification

### Systemic Risks
- **Lido dominance**: 30%+ of all ETH staked with Lido
- **Restaking complexity**: Cascading failures across AVSs
- **Yield chasing**: Risk mismanagement for higher returns

## Key Metrics

### Staking Ratio
- **Current**: ~28% of ETH supply
- **Target**: 50%+ for network security
- **Saturation**: Yields decrease as more ETH stakes

### LST Market Share
- **Lido**: ~32% of staked ETH
- **Coinbase**: ~15%
- **Rocket Pool**: ~3%
- **Solo/Other**: ~50%

### DeFi TVL in LSTs
- **Total**: ~$15B across protocols
- **Growth**: 300%+ since Shanghai upgrade (April 2023)

## Investment Thesis

### Bullish
- **Institutional adoption**: ETF staking integration (if approved)
- **DeFi growth**: More use cases for LST collateral
- **Restaking maturation**: Sustainable additional yield
- **L2 expansion**: Cheaper LST transactions

### Bearish
- **Regulatory crackdown**: Staking as securities
- **Technology failure**: Major slashing event
- **Competition**: Other L1s offer better yields
- **Yield compression**: Too much ETH staked, rates drop

## Research Questions

1. Will ETF issuers enable staking? When?
2. Can Lido maintain dominance vs decentralized alternatives?
3. What's the sustainable yield for restaking long-term?
4. How do LSTs perform in severe market stress?
5. Tax treatment across jurisdictions?

## Sources
- Dune Analytics (staking dashboards)
- Lido, Rocket Pool, EigenLayer documentation
- DeFi Llama (LST TVL)
- Beaconcha.in (validator data)
- Academic: SSRN staking papers

## Last Updated
2026-07-23 — 28% staked, Lido dominant, restaking emerging
