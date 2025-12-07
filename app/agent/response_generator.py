from app.common.prompts import render_template


def generate_order_response(order):
    """
    order = {
        "order_id": "...",
        "status": "...",
        "delivery_date": "..."
    }
    """
    if order is None:
        return render_template("unknown_order.j2")

    return render_template(
        "order_response.j2",
        order_id=order["order_id"],
        status=order["status"],
        delivery_date=order["delivery_date"]
    )


def generate_faq_response(answer: str):
    """
    answer = retrieved FAQ text (string)
    """
    return render_template(
        "faq_response.j2",
        answer=answer
    )


def generate_unknown_response():
    return render_template("unknown_response.j2")
