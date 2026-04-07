"""Responsible AI (RAI) Validation Service."""

import re
from typing import Any
from pydantic import BaseModel


class ValidationResult(BaseModel):
    """Result of RAI validation."""
    
    is_valid: bool
    notes: list[str] = []
    
    @property
    def notes_str(self) -> str:
        """Return notes as a single string."""
        return "; ".join(self.notes) if self.notes else "Validation passed"


class RAIService:
    """
    Validates output using rule-based checks.
    
    For MVP, this uses simple rules. Later can be expanded to use:
    - LLM-based content analysis
    - External content moderation APIs
    - Custom ML models
    """
    
    # Blocked patterns (case-insensitive)
    BLOCKED_PATTERNS = [
        r"\b(password|secret|api[_-]?key|token)\s*[:=]\s*\S+",  # Credentials
        r"<script[^>]*>.*?</script>",  # Script injection
        r"\b(drop|delete|truncate)\s+table\b",  # SQL injection patterns
    ]
    
    # Maximum reasonable output length
    MAX_OUTPUT_LENGTH = 50000
    
    # Minimum output length (empty check)
    MIN_OUTPUT_LENGTH = 1
    
    def __init__(self):
        self._compiled_patterns = [
            re.compile(pattern, re.IGNORECASE | re.DOTALL)
            for pattern in self.BLOCKED_PATTERNS
        ]
    
    def validate(self, output: dict[str, Any] | str) -> ValidationResult:
        """
        Validate output using rule-based checks.
        
        Checks:
        1. Output is not empty
        2. No blocked patterns detected
        3. Output length is within bounds
        
        Returns:
            ValidationResult with is_valid and notes
        """
        notes = []
        is_valid = True
        
        # Convert dict to string for pattern matching
        if isinstance(output, dict):
            output_str = str(output)
        else:
            output_str = str(output)
        
        # Check 1: Not empty
        if len(output_str.strip()) < self.MIN_OUTPUT_LENGTH:
            is_valid = False
            notes.append("Output is empty or too short")
        
        # Check 2: Length within bounds
        if len(output_str) > self.MAX_OUTPUT_LENGTH:
            is_valid = False
            notes.append(f"Output exceeds maximum length ({len(output_str)} > {self.MAX_OUTPUT_LENGTH})")
        
        # Check 3: No blocked patterns
        for i, pattern in enumerate(self._compiled_patterns):
            if pattern.search(output_str):
                is_valid = False
                notes.append(f"Blocked pattern detected (rule {i + 1})")
        
        # Add success note if valid
        if is_valid:
            notes.append("All validation checks passed")
        
        return ValidationResult(is_valid=is_valid, notes=notes)
    
    def validate_with_context(
        self, 
        output: dict[str, Any] | str,
        context: dict[str, Any] | None = None
    ) -> ValidationResult:
        """
        Validate output with optional context for more sophisticated checks.
        
        For MVP, this delegates to basic validate().
        Later can be extended for context-aware validation.
        """
        # For now, just use basic validation
        # Future: Compare output relevance to input context
        return self.validate(output)


# Singleton instance
_rai_service: RAIService | None = None


def get_rai_service() -> RAIService:
    """Get or create the RAI service singleton."""
    global _rai_service
    if _rai_service is None:
        _rai_service = RAIService()
    return _rai_service
