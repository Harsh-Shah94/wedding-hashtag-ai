BASIC_STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "for", "on", "with", "a", "an",
    "from", "by", "at", "this", "that", "it", "as", "are", "was", "were"
}

import re
from collections import Counter

def rule_hashtags(text, top_n=5):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in BASIC_STOPWORDS]
    common = Counter(words).most_common(top_n)
    return ["#" + word.capitalize() for word, _ in common]

def extract_names(text):
    words = text.split()
    names = []

    for w in words:
        if w.istitle() and len(w) > 2:
            names.append(w)

    # remove common non-name words
    blacklist = ["Wedding", "Engagement", "Reception", "With", "And", "Of"]
    names = [n for n in names if n not in blacklist]

    return list(dict.fromkeys(names))[:2]

def couple_hashtags(names):
    if len(names) < 2:
        return []

    n1, n2 = names[0], names[1]

    return [
        f"#{n1}Weds{n2}",
        f"#{n2}Weds{n1}",
        f"#{n1}{n2}Forever",
        f"#{n1}KiShaadi",
        f"#{n1}{n2}Wedding"
    ]

def story_based_hashtags(story):
    story = story.lower()
    tags = []

    if any(word in story for word in ["hinge", "tinder", "bumble", "dating app"]):
        tags += ["#FromSwipeToShaadi", "#MatchToMandap"]

    if any(word in story for word in ["long distance", "ldr", "miles apart"]):
        tags += ["#MilesToMandap", "#DistanceMadeUsCloser"]

    if any(word in story for word in ["school", "college", "classmate"]):
        tags += ["#ClassroomToMandap", "#SchoolLoveStory"]

    if any(word in story for word in ["best friend", "friends first"]):
        tags += ["#FriendshipToForever", "#BestFriendsToSoulmates"]

    return tags

def clean_hashtags(hashtags):
    cleaned = []

    for tag in hashtags:
        # Remove very short or generic hashtags
        if len(tag) < 6:
            continue

        # Remove single-word literal hashtags
        if tag.lower() in [
            "#harsh", "#yoshita", "#met", "#hinge", "#long"
        ]:
            continue

        # Remove hashtags with no creativity (single capitalized word)
        if tag.count("#") == 1 and tag[1:].isalpha() and tag[1:].istitle():
            continue

        cleaned.append(tag)

    return cleaned

LOCATION_METAPHORS = {
    "jaipur": ["#PinkCityPyaar", "#RoyalRishta", "#RajwadaShaadi"],
    "udaipur": ["#LakeCityLove", "#RegalVivaah", "#RoyalUdaipur"],
    "goa": ["#BeachsideBandhan", "#SunsetShaadi", "#GoaWedsLove"],
    "mumbai": ["#CityOfDreamsPyaar", "#MumbaiWeds", "#DreamsToShaadi"],
    "delhi": ["#DilliKiShaadi", "#CapitalCityLove", "#DilSeDelhi"],
    "bangalore": ["#GardenCityLove", "#BangaloreWeds", "#TechMeetsTradition"]
}

def location_based_hashtags(location):
    if not location:
        return []
    key = location.lower().strip()
    return LOCATION_METAPHORS.get(key, [])

EMOJI_MAP = {
    "weds": "💍",
    "shaadi": "💍",
    "wedding": "💍",
    "love": "❤️",
    "pyaar": "❤️",
    "dil": "❤️",
    "royal": "👑",
    "pinkcity": "🌸",
    "jaipur": "🌸",
    "goa": "🌊",
    "beach": "🌊",
    "mile": "✈️",
    "distance": "✈️",
    "forever": "♾️"
}

def add_emojis(hashtags, max_emojis=5):
    enhanced = []
    emoji_count = 0

    for tag in hashtags:
        lower = tag.lower()
        added = False

        for key, emoji in EMOJI_MAP.items():
            if key in lower and emoji_count < max_emojis:
                enhanced.append(f"{tag}{emoji}")
                emoji_count += 1
                added = True
                break

        if not added:
            enhanced.append(tag)

    return enhanced

