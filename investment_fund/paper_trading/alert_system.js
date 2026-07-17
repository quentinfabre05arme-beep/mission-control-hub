const fs = require('fs').promises;
const path = require('path');

class AlertSystem {
  constructor() {
    this.logFile = path.join(__dirname, 'trade_alerts.json');
  }

  async alertEntry(position) {
    const alert = {
      type: 'ENTRY',
      timestamp: new Date().toISOString(),
      symbol: position.symbol,
      side: position.side,
      size: position.size,
      entryPrice: position.entryPrice,
      stopLoss: position.stopLoss,
      target: position.target,
      tier: position.tier,
      rationale: position.rationale,
      riskReward: position.riskReward
    };

    await this.logAlert(alert);
    return this.formatAlert(alert);
  }

  async alertExit(position, exitPrice, pnl, reason) {
    const alert = {
      type: 'EXIT',
      timestamp: new Date().toISOString(),
      symbol: position.symbol,
      side: position.side,
      entryPrice: position.entryPrice,
      exitPrice: exitPrice,
      pnl: pnl,
      pnlPct: (pnl / (position.entryPrice * position.size)) * 100,
      reason: reason,
      duration: position.duration,
      tier: position.tier
    };

    await this.logAlert(alert);
    return this.formatAlert(alert);
  }

  async logAlert(alert) {
    let alerts = [];
    try {
      const data = await fs.readFile(this.logFile, 'utf8');
      alerts = JSON.parse(data);
    } catch {}
    alerts.push(alert);
    await fs.writeFile(this.logFile, JSON.stringify(alerts, null, 2));
  }

  formatAlert(alert) {
    if (alert.type === 'ENTRY') {
      return `🟢 ENTRY: ${alert.symbol}
Tier: ${alert.tier} | Size: €${alert.size.toFixed(0)}
Entry: $${alert.entryPrice} | Stop: $${alert.stopLoss} | Target: $${alert.target}
R/R: ${alert.riskReward}:1

Rationale: ${alert.rationale}`;
    } else {
      const emoji = alert.pnl > 0 ? '✅' : '❌';
      return `${emoji} EXIT: ${alert.symbol}
P&L: €${alert.pnl.toFixed(2)} (${alert.pnlPct.toFixed(1)}%)
Duration: ${alert.duration}
Reason: ${alert.reason}`;
    }
  }
}

module.exports = AlertSystem;