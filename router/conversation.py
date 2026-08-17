from anthropic import Anthropic

from config import TIER_MODELS

RECENT_CONTEXT_TURNS = 2


class ConversationManager:
    """Holds a single message history and resends full context to whichever
    model tier is picked each turn, since state doesn't persist automatically
    across model swaps."""

    def __init__(self):
        self.client = Anthropic()
        self.messages: list[dict] = []

    def recent_context(self) -> str:
        recent = self.messages[-(RECENT_CONTEXT_TURNS * 2):]
        lines = [f"{m['role']}: {m['content']}" for m in recent]
        return "\n".join(lines)

    def send(self, tier: str, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})

        model = TIER_MODELS[tier]
        response = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=self.messages,
        )

        reply_text = next(
            block.text for block in response.content if block.type == "text"
        )
        self.messages.append({"role": "assistant", "content": reply_text})
        return reply_text
