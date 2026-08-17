from dotenv import load_dotenv

load_dotenv()

from router.conversation import ConversationManager
from router.router import route

TIER_LABELS = {"haiku": "HAIKU", "sonnet": "SONNET", "opus": "OPUS"}


def main():
    print("LLM Router CLI — type 'exit' or 'quit' to stop.\n")
    convo = ConversationManager()

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        decision = route(user_input, recent_context=convo.recent_context())
        tier = decision["tier"]
        print(f"[routed to {TIER_LABELS[tier]} — {decision['source']}: {decision['reason']}]")

        reply = convo.send(tier, user_input)
        print(f"assistant> {reply}\n")


if __name__ == "__main__":
    main()
