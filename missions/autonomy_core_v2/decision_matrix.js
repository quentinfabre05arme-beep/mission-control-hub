/**
 * Auto-Pilot Decision Matrix v2.0
 * Makes autonomous decisions based on weighted scoring
 */
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'logs');
const DECISION_HISTORY = path.join(__dirname, 'data', 'decisions.json');

class DecisionMatrix {
  constructor() {
    this.ensureDirectories();
    this.decisions = this.loadDecisions();
    
    // Decision criteria weights
    this.weights = {
      roi: 0.25,
      risk: 0.20,
      urgency: 0.20,
      effort: 0.15,
      alignment: 0.10,
      confidence: 0.10
    };
  }

  ensureDirectories() {
    [LOG_DIR, path.join(__dirname, 'data')].forEach(dir => {
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    });
  }

  loadDecisions() {
    try {
      if (fs.existsSync(DECISION_HISTORY)) {
        return JSON.parse(fs.readFileSync(DECISION_HISTORY, 'utf8'));
      }
    } catch (e) {
      console.log('Creating new decision history');
    }
    return { decisions: [], stats: { total: 0, approved: 0, rejected: 0 } };
  }

  saveDecisions() {
    fs.writeFileSync(DECISION_HISTORY, JSON.stringify(this.decisions, null, 2));
  }

  /**
   * Evaluate a decision request
   * @param {Object} request - The decision to evaluate
   * @param {string} request.type - Type of decision (trade, investment, business, etc)
   * @param {number} request.roi - Expected ROI percentage
   * @param {number} request.risk - Risk level (0-10)
   * @param {number} request.urgency - Urgency (0-10)
   * @param {number} request.effort - Effort required (0-10)
   * @param {number} request.confidence - Confidence in data (0-1)
   * @param {Object} request.metadata - Additional context
   */
  evaluate(request) {
    console.log(`🤖 Evaluating decision: ${request.type}`);
    
    // Normalize inputs to 0-1 scale
    const normalized = {
      roi: Math.min(request.roi / 100, 1),
      risk: 1 - (request.risk / 10), // Invert: lower risk = higher score
      urgency: request.urgency / 10,
      effort: 1 - (request.effort / 10), // Invert: lower effort = higher score
      alignment: request.alignment || 0.7,
      confidence: request.confidence || 0.5
    };

    // Calculate weighted score
    let score = 0;
    Object.keys(this.weights).forEach(key => {
      score += normalized[key] * this.weights[key];
    });

    // Decision thresholds
    const thresholds = {
      auto_approve: 0.75,    // No human review needed
      conditional: 0.50,     // Proceed with logging
      review_required: 0.30, // Human review recommended
      auto_reject: 0.20     // Auto-reject
    };

    let decision;
    let requiresApproval = false;

    if (score >= thresholds.auto_approve) {
      decision = 'AUTO_APPROVE';
      requiresApproval = false;
    } else if (score >= thresholds.conditional) {
      decision = 'CONDITIONAL_APPROVE';
      requiresApproval = false;
    } else if (score >= thresholds.review_required) {
      decision = 'REVIEW_REQUIRED';
      requiresApproval = true;
    } else {
      decision = 'AUTO_REJECT';
      requiresApproval = false;
    }

    // Build result
    const result = {
      id: `dec_${Date.now()}`,
      timestamp: new Date().toISOString(),
      type: request.type,
      score: parseFloat(score.toFixed(3)),
      decision,
      requires_approval: requiresApproval,
      normalized_scores: normalized,
      raw_inputs: {
        roi: request.roi,
        risk: request.risk,
        urgency: request.urgency,
        effort: request.effort,
        confidence: request.confidence
      },
      metadata: request.metadata || {},
      executed: false,
      execution_time: null
    };

    // Log the decision
    this.logDecision(result);
    this.logToMemory(result);
    
    return result;
  }

  /**
   * Execute an approved decision
   */
  executeDecision(decisionId, executor) {
    const decision = this.decisions.decisions.find(d => d.id === decisionId);
    
    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    if (decision.decision === 'AUTO_REJECT') {
      throw new Error('Cannot execute rejected decision');
    }

    if (decision.requires_approval && !decision.approved_by) {
      throw new Error('Decision requires human approval');
    }

    console.log(`🚀 Executing decision: ${decisionId}`);
    
    try {
      const result = executor(decision);
      decision.executed = true;
      decision.execution_time = new Date().toISOString();
      decision.execution_result = result;
      
      this.saveDecisions();
      this.logExecution(decision, result);
      
      return { success: true, result };
    } catch (error) {
      decision.execution_error = error.message;
      this.saveDecisions();
      
      return { success: false, error: error.message };
    }
  }

  /**
   * Approve a decision requiring human review
   */
  approveDecision(decisionId, approver = 'human') {
    const decision = this.decisions.decisions.find(d => d.id === decisionId);
    
    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    decision.approved_by = approver;
    decision.approval_time = new Date().toISOString();
    decision.requires_approval = false;
    
    this.decisions.stats.approved++;
    this.saveDecisions();
    
    console.log(`✅ Decision ${decisionId} approved by ${approver}`);
    return decision;
  }

  /**
   * Reject a decision
   */
  rejectDecision(decisionId, reason = '') {
    const decision = this.decisions.decisions.find(d => d.id === decisionId);
    
    if (!decision) {
      throw new Error(`Decision ${decisionId} not found`);
    }

    decision.decision = 'REJECTED';
    decision.rejection_reason = reason;
    decision.rejection_time = new Date().toISOString();
    
    this.decisions.stats.rejected++;
    this.saveDecisions();
    
    console.log(`❌ Decision ${decisionId} rejected: ${reason}`);
    return decision;
  }

  /**
   * Get decision statistics
   */
  getStats() {
    const all = this.decisions.decisions;
    return {
      total: all.length,
      approved: all.filter(d => d.decision === 'AUTO_APPROVE').length,
      conditional: all.filter(d => d.decision === 'CONDITIONAL_APPROVE').length,
      review: all.filter(d => d.decision === 'REVIEW_REQUIRED').length,
      rejected: all.filter(d => d.decision === 'AUTO_REJECT' || d.decision === 'REJECTED').length,
      executed: all.filter(d => d.executed).length,
      pending: all.filter(d => !d.executed && d.decision !== 'AUTO_REJECT' && d.decision !== 'REJECTED').length,
      average_score: all.length > 0 
        ? (all.reduce((a, b) => a + b.score, 0) / all.length).toFixed(3)
        : 0
    };
  }

  /**
   * Get recent decisions
   */
  getRecent(limit = 10) {
    return this.decisions.decisions
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, limit);
  }

  logDecision(result) {
    this.decisions.decisions.push(result);
    this.decisions.stats.total++;
    this.saveDecisions();
    
    const logFile = path.join(LOG_DIR, 'decisions.log');
    const entry = `[${result.timestamp}] ${result.id}: ${result.type} | Score: ${result.score} | Decision: ${result.decision}\n`;
    fs.appendFileSync(logFile, entry);
  }

  logExecution(decision, result) {
    const logFile = path.join(LOG_DIR, 'executions.log');
    const entry = `[${decision.execution_time}] ${decision.id}: EXECUTED | Result: ${JSON.stringify(result)}\n`;
    fs.appendFileSync(logFile, entry);
  }

  logToMemory(result) {
    const MEMORY_FILE = path.join(process.cwd(), 'MEMORY.md');
    const entry = `
## Auto-Pilot Decision
**ID:** ${result.id}
**Time:** ${result.timestamp}
**Type:** ${result.type}
**Score:** ${result.score}
**Decision:** ${result.decision}
**Requires Approval:** ${result.requires_approval}
**Scores:** ROI=${(result.normalized_scores.roi * 100).toFixed(0)}% | Risk=${(result.normalized_scores.risk * 10).toFixed(1)}/10 | Urgency=${(result.normalized_scores.urgency * 10).toFixed(1)}/10

---
`;

    try {
      if (fs.existsSync(MEMORY_FILE)) {
        fs.appendFileSync(MEMORY_FILE, entry);
      }
    } catch (e) {
      // Silent fail
    }
  }

  /**
   * Adjust weights based on performance
   */
  adjustWeights(performance) {
    // Adjust weights based on past decision outcomes
    if (performance.roi > 0.2) {
      this.weights.roi += 0.02;
    }
    if (performance.risk < 0.3) {
      this.weights.risk += 0.02;
    }
    
    // Normalize to ensure sum = 1
    const total = Object.values(this.weights).reduce((a, b) => a + b, 0);
    Object.keys(this.weights).forEach(key => {
      this.weights[key] = parseFloat((this.weights[key] / total).toFixed(3));
    });
    
    console.log('⚖️ Weights adjusted:', this.weights);
  }
}

module.exports = DecisionMatrix;

// CLI usage
if (require.main === module) {
  const matrix = new DecisionMatrix();
  
  // Example: Evaluate a trade decision
  const trade = matrix.evaluate({
    type: 'crypto_trade',
    roi: 25,      // Expected 25% return
    risk: 4,      // Risk level 4/10
    urgency: 7,   // Urgency 7/10
    effort: 2,    // Low effort
    confidence: 0.8,
    metadata: { asset: 'BTC', strategy: 'dip_buy' }
  });
  
  console.log('\n📊 Decision Result:');
  console.log(JSON.stringify(trade, null, 2));
  console.log('\n📈 Stats:', matrix.getStats());
}
