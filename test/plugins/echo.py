def on_message_deleted(msg, server):
    return "Deleted: {}".format(msg["previous_message"]["text"])

def on_message_changed(msg, server):
    text = msg.get("message", {"text": ""}).get("text", "")
    if text.startswith("!echo"):
        return "Changed: {}".format(text)

def on_message(msg, server):
    if msg["text"].startswith("!echo"):
        return msg.get("text", "")

def on_channel_join(msg, server):
    return "saw user {} join".format(msg['user'])
