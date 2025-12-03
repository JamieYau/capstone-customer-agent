from app.common.llm import LLMClient
from app.common.prompts import render_template
from app.schemas.intent import IntentResult

def classify_intent(user_input: str) -> IntentResult:
    client = LLMClient()

    prompt = render_template("intent_classifier.j2", user_input=user_input)

    messages = [
        {"role": "user", "content": prompt}
    ]

    return client.run_structured(messages, IntentResult)
