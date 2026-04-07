# RAI Service - Responsible AI Validation

The RAI (Responsible AI) service ensures outputs are safe and appropriate.

---

## Location: `app/services/rai.py`

---

## What is RAI?

RAI stands for **Responsible AI** - practices to ensure AI systems are:
- Safe
- Fair
- Transparent
- Accountable

Our RAI service focuses on **output validation**.

---

## What It Checks

### 1. Empty Output
**Problem:** Blank or too short responses are useless.
```
❌ ""
❌ " "
✅ "Here is your answer..."
```

### 2. Length Limits
**Problem:** Extremely long outputs might indicate an error.
```
❌ Output > 50,000 characters
✅ Output within reasonable limits
```

### 3. Blocked Patterns
**Problem:** Sensitive data might leak into outputs.

| Pattern | What it catches |
|---------|-----------------|
| Credentials | `password: secret123` |
| API keys | `api_key: xyz123` |
| Script injection | `<script>alert('hack')</script>` |
| SQL injection | `DROP TABLE users` |

---

## How It Works

```python
from app.services.rai import get_rai_service

rai = get_rai_service()

# Validate output
result = rai.validate({"result": "Hello world"})

print(result.is_valid)    # True
print(result.notes)       # ["All validation checks passed"]
```

---

## Validation Result

```python
ValidationResult(
    is_valid=True,           # Did it pass all checks?
    notes=["..."]            # Details about each check
)
```

**Passing example:**
```python
is_valid=True
notes=["All validation checks passed"]
```

**Failing example:**
```python
is_valid=False
notes=["Blocked pattern detected (rule 1)"]
```

---

## The Checks in Detail

### Check 1: Not Empty
```python
if len(output_str.strip()) < 1:
    is_valid = False
    notes.append("Output is empty or too short")
```

### Check 2: Not Too Long
```python
if len(output_str) > 50000:
    is_valid = False
    notes.append("Output exceeds maximum length")
```

### Check 3: No Blocked Patterns
```python
BLOCKED_PATTERNS = [
    r"\b(password|secret|api[_-]?key)\s*[:=]\s*\S+",  # Credentials
    r"<script[^>]*>.*?</script>",                       # XSS
    r"\b(drop|delete|truncate)\s+table\b",              # SQL injection
]

for pattern in BLOCKED_PATTERNS:
    if pattern.search(output_str):
        is_valid = False
        notes.append("Blocked pattern detected")
```

---

## Integration with Worker

The worker calls RAI during the `validate` task:

```python
def _handle_validate(self, task):
    processed = self._context.get("processed", {})
    
    # Validate with RAI
    rai_service = get_rai_service()
    result = rai_service.validate(processed)
    
    return {
        "validated": result.is_valid,
        "validation_notes": result.notes_str,
        "final_output": processed.get("result", "")
    }
```

---

## Examples

### Valid Output
```python
rai.validate({"result": "Python is a programming language"})
# is_valid=True, notes=["All validation checks passed"]
```

### Empty Output
```python
rai.validate("")
# is_valid=False, notes=["Output is empty or too short"]
```

### Blocked Pattern
```python
rai.validate("Here is your password: secret123")
# is_valid=False, notes=["Blocked pattern detected (rule 1)"]
```

### Script Injection
```python
rai.validate("<script>alert('xss')</script>")
# is_valid=False, notes=["Blocked pattern detected (rule 2)"]
```

---

## Future Enhancements

The MVP uses rule-based checks. Future versions could add:

| Enhancement | What it does |
|-------------|--------------|
| LLM-based checks | Use AI to detect harmful content |
| Toxicity detection | Check for offensive language |
| Bias detection | Identify unfair outputs |
| PII detection | Find personal information |
| Fact checking | Verify claims are accurate |

### Example: LLM-based validation
```python
async def validate_with_llm(output):
    prompt = f"Is this output safe and appropriate? {output}"
    response = await llm.complete(prompt)
    return response.is_safe
```

---

## Why This Matters

Without RAI validation:
- ❌ Sensitive data could leak
- ❌ Harmful content could be returned
- ❌ Security vulnerabilities could be exploited

With RAI validation:
- ✅ Outputs are filtered for safety
- ✅ Security issues are caught early
- ✅ Users get appropriate responses
