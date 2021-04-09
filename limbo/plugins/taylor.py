"""!taylor to get random Taylor Swift Quotes"""
import re
from random import choice

quotes = [
  "People haven't always been there for me but music always has.",
  "I suffer from girlnextdooritis where the guy is friends with you and that's it.",
  "This is a new year. A new beginning. And things will change.",
  "I never want to change so much that people can't recognize me.",
  "I'll never change, but I'll never stay the same either",
  "This is a new year. A new beginning. And things will change.",
  "No matter what happens in life, be good to people. Being good to people is a wonderful legacy to leave behind.",
  "I never want to change so much that people can't recognize me.",
  "I’m intimidated by the fear of being average.",
  "Just be yourself, there is no one better.",
  "It's hard to fight when the fight ain't fair.",
  "The lesson I've learned the most often in life is that you're always going to know more in the future than you know now.",
  "There's more to life than dating the boy on the football team.",
  "And when someone apologizes to you enough times for things they'll never stop doing, I think it's FEARLESS to stop believing them. It's FEARLESS to say \"you're NOT sorry\" and walk away.",
  "If you're horrible to me, I'm going to write a song about it, and you won't like it. That's how I operate.",
  "You can write a book on how to ruin someone’s perfect day.",
  "Being FEARLESS isn't being 100% Not FEARFUL, it's being terrified but you jump anyway...",
  "You're an expert at sorry and keeping the lines blurry.",
  "You can walk away and say \"We don't need this.\" but something in your eyes says \"We can beat this\".",
  "So don't you worry your pretty little mind because people throw rocks at things that shine.",
  "Giving up doesn't always mean your weak sometimes your just strong enough to let go.",
  "The way you walk, way you talk, way you say my name; it's beautiful, wonderful, don't you ever change.",
  "The only one who's got enough of me to break my heart.",
  "I've wanted one thing for my whole life and I'm not going to be that girl who wants one thing her whole life then gets it and complains.",
  "Love is the one wild card.",
  "We should love, not fall in love, because everything that falls, gets broken.",
  "Turns out freedom ain't nothing but missing you...",
  "Life isn't how to survive the storm, it's about how to dance in the rain.",
  "If they don't like you for being yourself, be yourself even more.",
  "I don't let nobody see me wishin' he was mine",
  "But I miss screamin' and fightin' and kissin' in the rain and it's 2 a.m. and I'm cursin' your name. You're so in love the you act insane, and that's the way I loved you.",
  "And I'm dying to know, is it killing you like it's killing me? And the story of us looks a lot like a tragedy now.",
  "So watch me strike a match on all my wasted time. As far as I'm concerned you're just another picture to burn.",
  "I've always been a hugger. If we all hugged more, the world would be a better place :)",
  "I've found time can heal most anything and you just might find who you're supposed to be.",
  "There are two different categories of love. The first category is called a fairytale. The second category of love is called just another lesson.",
  "I haven't had that one great love, which is good. I don't want that to be in the past, I want it to be in the future.",
  "You made a rebel of a careless man's careful daughter. You are the best thing that's ever been mine.",
  "To truly love is to have the courage to walk away and let the other person who wishes to be free go no matter how much it hurts.",
  "I'm captivated by you, baby, like a firework show.",
  "At some point you have to forget about grudges because they only hurt.",
  "In high school, I used to think it was like sooooo cool if a guy had an awesome car. Now none of that matters. These days I look for character and honesty and trust.",
  "So i sneak out to the garden to see you, we keep quiet 'cause we're dead if they knew, so close your eyes, escape this town for a little while.",
  "I love you all so much, I just wanted you to know.",
  "Sparks Fly whenever you smile!",
  "Bring on all the pretenders!",
  "Just because as human beings, what we can't have is what we reply in our head over and over again before we go to sleep.",
  "There are two ways you can go with pain: You can let it destroy you or you can use it as fuel to drive you...",
  "Don’t worry. You may think you’ll never get over it. But you also thought it would last forever.",
  "Real love still happens sometimes. It's not just something we make up when you're nine. I have to believe that. You do too.",
  "Sometimes the person you'd take a bullet for is the person behind the trigger.",
  "I'm shining like fireworks over your sad, empty town.",
  "Romeo save me, I've been feeling so alone. I keep waiting for you, but you never come. Is this in my head? I don't know what to think.",
  "Love always ends differently and it always begins differently - especially with me.",
  "I know my flaws before other people point them out to me.",
  "All you need to do to be my friend is like me.",
  "I forgot that you existed and I thought that it would kill me, but it didn't.",
  "I've got a hundred thrown-out speeches I almost said to you",
  "Remember how I said I'd die for you?",
  "Why'd I have to break what I love so much?",
  "And I ain't gotta tell him, I think he knows",
  "You know I adore you, I'm crazier for you than I was at 16.",
  "I like shiny things, but I'd marry you with paper rings",
  "I don't wanna look at anything else now that I saw you.",
  "Have I known you twenty seconds or twenty years?",
  "Can we always be this close forever and ever?",
  "And I'm highly suspicious that everyone who sees you wants you...",
  "At every table, I'll save you a seat, lover...",
  "I hate accidents except when we went from friends to this.",
  "What doesn't kill me makes me want you more.",
  "Babe, don't threaten me with a good time.",
  "It isn't love, it isn't hate, it's just indifference.",
  "That's the kinda heartbreak time could never mend.",
  "I wanna be defined by the things that I love, not the things I hate.",
  "Your faithless love's the only hoax I believe in",
  "You play stupid games, you win stupid prizes",
  "Please don't ever become a stranger whose laugh I could recognize anywhere",
  "You drew stars around my scars but now I’m bleeding",
  "I could build a castle out of all the bricks they threw at me",
  "Back when you fit in my poems like a perfect rhyme",
  "I never grew up, it's getting so old",
  "You did a number on me, but honestly, baby, who’s counting?",
  "I knew you dancing in your Levis, drunk under a streetlight",
  "And if I get burned, at least we were electrified",
  "You held your pride like you should have held me",
  "I'm still a believer but I don't know why. I've never been a natural, all I do is try, try, try",
  "You said it was a great love, one for the ages, but if the story’s over, why am I still writing pages?",
  "You call me up again just to break me like a promise, so casually cruel in the name of being honest",
  "You can plan for a change in weather and time, but I never planned on you changing your mind",
  "You call me up again just to break me like a promise, so casually cruel in the name of being honest",
  "Take the words for what they are: A dwindling, mercurial high, a drug that only worked the first few hundred times",
  "How many days did I spend thinking 'bout how you did me wrong, wrong, wrong?"
]

def taylor():
    return choice(quotes)
       
def on_message(msg, server):
    """!
    @type server: limbo.server.LimboServer
    """
    text = msg.get("text", "")
    match = re.findall(r"!taylor", text)
    if not match:
        return

    return taylor()


on_bot_message = on_message
