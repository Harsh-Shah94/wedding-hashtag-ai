import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_name_variants(name):
    name = name.strip()
    variants = [name]

    if len(name) >= 4:
        variants.append(name[:4])      # Sunaina → Suna
    if len(name) >= 5:
        variants.append(name[-4:])     # Sunaina → aina
    if name.lower().endswith("na"):
        variants.append("Naina")       # cultural common case

    # Clean & unique
    return list(dict.fromkeys([v.capitalize() for v in variants]))

def get_name_variants(name):
    name = name.strip()
    variants = [name]

    if len(name) >= 4:
        variants.append(name[:4])      # Sunaina → Suna
    if len(name) >= 5:
        variants.append(name[-4:])     # Sunaina → aina
    if name.lower().endswith("na"):
        variants.append("Naina")       # culturally common

    return list(dict.fromkeys([v.capitalize() for v in variants]))

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
        bride_variants = get_name_variants(bride_name)
        groom_variants = get_name_variants(groom_name)
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

Rules:
- Prefer using poetic short-forms for some hashtags
- You may mix full names and short-forms
- Do NOT invent any new name forms
- Do NOT change spellings
- Use ONLY these forms consistently

NAME VARIATION MEMORY (VERY IMPORTANT):

Bride allowed name forms:
{bride_variants}

Groom allowed name forms:
{groom_variants}

CREATIVE RULES:
- Use Indian wedding slang (shaadi, rishta, pyaar, bandhan, dulhan, dulha)
- Create playful couple-name hashtags
- Use city wordplay and metaphors creatively
- Add rhyme, emotion, filmy and desi charm
- Hashtags must feel personal, not generic

INPUTS:
Bride Name: {bride_name}
Groom Name: {groom_name}
Bride City: {bride_city}
Groom City: {groom_city}
Wedding City: {wedding_city}
Couple Story: {story}
Tone: {tone}

--------------------------------------------------
STRICT IDENTITY & NAME SAFETY RULES (VERY IMPORTANT):

- Do NOT invent new person names
- Use ONLY the provided Bride and Groom names
- Do NOT change spellings of the original names
- Do NOT introduce any third names
- Identities must remain constant across generations

--------------------------------------------------
ALLOWED NAME VARIATION RULES (CREATIVE BUT SAFE):

- You MAY create poetic or culturally common short-forms of the provided names
- Short-forms must be clearly derived from the original name
- Examples of VALID poetic shortening:
  • Sunaina → Naina
  • Ananya → Anu
  • Pooja → Poo
  • Rishabh → Rishi
  • Rohit → Roh
- These short-forms may be used ONLY for wordplay and poetry
- If unsure, ALWAYS fall back to the original full name
- Never invent unrelated nicknames or westernized versions

--------------------------------------------------
HINDI / HINGLISH WORDPLAY RULES:

- You may blend name parts with romantic Hindi / Hinglish phrases
- These constructions should feel natural, filmy, and wedding-appropriate
- Examples of acceptable patterns:
  • Jai Se Tere Naina
  • Dil Se Naina
  • Jai Ki Naina
  • Naina Aur Jai
  • Jai Weds Naina
- Avoid forced grammar or awkward phrasing
- Emotional and poetic tone is preferred

--------------------------------------------------
STORY INTELLIGENCE:

- If story suggests dating apps → swipe to shaadi theme
- If story suggests long distance → miles to mandap theme
- If story suggests school/college love → bachpan se bandhan theme

--------------------------------------------------
FOR VARIATION (CRITICAL FOR “GENERATE MORE”):

- Keep Bride Name, Groom Name, and their poetic short-forms CONSISTENT
- Keep all cities EXACTLY the same
- Change phrasing, metaphors, rhyme, and wordplay only
- Do NOT change identities or name fragments once established

--------------------------------------------------
HASHTAG GUIDELINES:

- Generate exactly 15 hashtags
- Include a mix of:
  • Couple-name hashtags (full & poetic short-forms)
  • Hindi / Hinglish wordplay hashtags
  • Bride City × Groom City mashups
  • Wedding City inspired hashtags
  • Story-driven emotional hashtags
- Avoid plain single-word hashtags
- Keep each hashtag under 25 characters
- Make them Instagram-friendly, shareable, and reel-ready

Only return hashtags.  
No explanations.  
No numbering.  
No extra text.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )

        text = response.choices[0].message.content

        hashtags = [tag for tag in text.split() if tag.startswith("#")]
        return hashtags if hashtags else []

    except Exception as e:
        print("GPT ERROR:", e)
        return []

