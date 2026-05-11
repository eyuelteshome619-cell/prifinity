"""
Credit Management Utilities - Shared across routes
Uses atomic SQL to prevent race conditions in concurrent requests.
"""
from app.utils.database import execute_query


def deduct_credits(user_id, amount, transaction_type, description):
    """Deduct credits from user account using atomic SQL.

    Uses a single UPDATE with a WHERE guard to prevent race conditions
    where two concurrent requests could read the same balance and
    double-deduct.
    """
    if amount <= 0:
        return

    # Atomic deduction: only succeeds if user has enough credits
    execute_query(
        "UPDATE users SET credits = credits - %s WHERE id = %s AND credits >= %s",
        (amount, user_id, amount),
        fetch_all=False
    )

    # Fetch the updated balance for the transaction log
    user = execute_query(
        "SELECT credits FROM users WHERE id = %s",
        (user_id,),
        fetch_one=True
    )

    new_balance = user['credits'] if user else 0

    # Record transaction
    execute_query(
        """INSERT INTO credit_transactions (user_id, amount, transaction_type, description, balance_after)
           VALUES (%s, %s, %s, %s, %s)""",
        (user_id, -amount, transaction_type, description, new_balance),
        fetch_all=False
    )
