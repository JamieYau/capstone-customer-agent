def classify_intent(user_input):
    user_input = user_input.lower()

    if "order" in user_input or "track" in user_input:
        return "order_tracking"

    if "return" in user_input or "refund" in user_input or "cancel" in user_input:
        return "policy"

    return "faq"
