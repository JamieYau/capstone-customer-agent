import re


def extract_order_id(user_message: str):
    """
    Extracts an order number like 1001, 12345 from user text.
    Returns None if no valid order ID found.
    """
    if not user_message:
        return None

    # Look for a sequence of digits 3–10 digits long
    match = re.search(r"\b(\d{3,10})\b", user_message)
    if match:
        return match.group(1)

    return None