import os
import sys
from limbo import FakeServer

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from poll import on_message, ERROR_WRONG_NUMBER_OF_ARGUMENTS, ERROR_INVALID_FORMAT


def test_poll():
    ret = on_message({"text": u"!poll ''"}, None)
    assert ERROR_WRONG_NUMBER_OF_ARGUMENTS in ret

    ret = on_message({
        "text": u"!poll 'q?' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11'"
        }, None)
    assert ERROR_WRONG_NUMBER_OF_ARGUMENTS in ret

    ret = on_message({
        "text": u"!poll unbalanced 'parentheses"
        }, None)
    assert ERROR_INVALID_FORMAT in ret

    fakeserver = FakeServer()
    ret = on_message({
        "text": u"!poll 'Hello?' 'is it me your looking for' 'i can see it'",
        "channel": "xyz"}, fakeserver)
    assert ret is None
    assert len(fakeserver.slack.posted_reactions) == 1
    assert len(list(fakeserver.slack.posted_reactions.values())[0]) == 2
    assert len(fakeserver.slack.posted_messages) == 1
