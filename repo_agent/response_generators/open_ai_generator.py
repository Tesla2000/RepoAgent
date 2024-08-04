from typing import Optional

from repo_agent.response_generators.response import Response
from repo_agent.response_generators.response_generator import ResponseGenerator
from openai import OpenAI

class OpenaiGenerator(ResponseGenerator):
    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Optional[Response]:
        client = OpenAI(
            api_key=self.settings.chat_completion.openai_api_key.get_secret_value(),
            base_url=str(self.settings.chat_completion.base_url),
            timeout=self.settings.chat_completion.request_timeout,
        )

        messages = self._get_messages(sys_prompt, usr_prompt)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=self.settings.chat_completion.temperature,
            max_tokens=max_tokens,
        )

        response_message = response.choices[0].message
        if isinstance(response_message, Response):
            return response_message
        return
    
    @classmethod
    def is_valid(cls, model: str) -> bool:
        return model.startswith("gpt")

    def _get_messages(self, sys_prompt: str, usr_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]
        