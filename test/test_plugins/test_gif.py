# -*- coding: UTF-8 -*-
import os
import sys

from nose.tools import eq_
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from gif import on_message

# The set of valid gifs given the bananas fixture
bananas_gifs = [u'http://fc05.deviantart.net/fs71/f/2012/269/a/b/i_heart_banana_by_mnrart-d5fyx04.gif', u'http://www.angelfire.com/pa5/anastasiaandbob4/banana.gif', u'http://newsimg.ngfiles.com/170000/170422_dancing_banana.gif', u'http://fc05.deviantart.net/fs71/f/2013/176/3/e/banana_jam_by_hat_kid-d6anoqh.gif', u'http://www.webweaver.nu/clipart/img/misc/food/banana.gif', u'http://www.sherv.net/cm/emo/funny/2/big-dancing-banana-smiley-emoticon.gif', u'http://4.bp.blogspot.com/-pPLoyosI_Zo/VJ12aP5QpyI/AAAAAAAADCY/XZvWpC0xc4E/s1600/banana-gif.gif', u'http://3.bp.blogspot.com/-71EXQ4bvCeA/U17dnGe4kzI/AAAAAAAABmk/YDBtHjZOBjQ/s1600/gif-banana.gif', u'http://byt.wpengine.netdna-cdn.com/wp-content/uploads/2014/09/banana-dolphin-and-boy.gif', u'http://www.animatedimages.org/data/media/330/animated-banana-image-0031.gif', u'http://ww2.valdosta.edu/~kabehland/gobananas.gif', u'http://volweb.utk.edu/SCHOOL/sweetwjh/dancing%20banana.gif', u'http://www.webweaver.nu/clipart/img/misc/food/fruit/bunch-of-bananas.gif', u'http://www.thedailyquarterly.com/articles/wp-content/uploads/2013/11/DancingBanana.gif', u'http://sagworks.files.wordpress.com/2011/07/071011-banana-animation.gif', u'http://joedale.typepad.com/photos/uncategorized/2008/05/29/bananas.gif', u'http://cdn2.scratch.mit.edu/get_image/gallery/217706_170x100.png?v=1371138299.28', u'http://runeatrepeat.com/wp-content/uploads/2015/01/banana-time-running-blog.gif', u'http://www.comevisit.com/chuckali/bananas.gif', u'http://www.sweetcomments.net/images/random/go-bananas.gif']

def test_gif():
    with vcr.use_cassette('test/fixtures/gif_bananas.yaml'):
        ret = on_message({"text": u"!gif bananas"}, None)
        assert ret in bananas_gifs

def test_unicode():
    with vcr.use_cassette('test/fixtures/gif_unicode.yaml'):
        ret = on_message({"text": u"!gif Mötörhead"}, None)
        # not blowing up == success, for our purposes
