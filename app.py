from flask import Flask, render_template, request
from rules import (
    rule_hashtags,
    story_based_hashtags,
    location_based_hashtags,
    clean_hashtags,
    add_emojis,
    filter_boring_hashtags,
    rank_hashtags
)
from gpt_engine import gpt_hashtags

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hashtags = []

    # ✅ DEFAULT VALUES (CRITICAL FIX)
    bride_name = ""
    groom_name = ""
    bride_city = ""
    groom_city = ""
    wedding_city = ""
    story = ""
    use_emojis = True

    if request.method == "POST":
        # Read form inputs
        bride_name = request.form.get("bride_name", "")
        groom_name = request.form.get("groom_name", "")
        bride_city = request.form.get("bride_city", "")
        groom_city = request.form.get("groom_city", "")
        meet_type = request.form.get("meet_type", "")
        vibe = request.form.get("vibe", "")
        wedding_city = request.form.get("wedding_city", "")
        story = request.form.get("story", "")
        action = request.form.get("action", "generate")
        use_emojis = request.form.get("use_emojis") == "on"

        # 👉 OPTION A: Create internal synthetic caption
        caption = f"""
        Wedding of {bride_name} and {groom_name}
        Bride from {bride_city}, Groom from {groom_city}
        Wedding city: {wedding_city}
        {story}
        """

        # Rule-based layers
        rule_tags = rule_hashtags(caption)
        story_tags = story_based_hashtags(story)
        location_tags = location_based_hashtags(wedding_city)

        # GPT-based hashtags
        gpt_tags = gpt_hashtags(
            bride_name,
            groom_name,
            bride_city,
            groom_city,
            wedding_city,
            story=f"{story}.Met via: {meet_type}. Vibe: {vibe}",
            tone="fun"
        )

        # Merge sources
        raw_hashtags = location_tags + story_tags + rule_tags + (gpt_tags or [])

        # Deduplicate & basic clean
        cleaned = clean_hashtags(list(dict.fromkeys(raw_hashtags)))

        # Light filter only
        filtered = filter_boring_hashtags(cleaned)

        # Rank by quality
        ranked = rank_hashtags(filtered, bride_name, groom_name)

        # Final output (limit but not starve)
        final_hashtags = ranked[:15]

        hashtags = add_emojis(final_hashtags) if use_emojis else final_hashtags

    return render_template(
        "index.html",
        hashtags=hashtags,
        bride_name=bride_name,
        groom_name=groom_name,
        bride_city=bride_city,
        groom_city=groom_city,
        meet_type=meet_type if request.method == "POST" else "",
        vibe=vibe if request.method == "POST" else "",
        wedding_city=wedding_city,
        story=story,
        use_emojis=use_emojis
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

