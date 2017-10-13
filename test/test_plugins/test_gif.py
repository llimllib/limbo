# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from gif import on_message

# The set of valid gifs given the bananas fixture
bananas_gifs = ['http://byt.wpengine.netdna-cdn.com/wp-content/uploads/2014/09/banana-dolphin-and-boy.gif', 'http://joedale.typepad.com/photos/uncategorized/2008/05/29/bananas.gif', 'http://orig04.deviantart.net/a8fc/f/2012/269/a/b/i_heart_banana_by_mnrart-d5fyx04.gif', 'http://images2.wikia.nocookie.net/illogicopedia/images/3/31/Dancing_Banana.gif', 'http://media.giphy.com/media/PlwtdKszlxyLK/giphy.gif', 'https://s-media-cache-ak0.pinimg.com/originals/81/36/86/813686513bb0ea580e9891fc15ec7678.jpg', 'http://www.webweaver.nu/clipart/img/misc/food/fruit/bunch-of-bananas.gif', 'http://www.animatedimages.org/data/media/330/animated-banana-image-0039.gif', 'http://www.rockinghamremembered.com/images/bananas.gif', 'http://ak-hdl.buzzfed.com/static/2015-09/11/13/imagebuzz/webdr07/anigif_optimized-6124-1441992418-1.gif', 'http://www.picgifs.com/graphics/b/bananas/graphics-bananas-761495.gif', 'http://volweb.utk.edu/SCHOOL/sweetwjh/dancing%20banana.gif', 'http://i.imgur.com/LQzD19d.gif', 'http://media.giphy.com/media/LldwJVCUlhRmg/giphy.gif', 'http://images5.fanpop.com/image/photos/30600000/Banana-gif-bananas-30667445-140-140.gif', 'http://www.sevenoaksart.co.uk/images/banana2.gif', 'http://ww2.valdosta.edu/~kabehland/gobananas.gif', 'http://www.comevisit.com/chuckali/bananas.gif', 'http://media.giphy.com/media/1MqvxsrhMHrGw/giphy.gif', 'https://strengthandsweets.files.wordpress.com/2014/01/bananadance.gif']

def test_gif():
    with VCR.use_cassette('test/fixtures/gif_bananas.yaml'):
        ret = on_message({"text": u"!gif bananas"}, None)
        assert ret in bananas_gifs, "{0} not in {1}".format(ret, bananas_gifs)

def test_unicode():
    with VCR.use_cassette('test/fixtures/gif_unicode.yaml'):
        ret = on_message({"text": u"!gif Mötörhead"}, None)
        # not blowing up == success, for our purposes
