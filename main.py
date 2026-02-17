import os
import requests
import json
import random
from datetime import datetime

# GitHub Secrets
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')

VIDEOS_DIR = 'videos'
HISTORY_FILE = 'history.json'

# --- Motorcycle Riding SEO Data Pool (50+ Titles) ---
TITLES = [
    "Epic Motorcycle Ride Adventure Vlog", "Ultimate Bike Riding Experience 4K",
    "Solo Motorcycle Road Trip Journey", "Night Highway Bike Ride Cinematic",
    "High Speed Motorcycle Riding POV", "Best Bike Ride Moments Compilation",
    "Freedom on Two Wheels Ride Video", "Long Drive Motorcycle Vibes",
    "City Night Motorcycle Run", "Extreme Bike Riding Skills",
    "Open Road Motorcycle Adventure", "Fast Lane Bike Ride Story",
    "Powerful Engine Sound Ride", "Urban Motorcycle Rider Life",
    "Dream Bike Long Ride Journey", "Street Racing Style Bike Ride",
    "Full Throttle Motorcycle Run", "Adventure Bike Travel Vlog",
    "Smooth Highway Motorcycle Cruise", "Legendary Rider Bike Moments",
    "Fearless Motorcycle Road Run", "Two Wheels Travel Experience",
    "Bike Life Cinematic Ride", "Endless Road Motorcycle Trip",
    "Speed and Freedom Bike Ride", "Epic Night Motorcycle Journey",
    "Professional Bike Riding Skills", "Wild Road Motorcycle Adventure",
    "Daily Rider Motorcycle Vlog", "Next Level Bike Ride Experience",
    "Highway King Motorcycle Ride", "Super Fast Bike POV Ride",
    "Real Rider Road Story", "Mountain Road Motorcycle Ride",
    "Desert Highway Bike Adventure", "Ultimate Rider Lifestyle Video",
    "Extreme Speed Motorcycle POV", "City Traffic Bike Riding Skills",
    "Dream Ride Motorcycle Journey", "Sunset Highway Bike Ride",
    "Power Bike Engine Sound Ride", "Travel With Motorcycle Vlog",
    "Ultimate Road King Ride", "Bike Rider Cinematic Shots",
    "Unlimited Freedom Bike Life", "Night City Bike Cruise",
    "Adventure Seeker Motorcycle Ride", "Long Distance Bike Travel",
    "Rider Passion Motorcycle Vlog", "Epic Two Wheel Freedom Ride",
    "Smooth & Silent Bike Journey", "Superbike Road Trip Experience",
    "Professional Rider POV Ride", "Fast & Furious Style Bike Run",
    "Daily Motorcycle Ride Routine"
]


# --- Motorcycle Riding SEO Captions Data Pool ---
CAPTIONS = [
    "Feel the freedom of the open road on two wheels.",
    "Every ride tells a new adventure story.",
    "Engine roar and endless highways.",
    "Live fast, ride smart, stay safe.",
    "Two wheels, one passion.",
    "Night rides hit different.",
    "Chasing sunsets with my motorcycle.",
    "Speed meets freedom.",
    "Born to ride, forced to work.",
    "Highway vibes and city lights.",
    "Ride more, worry less.",
    "Fuel, throttle, repeat.",
    "Life is better on a bike.",
    "Adventure begins with ignition.",
    "Freedom feels like this ride.",
    "Exploring roads one mile at a time.",
    "Heartbeat syncs with engine sound.",
    "Keep calm and twist the throttle.",
    "Where the road ends, memories begin.",
    "Riding into the horizon.",
    "Feel the wind, own the road.",
    "No traffic, just vibes.",
    "Dream big, ride bigger.",
    "Every mile is a memory.",
    "Escape the ordinary, ride extraordinary.",
    "Helmet on, world off.",
    "Just me, my bike, and the road.",
    "Midnight rides, endless thoughts.",
    "Power, speed, and balance.",
    "Two wheels move the soul.",
    "Ride safe, ride strong.",
    "The road is my therapy.",
    "Adventure is calling — start the engine.",
    "City streets to mountain peaks.",
    "Freedom has two wheels.",
    "Ride hard, live free.",
    "Engine sound is pure music.",
    "Speed with responsibility.",
    "Journey over destination.",
    "Wind therapy in motion.",
    "Road trips start with bikes.",
    "Throttle therapy activated.",
    "Feel alive, ride today.",
    "The biker lifestyle never stops.",
    "Open roads, open mind.",
    "Driven by passion, powered by fuel.",
    "Night city motorcycle cruise vibes.",
    "Keep riding, keep exploring.",
    "Miles before sleep.",
    "One rider, endless roads.",
    "Speed thrills, safety saves.",
    "Every ride is a new chapter."
]


# --- SEO & Insta Hashtags for USA/Global ASMR ---
# SEO Hashtags: Targeted for US Search & Discovery
SEO_HASHTAGS = "#ASMR #SleepAid #Relaxation #Satisfying #Tingles #OddlySatisfying #StressRelief #DeepSleep #ASMRCommunity #Mindfulness #Sensory #USA #TrendingVideo #BrainMassage"

# Insta SEO Hashtags: Top 5 Viral for Instagram Reels
INSTA_SEO_HASHTAGS = "#asmrvideo #satisfyingvideo #reelsusa #asmrtingles #explorepage"

# 1. History load & 15 days clean-up
history = {}
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            history = data if isinstance(data, dict) else {}
    except:
        history = {}

now = datetime.now()
current_history = history.copy()

for vid, d_str in history.items():
    try:
        if (now - datetime.fromisoformat(d_str)).days >= 15:
            p = os.path.join(VIDEOS_DIR, vid)
            if os.path.exists(p): os.remove(p)
            if vid in current_history: del current_history[vid]
    except: pass

# 2. Pickup new video
if not os.path.exists(VIDEOS_DIR): os.makedirs(VIDEOS_DIR)
all_vids = [f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')]
new_video = next((v for v in all_vids if v not in current_history), None)

if not new_video:
    with open(HISTORY_FILE, 'w') as f: json.dump(current_history, f, indent=4)
    print("No new ASMR video found.")
    exit(0)

# 3. Random Selection
selected_title = random.choice(TITLES)
selected_caption = random.choice(CAPTIONS)

# 4. GitHub Raw Link
raw_video_link = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{VIDEOS_DIR}/{new_video}"

# 5. Telegram Posting Format (Requested Format)
tg_full_msg = (
    f"*{selected_title}*\n"
    f"{selected_caption}\n"
    ".\n"
    ".\n"
    ".\n"
    ".\n"
    f"{SEO_HASHTAGS}"
)

try:
    # Telegram Upload
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    with open(os.path.join(VIDEOS_DIR, new_video), 'rb') as f:
        requests.post(tg_url, data={'chat_id': CHAT_ID, 'caption': tg_full_msg, 'parse_mode': 'Markdown'}, files={'video': f})

    # 6. Webhook Posting
    webhook_data = {
        "video_link": raw_video_link,
        "title": selected_title,
        "caption": selected_caption,
        "seo_hashtags": SEO_HASHTAGS,
        "insta_hashtags": INSTA_SEO_HASHTAGS
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # 7. Update History
    current_history[new_video] = now.isoformat()
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(current_history, f, indent=4)
    print(f"Success: Posted ASMR {new_video} for USA Audience")

except Exception as e:
    print(f"Error: {e}")
