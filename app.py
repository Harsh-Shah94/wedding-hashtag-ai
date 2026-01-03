from flask import Flask, render_template, request
from rules import (
    rule_hashtags,
    story_based_hashtags,
    location_based_hashtags,
    clean_hashtags,
    add_emojis
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
            story,
            tone="fun"
        )

        # Merge, deduplicate, clean
        raw_hashtags = location_tags + story_tags + rule_tags + (gpt_tags or [])
        cleaned = clean_hashtags(list(dict.fromkeys(raw_hashtags)))

        # Apply emoji toggle
        hashtags = add_emojis(cleaned) if use_emojis else cleaned

    return render_template(
        "index.html",
        hashtags=hashtags,
        bride_name=bride_name,
        groom_name=groom_name,
        bride_city=bride_city,
        groom_city=groom_city,
        wedding_city=wedding_city,
        story=story,
        use_emojis=use_emojis
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

