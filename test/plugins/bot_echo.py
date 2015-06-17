def on_bot_message(msg, server):
    if msg["text"].startswith("!echo"):
        text = msg.get("text", "")
        return text
