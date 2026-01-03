import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_hashtags(
    bride_name="",
    groom_name="",
    bride_city="",
    groom_city="",
    wedding_city="",
    story="",
    tone="fun"
):
    try:
        prompt = f"""
You are a creative Indian wedding hashtag expert.

Your job:
- Create emotionally engaging, fun, and culturally Indian wedding hashtags
- Focus on wordplay, emotions, and storytelling
- Think like a premium Instagram wedding creator in India

LANGUAGE RULES:
- Use Roman Hindi / Hinglish only (no Hindi script)
- Mix English + Hindi naturally
- Avoid awkward or literal translations

CREATIVE RULES:
- Use Indian wedding slang (shaadi, rishta, pyaar, bandhan, dulhan, dulha)
- Create playful couple-name hashtags
- Use city wordplay and metaphors creatively
- Add rhyme, emotion, and desi charm
- Hashtags must feel personal, not generic

INPUTS:
Bride Name: {bride_name}
Groom Name: {groom_name}
Bride City: {bride_city}
Groom City: {groom_city}
Wedding City: {wedding_city}
Couple Story: {story}
Tone: {tone}

STRICT IDENTITY RULES (VERY IMPORTANT):
- Do NOT invent new names
- Use ONLY these names:
  Bride: {bride_name}
  Groom: {groom_name}
- Do NOT change spellings of names
- Do NOT add any other couple names
- All couple hashtags MUST use the provided names only
- If unsure, repeat the same names rather than inventing new ones

STORY INTELLIGENCE:
- If story suggests dating apps → swipe to shaadi theme
- If story suggests long distance → miles to mandap theme
- If story suggests school/college love → childhood to wedding theme

FOR VARIATION (IMPORTANT FOR “GENERATE MORE”):
- Keep names and cities EXACTLY the same
- Change phrasing, metaphors, and wordplay only
- Do NOT change identities

HASHTAG GUIDELINES:
- Generate 15 hashtags
- Include:
  • Couple-name hashtags
  • City-mashup hashtags (Bride City × Groom City)
  • Wedding-city inspired hashtags
  • Story-driven emotional hashtags
- Avoid plain single-word hashtags
- Keep each hashtag under 25 characters
- Make them Instagram-friendly and shareable

Only return hashtags. No explanations.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        text = response.choices[0].message.content

        # Extract only hashtags safely
        hashtags = [tag for tag in text.split() if tag.startswith("#")]

        return hashtags if hashtags else []

    except Exception as e:
        print("GPT ERROR:", e)
        return []

