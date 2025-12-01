from langgraph.graph import StateGraph, END
from app.agent.intent_classifier import classify_intent
from app.tools.order_lookup import lookup_order
from app.tools.faq_retriever import retrieve_faq_answer
from app.utils.extract_order_id import extract_order_id


def build_graph():

    # Step 1: Intent classification
    def classify(state):
        state["intent"] = classify_intent(state["user_input"])

        # Extract order ID here if it is an order query
        if state["intent"] == "order_tracking":
            state["order_id"] = extract_order_id(state["user_input"])

        return state

    # Step 2: Handle order tracking
    def handle_order(state):
        order_id = state.get("order_id", None)

        if not order_id:
            state["result"] = {
                "error": "No order ID found. Please provide your order number."
            }
            return state

        state["result"] = lookup_order(order_id)
        return state

    # Step 3: FAQ / policy / fallback
    def handle_faq(state):
        state["result"] = retrieve_faq_answer(state["user_input"])
        return state


    # Build state graph
    graph = StateGraph(dict)

    graph.add_node("classify", classify)
    graph.add_node("order", handle_order)
    graph.add_node("faq", handle_faq)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        lambda state: state["intent"],
        {
            "order_tracking": "order",
            "faq": "faq",
            "policy": "faq"
        }
    )

    graph.add_edge("order", END)
    graph.add_edge("faq", END)

    return graph.compile()
