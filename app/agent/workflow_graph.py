# app/agent/workflow.py
from langgraph.graph import StateGraph, END
from app.agent.intent_classifier import classify_intent
from app.tools.order_lookup import lookup_order
from app.tools.faq_retriever import retrieve_faq_answer


def build_graph():

    def node_classify(state):
        res = classify_intent(state["user_input"])
        state["intent"] = res.intent
        state["order_id"] = res.order_id
        return state

    def node_order(state):
        order_id = state.get("order_id")
        state["result"] = lookup_order(order_id)
        return state

    def node_faq(state):
        state["result"] = retrieve_faq_answer(state["user_input"])
        return state

    def node_unknown(state):
        state["result"] = (
            "I'm not sure what you meant. "
            "You can ask about orders, delivery, returns, or store policy."
        )
        return state

    graph = StateGraph(dict)

    graph.add_node("classify", node_classify)
    graph.add_node("order", node_order)
    graph.add_node("faq", node_faq)
    graph.add_node("unknown", node_unknown)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        lambda s: s["intent"],
        {
            "order_tracking": "order",
            "faq": "faq",
            "policy": "faq",
            "unknown": "unknown",
        }
    )

    graph.add_edge("order", END)
    graph.add_edge("faq", END)
    graph.add_edge("unknown", END)

    return graph.compile()
