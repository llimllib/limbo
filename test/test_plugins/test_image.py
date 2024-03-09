# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from image import on_message

# The set of valid images given the bananas fixture
bananas_images = [
    "https://images.immediate.co.uk/production/volatile/sites/30/2017/01/Bunch-of-bananas-67e91d5.jpg?quality%3D90%26resize%3D440,400",
    "https://images.everydayhealth.com/images/diet-nutrition/all-about-bananas-nutrition-facts-health-benefits-recipes-and-more-rm-722x406.jpg",
    "https://media.cnn.com/api/v1/images/stellar/prod/120604032828-fresh-ripe-bananas.jpg?q%3Dw_3590,h_2774,x_0,y_0,c_fill",
    "https://hips.hearstapps.com/hmg-prod/images/bananas-royalty-free-image-1702061943.jpg",
    "https://cdn-prod.medicalnewstoday.com/content/images/articles/271/271157/bananas-chopped-up-in-a-bowl.jpg",
    "https://domf5oio6qrcr.cloudfront.net/medialibrary/6372/202ebeef-6657-44ec-8fff-28352e1f5999.jpg",
    "https://draxe.com/wp-content/uploads/2015/01/BananaNutritionThumbnail.jpg",
    "https://media.post.rvohealth.io/wp-content/uploads/2020/09/bananas-732x549-thumbnail.jpg",
    "https://www.health.com/thmb/zvIgtdQscZdYENlsSg1a0LmveJs%3D/2121x0/filters:no_upscale():max_bytes(150000):strip_icc()/Bananas-02809456216b4984b8771f12be063cdf.jpg",
    "https://ip.prod.freshop.retail.ncrcloud.com/resize?url%3Dhttps://images.freshop.ncrcloud.com/produce_bananas/d6b28f69c0414ca28c61935a591654d4_large.png%26width%3D512%26type%3Dwebp%26quality%3D90",
    "https://cdn.mos.cms.futurecdn.net/YDFk8cgmSKu8VYFVedUQ8j.jpg",
    "https://i5.walmartimages.com/asr/3bbb1151-d69a-43fb-b132-47e0bc066307.1f28c1acf3df725a6a39ba4c8738e025.jpeg?odnHeight%3D768%26odnWidth%3D768%26odnBg%3DFFFFFF",
    "https://th-thumbnailer.cdn-si-edu.com/xK6NAJHiv_51fzn5sDiQt0eD5Is%3D/fit-in/1600x0/https://tf-cmsv2-smithsonianmag-media.s3.amazonaws.com/filer/d5/24/d5243019-e0fc-4b3c-8cdb-48e22f38bff2/istock-183380744.jpg",
    "https://www.usatoday.com/gcdn/-mm-/ac688eec997d2fce10372bf71657297ff863814d/c%3D171-0-1195-768/local/-/media/2022/01/25/USATODAY/usatsports/gettyimages-174959827.jpg",
    "https://parade.com/.image/ar_4:3%252Cc_fill%252Ccs_srgb%252Cfl_progressive%252Cq_auto:good%252Cw_1200/MTk3MDYyOTU3MDI3MzA0NzY3/are-bananas-good-for-you.jpg",
    "https://www.theglobeandmail.com/resizer/v2/UY7R46JKR5HHTDH34DXVXI6KZI?auth%3D9a3f2d7281510d7e0f8989bdc3ed02943111bc60c2e009c7e4b9e548d0474c18%26width%3D1500%26height%3D1000%26quality%3D80",
    "https://m.media-amazon.com/images/I/61fZ%2BYAYGaL._AC_UF1000,1000_QL80_.jpg",
    "https://media.tegna-media.com/assets/VERIFY/images/b24f0d90-0844-43d8-97f5-9fc0653c0f65/b24f0d90-0844-43d8-97f5-9fc0653c0f65_750x422.jpg",
    "https://www.forbesindia.com/media/images/2022/Sep/img_193775_bananas.jpg",
    "https://media.npr.org/assets/img/2011/08/19/istock_000017061174small-6ca3bb7c8b6c768b92153932e822623a95065935.jpg",
]


def msgobj(msg):
    return {"text": msg, "channel": "abc123"}


def test_image():
    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/image_bananas.yaml"):
        on_message(msgobj("!image bananas"), server)

    url = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]["image_url"]
    assert url in bananas_images, "{0} not in {1}".format(url, bananas_images)


def test_unicode():
    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/image_unicode.yaml"):
        on_message(msgobj("!image Mötörhead"), server)
        # not blowing up == success, for our purposes
