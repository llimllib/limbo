def on_member_left_channel(msg, server):
    return "user {} left".format(msg['user'])
