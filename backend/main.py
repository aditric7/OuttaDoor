import json
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="OuttaDoor API",
    description="Personalized outdoor adventure planner",
    version="1.0.0",
)

# Allows the local frontend to communicate with the backend.
# Restrict origins before deploying the app publicly.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestRequest(BaseModel):
    activity: str = Field(min_length=1, max_length=30)
    duration: str = Field(min_length=1, max_length=30)
    mood: str = Field(min_length=1, max_length=30)


# Each mood/activity combination has three suggested quest steps.
QUEST_TEMPLATES = {
    "Nature": {
        "Relaxing": [
            ("Find your green corner", "Choose a safe, accessible green space and settle in."),
            ("Notice nature's details", "Observe leaves, clouds, birds, or changing light."),
            ("Take a mindful pause", "Put distractions away and enjoy a few quiet moments."),
        ],
        "Active": [
            ("Warm up gently", "Begin with an easy walk along a familiar path."),
            ("Explore the surroundings", "Walk at a comfortable pace and notice the landscape."),
            ("Finish with a stretch", "Slow down and gently stretch if comfortable."),
        ],
        "Curious": [
            ("Become a nature detective", "Look for three different leaf shapes or natural textures."),
            ("Discover small details", "Notice patterns, shadows, sounds, and colours around you."),
            ("Capture one discovery", "Photograph or write down your favourite observation."),
        ],
        "Social": [
            ("Pick a shared green space", "Choose a convenient public park to visit together."),
            ("Play observation bingo", "Take turns spotting interesting plants, birds, or shapes."),
            ("Share your favourite find", "Each person shares one thing they enjoyed noticing."),
        ],
    },
    "Walking": {
        "Relaxing": [
            ("Choose a gentle route", "Pick a familiar path at a comfortable pace."),
            ("Walk without rushing", "Notice the breeze, sounds, and scenery around you."),
            ("Pause and reset", "Find a safe resting spot and enjoy a quiet moment."),
        ],
        "Active": [
            ("Start at an easy pace", "Let your body warm up before increasing your pace."),
            ("Explore a little farther", "Continue along a familiar route within your time limit."),
            ("Cool down", "Slow your pace before finishing your walk."),
        ],
        "Curious": [
            ("Take a different turn", "Try a safe, familiar route you have not explored recently."),
            ("Spot five details", "Look for architecture, plants, colours, or interesting signs."),
            ("Make a mini photo diary", "Capture one or two details that caught your attention."),
        ],
        "Social": [
            ("Invite a walking buddy", "Choose a public route that suits everyone's comfort level."),
            ("Start a conversation", "Take turns sharing a favourite memory or current interest."),
            ("Choose a shared highlight", "Find one interesting thing you both noticed."),
        ],
    },
    "Photography": {
        "Relaxing": [
            ("Find a peaceful view", "Choose a safe spot with pleasant natural light."),
            ("Capture tiny details", "Photograph leaves, shadows, flowers, or textures."),
            ("Choose your favourite frame", "Review your photos and keep the moment you like best."),
        ],
        "Active": [
            ("Explore different angles", "Move around a safe area to find varied perspectives."),
            ("Try three compositions", "Experiment with close-ups, wide shots, and leading lines."),
            ("Review your collection", "Pick your favourite image from the mini photo walk."),
        ],
        "Curious": [
            ("Choose a photo theme", "Try patterns, reflections, colours, or shapes."),
            ("Find five examples", "Look for different interpretations of your theme."),
            ("Create a mini collection", "Choose three photos that tell a small visual story."),
        ],
        "Social": [
            ("Choose a photo challenge", "Agree on a theme such as green, symmetry, or happiness."),
            ("Capture your own version", "Take turns finding different interpretations of the theme."),
            ("Share your favourite shot", "Show each other your favourite image and why you chose it."),
        ],
    },
    "Friends": {
        "Relaxing": [
            ("Pick a comfortable meeting spot", "Choose a familiar public park or outdoor seating area."),
            ("Bring a conversation prompt", "Share favourite memories, future plans, or fun questions."),
            ("Enjoy an unhurried break", "Put your phones aside for a little while, if everyone agrees."),
        ],
        "Active": [
            ("Choose a simple outdoor game", "Try a casual game everyone enjoys."),
            ("Make it a friendly challenge", "Set a light-hearted goal that works for the group."),
            ("Wind down together", "Take a break, hydrate, and decide on a favourite moment."),
        ],
        "Curious": [
            ("Set a mini exploration theme", "Look for interesting architecture, public art, or nature."),
            ("Try a photo scavenger hunt", "Make a list of five things to find in your chosen area."),
            ("Compare your discoveries", "Share what surprised everyone most."),
        ],
        "Social": [
            ("Plan a mini picnic", "Choose a permitted public spot and bring simple snacks."),
            ("Play a group game", "Try charades, word games, or a conversation challenge."),
            ("Make a shared memory", "Take a group photo only if everyone is comfortable."),
        ],
    },
}

MOOD_INTROS = {
    "Relaxing": "A gentle little reset to help you slow down and enjoy the moment.",
    "Active": "A feel-good outing with comfortable movement and a change of scenery.",
    "Curious": "A mini exploration designed to help you notice something new.",
    "Social": "A chance to connect, share a few laughs, and enjoy the outdoors.",
}

DURATION_GUIDANCE = {
    "15 minutes": [
        "Keep the route nearby and the plan simple.",
        "Choose one or two highlights if you are short on time.",
    ],
    "30 minutes": [
        "Leave a little time to get to your chosen spot.",
        "Keep the route manageable so you can finish without rushing.",
    ],
    "1 hour": [
        "Allow time for getting there, exploring, and returning.",
        "Take breaks whenever you need them.",
    ],
    "2 hours": [
        "Plan a comfortable route with time for breaks.",
        "Check travel time and the return journey before setting out.",
    ],
}



def generate_with_gemma(activity, duration, mood):
    prompt = f"""
Create one personalized, safe, practical outdoor quest.

User preferences:
- Activity: {activity}
- Available time: {duration}
- Mood: {mood}

Requirements:
- Match the selected activity, duration, and mood.
- Walking: include an actual walk on a familiar, safe public route.
- Photography: focus on photo subjects and composition.
- Nature: focus on observing nature without disturbing it.
- Friends: include an optional activity to enjoy together.
- Give exactly 3 distinct, actionable steps in a sensible order.
- Each step needs a descriptive, unnumbered title and clear instructions.
- Keep the plan realistic for the available time.
- Never suggest trespassing, isolated locations, or risky activities.
- Do not encourage collecting plants, disturbing wildlife, or littering.
- Include 2 to 4 concise, useful tips and a practical safety reminder.
- Avoid generic filler and repetitive steps.

Return ONLY valid JSON in this exact structure:
{{
  "title": "Creative quest title",
  "intro": "One-sentence introduction",
  "activities": [
    {{"title": "Descriptive title", "detail": "Clear instructions"}},
    {{"title": "Descriptive title", "detail": "Clear instructions"}},
    {{"title": "Descriptive title", "detail": "Clear instructions"}}
  ],
  "tips": ["Useful tip 1", "Useful tip 2"],
  "safety_note": "Brief safety reminder"
}}
"""

    payload = {
        "model": "gemma3:1b",
        "messages": [{"role": "user", "content": prompt}],
        "format": "json",
        "stream": False,
        "options": {"temperature": 0.2}
    }

    for attempt in range(2):
        try:
            request = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))

            quest = json.loads(result["message"]["content"])

            if not isinstance(quest, dict):
                raise ValueError("AI response must be a JSON object")

            for key in ("title", "intro", "safety_note"):
                if not isinstance(quest.get(key), str) or not quest[key].strip():
                    raise ValueError(f"Invalid or empty {key}")

            activities = quest.get("activities")
            if not isinstance(activities, list) or len(activities) != 3:
                raise ValueError("Quest must have exactly 3 steps")

            for step in activities:
                if not isinstance(step, dict):
                    raise ValueError("Each step must be an object")

                for key in ("title", "detail"):
                    if not isinstance(step.get(key), str) or not step[key].strip():
                        raise ValueError(f"Each step needs a non-empty {key}")

            tips = quest.get("tips")
            if (
                not isinstance(tips, list)
                or not 2 <= len(tips) <= 4
                or not all(isinstance(tip, str) and tip.strip() for tip in tips)
            ):
                raise ValueError("Quest must have 2 to 4 non-empty tips")

            print("SUCCESS: Quest generated by local Gemma AI!")
            return quest

        except Exception as error:
            print(f"Gemma attempt {attempt + 1} failed: {error}")

            if attempt == 0:
                payload["messages"].append({
                    "role": "user",
                    "content": (
                        "Your previous response was invalid. Try again. "
                        "Return a JSON object with exactly 3 activities, "
                        "each containing a non-empty title and detail, "
                        "and between 2 and 4 non-empty tips. "
                        "Follow the requested schema exactly."
                    )
                })

    raise ValueError("Gemma failed to generate a valid quest after 2 attempts")

@app.get("/")
def home():
    return {
        "message": "Welcome to OuttaDoor!",
        "status": "running",
    }


@app.post("/generate-quest")
def generate_quest(request: QuestRequest):
    activity = request.activity.strip().title()
    mood = request.mood.strip().title()
    duration = request.duration.strip()

    if activity not in QUEST_TEMPLATES:
        raise HTTPException(
            status_code=422,
            detail="Please choose a supported outdoor activity.",
        )

    if mood not in MOOD_INTROS:
        raise HTTPException(
            status_code=422,
            detail="Please choose a supported mood.",
        )

    if duration not in DURATION_GUIDANCE:
        raise HTTPException(
            status_code=422,
            detail="Please choose a supported duration.",
        )

   
    try:
        quest = generate_with_gemma(activity, duration, mood)
        print("SUCCESS: Quest generated by local Gemma AI!")
        return {
            "title": quest["title"],
            "duration": duration,
            "intro": quest["intro"],
            "activities": quest["activities"],
            "tips": quest["tips"],
            "safety_note": quest["safety_note"],
        }

    except Exception as error:
        print(f"Local AI unavailable or invalid response: {error}")
        # Fall back to the original, reliable templates.
        steps = QUEST_TEMPLATES[activity][mood]

        return {
            "title": f"Your {mood} {activity} Quest",
            "duration": duration,
            "intro": MOOD_INTROS[mood],
            "activities": [
                {"title": title, "detail": detail}
                for title, detail in steps
            ],
            "tips": DURATION_GUIDANCE[duration] + [
                "Bring water and check the weather before leaving.",
                "Choose a safe public area and respect local rules.",
            ],
            "safety_note": (
                "Stay aware of your surroundings, follow local guidance, "
                "and choose activities that feel comfortable for you. "
                "For longer outings, plan your return journey too."
            ),
        }