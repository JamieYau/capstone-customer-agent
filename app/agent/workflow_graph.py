from langgraph.graph import StateGraph, END
from langsmith import traceable

from app.agent.intent_classifier import classify_intent
from app.tools.order_lookup import lookup_order
from app.tools.faq_retriever import retrieve_faq_answer
from app.agent.response_generator import (
    generate_order_response,
    generate_faq_response,
    generate_unknown_response
)


def build_graph():
    @traceable(name="intent_classification_node")
    def node_classify(state):
        result = classify_intent(state["user_input"])
        state["intent"] = result.intent
        state["order_id"] = result.order_id
        return state

    @traceable(name="order_tracking_node")
    def node_order(state):
        raw = lookup_order(state.get("order_id"))
        state["result"] = generate_order_response(raw)
        return state

    @traceable(name="faq_tracking_node")
    def node_faq(state):
        raw_answer = retrieve_faq_answer(state["user_input"])
        state["result"] = generate_faq_response(raw_answer)
        return state

    @traceable(name="unknown_tracking_node")
    def node_unknown(state):
        state["result"] = generate_unknown_response()
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
            "unknown": "unknown"
        }
    )

    graph.add_edge("order", END)
    graph.add_edge("faq", END)
    graph.add_edge("unknown", END)

    return graph.compile()
