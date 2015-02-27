# -*- coding: UTF-8 -*-
import os
import sys

from nose.tools import eq_
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from image import on_message

# The set of valid images given the bananas fixture
bananas_images = [u'http://foodmatters.tv/images/bananas.jpg', u'http://minionslovebananas.com/images/gallery/preview/Chiquita-DM2-minion-dave-bananas.jpg?w=420&h=356', u'http://upload.wikimedia.org/wikipedia/commons/9/99/Bananas.JPG', u'http://www.medicalnewstoday.com/images/articles/271157-bananas.jpg', u'http://upload.wikimedia.org/wikipedia/commons/4/4c/Bananas.jpg', u'http://guardianlv.com/wp-content/uploads/2013/12/Banana-Bioplastic.jpg', u'http://i2.cdn.turner.com/cnnnext/dam/assets/120604032828-fresh-ripe-bananas-story-top.jpg', u'http://parade.com/wp-content/uploads/2014/08/bananas-ftr.jpg', u'https://www.organicfacts.net/wp-content/uploads/2013/05/Banana21.jpg', u'http://bed56888308e93972c04-0dfc23b7b97881dee012a129d9518bae.r34.cf1.rackcdn.com/sites/default/files/imagecache/310_square/bananas_1.jpg', u'http://higherperspective.com/wp-content/uploads/2014/11/525916-07167048-7f61-11e3-8cdb-58f79d3137a3.jpg', u'https://commoditychainsthatbind.files.wordpress.com/2013/03/bananas-925216.jpeg', u'http://homestead-and-survival.com/wp-content/uploads/2013/03/Grow-Bananas.jpg', u'http://i.huffpost.com/gen/1517660/thumbs/o-BANANAS-facebook.jpg', u'http://www.creativeinyourheart.com/wp-content/uploads/2014/02/Bananas.jpg', u'http://www.undergroundhealth.com/wp-content/uploads/bananastages.jpg', u'http://nutr.ehhs.kent.edu/info/wp-content/uploads/2013/02/file3751250745449.jpg', u'http://mdwincorp.com/wp-content/uploads/2014/11/benefits-of-bananas.jpg', u'http://media.npr.org/assets/img/2011/08/19/istock_000017061174small_wide-69bb958273302dc0a2ecaf5050d94a2beeee3376.jpg?s=6', u'http://angrytrainerfitness.com/wp-content/uploads/2012/08/bananas.jpg']

def test_image():
    with vcr.use_cassette('test/fixtures/image_bananas.yaml'):
        ret = on_message({"text": u"!image bananas"}, None)
        assert ret in bananas_images

def test_unicode():
    with vcr.use_cassette('test/fixtures/image_unicode.yaml'):
        ret = on_message({"text": u"!image Mötörhead"}, None)
        # not blowing up == success, for our purposes
