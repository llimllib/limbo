# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from image import on_message

# The set of valid images given the bananas fixture
bananas_images = [u'https://cdn.mos.cms.futurecdn.net/42E9as7NaTaAi4A6JcuFwG-320-80.jpg', u'https://article.images.consumerreports.org/f_auto/prod/content/dam/CRO%2520Images%25202018/Health/April/CR-Health-Inlinehero-bananas-good-for-you-0418', u'https://s7d6.scene7.com/is/image/bjs/14526?$bjs-Zoom$', u'https://i5.walmartimages.com/asr/209bb8a0-30ab-46be-b38d-58c2feb93e4a_1.1a15fb5bcbecbadd4a45822a11bf6257.jpeg?odnWidth%3D450%26odnHeight%3D450%26odnBg%3Dffffff', u'https://images-na.ssl-images-amazon.com/images/I/61fZ%252BYAYGaL._SL1500_.jpg', u'https://images.agoramedia.com/everydayhealth/gcms/All-About-Bananas-Nutrition-Facts-Health-Benefits-Recipes-and-More-RM-722x406.jpg', u'https://www.kroger.com/product/images/large/front/0000000004011', u'https://i0.wp.com/cdn-prod.medicalnewstoday.com/content/images/articles/271/271157/bananas-chopped-up-in-a-bowl.jpg?w%3D1155%26h%3D1528', u'https://cdn1.sph.harvard.edu/wp-content/uploads/sites/30/2018/08/bananas-1354785_1920-1200x800.jpg', u'http://static1.squarespace.com/static/5a3ed64f4c326d77c53e744a/5a48ed5d0d92977993050ffe/5c44e6630ebbe823a7957ee1/1549560889543/Bananas.jpg?format%3D1500w', u'https://static.toiimg.com/photo/72169067.cms', u'https://www.chiquita.com/sites/default/files/styles/cover_mobile_retinafied/public/2018-07/header_banans_around_world_1536x1024_60.jpg?itok%3DlZqjnwV_', u'https://cosmos-images2.imgix.net/file/spina/photo/13954/100118_Debunked_01.jpg?ixlib%3Drails-2.1.4%26auto%3Dformat%26ch%3DWidth%252CDPR%26fit%3Dmax%26w%3D835', u'https://target.scene7.com/is/image/Target/GUEST_7d6b94b8-2680-4143-bfa4-0216ca301d4d?wid%3D488%26hei%3D488%26fmt%3Dpjpeg']

def msgobj(msg):
    return {
        "text": msg,
        "channel": "abc123"
    }

def test_image():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/image_bananas.yaml'):
        on_message(msgobj(u"!image bananas"), server)

    url = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]['image_url']
    assert url in bananas_images, "{0} not in {1}".format(url, bananas_images)

def test_unicode():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/image_unicode.yaml'):
        on_message(msgobj(u"!image Mötörhead"), server)
        # not blowing up == success, for our purposes
