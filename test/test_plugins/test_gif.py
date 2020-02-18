# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from gif import on_message

# The set of valid gifs given the bananas fixture
bananas_gifs = [u'https://i.pinimg.com/originals/1f/b3/74/1fb374f6326f6539a08118c79d3987e0.gif', u'http://www.thepluspaper.com/wp-content/uploads/2016/07/1.gif', u'https://i.pinimg.com/originals/15/cb/72/15cb72f7530d6ba8e881ac54836f292f.gif', u'http://www.fubiz.net/wp-content/uploads/2016/07/Hilarious-and-Surprising-Bananas-GIFs1.gif', u'https://www.chiquita.com/sites/default/files/inline-images/Chiquita_Cheering_fb.gif', u'https://media0.giphy.com/media/GNLJpyWdB77AQ/source.gif', u'https://thumbs.gfycat.com/HugeTerrificClumber-size_restricted.gif', u'https://www.dictionary.com/e/wp-content/uploads/2018/05/banana_emoji.gif', u'https://media.tenor.com/images/d0da2ad434e827f5ecf4544e6dca82af/tenor.gif', u'https://static.designboom.com/wp-content/uploads/2015/07/nendo-banana-package-UNIFRUTTI-designboom-100.gif', u'https://imagesvc.meredithcorp.io/v3/mm/gif?url%3Dhttps%253A%252F%252Fcdn-image.myrecipes.com%252Fsites%252Fdefault%252Ffiles%252Fstyles%252F4_3_horizontal_-_1200x900%252Fpublic%252Ffield%252Fimage%252Fchiquita-sticker-hero.gif%253Fitok%253DEE5WQN-d%26w%3D450%26c%3Dsc%26poi%3Dface%26q%3D85', u'https://i.pinimg.com/originals/f3/27/bd/f327bd3d4cdf09610be97a80484a07a6.gif', u'https://i.ya-webdesign.com/images/vector-banana-4.gif', u'https://i2.wp.com/netart.commons.gc.cuny.edu/wp-content/blogs.dir/3087/files/2018/02/Banana-Rain.gif?resize%3D620%252C618%26ssl%3D1']

def msgobj(msg):
    return {
        "text": msg,
        "channel": "abc123"
    }

def test_gif():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/gif_bananas.yaml'):
        on_message(msgobj(u"!gif bananas"), server)

    url = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]['image_url']
    assert url in bananas_gifs, "{0} not in {1}".format(url, bananas_gifs)

def test_unicode():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/gif_unicode.yaml'):
        on_message(msgobj(u"!gif Mötörhead"), server)
        # not blowing up == success, for our purposes
