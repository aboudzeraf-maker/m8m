from __future__ import annotations

import os
from typing import Any

from ai import generateText, generateObject
from pydantic import BaseModel


class AIServiceConfig:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.default_model = os.getenv("DEFAULT_AI_MODEL", "gpt-4")


class AIService:
    def __init__(self):
        self.config = AIServiceConfig()

    def get_model_id(self, model: str | None = None) -> str:
        """Get the model ID based on provider"""
        model = model or self.config.default_model

        if "gpt" in model.lower():
            return model  # e.g., gpt-4, gpt-3.5-turbo
        elif "claude" in model.lower():
            return model  # e.g., claude-3-sonnet-20240229
        elif "gemini" in model.lower():
            return model  # e.g., gemini-pro
        else:
            return self.config.default_model

    async def generate_text(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate text using Vercel AI SDK"""
        model_id = self.get_model_id(model)

        try:
            result = await generateText(
                model=model_id,
                prompt=prompt,
                temperature=temperature,
                maxTokens=max_tokens,
            )
            return result.text
        except Exception as e:
            raise ValueError(f"AI generation failed: {str(e)}")

    async def generate_object(
        self,
        prompt: str,
        schema: type[BaseModel],
        model: str | None = None,
    ) -> BaseModel:
        """Generate structured object using Vercel AI SDK"""
        model_id = self.get_model_id(model)

        try:
            result = await generateObject(
                model=model_id,
                prompt=prompt,
                schema=schema,
            )
            return result.object
        except Exception as e:
            raise ValueError(f"Object generation failed: {str(e)}")

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
    ) -> str:
        """Chat with AI using message history"""
        model_id = self.get_model_id(model)

        # Format messages for Vercel AI
        formatted_messages = [msg for msg in messages]

        try:
            # Using generateText with formatted prompt for now
            # In real implementation, use actual chat model
            last_message = formatted_messages[-1]["content"] if formatted_messages else ""
            result = await generateText(
                model=model_id,
                prompt=last_message,
                temperature=temperature,
            )
            return result.text
        except Exception as e:
            raise ValueError(f"Chat failed: {str(e)}")
