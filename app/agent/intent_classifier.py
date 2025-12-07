from __future__ import annotations
import os

from langchain_openai import ChatOpenAI
from langsmith import traceable

from app.schemas.intent import IntentResult
from app.utils.extract_order_id import extract_order_id
from app.common.prompts import render_template


@traceable(name="intent_classification")
def classify_intent(user_input: str) -> IntentResult:
    """
    LLM-powered intent classifier with LangSmith tracing.
    """

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0
    )

    prompt = render_template(
        "intent_classifier.j2",
        user_input=user_input
    )

    response = llm.invoke(prompt)

    # Parse + validate structured output
    result = IntentResult.model_validate_json(response.content)

    # Safety net: force regex-based extraction if missing
    if result.intent == "order_tracking" and not result.order_id:
        result.order_id = extract_order_id(user_input)

    return result
