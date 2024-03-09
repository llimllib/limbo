# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from gif import on_message

# The set of valid gifs given the bananas fixture
bananas_gifs = [
    "https://www.thespruceeats.com/thmb/j3JUCjFKjju2er6BzsbL1mhHRPE%3D/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Types-of-bananas-4018334-V3-0b1563d7e6e04328b8dc7c48a86721fb.gif",
    "https://www.rd.com/wp-content/uploads/2023/01/GettyImages-938346402-MW-Edit.gif",
    "https://images.eatsmarter.com/sites/default/files/bananas_us_0.gif",
    "https://www.healthshots.com/wp-content/uploads/2019/12/banana.gif",
    "https://miamifruit.org/cdn/shop/files/bananavarietyboxmiamifruit_300x.gif?v%3D1706903566",
    "https://qph.cf2.quoracdn.net/main-qimg-71e3e4dd4f3f6eeeea19ed5306365169",
    "https://www.chiquita.com/wp-content/uploads/2020/03/Make-memories-at-breakfast-6.gif",
    "https://si.wsj.net/public/resources/images/OG-EG460_202004_8SR_20200430092718.gif",
    "https://www.localguidesconnect.com/t5/image/serverpage/image-id/1073068i64783B1241CEC85A/image-size/large?v%3Dv2%26px%3D999",
    "https://scx2.b-cdn.net/gfx/news/2022/ecological-coating-for.gif",
    "https://www.thisiscolossal.com/wp-content/uploads/2016/07/banana-2-big.gif",
    "https://www.bu.edu/lernet/artemis/years/2016/students/AnnaWebsite/Images/banana.gif",
    "https://assets.bonappetit.com/photos/650b3b9f3c38ccae3fa89d55/3:2/w_1686,h_1124,c_limit/bananas-2.gif",
    "https://static.wixstatic.com/media/50ae26_7aebc968b0ff4d139a2f3ef284274160~mv2.gif",
    "http://www.thebahamasweekly.com/uploads/12/BANANA.gif",
    "https://hips.hearstapps.com/delish/assets/16/20/1463601723-banana.gif",
    "https://media.baamboozle.com/uploads/images/78483/1650297704_182548_gif-url.gif",
    "https://i.pinimg.com/originals/d0/56/90/d05690d485adb123ff3d3e836fed290f.gif",
    "https://theprintableconcept.com/cdn/shop/products/ezgif.com-gif-maker-11_360x.gif?v%3D1677370556",
    "https://cdn.dribbble.com/users/515313/screenshots/2947416/dribble_dancing_nanas.gif",
]


def msgobj(msg):
    return {"text": msg, "channel": "abc123"}


def test_gif():
    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/gif_bananas.yaml"):
        on_message(msgobj("!gif bananas"), server)

    url = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]["image_url"]
    assert url in bananas_gifs, "{0} not in {1}".format(url, bananas_gifs)


def test_unicode():
    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/gif_unicode.yaml"):
        on_message(msgobj("!gif Mötörhead"), server)
        # not blowing up == success, for our purposes
