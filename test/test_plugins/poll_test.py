import os
import sys
from limbo import FakeServer

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from poll import on_message, ERROR_WRONG_NUMBER_OF_ARGUMENTS


def test_poll():
    # wrong number of args
    ret = on_message({"text": u"!poll ''"}, None)
    assert ERROR_WRONG_NUMBER_OF_ARGUMENTS in ret
    # one more than it can be
    ret = on_message({"text": u"!poll 'q?' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' '11'"}, None)
    assert ERROR_WRONG_NUMBER_OF_ARGUMENTS in ret

    fakeserver = FakeServer()
    ret = on_message({"text": u"!poll 'Hello?' 'is it me your looking for' 'i can see it in your eyes'",
                      "channel": "xyz"}, fakeserver)
    assert None == ret
    assert len(fakeserver.slack.posted_reactions) is 1  # one timestamp
    assert len(list(fakeserver.slack.posted_reactions.values())[0]) is 2 # two reactions
    assert len(fakeserver.slack.posted_messages) is 1  # the question and the two answers is a single message
