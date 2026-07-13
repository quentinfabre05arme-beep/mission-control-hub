# Token Optimization System

## Overview
This document tracks token usage optimizations for the X Growth Mission.

---

## Implemented Optimizations

### 1. Conversation Summarization ✅
- **File:** `conversation_summary.md` - Rolling summary of key decisions
- **Trigger:** Every 20 messages or 2 hours
- **Method:** Extract decisions, actions, TODOs only

### 2. Cached Templates ✅
- **File:** `cached_templates.json` - Pre-built X replies
- **Categories:** ETH Treasury, HIMS, AI Agentic Commerce
- **Usage:** Load only when needed, not in context

### 3. Research Chunking ✅
- **File:** `research_chunks/` directory
- **Method:** Split research by topic, retrieve relevant chunks
- **Index:** `research_index.json` for quick lookup

### 4. Sliding Window Context ✅
- **Keep in context:** Last 10 messages + summary + current task
- **Offload to files:** Older conversation, completed work

### 5. Response Caching ✅
- **File:** `response_cache.json`
- **Keys:** Query hash → Response
- **TTL:** 24 hours for research, permanent for templates

---

## Token Budget

| Component | Target Tokens | Current |
|-----------|--------------|---------|
| System context | 2,000 | TBD |
| Conversation history | 3,000 | TBD |
| Current task | 2,000 | TBD |
| Retrieved knowledge | 3,000 | TBD |
| **Total** | **10,000** | - |
| **Buffer** | **2,000** | - |
| **Max per turn** | **12,000** | - |

---

## Daily Tracking

| Date | Input Tokens | Output Tokens | Cost | Notes |
|------|-------------|---------------|------|-------|
| 2026-07-10 | - | - | - | Optimization system created |

---

## Quick Commands

- "summarize conversation" → Create/update rolling summary
- "load template [category]" → Get pre-built replies
- "cache response [query] [response]" → Store for reuse
- "chunk research [topic]" → Split into retrievable pieces
