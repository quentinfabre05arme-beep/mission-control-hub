const EtherscanService = require('./etherscan_service');
const LidoService = require('./lido_service');
const EigenLayerService = require('./eigenlayer_service');
const CoinGeckoProService = require('./coingecko_pro');

class UnifiedDataService {
  constructor() {
    this.etherscan = new EtherscanService();
    this.lido = new LidoService();
    this.eigenlayer = new EigenLayerService();
    this.coingecko = new CoinGeckoProService();
  }

  // Aggregate all Ethereum data for daily research
  async getDailySnapshot() {
    console.log('Fetching unified Ethereum data snapshot...\n');
    
    const snapshot = {
      timestamp: new Date().toISOString(),
      sources: {}
    };

    // CoinGecko (Price - most reliable)
    try {
      const [ethPrice, lstPrices, global] = await Promise.all([
        this.coingecko.getEthPrice(),
        this.coingecko.getLstPrices(),
        this.coingecko.getGlobalData()
      ]);
      
      snapshot.sources.coingecko = {
        ethPrice,
        lstPrices,
        global
      };
      
      snapshot.price = ethPrice.price;
      snapshot.change24h = ethPrice.change24h;
      snapshot.marketCap = ethPrice.marketCap;
      snapshot.ethDominance = global.ethDominance;
    } catch (e) {
      console.error('CoinGecko error:', e.message);
      snapshot.sources.coingecko = { error: e.message };
    }

    // Etherscan (On-chain metrics)
    try {
      const [supply, gas, beacon] = await Promise.all([
        this.etherscan.getEthSupply(),
        this.etherscan.getGasOracle(),
        this.etherscan.getBeaconDeposits()
      ]);
      
      snapshot.sources.etherscan = {
        supply,
        gas,
        beacon
      };
      
      const totalSupply = parseInt(supply.totalSupply) / 1e18;
      snapshot.totalSupply = totalSupply;
      snapshot.ethStaked = beacon.ethStaked;
      snapshot.stakingRatio = ((beacon.ethStaked / totalSupply) * 100).toFixed(2);
      snapshot.gasPrice = {
        safe: gas.safeGasPrice,
        standard: gas.proposeGasPrice,
        fast: gas.fastGasPrice
      };
    } catch (e) {
      console.error('Etherscan error:', e.message);
      snapshot.sources.etherscan = { error: e.message };
    }

    // Lido (Staking data)
    try {
      const [apr, supply] = await Promise.all([
        this.lido.getStethAPR(),
        this.lido.getStethSupply()
      ]);
      
      snapshot.sources.lido = {
        apr,
        supply
      };
      
      snapshot.stakingYield = (apr.apr * 100).toFixed(2);
      snapshot.stethSupply = parseInt(supply.totalSupply) / 1e18;
    } catch (e) {
      console.error('Lido error:', e.message);
      snapshot.sources.lido = { error: e.message };
      // Fallback
      snapshot.stakingYield = 3.2;
    }

    // EigenLayer (Restaking)
    try {
      const yields = await this.eigenlayer.getRestakingYields();
      
      snapshot.sources.eigenlayer = {
        yields
      };
      
      snapshot.restakingYield = {
        conservative: yields.totalYieldEstimate.conservative,
        moderate: yields.totalYieldEstimate.moderate,
        aggressive: yields.totalYieldEstimate.aggressive
      };
    } catch (e) {
      console.error('EigenLayer error:', e.message);
      snapshot.sources.eigenlayer = { error: e.message };
    }

    // Calculate X insight
    snapshot.xInsight = this.generateXInsight(snapshot);

    return snapshot;
  }

  generateXInsight(snapshot) {
    const insights = [];
    
    // Price-based insight
    if (snapshot.change24h > 5) {
      insights.push(`ETH +${snapshot.change24h.toFixed(1)}% — momentum building`);
    } else if (snapshot.change24h < -5) {
      insights.push(`ETH ${snapshot.change24h.toFixed(1)}% — buying opportunity or trend shift?`);
    }
    
    // Staking insight
    if (snapshot.stakingRatio) {
      insights.push(`${snapshot.stakingRatio}% of ETH staked — ${snapshot.stakingYield}% yield available`);
    }
    
    // Restaking insight
    if (snapshot.restakingYield) {
      insights.push(`Restaking adds ${snapshot.restakingYield.conservative}-${snapshot.restakingYield.aggressive}% on top of base staking`);
    }
    
    // Default insight
    if (insights.length === 0) {
      insights.push(`ETH at $${snapshot.price?.toLocaleString() || 'N/A'} — ${snapshot.ethDominance?.toFixed(1) || 'N/A'}% market dominance`);
    }
    
    return insights[0];
  }

  async saveSnapshot() {
    const snapshot = await this.getDailySnapshot();
    const date = new Date().toISOString().split('T')[0];
    const fs = require('fs');
    const path = require('path');
    
    const outputPath = path.join(__dirname, '../../data/snapshots');
    fs.mkdirSync(outputPath, { recursive: true });
    
    const filePath = path.join(outputPath, `${date}_snapshot.json`);
    fs.writeFileSync(filePath, JSON.stringify(snapshot, null, 2));
    
    console.log(`\n✅ Snapshot saved to: ${filePath}`);
    return { snapshot, filePath };
  }
}

// CLI execution
if (require.main === module) {
  const service = new UnifiedDataService();
  
  (async () => {
    try {
      const { snapshot } = await service.saveSnapshot();
      
      console.log('\n=== UNIFIED ETHEREUM SNAPSHOT ===');
      console.log(`Timestamp: ${snapshot.timestamp}`);
      console.log(`\nPRICE DATA:`);
      console.log(`  ETH: $${snapshot.price?.toLocaleString() || 'N/A'}`);
      console.log(`  24h Change: ${snapshot.change24h?.toFixed(2) || 'N/A'}%`);
      console.log(`  Market Cap: $${(snapshot.marketCap / 1e9).toFixed(2) || 'N/A'}B`);
      
      console.log(`\nSTAKING DATA:`);
      console.log(`  Staking Ratio: ${snapshot.stakingRatio || 'N/A'}%`);
      console.log(`  ETH Staked: ${snapshot.ethStaked?.toLocaleString() || 'N/A'}`);
      console.log(`  Staking Yield: ${snapshot.stakingYield || 'N/A'}%`);
      
      console.log(`\nRESTAKING:`);
      if (snapshot.restakingYield) {
        console.log(`  Conservative: ${snapshot.restakingYield.conservative}%`);
        console.log(`  Moderate: ${snapshot.restakingYield.moderate}%`);
        console.log(`  Aggressive: ${snapshot.restakingYield.aggressive}%`);
      }
      
      console.log(`\nGAS PRICES:`);
      if (snapshot.gasPrice) {
        console.log(`  Safe: ${snapshot.gasPrice.safe} Gwei`);
        console.log(`  Standard: ${snapshot.gasPrice.standard} Gwei`);
        console.log(`  Fast: ${snapshot.gasPrice.fast} Gwei`);
      }
      
      console.log(`\n📝 X INSIGHT:`);
      console.log(`  "${snapshot.xInsight}"`);
      
      console.log(`\n=== DATA SOURCES ===`);
      Object.keys(snapshot.sources).forEach(source => {
        const status = snapshot.sources[source].error ? '❌' : '✅';
        console.log(`  ${status} ${source}`);
      });
      
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = UnifiedDataService;
