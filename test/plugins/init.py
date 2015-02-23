HAVE_RUN_INIT="False"
def on_init(server):
    HAVE_RUN_INIT="True"

def on_message(msg, server):
    if msg["text"] == u"test_init":
        return HAVE_RUN_INIT
