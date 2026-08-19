# Kinky SMS system - random personality-tuned messages based on affection tier.
# Tiers: 30+ sweet, 50+ flirty/picant, 75+ kinky/adult.

init python:

    # Each character gets three tiers of messages tuned to their personality.
    KINKY_SMS_POOLS = {
        "marcus": {
            "sweet": [
                "Hey champ, hope your day's treating you right.",
                "Saw a dog that looked like you and almost texted it a pic.",
                "You up? Thought about telling you the hot water thing was actually my fault. It wasn't.",
                "Left a slice of pizza on your doormat. No notes, no questions.",
                "The stairwell smells like your coffee this morning. I'm not complaining.",
            ],
            "flirty": [
                "Can't stop thinking about how you handled that lock. Smooth operator.",
                "If you need an excuse to skip work, I'll say you're at mine. You don't have to be.",
                "Your name keeps popping up in my head like a song I can't shake off.",
                "I moved the couch so there's more room for you. That's not a big deal. It is a big deal.",
                "You look good when you're mid-argument with a door handle. Noted.",
            ],
            "kinky": [
                "I miss you daddy",
                "The couch is getting lonely and so am I. Come over?",
                "I've been rewatching that chili scene in my head. You looked good eating, by the way.",
                "Tell me something dirty you did today. Or make up one. I'll believe it.",
                "Your key still jingles when I walk past your door. It's driving me crazy in a good way.",
                "I'm wearing that shirt you liked. You don't have to come over. But you should.",
            ],
        },
        "zoe": {
            "sweet": [
                "You're actually kind of well-proportioned. Not saying that often.",
                "Saw a color today that reminded me of your eyes. It was nice.",
                "I'm not ignoring you. I'm composing my response with the care it deserves.",
                "Your handwriting is worse than mine but I like it more. That's the problem.",
                "The light this morning was doing something to the building and I thought of you.",
            ],
            "flirty": [
                "You have this habit of looking at things like you're trying to solve them. It's... effective on me.",
                "If I drew you, I'd make the jawline a little more aggressive. You deserve that kind of attention.",
                "I keep sketching your hands. Don't ask why.",
                "You exist in my peripheral vision even when you're not here. It's becoming a structural issue.",
                "Your silence is actually very good composition. Negative space and all that.",
            ],
            "kinky": [
                "You're my favorite subject and I don't even like most people",
                "Come over. I'll draw you in one piece this time. Maybe two pieces.",
                "I've been thinking about the weight of your hand on my hip. It's a good composition.",
                "Stop being so easy to want. It's ruining my focus.",
                "If you touch me while I'm sketching, I'll put it in the piece. You'll be immortal and slightly naked.",
                "You're the only person who makes me want to stop analyzing and just feel things. It's terrifying.",
            ],
        },
        "nora": {
            "sweet": [
                "You left a napkin at the counter. I'm keeping it. It's got your coffee ring on it and I like that.",
                "The regulars ask about you. I tell them 'the one who actually tips'. They're impressed.",
                "I saved you a seat by the window. No pressure.",
                "Your usual is ready if you want to swing by. The milk's still good, unlike my patience with the espresso machine.",
                "You hum while you drink your coffee. I noticed. I'm not saying that in a weird way. Slightly weird way.",
            ],
            "flirty": [
                "You always order the same thing. I've started to think it's a love language.",
                "If you come in today, I'm making your drink extra strong. You look like you need it. And so do I.",
                "I caught myself smiling at the register because someone walked in and it wasn't you but almost was.",
                "Your hands are very good at holding a mug. I've been thinking about that more than is professional.",
                "The back room has better acoustics for what I want to say to you. Come after close.",
            ],
            "kinky": [
                "Come in after close. The espresso machine is off and my standards are lower.",
                "I keep a spare key under the mat. You know which one. You don't have to pretend you don't.",
                "You taste like dark roast and I'm not being poetic, I'm being specific.",
                "The back room has better lighting for what I want to do with your hair.",
                "I've been rehearsing how to say this without blushing. You're in my head every time the bell above the door rings.",
                "Your coffee ring on my counter is basically a claim. I'm accepting it.",
            ],
        },
    }

    # Characters eligible for kinky SMS (must be met and have affection >= 30).
    KINKY_SMS_CHARACTERS = ["marcus", "zoe", "nora"]

    # Probability of sending a message per character per day check.
    KINKY_SMS_DAILY_CHANCE = 0.35


def kinky_sms_tier(affection):
    """Return the tier string for a given affection value."""
    if affection >= 75:
        return "kinky"
    elif affection >= 50:
        return "flirty"
    elif affection >= 30:
        return "sweet"
    else:
        return None


def kinky_sms_pick_message(char_id, tier):
    """Pick a random message from the pool for a character and tier."""
    import random
    pools = KINKY_SMS_POOLS.get(char_id)
    if not pools or tier not in pools:
        return None
    msgs = pools[tier]
    if not msgs:
        return None
    return random.choice(msgs)


def kinky_sms_daily_check():
    """
    Called once per day. For each eligible character, roll the daily chance.
    If it passes and affection is >= 30, send a tier-appropriate SMS to the phone inbox.
    Returns list of (char_id, message_text) tuples that were sent.
    """
    import random
    sent = []
    for char_id in KINKY_SMS_CHARACTERS:
        # Get affection from store (fallback to 0 if not set).
        aff_key = char_id + "_affection"
        affection = getattr(store, aff_key, 0)
        tier = kinky_sms_tier(affection)
        if tier is None:
            continue
        if random.random() > KINKY_SMS_DAILY_CHANCE:
            continue
        msg = kinky_sms_pick_message(char_id, tier)
        if msg is None:
            continue
        # Add to phone inbox. The phone system stores messages as a list of dicts.
        if not hasattr(store, "phone_inbox"):
            store.phone_inbox = []
        store.phone_inbox.append({
            "sender": char_id,
            "text": msg,
            "tier": tier,
        })
        sent.append((char_id, msg))
    return sent
