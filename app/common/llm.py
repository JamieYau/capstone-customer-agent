from __future__ import annotations
import os, json, requests
from typing import List, Dict, Literal
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

Provider = Literal["openai", "ollama"]


class LLMError(RuntimeError):
    pass


class LLMClient:
    def __init__(self):
        self.provider: Provider = os.getenv("PROVIDER", "openai")

        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "mistral")

        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise LLMError("Missing OPENAI_API_KEY")
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            self.ollama_url = "http://localhost:11434/api/chat"

    def _openai_chat(self, messages, temperature):
        resp = self.client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content or ""

    def _ollama_chat(self, messages):
        r = requests.post(
            self.ollama_url,
            json={"model": self.ollama_model, "messages": messages, "stream": False},
            timeout=30,
        )
        if r.status_code != 200:
            raise LLMError(f"Ollama error {r.status_code}: {r.text}")

        return r.json().get("message", {}).get("content", "")

    def chat_json(self, messages, temperature=0.2):
        if self.provider == "openai":
            return self._openai_chat(messages, temperature)
        return self._ollama_chat(messages)

    def run_structured(self, messages, schema: type[BaseModel], attempts=3):
        last_error = None

        for _ in range(attempts):
            raw = self.chat_json(messages)

            try:
                data = json.loads(raw)
                return schema.model_validate(data)

            except (json.JSONDecodeError, ValidationError) as e:
                last_error = e
                messages.append({
                    "role": "system",
                    "content": f"Output was invalid: {e}. Return VALID JSON only."
                })

        raise LLMError(f"Structured output failed after {attempts} attempts: {last_error}")
