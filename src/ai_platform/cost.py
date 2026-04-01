
from ai_platform.logger import get_logger
from ai_platform.exceptions import BudgetExceededError
logger = get_logger(__name__)
total_cost = 0.0

def add_cost(cpr:float) -> float:
    global total_cost
    total_cost = total_cost + cpr
    logger.info(f"cost per request is {cpr}")
    return total_cost


def check_budget_exceeded(cost_limit:float) -> bool:
    global total_cost
    if total_cost > cost_limit:
        logger.error(f"Budget limit exceeded: spent {total_cost} / limit {cost_limit}")
        raise BudgetExceededError("Budget limit exceeded")
    return True