---
name: "error-handler"
description: "Resilient error handling with exponential backoff and automatic retry for autonomous operations"
---

# Error Handler

Use this skill when executing external calls, API requests, file operations, or any action that might fail. Implements resilient patterns for autonomous operation.

## Workflow

1. **Attempt Operation** with timeout
2. **On Failure:** Log error details
3. **Apply Backoff:** Wait 2^attempt seconds (max 60s)
4. **Retry:** Up to 3 attempts by default
5. **On Exhaustion:** Escalate or use fallback

## Configuration

```json
{
  "maxRetries": 3,
  "baseDelay": 2,
  "maxDelay": 60,
  "backoffMultiplier": 2,
  "retryableErrors": ["ETIMEDOUT", "ECONNRESET", "429", "503"]
}
```

## Patterns

### Basic Retry Wrapper
```javascript
async function withRetry(fn, context) {
  const maxRetries = context.maxRetries || 3;
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      const delay = Math.min(Math.pow(2, i) * 1000, 60000);
      await sleep(delay);
    }
  }
}
```

### Circuit Breaker
- After 5 failures, open circuit for 5 minutes
- Return cached result or fallback
- Log circuit state changes

### Graceful Degradation
- Primary: Full functionality
- Secondary: Reduced functionality
- Tertiary: Error message with log reference

## Usage

```javascript
const result = await errorHandler.execute({
  operation: () => fetchData(),
  context: "research-cycle-42",
  fallback: () => cachedData
});
```

## Logging

All errors logged to:
- `logs/errors/YYYY-MM-DD.log`
- Include: timestamp, context, error type, retry count

## Safety

- Never retry on 4xx client errors (except 429)
- Always log before retry
- Never infinite loop
- Always respect rate limits
