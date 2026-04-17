"""
Custom exception definitions for the AI Platform.
Provides specific error types for budget and credit management.
"""


class BudgetExceededError(Exception):
    """Raised when the application's total cost exceeds the defined max_cost setting."""

    pass


class InsufficientCreditsError(Exception):
    """Raised when a user or project lacks the balance to perform an operation."""

    pass
