HAVE_RUN_INIT = "False"

def on_init(server):
    global HAVE_RUN_INIT
    HAVE_RUN_INIT = "True"

def on_message(msg, server):
    if msg["text"] == u"test_init":
        return HAVE_RUN_INIT
