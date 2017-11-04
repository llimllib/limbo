# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from stockphoto import on_message

def test_basic():
    with vcr.use_cassette('test/fixtures/stockphoto_basic.yaml'):
        ret = on_message({"text": u"!stock woman eating salad"}, None)
        assert ret in WOMEN_EATING_SALAD

def test_unicode():
    with vcr.use_cassette('test/fixtures/stockphoto_unicode.yaml'):
        ret = on_message({"text": u"!stock übermensch"}, None)
        # not blowing up == success


WOMEN_EATING_SALAD = [
    'https://thumb9.shutterstock.com/display_pic_with_logo/2418950/600370532/stock-photo-beautiful-fit-woman-eating-healthy-salad-after-fitness-workout-600370532.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/4187011/624636659/stock-photo-woman-eating-salad-624636659.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/52013/137318150/stock-photo-woman-eating-salad-137318150.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/2237975/224737129/stock-photo-blonde-woman-eating-green-healthy-tasty-eco-salad-on-city-street-terrace-224737129.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/437830/306417665/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-306417665.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/101595/131983145/stock-photo-close-up-of-beautiful-african-american-woman-eating-salad-at-home-131983145.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/90989/457072153/stock-photo-nice-joyful-woman-eating-salad-457072153.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/437830/557309647/stock-photo-young-woman-eating-salad-and-holding-a-mixed-557309647.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/2104622/288126602/stock-photo-portrait-of-attractive-caucasian-smiling-woman-eating-salad-focus-on-hand-and-fork-soft-backlight-288126602.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/345733/450579463/stock-photo-happy-woman-eating-lunch-in-restaurant-450579463.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/4187011/585252509/stock-photo-woman-eating-salad-585252509.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/97565/157504958/stock-photo-healthy-lifestyle-woman-eating-salad-smiling-happy-outdoors-on-beautiful-day-young-female-eating-157504958.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/91282/172349879/stock-photo-close-up-of-pretty-girl-eating-fresh-vegetable-salad-172349879.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/1619858/622381901/stock-photo-young-and-happy-woman-eating-healthy-salad-sitting-on-the-table-with-green-fresh-ingredients-indoors-622381901.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/90989/457072177/stock-photo-cheerful-woman-eating-vegetable-salad-457072177.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/345733/318311855/stock-photo-young-woman-eating-salad-at-restaurant-and-texting-on-smartphone-318311855.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/137002/513222982/stock-photo-woman-eating-tasty-salad-in-cafe-513222982.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2104622/357958574/stock-photo-portrait-of-attractive-caucasian-smiling-woman-eating-salad-357958574.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/76219/147994505/stock-photo-happy-woman-relaxing-on-the-sofa-eating-salad-in-her-living-room-147994505.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/437830/500868532/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-500868532.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/1619858/622381859/stock-photo-young-and-happy-woman-eating-healthy-salad-sitting-on-the-table-with-green-fresh-ingredients-indoors-622381859.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/437830/306417644/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-306417644.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/503397964/stock-photo-face-portrait-of-young-happy-woman-eating-salad-healthy-lifestyle-with-green-food-503397964.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/557818627/stock-photo-healthy-food-healthy-life-style-with-young-woman-eating-salad-isolated-portrait-on-white-557818627.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2418950/533084047/stock-photo-pregnant-woman-eating-organic-fresh-salad-533084047.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1860644/607298564/stock-photo-eating-607298564.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/437830/542791231/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-542791231.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/169311892/737651344/stock-photo-healthy-eating-737651344.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/3867728/595918643/stock-photo-healthy-food-fresh-vegetable-salad-beautiful-woman-eating-healthy-ingredient-for-good-health-595918643.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/91282/116541337/stock-photo-close-up-of-pretty-girl-eating-fresh-vegetable-salad-116541337.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/91858/110181626/stock-photo-a-beautiful-girl-eating-healthy-food-110181626.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/2543926/531738652/stock-photo-beautiful-young-asian-girl-eating-salad-smiling-happy-girl-eating-healthy-food-531738652.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/1860644/540110359/stock-photo-eating-540110359.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/90989/704523193/stock-photo-happy-positive-women-drinking-wine-704523193.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1619858/291921743/stock-photo-woman-eating-healthy-salad-from-plastic-container-near-the-river-291921743.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/101595/321940568/stock-photo-closeup-shot-of-young-woman-eating-fresh-salad-at-restaurant-healthy-african-girl-eating-salad-and-321940568.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/735778/460675771/stock-photo-happy-woman-eating-salad-in-bikini-outdoor-460675771.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/256624/600509087/stock-photo-woman-having-breakfast-on-window-600509087.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2711341/618610898/stock-photo-mature-lady-cooking-healthy-food-618610898.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/427951/302211986/stock-photo-young-woman-mixing-fresh-salad-oil-recharge-302211986.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2418950/600370538/stock-photo-beautiful-fit-woman-eating-healthy-salad-after-fitness-workout-600370538.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/580987/564719857/stock-photo-cropped-image-of-young-woman-dressed-in-white-t-shirt-showing-broccoli-to-camera-564719857.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2117717/497250184/stock-photo-women-communication-dinner-together-concept-497250184.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2418950/533084080/stock-photo-woman-eating-healthy-salad-after-working-out-at-home-533084080.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/161139997/584553034/stock-photo-woman-s-hands-with-caesar-salad-on-table-in-restaurant-584553034.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/580987/613494896/stock-photo-happy-pregnant-young-woman-sitting-and-eating-fruit-salad-on-sofa-at-home-613494896.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/156673/692472031/stock-photo-woman-has-healthy-business-lunch-in-modern-office-interior-young-beautiful-businesswoman-at-692472031.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/91858/614415680/stock-photo-healthy-food-at-home-happy-woman-is-preparing-the-vegetables-and-fruit-in-the-kitchen-614415680.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/4020958/570035434/stock-photo-fitness-sports-teen-hide-face-with-salad-healthy-sports-food-concept-570035434.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/270058/197242181/stock-photo-healthy-young-woman-eating-green-salad-197242181.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2117717/526804483/stock-photo-women-communication-dinner-together-concept-526804483.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/586093/545789863/stock-photo-office-job-busy-working-businessman-eating-a-salad-while-working-in-office-545789863.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/322021/152884361/stock-photo-beautiful-healthy-woman-eating-salad-dieting-concept-healthy-lifestyle-152884361.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/1860644/545666941/stock-photo-eating-545666941.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/90989/457072180/stock-photo-positive-smiling-woman-eating-salad-457072180.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/254635/673823893/stock-photo-young-woman-cooking-vegetable-salad-673823893.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/330511/149315039/stock-photo-woman-diet-concept-portrait-female-model-hold-green-salad-isolated-portrait-149315039.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/218353/296148656/stock-photo-pretty-woman-taking-a-picture-of-her-healthy-food-296148656.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1860644/540185563/stock-photo-eating-540185563.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/111616/122347225/stock-photo-young-funny-woman-eating-salad-over-white-background-122347225.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/511733434/stock-photo-healthy-food-healthy-life-style-with-young-woman-eating-salad-isolated-portrait-on-white-511733434.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/210376/193640225/stock-photo-young-woman-eating-a-healthy-salad-193640225.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/124564/666032644/stock-photo-young-woman-is-eating-salad-because-she-being-on-vegetable-diet-at-home-666032644.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1207733/528795088/stock-photo-young-woman-cooking-in-the-kitchen-healthy-food-528795088.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/52959/246734332/stock-photo-beautiful-healthy-woman-eating-lettuce-246734332.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/64260/268998200/stock-photo-healthy-eating-dieting-and-people-concept-close-up-of-young-woman-hands-showing-salad-bowl-at-268998200.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/4187011/409883299/stock-photo-eat-409883299.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/427951/314697827/stock-photo-young-woman-eating-fresh-salad-in-modern-kitchen-314697827.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/437830/309513473/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-309513473.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/875983/188281055/stock-photo-woman-smiling-and-eating-salad-in-front-of-a-window-188281055.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/696460/655400392/stock-photo-happy-woman-with-plate-of-vegetables-655400392.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/437830/339249407/stock-photo-young-woman-eating-salad-and-holding-a-mixed-salad-339249407.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/137002/398747407/stock-photo-pregnant-woman-holding-glass-bowl-with-fresh-salad-398747407.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/137278037/stock-photo-woman-diet-concept-portrait-female-model-hold-green-salad-isolated-portrait-137278037.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/158350/604342055/stock-photo-fit-woman-eating-healthy-salad-after-workout-604342055.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/854635/647714542/stock-vector-sad-girl-eating-diet-food-dreaming-of-cake-647714542.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/64260/494862055/stock-photo-pregnancy-healthy-food-and-people-concept-happy-pregnant-woman-eating-vegetable-salad-for-494862055.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/64260/280126973/stock-photo-healthy-eating-dieting-and-people-concept-close-up-of-young-woman-eating-vegetable-salad-at-home-280126973.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/137277953/stock-photo-woman-close-up-smiling-face-diet-food-concept-137277953.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/707224/639464032/stock-photo-charming-beautiful-tan-skin-sporty-asian-woman-with-exercise-suit-hand-hold-fork-and-salad-bowl-639464032.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/120550/556528951/stock-photo-young-woman-eating-mixed-salad-in-kitchen-556528951.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/287881/117848083/stock-photo-portrait-of-healthy-woman-eating-salad-indoor-117848083.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/584183860/stock-photo-casual-dressed-woman-eating-salad-isolated-studio-portrait-long-hair-smiling-girl-584183860.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/696460/626574635/stock-photo-displeased-young-woman-eating-green-leaf-lettuce-tired-of-diet-restrictions-626574635.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/4187011/592178801/stock-photo-woman-eating-salad-592178801.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1619858/622381898/stock-photo-young-and-happy-woman-eating-healthy-salad-sitting-on-the-table-with-green-fresh-ingredients-indoors-622381898.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/101595/342626339/stock-photo-closeup-shot-of-young-woman-eating-salad-with-her-friend-african-girl-smiling-at-lunch-lughing-342626339.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/427951/622785371/stock-photo-young-woman-holding-grocery-shopping-bag-with-vegetables-standing-in-the-kitchen-622785371.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/97565/220432426/stock-photo-business-woman-eating-salad-on-lunch-break-in-city-park-living-healthy-lifestyle-happy-smiling-220432426.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/2247890/569322193/stock-photo-healthy-woman-with-salad-on-white-background-isolated-healthy-lifestyle-569322193.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/137002/615383603/stock-photo-young-beautiful-woman-eating-salad-on-white-background-615383603.jpg',
    'https://thumb7.shutterstock.com/display_pic_with_logo/4187011/592178831/stock-photo-woman-eating-salad-592178831.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/330511/522519847/stock-photo-face-close-up-portrait-of-happy-woman-eating-salad-vegan-life-style-isolated-portrait-522519847.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/788683/550631314/stock-photo-young-woman-eating-a-healthy-fruit-salad-after-workout-fitness-and-healthy-lifestyle-concept-550631314.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1721545/608083310/stock-photo-happy-young-woman-eating-salad-608083310.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/156673/585745388/stock-photo-woman-eating-healthy-business-lunch-in-modern-office-interior-young-beautiful-businesswoman-at-585745388.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/162908094/606319436/stock-photo-woman-eating-salad-looking-at-camera-606319436.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/1207733/608213054/stock-photo-young-woman-cooking-in-the-kitchen-healthy-food-608213054.jpg',
    'https://thumb1.shutterstock.com/display_pic_with_logo/67766/608546498/stock-photo-young-arab-family-in-the-kitchen-608546498.jpg',
    'https://thumb9.shutterstock.com/display_pic_with_logo/2247890/604664126/stock-photo-happy-healthy-woman-with-salad-isolated-healthy-lifestyle-604664126.jpg'
]
