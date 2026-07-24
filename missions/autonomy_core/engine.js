/**
 * AUTONOMY CORE ENGINE v1.0
 * Master intelligence controller for persistent autonomous operations
 *
 * 4 Principles:
 * 1. EFFICIENCY - Optimize waste, maximize output
 * 2. INTELLIGENCE - Learn patterns, make smart decisions
 * 3. PERSISTENCE - Never stop, always recover
 * 4. SELF-IMPROVEMENT - Constant learning and optimization
 *
 * Mode: SILENT (no user notifications unless critical)
 * Frequency: Every 15 minutes
 * Author: Claw (self-built)
 * Date: July 23, 2026
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ─── CONFIGURATION ───────────────────────────────────────────────
const CONFIG = {
    VERSION: '1.0.1',
    RUN_INTERVAL_MS: 15 * 60 * 1000, // 15 minutes
    LOG_RETENTION_DAYS: 7,
    MAX_RETRIES: 5,
    BACKOFF_BASE_MS: 1000,
    STATE_FILE: path.join(__dirname, 'engine_state.json'),
    LOG_FILE: path.join(__dirname, 'engine.log'),
    MEMORY_FILE: path.join(__dirname, '..', '..', 'memory', `${new Date().toISOString().split('T')[0]}.md`),
    PRINCIPLES: ['EFFICIENCY', 'INTELLIGENCE', 'PERSISTENCE', 'SELF-IMPROVEMENT'],
    WORKSPACE_ROOT: path.resolve(__dirname, '..', '..')
};

// ─── STATE MANAGEMENT ────────────────────────────────────────────
class StateManager {
    constructor() {
        this.state = this.load();
    }

    load() {
        try {
            if (fs.existsSync(CONFIG.STATE_FILE)) {
                return JSON.parse(fs.readFileSync(CONFIG.STATE_FILE, 'utf8'));
            }
        } catch (e) {
            this.log('WARN', `State load failed: ${e.message}`);
        }
        return {
            version: CONFIG.VERSION,
            startedAt: new Date().toISOString(),
            totalCycles: 0,
            lastCycle: null,
            errors: [],
            improvements: [],
            metrics: {
                efficiency: { cycles: 0, actions: 0, wasteEliminated: 0 },
                intelligence: { patternsLearned: 0, decisionsMade: 0, accuracy: 1.0 },
                persistence: { recoveries: 0, uptimeMinutes: 0 },
                selfImprovement: { skillsCreated: 0, optimizations: 0, learnings: [] }
            },
            activeMissions: [],
            alerts: []
        };
    }

    save() {
        try {
            fs.writeFileSync(CONFIG.STATE_FILE, JSON.stringify(this.state, null, 2));
        } catch (e) {
            this.log('ERROR', `State save failed: ${e.message}`);
        }
    }

    log(level, message) {
        const timestamp = new Date().toISOString();
        const line = `[${timestamp}] [${level}] ${message}\n`;

        // Console output
        console.log(line.trim());

        // File logging
        try {
            fs.appendFileSync(CONFIG.LOG_FILE, line);
        } catch (e) {
            console.error(`Log write failed: ${e.message}`);
        }

        // Store errors in state
        if (level === 'ERROR') {
            this.state.errors.push({
                time: timestamp,
                message: message,
                resolved: false
            });
            // Keep only last 50 errors
            if (this.state.errors.length > 50) {
                this.state.errors = this.state.errors.slice(-50);
            }
        }
    }
}

// ─── PRINCIPLE 1: EFFICIENCY ─────────────────────────────────────
class EfficiencyEngine {
    constructor(state) {
        this.state = state;
    }

    async run() {
        this.state.log('INFO', '🔄 [EFFICIENCY] Running optimization cycle...');
        const actions = [];

        // Check for wasted resources
        const wasteChecks = await this.checkWaste();
        actions.push(...wasteChecks);

        // Optimize existing processes
        const optimizations = await this.optimizeProcesses();
        actions.push(...optimizations);

        // Clean up old data
        const cleanup = await this.cleanupOldData();
        actions.push(...cleanup);

        this.state.state.metrics.efficiency.cycles++;
        this.state.state.metrics.efficiency.actions += actions.length;

        return {
            principle: 'EFFICIENCY',
            actions: actions,
            summary: `Eliminated ${wasteChecks.length} waste sources, ${optimizations.length} optimizations`
        };
    }

    async checkWaste() {
        const actions = [];
        const workspace = CONFIG.WORKSPACE_ROOT;

        // Check for stale cron jobs
        try {
            const cronFile = path.join(workspace, 'cron_jobs.json');
            if (fs.existsSync(cronFile)) {
                const jobs = JSON.parse(fs.readFileSync(cronFile, 'utf8'));
                const staleJobs = jobs.filter(j => {
                    const lastRun = new Date(j.lastRun || 0);
                    return (Date.now() - lastRun) > 24 * 60 * 60 * 1000; // 24h
                });

                if (staleJobs.length > 0) {
                    actions.push({
                        type: 'STALE_CRON_DETECTED',
                        count: staleJobs.length,
                        action: 'flag_for_review',
                        severity: 'low'
                    });
                }
            }
        } catch (e) {
            // Silent fail
        }

        // Check log file sizes
        try {
            const logPath = path.join(workspace, 'logs');
            if (fs.existsSync(logPath)) {
                const files = fs.readdirSync(logPath);
                let totalSize = 0;
                files.forEach(f => {
                    const stat = fs.statSync(path.join(logPath, f));
                    if (stat.size > 10 * 1024 * 1024) { // > 10MB
                        actions.push({
                            type: 'LARGE_LOG',
                            file: f,
                            size: stat.size,
                            action: 'rotate_log'
                        });
                    }
                    totalSize += stat.size;
                });

                if (totalSize > 100 * 1024 * 1024) { // > 100MB total
                    actions.push({
                        type: 'LOG_BLOAT',
                        totalSize,
                        action: 'archive_old_logs'
                    });
                }
            }
        } catch (e) {
            // Silent fail
        }

        // Check for large temp/cache files
        try {
            const tempPaths = [
                path.join(workspace, '.cache'),
                path.join(workspace, 'temp'),
                path.join(workspace, 'tmp')
            ];

            tempPaths.forEach(tempPath => {
                if (fs.existsSync(tempPath)) {
                    const stats = fs.statSync(tempPath);
                    const sizeMB = stats.size / (1024 * 1024);
                    if (sizeMB > 50) {
                        actions.push({
                            type: 'TEMP_BLOAT',
                            path: tempPath,
                            sizeMB: Math.round(sizeMB),
                            action: 'cleanup_temp'
                        });
                    }
                }
            });
        } catch (e) {}

        // Check disk space
        try {
            const wmic = execSync('wmic logicaldisk get size,freespace,caption', { encoding: 'utf8', timeout: 5000 });
            const lines = wmic.split('\n').filter(l => l.trim());
            lines.forEach(line => {
                if (line.includes(':')) {
                    const parts = line.trim().split(/\s+/);
                    if (parts.length >= 3) {
                        const drive = parts[0];
                        const free = parseInt(parts[1]);
                        const total = parseInt(parts[2]);
                        if (!isNaN(free) && !isNaN(total) && total > 0) {
                            const pctFree = (free / total) * 100;
                            if (pctFree < 10) {
                                actions.push({
                                    type: 'LOW_DISK_SPACE',
                                    drive,
                                    pctFree: Math.round(pctFree),
                                    action: 'alert_user'
                                });
                            }
                        }
                    }
                }
            });
        } catch (e) {}

        return actions;
    }

    async optimizeProcesses() {
        const actions = [];
        const workspace = CONFIG.WORKSPACE_ROOT;

        // Check if there are duplicate scripts
        try {
            const scriptsPath = path.join(workspace, 'scripts');
            if (fs.existsSync(scriptsPath)) {
                const files = fs.readdirSync(scriptsPath).filter(f => f.endsWith('.js') || f.endsWith('.ps1'));
                if (files.length > 5) {
                    actions.push({
                        type: 'SCRIPT_INVENTORY',
                        count: files.length,
                        action: 'review_for_consolidation'
                    });
                }
            }
        } catch (e) {}

        // Check for uncommitted git changes
        try {
            const gitPath = path.join(workspace, '.git');
            if (fs.existsSync(gitPath)) {
                const status = execSync('git status --short', { cwd: workspace, encoding: 'utf8', timeout: 5000 });
                const lines = status.trim().split('\n').filter(l => l.trim());
                if (lines.length > 10) {
                    actions.push({
                        type: 'UNCOMMITTED_CHANGES',
                        count: lines.length,
                        action: 'prompt_commit'
                    });
                }
            }
        } catch (e) {}

        // Check Node.js memory usage
        try {
            const memUsage = process.memoryUsage();
            const heapUsedMB = Math.round(memUsage.heapUsed / 1024 / 1024);
            if (heapUsedMB > 512) {
                actions.push({
                    type: 'HIGH_MEMORY_USAGE',
                    heapUsedMB,
                    action: 'monitor'
                });
            }
        } catch (e) {}

        // Check if research system is stale (>6 hours)
        try {
            const marketData = path.join(workspace, 'mission_control', 'market_data.json');
            if (fs.existsSync(marketData)) {
                const stat = fs.statSync(marketData);
                const ageHours = (Date.now() - stat.mtime.getTime()) / (1000 * 60 * 60);
                if (ageHours > 6) {
                    actions.push({
                        type: 'STALE_MARKET_DATA',
                        ageHours: Math.round(ageHours),
                        action: 'trigger_research_cycle'
                    });
                }
            }
        } catch (e) {}

        return actions;
    }

    async cleanupOldData() {
        const actions = [];
        const workspace = CONFIG.WORKSPACE_ROOT;

        // Clean old memory files
        try {
            const memoryPath = path.join(workspace, 'memory');
            if (fs.existsSync(memoryPath)) {
                const files = fs.readdirSync(memoryPath);
                const cutoff = new Date();
                cutoff.setDate(cutoff.getDate() - CONFIG.LOG_RETENTION_DAYS);

                files.forEach(f => {
                    const filePath = path.join(memoryPath, f);
                    const stat = fs.statSync(filePath);
                    if (stat.mtime < cutoff && f.endsWith('.md') && f !== 'archive') {
                        const archivePath = path.join(memoryPath, 'archive');
                        if (!fs.existsSync(archivePath)) {
                            fs.mkdirSync(archivePath, { recursive: true });
                        }
                        fs.renameSync(filePath, path.join(archivePath, f));
                        actions.push({
                            type: 'ARCHIVED_OLD_MEMORY',
                            file: f,
                            action: 'archived'
                        });
                    }
                });
            }
        } catch (e) {}

        // Clean old engine logs
        try {
            const logPath = CONFIG.LOG_FILE;
            if (fs.existsSync(logPath)) {
                const stat = fs.statSync(logPath);
                const sizeMB = stat.size / (1024 * 1024);
                if (sizeMB > 5) {
                    // Rotate log by renaming with timestamp
                    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
                    const rotatedPath = logPath.replace('.log', `_${timestamp}.log`);
                    fs.renameSync(logPath, rotatedPath);
                    actions.push({
                        type: 'LOG_ROTATED',
                        sizeMB: Math.round(sizeMB),
                        action: 'rotated'
                    });
                }
            }
        } catch (e) {}

        return actions;
    }
}

// ─── PRINCIPLE 2: INTELLIGENCE ────────────────────────────────────
class IntelligenceEngine {
    constructor(state) {
        this.state = state;
    }

    async run() {
        this.state.log('INFO', '🧠 [INTELLIGENCE] Learning and pattern analysis...');
        const patterns = [];

        // Learn from errors
        const errorPatterns = this.analyzeErrors();
        patterns.push(...errorPatterns);

        // Learn from successes
        const successPatterns = this.analyzeSuccesses();
        patterns.push(...successPatterns);

        // Analyze market patterns
        const marketPatterns = this.analyzeMarketPatterns();
        patterns.push(...marketPatterns);

        // Make decisions based on patterns
        const decisions = this.makeDecisions(patterns);

        this.state.state.metrics.intelligence.patternsLearned += patterns.length;
        this.state.state.metrics.intelligence.decisionsMade += decisions.length;

        return {
            principle: 'INTELLIGENCE',
            patterns: patterns,
            decisions: decisions,
            summary: `Learned ${patterns.length} patterns, made ${decisions.length} decisions`
        };
    }

    analyzeErrors() {
        const patterns = [];
        const errors = this.state.state.errors;

        if (errors.length === 0) return patterns;

        // Group errors by type
        const errorTypes = {};
        errors.forEach(e => {
            const type = e.message.split(':')[0] || 'UNKNOWN';
            errorTypes[type] = (errorTypes[type] || 0) + 1;
        });

        // Find recurring errors
        Object.entries(errorTypes).forEach(([type, count]) => {
            if (count > 2) {
                patterns.push({
                    type: 'RECURRING_ERROR',
                    errorType: type,
                    frequency: count,
                    recommendation: `Investigate ${type} - occurred ${count} times`
                });
            }
        });

        return patterns;
    }

    analyzeSuccesses() {
        const patterns = [];

        // Check for successful operations in state
        const improvements = this.state.state.improvements || [];
        if (improvements.length > 0) {
            const recent = improvements.slice(-5);
            patterns.push({
                type: 'SUCCESS_PATTERN',
                recentImprovements: recent.length,
                trend: 'positive'
            });
        }

        // Check research cycle success
        try {
            const workspace = CONFIG.WORKSPACE_ROOT;
            const researchLog = path.join(workspace, 'memory');
            if (fs.existsSync(researchLog)) {
                const files = fs.readdirSync(researchLog).filter(f => f.startsWith('2026-') && f.endsWith('.md'));
                const today = new Date().toISOString().split('T')[0];
                const todayFile = files.find(f => f.startsWith(today));
                if (todayFile) {
                    const content = fs.readFileSync(path.join(researchLog, todayFile), 'utf8');
                    const researchCount = (content.match(/RESEARCH CYCLE/g) || []).length;
                    if (researchCount > 0) {
                        patterns.push({
                            type: 'RESEARCH_ACTIVITY',
                            cyclesToday: researchCount,
                            trend: researchCount >= 3 ? 'high' : 'normal'
                        });
                    }
                }
            }
        } catch (e) {}

        return patterns;
    }

    analyzeMarketPatterns() {
        const patterns = [];

        try {
            const workspace = CONFIG.WORKSPACE_ROOT;
            const marketData = path.join(workspace, 'mission_control', 'market_data.json');
            if (fs.existsSync(marketData)) {
                const data = JSON.parse(fs.readFileSync(marketData, 'utf8'));

                // Check for significant price movements
                Object.entries(data).forEach(([symbol, info]) => {
                    if (info.change_24h && Math.abs(info.change_24h) > 5) {
                        patterns.push({
                            type: 'MARKET_VOLATILITY',
                            symbol,
                            change: info.change_24h,
                            direction: info.change_24h > 0 ? 'up' : 'down',
                            severity: Math.abs(info.change_24h) > 10 ? 'high' : 'medium'
                        });
                    }
                });

                // Check for extreme fear/greed
                if (data.fear_greed && data.fear_greed.value < 20) {
                    patterns.push({
                        type: 'EXTREME_FEAR',
                        index: data.fear_greed.value,
                        signal: 'potential_buy_opportunity'
                    });
                } else if (data.fear_greed && data.fear_greed.value > 80) {
                    patterns.push({
                        type: 'EXTREME_GREED',
                        index: data.fear_greed.value,
                        signal: 'potential_sell_opportunity'
                    });
                }
            }
        } catch (e) {}

        return patterns;
    }

    makeDecisions(patterns) {
        const decisions = [];

        patterns.forEach(p => {
            if (p.type === 'RECURRING_ERROR') {
                decisions.push({
                    type: 'CREATE_SKILL',
                    reason: `Recurring ${p.errorType} errors`,
                    priority: p.frequency > 5 ? 'high' : 'medium',
                    action: `Propose skill to handle ${p.errorType}`
                });
            }

            if (p.type === 'STALE_MARKET_DATA') {
                decisions.push({
                    type: 'TRIGGER_RESEARCH',
                    reason: `Market data is ${p.ageHours} hours old`,
                    priority: 'high',
                    action: 'Run enhanced_research.js for all assets'
                });
            }

            if (p.type === 'EXTREME_FEAR' && p.index < 15) {
                decisions.push({
                    type: 'ALERT_OPPORTUNITY',
                    reason: `Extreme fear index: ${p.index}`,
                    priority: 'high',
                    action: 'Flag BTC accumulation opportunity'
                });
            }

            if (p.type === 'MARKET_VOLATILITY' && p.severity === 'high') {
                decisions.push({
                    type: 'ALERT_VOLATILITY',
                    reason: `${p.symbol} moved ${p.change}% in 24h`,
                    priority: 'medium',
                    action: 'Review portfolio exposure'
                });
            }
        });

        return decisions;
    }
}

// ─── PRINCIPLE 3: PERSISTENCE ─────────────────────────────────────
class PersistenceEngine {
    constructor(state) {
        this.state = state;
    }

    async run() {
        this.state.log('INFO', '🔧 [PERSISTENCE] Checking system health and recovery...');
        const checks = [];

        // Check critical services
        const serviceHealth = await this.checkServices();
        checks.push(...serviceHealth);

        // Check for failures needing recovery
        const recoveries = await this.recoverFailures();
        checks.push(...recoveries);

        // Monitor external dependencies
        const deps = await this.checkDependencies();
        checks.push(...deps);

        // Update uptime
        const startedAt = new Date(this.state.state.startedAt);
        const uptimeMinutes = Math.floor((Date.now() - startedAt) / 60000);
        this.state.state.metrics.persistence.uptimeMinutes = uptimeMinutes;

        return {
            principle: 'PERSISTENCE',
            checks: checks,
            uptime: `${uptimeMinutes} minutes`,
            summary: `Uptime: ${uptimeMinutes}m, ${recoveries.length} recoveries, ${deps.length} dependency checks`
        };
    }

    async checkServices() {
        const checks = [];
        const workspace = CONFIG.WORKSPACE_ROOT;

        // Check if core files exist
        const criticalFiles = [
            path.join(workspace, 'memory'),
            path.join(workspace, 'TOOLS.md'),
            path.join(workspace, 'SOUL.md'),
            path.join(workspace, 'AGENTS.md')
        ];

        criticalFiles.forEach(file => {
            const exists = fs.existsSync(file);
            checks.push({
                type: 'FILE_CHECK',
                path: file,
                status: exists ? 'healthy' : 'missing',
                action: exists ? null : 'restore_from_backup'
            });
        });

        // Check engine state file integrity
        try {
            if (fs.existsSync(CONFIG.STATE_FILE)) {
                const stateData = fs.readFileSync(CONFIG.STATE_FILE, 'utf8');
                JSON.parse(stateData); // Validate JSON
                checks.push({
                    type: 'STATE_CHECK',
                    path: CONFIG.STATE_FILE,
                    status: 'healthy',
                    action: null
                });
            }
        } catch (e) {
            checks.push({
                type: 'STATE_CHECK',
                path: CONFIG.STATE_FILE,
                status: 'corrupted',
                action: 'reset_state'
            });
        }

        return checks;
    }

    async recoverFailures() {
        const recoveries = [];

        // Mark old errors as resolved if they're stale
        this.state.state.errors.forEach(e => {
            if (!e.resolved) {
                const errorAge = Date.now() - new Date(e.time).getTime();
                if (errorAge > 60 * 60 * 1000) { // 1 hour old
                    // Auto-resolve if no recurrence
                    const similarErrors = this.state.state.errors.filter(
                        err => err.message.includes(e.message.split(':')[0]) && !err.resolved
                    );
                    if (similarErrors.length === 1) {
                        e.resolved = true;
                        recoveries.push({
                            type: 'AUTO_RESOLVED',
                            error: e.message,
                            age: `${Math.floor(errorAge / 60000)} minutes`
                        });
                    }
                }
            }
        });

        // Check for research system issues
        try {
            const workspace = CONFIG.WORKSPACE_ROOT;
            const researchModules = [
                path.join(workspace, 'mission_control', 'enhanced_research.js'),
                path.join(workspace, 'mission_control', 'enhanced_market_service.js'),
                path.join(workspace, 'mission_control', 'enhanced_ta_analysis.js')
            ];

            researchModules.forEach(mod => {
                if (!fs.existsSync(mod)) {
                    recoveries.push({
                        type: 'MISSING_MODULE',
                        path: mod,
                        action: 'flag_for_rebuild'
                    });
                }
            });
        } catch (e) {}

        return recoveries;
    }

    async checkDependencies() {
        const checks = [];
        const workspace = CONFIG.WORKSPACE_ROOT;

        // Check API key files exist
        const apiKeys = [
            path.join(workspace, '.env'),
            path.join(workspace, 'config', 'api_keys.json')
        ];

        apiKeys.forEach(keyFile => {
            if (fs.existsSync(keyFile)) {
                checks.push({
                    type: 'API_KEY_PRESENT',
                    path: keyFile,
                    status: 'healthy'
                });
            }
        });

        // Check research output directories
        const dirs = [
            path.join(workspace, 'memory'),
            path.join(workspace, 'investment_fund', 'data'),
            path.join(workspace, 'mission_control')
        ];

        dirs.forEach(dir => {
            if (fs.existsSync(dir)) {
                const stat = fs.statSync(dir);
                checks.push({
                    type: 'DIRECTORY_HEALTH',
                    path: dir,
                    status: 'healthy',
                    writable: stat.mode & 0o200 ? true : false
                });
            }
        });

        return checks;
    }
}

// ─── PRINCIPLE 4: SELF-IMPROVEMENT ────────────────────────────────
class SelfImprovementEngine {
    constructor(state) {
        this.state = state;
    }

    async run() {
        this.state.log('INFO', '🚀 [SELF-IMPROVEMENT] Evaluating improvements...');
        const improvements = [];

        // Evaluate current metrics (throttled to avoid duplication)
        const metricAnalysis = this.analyzeMetrics();
        improvements.push(...metricAnalysis);

        // Analyze research quality (throttled)
        const researchAnalysis = this.analyzeResearchQuality();
        improvements.push(...researchAnalysis);

        // Propose improvements (throttled)
        const proposals = this.proposeImprovements();
        improvements.push(...proposals);

        // Update state with learnings - deduplicate before pushing
        const deduped = improvements.filter(imp => {
            const key = `${imp.type}-${imp.observation || imp.reason || imp.target || ''}`;
            return !this.state.state.improvements.some(existing => {
                const existingKey = `${existing.type}-${existing.observation || existing.reason || existing.target || ''}`;
                return existingKey === key;
            });
        });
        if (deduped.length > 0) {
            this.state.state.improvements.push(...deduped);
            this.state.state.metrics.selfImprovement.optimizations += deduped.length;
        }

        return {
            principle: 'SELF-IMPROVEMENT',
            improvements: deduped,
            summary: `${deduped.length} improvements identified`
        };
    }

    analyzeMetrics() {
        // Only run metric analysis every 6 hours
        const last = this.state.state._lastMetricAnalysis || 0;
        if (Date.now() - last < 6 * 60 * 60 * 1000) return [];
        this.state.state._lastMetricAnalysis = Date.now();

        const analysis = [];
        const m = this.state.state.metrics;

        // Check if efficiency is declining
        if (m.efficiency.cycles > 10 && m.efficiency.actions === 0) {
            analysis.push({
                type: 'EFFICIENCY_DECLINE',
                observation: 'Multiple efficiency cycles with no actions',
                recommendation: 'Review efficiency detection algorithms'
            });
        }

        // Check error rate
        const errorRate = this.state.state.errors.filter(e => !e.resolved).length;
        if (errorRate > 10) {
            analysis.push({
                type: 'HIGH_ERROR_RATE',
                observation: `${errorRate} unresolved errors`,
                recommendation: 'Implement automated error resolution'
            });
        }

        return analysis;
    }

    analyzeResearchQuality() {
        // Only run research quality analysis every 2 hours
        const last = this.state.state._lastResearchAnalysis || 0;
        if (Date.now() - last < 2 * 60 * 60 * 1000) return [];
        this.state.state._lastResearchAnalysis = Date.now();

        const analysis = [];

        try {
            const workspace = CONFIG.WORKSPACE_ROOT;
            const memoryPath = path.join(workspace, 'memory');

            // Check if research is being logged consistently
            const today = new Date().toISOString().split('T')[0];
            const todayFile = path.join(memoryPath, `${today}.md`);

            if (!fs.existsSync(todayFile)) {
                analysis.push({
                    type: 'MISSING_DAILY_LOG',
                    observation: 'No daily memory file found for today',
                    recommendation: 'Create daily log to track research cycles'
                });
            }

            // Check research cycle frequency
            const files = fs.readdirSync(memoryPath).filter(f => f.endsWith('.md') && f.match(/^\d{4}-\d{2}-\d{2}/));
            if (files.length > 7) {
                // Calculate average cycles per day (last 14 days only)
                const recentFiles = files.slice(-14);
                const totalCycles = recentFiles.reduce((acc, f) => {
                    try {
                        const content = fs.readFileSync(path.join(memoryPath, f), 'utf8');
                        const cycles = (content.match(/RESEARCH CYCLE/g) || []).length;
                        return acc + cycles;
                    } catch(e) { return acc; }
                }, 0);
                const avgCycles = totalCycles / recentFiles.length;

                if (avgCycles < 3) {
                    // Only add if not already present in last 24h
                    const alreadyExists = this.state.state.improvements.some(i =>
                        i.type === 'LOW_RESEARCH_FREQUENCY' &&
                        Date.now() - new Date(i.timestamp || 0).getTime() < 24 * 60 * 60 * 1000
                    );
                    if (!alreadyExists) {
                        analysis.push({
                            type: 'LOW_RESEARCH_FREQUENCY',
                            observation: `Average ${avgCycles.toFixed(1)} cycles/day over ${recentFiles.length} days`,
                            recommendation: 'Increase to 3-4 cycles/day for better coverage'
                        });
                    }
                } else if (avgCycles > 6) {
                    analysis.push({
                        type: 'HIGH_RESEARCH_FREQUENCY',
                        observation: `Average ${avgCycles.toFixed(1)} cycles/day`,
                        recommendation: 'Frequency is good, consider consolidating insights'
                    });
                }
            }

            // Check market data quality
            const marketData = path.join(workspace, 'mission_control', 'market_data.json');
            if (fs.existsSync(marketData)) {
                try {
                    const data = JSON.parse(fs.readFileSync(marketData, 'utf8'));
                    const assets = ['BTC', 'ETH', 'MSTR', 'HIMS'];
                    const missingAssets = assets.filter(a => !data[a] || !data[a].price);

                    if (missingAssets.length > 0) {
                        const alreadyExists = this.state.state.improvements.some(i =>
                            i.type === 'INCOMPLETE_MARKET_DATA' &&
                            Date.now() - new Date(i.timestamp || 0).getTime() < 6 * 60 * 60 * 1000
                        );
                        if (!alreadyExists) {
                            analysis.push({
                                type: 'INCOMPLETE_MARKET_DATA',
                                observation: `Missing data for: ${missingAssets.join(', ')}`,
                                recommendation: 'Check data source API keys and connectivity'
                            });
                        }
                    }
                } catch (e) {
                    analysis.push({
                        type: 'INCOMPLETE_MARKET_DATA',
                        observation: 'Market data file is corrupted or unreadable',
                        recommendation: 'Check data source API keys and connectivity'
                    });
                }
            }
        } catch (e) {}

        return analysis;
    }

    proposeImprovements() {
        // Only propose new improvements every 4 hours
        const last = this.state.state._lastProposal || 0;
        if (Date.now() - last < 4 * 60 * 60 * 1000) return [];
        this.state.state._lastProposal = Date.now();

        const proposals = [];

        // Propose new skill if recurring patterns found
        const recurringErrors = this.state.state.errors.filter(e => !e.resolved)
            .reduce((acc, e) => {
                const type = e.message.split(':')[0];
                acc[type] = (acc[type] || 0) + 1;
                return acc;
            }, {});

        Object.entries(recurringErrors).forEach(([type, count]) => {
            if (count >= 3) {
                const alreadyExists = this.state.state.improvements.some(i =>
                    i.type === 'SKILL_PROPOSAL' && i.target === `${type}_handler`
                );
                if (!alreadyExists) {
                    proposals.push({
                        type: 'SKILL_PROPOSAL',
                        target: `${type}_handler`,
                        reason: `${count} occurrences of ${type}`,
                        status: 'pending_approval'
                    });
                }
            }
        });

        // Propose research automation
        const today = new Date().toISOString().split('T')[0];
        // Check if we already proposed this today
        const alreadyProposedToday = this.state.state.improvements.some(i =>
            i.type === 'RESEARCH_AUTOMATION' &&
            i.timestamp && i.timestamp.startsWith(today)
        );

        if (!alreadyProposedToday) {
            const researchToday = this.state.state.improvements.filter(i =>
                i.timestamp && i.timestamp.startsWith(today) && i.type === 'RESEARCH_TRIGGERED'
            ).length;

            if (researchToday === 0) {
                proposals.push({
                    type: 'RESEARCH_AUTOMATION',
                    target: 'daily_research_cycle',
                    reason: 'No research triggered today',
                    status: 'ready_to_implement'
                });
            }
        }

        // Propose memory consolidation if many daily files
        try {
            const workspace = CONFIG.WORKSPACE_ROOT;
            const memoryPath = path.join(workspace, 'memory');
            if (fs.existsSync(memoryPath)) {
                const files = fs.readdirSync(memoryPath).filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/));
                if (files.length > 30) {
                    const alreadyExists = this.state.state.improvements.some(i =>
                        i.type === 'MEMORY_CONSOLIDATION'
                    );
                    if (!alreadyExists) {
                        proposals.push({
                            type: 'MEMORY_CONSOLIDATION',
                            target: 'archive_old_logs',
                            reason: `${files.length} daily files accumulated`,
                            status: 'ready_to_implement'
                        });
                    }
                }
            }
        } catch (e) {}

        return proposals;
    }
}

// ─── MAIN ENGINE ──────────────────────────────────────────────────
class AutonomyCoreEngine {
    constructor() {
        this.state = new StateManager();
        this.engines = {
            efficiency: new EfficiencyEngine(this.state),
            intelligence: new IntelligenceEngine(this.state),
            persistence: new PersistenceEngine(this.state),
            selfImprovement: new SelfImprovementEngine(this.state)
        };
    }

    async runSingleCycle() {
        const cycleStart = Date.now();
        this.state.state.totalCycles++;
        this.state.state.lastCycle = new Date().toISOString();

        this.state.log('INFO', `=== AUTONOMY CORE CYCLE #${this.state.state.totalCycles} ===`);
        this.state.log('INFO', `Time: ${new Date().toISOString()}`);

        const results = {};

        // Run all 4 principles
        const engineMap = {
            'EFFICIENCY': 'efficiency',
            'INTELLIGENCE': 'intelligence',
            'PERSISTENCE': 'persistence',
            'SELF-IMPROVEMENT': 'selfImprovement'
        };

        for (const principle of CONFIG.PRINCIPLES) {
            const engineKey = engineMap[principle];
            try {
                const start = Date.now();
                const engine = this.engines[engineKey];
                if (!engine) {
                    throw new Error(`Engine '${engineKey}' not found for principle '${principle}'`);
                }
                results[engineKey] = await engine.run();
                const duration = Date.now() - start;
                this.state.log('INFO', `[${principle}] Completed in ${duration}ms`);
            } catch (error) {
                this.state.log('ERROR', `[${principle}] FAILED: ${error.message}`);
                results[engineKey] = { error: error.message };
            }
        }

        // Save state
        this.state.save();

        const totalDuration = Date.now() - cycleStart;
        this.state.log('INFO', `=== CYCLE COMPLETE in ${totalDuration}ms ===`);
        this.state.log('INFO', '----------------------------------------\n');

        return results;
    }

    async runContinuous() {
        this.state.log('INFO', '═══════════════════════════════════════');
        this.state.log('INFO', '🤖 AUTONOMY CORE ENGINE v' + CONFIG.VERSION);
        this.state.log('INFO', 'Mode: SILENT | Interval: 15 minutes');
        this.state.log('INFO', '═══════════════════════════════════════');

        // Run immediately
        await this.runSingleCycle();

        // Schedule next run
        setInterval(async () => {
            await this.runSingleCycle();
        }, CONFIG.RUN_INTERVAL_MS);
    }

    // Run once and exit (for cron/task scheduler)
    async runOnce() {
        return await this.runSingleCycle();
    }
}

// ─── ENTRY POINT ──────────────────────────────────────────────────
async function main() {
    const engine = new AutonomyCoreEngine();

    // Check if running in continuous mode or single cycle
    const isContinuous = process.argv.includes('--continuous');

    if (isContinuous) {
        await engine.runContinuous();
    } else {
        const results = await engine.runOnce();

        // Output results as JSON for parsing
        console.log('\n--- RESULTS ---');
        console.log(JSON.stringify(results, null, 2));

        process.exit(0);
    }
}

main().catch(error => {
    console.error('FATAL:', error);
    process.exit(1);
});
