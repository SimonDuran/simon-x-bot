import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

def generate_posts():
    client = anthropic.Anthropic()
    
    prompt = """Generate exactly 20 tweets for the Twitter account @simonduranalv.

PROFILE: 18-year-old from Colombia. Teen investor, into finance, coding, AI, and anime. Thoughtful, mature tone. Building his life deliberately.

TONE: Direct, calm, slightly detached but warm. Never preachy. Never generic. Sounds like a real person who thinks a lot.

CONTENT MIX:
- 9 reflections/phrases: discipline, dreams, happiness, life, identity, growth, solitude
- 3 "BE BORING" style lists: simple daily habits, direct and clean
- 6 community questions: one-liners, easy to answer, spark engagement
- 2 free posts: whatever feels natural

ANIME PHILOSOPHY TO DRAW FROM (never cite, just absorb the ideas):
- Vinland Saga: true strength, freedom, purpose beyond revenge
- Frieren: patience, the value of time, what we leave behind
- Oshi no Ko: the cost of dreams, reality vs illusion
- One Punch Man: the emptiness after achieving everything, finding meaning
- Mob Psycho: emotion over power, being human
- Classroom of the Elite: strategy, self-awareness, social dynamics
- MHA: what it means to be a hero without talent
- AOT: freedom at any cost, the weight of choices

RULES:
- 100% English
- No hashtags ever
- No emojis ever
- No Pinterest-generic phrases ("believe in yourself", "you got this")
- Lowercase for casual posts, capitalized for serious reflections
- Max 280 characters per tweet
- No contradicting ideas between posts
- Sound like a real 18-year-old who reads and thinks, not a motivational account

EXAMPLES OF GOOD POSTS:
"if you don't spend enough time getting to know yourself, you'll end up absorbing everyone else's definition of you."
"What's one habit that quietly improved your life more than you expected?"
"BE BORING 2026: wake up early, read before your phone, eat the same breakfast, say less, do more."

Return ONLY a JSON array with this format, no other text:
[
  {"id": 1, "type": "reflection", "content": "..."},
  {"id": 2, "type": "list", "content": "..."},
  {"id": 3, "type": "question", "content": "..."}
]
Types: "reflection", "list", "question", "free"
"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text
    posts = json.loads(response_text)
    
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=2)
    
    print(f"Generated {len(posts)} posts successfully")
    return posts

if __name__ == "__main__":
    generate_posts()