"""
Cost management utility.
Tracks the cumulative cost of LLM requests and enforces budget limits.
"""

from ai_platform.logger import get_logger
from ai_platform.exceptions import BudgetExceededError

# Initialize logger for tracking financial events
logger = get_logger(__name__)

# Global variable to track total spend during the application lifecycle
total_cost = 0.0


def add_cost(cpr: float) -> float:
    """
    Adds the cost of a single request (cpr) to the total running cost.
    """
    global total_cost
    total_cost = total_cost + cpr
    logger.info(f"cost per request is {cpr}")
    return total_cost


def check_budget_exceeded(cost_limit: float) -> bool:
    """
    Validates if the current spend has crossed the user-defined threshold.
    Raises BudgetExceededError if the limit is breached.
    """
    global total_cost
    if total_cost > cost_limit:
        logger.error(f"Budget limit exceeded: spent {total_cost} / limit {cost_limit}")
        raise BudgetExceededError("Budget limit exceeded")
    return True
