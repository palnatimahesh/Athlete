import streamlit as st
import datetime
import pandas as pd
import os

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(page_title="Bulletproof Athlete v10", page_icon="🛡️", layout="wide")

HISTORY_FILE = "workout_history.csv"

# --- HELPER: HISTORY MANAGEMENT ---
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(columns=["Date", "Phase", "Mood", "Completed"])
    return pd.read_csv(HISTORY_FILE)

def save_history(date, phase, mood, completed):
    df = load_history()
    # Ensure Date column is string to match input
    df["Date"] = df["Date"].astype(str)
    
    if date in df["Date"].values:
        df.loc[df["Date"] == date, ["Phase", "Mood", "Completed"]] = [phase, mood, completed]
    else:
        new_row = pd.DataFrame({"Date": [date], "Phase": [phase], "Mood": [mood], "Completed": [completed]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

def get_streak(df):
    if df.empty: return 0
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    today = pd.to_datetime(datetime.date.today())
    
    # Check if today is logged
    is_today_logged = not df[df["Date"] == today].empty
    
    streak = 0
    # Start counting from today if logged, otherwise yesterday
    current_date = today if is_today_logged else today - datetime.timedelta(days=1)
    
    for date in df["Date"]:
        if date == current_date:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        elif date > current_date: continue # Skip newer dates if list isn't perfectly sorted
        else: break # Break if gap found
    return streak

def get_youtube_link(name):
    # Clean the name (remove parenthesis) for better search results
    clean_name = name.split("(")[0].strip()
    return f"https://www.youtube.com/results?search_query={clean_name.replace(' ', '+')}+exercise+form"

# --- CSS STYLING (DARK MODE COMPATIBLE) ---
st.markdown("""
<style>
    /* Banners */
    .banner { padding: 20px; border-radius: 12px; color: white; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .build { background: linear-gradient(135deg, #2E7D32, #1B5E20); }
    .shred { background: linear-gradient(135deg, #C62828, #B71C1C); }
    .flow { background: linear-gradient(135deg, #1565C0, #0D47A1); }
    .repair { background: linear-gradient(135deg, #F57C00, #E65100); }
    .recovery { background: linear-gradient(135deg, #607D8B, #455A64); }
    
    /* Text Helpers */
    .alt-text { color: #ff5252 !important; font-size: 0.85em; font-style: italic; display: block; margin-top: 4px; }
    .tempo-tag { background-color: #e3f2fd; color: #1565c0 !important; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
    
    /* Bible Card - Force Dark Text for Readability */
    .bible-card { 
        background-color: #f1f8e9; 
        color: #1a1a1a !important; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #558b2f; 
        margin-bottom: 10px; 
    }
    .bible-card h4 { color: #2e7d32 !important; margin: 0 0 5px 0; }
    .bible-card p { color: #1a1a1a !important; margin: 5px 0; }
    
    /* Core Box */
    .core-box { 
        background-color: #e9ecef; 
        color: #1a1a1a !important; 
        border-left: 5px solid #343a40; 
        padding: 15px; 
        border-radius: 0 8px 8px 0; 
        margin-top: 20px; 
    }
    .core-box h4 { color: #1a1a1a !important; margin: 0 0 10px 0; }
    
    /* Links */
    a { text-decoration: none; font-weight: bold; color: #0288D1 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
WARMUPS = {
    "Lower": [
        {"name": "90/90 Hip Switch", "time": "2 mins"},
        {"name": "Leg Swings (Front/Side)", "time": "15 reps"},
        {"name": "World's Greatest Stretch", "time": "5 reps/side"},
        {"name": "Glute Bridges", "time": "20 reps"}
    ],
    "Push": [
        {"name": "Arm Circles", "time": "30 secs"},
        {"name": "Band Pull-Aparts", "time": "20 reps"},
        {"name": "Thoracic Rotations", "time": "10 reps/side"},
        {"name": "Scapular Pushups", "time": "15 reps"}
    ],
    "Pull": [
        {"name": "Cat-Cow", "time": "1 min"},
        {"name": "Dead Hang", "time": "30 secs"},
        {"name": "Band Pass-Throughs", "time": "15 reps"},
        {"name": "Bird-Dog", "time": "10 reps"}
    ],
    "Mobility": [
        {"name": "Light Walk", "time": "5 mins"},
        {"name": "Joint Circles", "time": "2 mins"}
    ]
}

COOLDOWNS = {
    "Lower": [
        {"name": "Deep Squat Hold", "time": "1 min", "target": "Hips/Ankles"},
        {"name": "Couch Stretch", "time": "2 mins/side", "target": "Quads/Hip Flexors"},
        {"name": "Pigeon Pose", "time": "2 mins/side", "target": "Glutes"}
    ],
    "Push": [
        {"name": "Doorway Pec Stretch", "time": "1 min/side", "target": "Chest"},
        {"name": "Cross-Body Shoulder", "time": "1 min/side", "target": "Rear Delts"},
        {"name": "Overhead Tricep", "time": "1 min/side", "target": "Triceps"}
    ],
    "Pull": [
        {"name": "Child's Pose", "time": "2 mins", "target": "Lats/Lower Back"},
        {"name": "Lat Stretch (Doorframe)", "time": "1 min/side", "target": "Lats"},
        {"name": "Neck Tilts", "time": "1 min", "target": "Traps"}
    ],
    "Mobility": [
        {"name": "Corpse Pose", "time": "5 mins", "target": "CNS Reset"}
    ]
}

# ==========================================
# 3. THE "IRON BIBLE" (COMPLETE)
# ==========================================
EXERCISE_BIBLE = {
    # --- QUADS (Front Thighs) ---
    "Goblet Squat": {"Muscle": "Quads & Core", "Stretch": "Couch Stretch", "Cue": "Hold weight at chest. Elbows inside knees."},
    "Front Squat": {"Muscle": "Upper Quads", "Stretch": "Standing Quad Stretch", "Cue": "Elbows high. Torso vertical."},
    "Leg Press": {"Muscle": "Quads (Isolation)", "Stretch": "Standing Quad Stretch", "Cue": "Feet low on platform for quads. Don't lock knees."},
    "Bulgarian Split Squat": {"Muscle": "Quads & Glutes", "Stretch": "Couch Stretch", "Cue": "Torso upright for quads. Lean forward for glutes."},
    "Walking Lunges": {"Muscle": "Legs (Unilateral)", "Stretch": "Deep Lunge Stretch", "Cue": "Step far enough to get 90-degree knee bend."},
    
    # --- HAMSTRINGS & GLUTES ---
    "Trap Bar Deadlift": {"Muscle": "Full Body / Legs", "Stretch": "Seated Forward Fold", "Cue": "Hips low. Chest up. Push the floor away."},
    "Romanian Deadlift (RDL)": {"Muscle": "Hamstrings", "Stretch": "Toe Touch", "Cue": "Push hips BACK. Soft knees. Stop at mid-shin."},
    "Lying Leg Curls": {"Muscle": "Hamstrings", "Stretch": "Seated Hamstring Stretch", "Cue": "Keep hips glued to the pad. Don't swing."},
    "Cable Pull-Throughs": {"Muscle": "Glutes & Hams", "Stretch": "Pigeon Pose", "Cue": "Reach through legs. Snap hips forward."},
    
    # --- ADDUCTORS (Inner Thigh) ---
    "Copenhagen Plank": {"Muscle": "Adductors", "Stretch": "Butterfly Stretch", "Cue": "Top leg on bench. Bridge up. Squeeze legs together."},
    "Adductor Machine": {"Muscle": "Inner Thigh", "Stretch": "Frog Stretch", "Cue": "Control the opening (eccentric). Don't let weights slam."},
    
    # --- CHEST (Push) ---
    "Seated DB Press": {"Muscle": "Front Delts", "Stretch": "Hands-Clasped Behind Back", "Cue": "Ribcage down. Press slightly forward."},
    "Incline DB Press": {"Muscle": "Upper Chest", "Stretch": "Doorway Pec Stretch", "Cue": "Bench at 30 degrees. Elbows tucked 45 degrees."},
    "Chest Fly": {"Muscle": "Pecs (Stretch)", "Stretch": "Doorway Pec Stretch", "Cue": "Huge hug motion. Slight bend in elbows."},
    "Dips": {"Muscle": "Lower Chest", "Stretch": "Overhead Tricep Stretch", "Cue": "Lean forward for chest. Shoulders below elbows."},
    "Pushups": {"Muscle": "Chest & Core", "Stretch": "Chest Opener", "Cue": "Elbows arrow shape (->), not T-shape."},
    
    # --- BACK (Pull) ---
    "Pullups": {"Muscle": "Lats (Width)", "Stretch": "Lat Prayer", "Cue": "Drive elbows to ribs. Chest to bar."},
    "Lat Pulldowns": {"Muscle": "Lats", "Stretch": "Dead Hang", "Cue": "Thumbless grip. Pull to upper chest."},
    "Chest Supported Row": {"Muscle": "Upper Back", "Stretch": "Cross-Body Stretch", "Cue": "Chest on pad. Squeeze shoulder blades together."},
    "Face Pulls": {"Muscle": "Rear Delts", "Stretch": "Cross-Body Stretch", "Cue": "Pull to forehead. Thumbs point back."},
    
    # --- ARMS ---
    "Barbell Curl": {"Muscle": "Biceps", "Stretch": "Bicep Wall Stretch", "Cue": "Elbows pinned to ribs. No swinging."},
    "Hammer Curl": {"Muscle": "Brachialis", "Stretch": "Wrist Extension", "Cue": "Thumbs up. Squeeze at top."},
    "Skullcrushers": {"Muscle": "Triceps", "Stretch": "Overhead Tricep Stretch", "Cue": "Bar goes behind head. Tucked elbows."},
    "Tricep Pushdown": {"Muscle": "Triceps", "Stretch": "Overhead Tricep Stretch", "Cue": "Elbows glued to side."},

    # --- CORE ---
    "Deadbug": {"Muscle": "Deep Core", "Stretch": "Cobra Pose", "Cue": "Lower back GLUED to floor. Move slow."},
    "Pallof Press": {"Muscle": "Anti-Rotation", "Stretch": "Side Bend", "Cue": "Fight the rotation. Keep hands center."},
    "Plank": {"Muscle": "Stability", "Stretch": "Cobra Pose", "Cue": "Squeeze glutes. Pull elbows towards toes."},
    "McGill Curl Up": {"Muscle": "Core Stiffness", "Stretch": "None", "Cue": "Hands under lower back. Lift head only 1 inch."}
}

# --- HOME ALTERNATIVES ---
HOME_ROUTINES = {
    "Lower": [{"name": "BW Squat (Slow)", "sets": "4x20", "tempo": "3-1-1", "alt":"-"}, {"name": "Lunges", "sets": "3x15", "tempo": "2-0-1", "alt":"-"}, {"name": "Glute Bridge", "sets": "3x20", "tempo": "Hold", "alt":"-"}],
    "Push": [{"name": "Pushups", "sets": "4xF", "tempo": "2-0-1", "alt":"-"}, {"name": "Pike Pushups", "sets": "3x10", "tempo": "Slow", "alt":"-"}, {"name": "Dips", "sets": "3x15", "tempo": "Slow", "alt":"-"}],
    "Pull": [{"name": "Door Row", "sets": "4x15", "tempo": "Squeeze", "alt":"-"}, {"name": "Superman", "sets": "3x45s", "tempo": "Hold", "alt":"-"}, {"name": "Scap Retract", "sets": "3x20", "tempo": "Hold", "alt":"-"}],
    "Mobility": [{"name": "Full Body Flow", "sets": "20m", "tempo": "Flow", "alt":"-"}, {"name": "90/90 Breathing", "sets": "5m", "tempo": "Slow", "alt":"-"}],
    "Rehab": [{"name": "Pillow Squeeze Bridge", "sets": "3x15", "note": "Fixes Adductors.", "alt":"-"}, {"name": "Prone Cobra", "sets": "3x45s", "note": "Fixes Posture.", "alt":"-"}, {"name": "Bird Dog", "sets": "3x10", "note": "Fixes Core.", "alt":"-"}]
}

# --- DATABASES: FOUNDATION & INFINITY ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Theme": "Fix Back. Fire Adductors. Detox.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Lower Body A", "Type": "Gym", "Category": "Lower", "Exercises": [
                {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "tempo": "Hold", "note": "Squeeze legs hard.", "alt": "Side Plank"},
                {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "tempo": "3-1-1", "note": "Torso vertical.", "alt": "Leg Press"},
                {"name": "Cable Pull-Throughs", "sets": "3 x 15", "tempo": "2-0-1", "note": "Hinge hips.", "alt": "DB RDL (Light)"},
                {"name": "Adductor Machine", "sets": "3 x 15", "tempo": "3-0-1", "note": "Control.", "alt": "Cable Adduction"}
            ], "Core": [{"name": "Deadbugs", "sets": "3 x 10"}]},
            "Tuesday": {"Focus": "Upper Push", "Type": "Gym", "Category": "Push", "Exercises": [
                {"name": "Seated DB Press", "sets": "3 x 10", "tempo": "2-1-1", "note": "Protect spine.", "alt": "Machine Press"},
                {"name": "Incline DB Press", "sets": "3 x 12", "tempo": "3-0-1", "note": "Upper chest.", "alt": "Inc Machine"},
                {"name": "Chest Fly", "sets": "3 x 15", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Pec Deck"}
            ], "Core": [{"name": "Pallof Press", "sets": "3 x 15s"}]},
            "Wednesday": {"Focus": "Active Recovery", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Incline Walk", "sets": "30m", "tempo": "Zone 2", "note": "No run.", "alt": "-"}], "Core": []},
            "Thursday": {"Focus": "Lower Body B", "Type": "Gym", "Category": "Lower", "Exercises": [
                {"name": "Lying Leg Curls", "sets": "3 x 12", "tempo": "3-0-1", "note": "Control.", "alt": "Seat Curl"},
                {"name": "DB RDL (Light)", "sets": "3 x 10", "tempo": "3-1-1", "note": "Stop at shins.", "alt": "Back Ext"},
                {"name": "Back Extensions", "sets": "3 x 15", "tempo": "2-1-1", "note": "Glutes.", "alt": "Bird Dog"}
            ], "Core": [{"name": "McGill Curl Up", "sets": "5 x 10s"}]},
            "Friday": {"Focus": "Upper Pull", "Type": "Gym", "Category": "Pull", "Exercises": [
                {"name": "Chest Supp Row", "sets": "3 x 10", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Cable Row"},
                {"name": "Face Pulls", "sets": "4 x 15", "tempo": "Hold", "note": "Posture.", "alt": "Rev Pec Deck"},
                {"name": "Lat Pulldowns", "sets": "3 x 12", "tempo": "2-0-1", "note": "Elbows.", "alt": "Ast Pullup"}
            ], "Core": [{"name": "Plank Taps", "sets": "3 x 45s"}]},
            "Saturday": {"Focus": "Outdoor", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Hike/Swim", "sets": "60m", "tempo": "Fun", "note": "Move.", "alt": "-"}], "Core": []},
            "Sunday": {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Vitamin D3", "sets": "1 Sachet", "tempo": "-", "note": "With Fat.", "alt": "-"}], "Core": []}
        }
    }
}

INFINITY_SEASONS = {
    "BUILD (Strength)": {
        "Theme": "Heavy Loads.", "Class": "build",
        "Routine": {
            "Monday": {"Focus": "Max Lower", "Type": "Gym", "Category": "Lower", "Exercises": [{"name": "Trap Bar Deadlift", "sets": "5x3", "tempo": "X-1-X", "note": "Heavy", "alt": "Sumo DL"}, {"name": "Split Squat", "sets": "3x8", "tempo": "3-0-1", "note": "Deep", "alt": "Lunge"}, {"name": "Leg Press", "sets": "3x10", "tempo": "2-0-1", "note": "Heavy", "alt": "Hack Squat"}], "Core": [{"name": "Weighted Plank", "sets": "3x45s"}]},
            "Wednesday": {"Focus": "Max Upper", "Type": "Gym", "Category": "Push", "Exercises": [{"name": "Seated DB Press", "sets": "5x5", "tempo": "2-0-1", "note": "Strict", "alt": "OH Press"}, {"name": "Weighted Pullup", "sets": "4x6", "tempo": "2-1-1", "note": "Full", "alt": "Lat Pull"}, {"name": "Incline Bench", "sets": "4x8", "tempo": "3-0-1", "note": "Upper", "alt": "DB Inc"}], "Core": [{"name": "Leg Raise", "sets": "3x10"}]},
            "Friday": {"Focus": "Hypertrophy", "Type": "Gym", "Category": "Pull", "Exercises": [{"name": "Front Squat", "sets": "3x8", "tempo": "3-1-1", "note": "Quads", "alt": "Goblet"}, {"name": "RDL", "sets": "3x10", "tempo": "3-1-1", "note": "Hams", "alt": "Curl"}, {"name": "Dips", "sets": "3xF", "tempo": "Slow", "note": "Chest", "alt": "Pushup"}], "Core": [{"name": "Ab Wheel", "sets": "3x10"}]}
        }
    },
    "SHRED (Athlete)": {
        "Theme": "Speed & Agility.", "Class": "shred",
        "Routine": {
            "Monday": {"Focus": "Power", "Type": "Gym", "Category": "Lower", "Exercises": [{"name": "Power Clean", "sets": "5x3", "tempo": "Fast", "note": "Snap", "alt": "DB Snatch"}, {"name": "Box Jump", "sets": "4x5", "tempo": "Fast", "note": "Soft", "alt": "Broad Jump"}, {"name": "Sled Push", "sets": "5x", "tempo": "Max", "note": "Drive", "alt": "Sprint"}], "Core": [{"name": "Slams", "sets": "3x15"}]},
            "Wednesday": {"Focus": "Athletic Upper", "Type": "Gym", "Category": "Push", "Exercises": [{"name": "Plyo Pushup", "sets": "4x8", "tempo": "Fast", "note": "Explode", "alt": "Throw"}, {"name": "Fast Pullup", "sets": "4x8", "tempo": "Fast", "note": "Speed", "alt": "Lat Pull"}, {"name": "Ropes", "sets": "4x30s", "tempo": "Max", "note": "Burn", "alt": "Burpee"}], "Core": [{"name": "Twist", "sets": "3x20"}]},
            "Friday": {"Focus": "Conditioning", "Type": "Gym", "Category": "Pull", "Exercises": [{"name": "KB Swing", "sets": "4x20", "tempo": "Fast", "note": "Hips", "alt": "DB Swing"}, {"name": "Jump Lunge", "sets": "3x15", "tempo": "Fast", "note": "Burn", "alt": "Step Up"}, {"name": "Farm Carry", "sets": "4x40m", "tempo": "Fast", "note": "Grip", "alt": "Suitcase"}], "Core": [{"name": "Climbers", "sets": "3x45s"}]}
        }
    },
    "FLOW (Mobility)": {
        "Theme": "Joint Health.", "Class": "flow",
        "Routine": {
            "Monday": {"Focus": "Hip Mob", "Type": "Gym", "Category": "Lower", "Exercises": [{"name": "ATG Split", "sets": "3x10", "tempo": "Slow", "note": "Knee>Toe", "alt": "Lunge"}, {"name": "Jeff Curl", "sets": "3x10", "tempo": "5-1-5", "note": "Light", "alt": "RDL"}, {"name": "Copenhagen", "sets": "3x45s", "tempo": "Hold", "note": "Adduct", "alt": "Side Plk"}], "Core": [{"name": "Side Bend", "sets": "3x15"}]},
            "Wednesday": {"Focus": "Shoulder Mob", "Type": "Gym", "Category": "Push", "Exercises": [{"name": "Ring Pushup", "sets": "3x12", "tempo": "2-2-1", "note": "Stab", "alt": "DB Press"}, {"name": "Face Pull", "sets": "4x20", "tempo": "Hold", "note": "Rear", "alt": "Band"}, {"name": "Skin Cat", "sets": "3x5", "tempo": "Slow", "note": "Mob", "alt": "Hang"}], "Core": [{"name": "Hollow Hold", "sets": "3x45s"}]},
            "Friday": {"Focus": "Spine Mob", "Type": "Gym", "Category": "Pull", "Exercises": [{"name": "SL RDL", "sets": "3x10", "tempo": "3-1-1", "note": "Bal", "alt": "B-Stance"}, {"name": "Cosack", "sets": "3x8", "tempo": "Slow", "note": "Side", "alt": "Lat Lunge"}, {"name": "Back Ext", "sets": "3x20", "tempo": "Hold", "note": "Endure", "alt": "Superman"}], "Core": [{"name": "Pallof", "sets": "3x15s"}]}
        }
    }
}

# --- LOGIC FUNCTIONS ---
def get_daily_plan(data_source, day_name, is_home):
    gym_plan = data_source["Routine"].get(day_name, {"Focus": "Active Recovery", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-"}], "Core": []})
    
    cat = gym_plan.get("Category", "Mobility")
    warmup = WARMUPS.get(cat, WARMUPS["Mobility"])
    cooldown = COOLDOWNS.get(cat, COOLDOWNS["Mobility"])

    if is_home and gym_plan["Type"] == "Gym":
        home_exs = HOME_ROUTINES.get(cat, [{"name": "Mobility Flow", "sets": "20m", "tempo": "-", "alt": "-"}])
        return {"Focus": f"Home: {gym_plan['Focus']}", "Type": "Home", "Exercises": home_exs, "Core": gym_plan.get("Core", []), "Warmup": warmup, "Cooldown": cooldown}
    
    return {**gym_plan, "Warmup": warmup, "Cooldown": cooldown}

def get_hybrid_plan(day_name, is_home):
    season_key = ""
    short_code = ""
    if day_name == "Monday": season_key = "BUILD (Strength)"; short_code="BUILD"
    elif day_name == "Wednesday": season_key = "SHRED (Athlete)"; short_code="SHRED"
    elif day_name == "Friday": season_key = "FLOW (Mobility)"; short_code="FLOW"
    else: return {"Focus": "Active Recovery", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-"}], "Core": [], "Warmup": WARMUPS["Mobility"], "Cooldown": COOLDOWNS["Mobility"]}, "Recovery", "recovery"

    gym_plan = INFINITY_SEASONS[season_key]["Routine"][day_name]
    cat = gym_plan.get("Category", "Mobility")
    warmup = WARMUPS.get(cat, WARMUPS["Mobility"])
    cooldown = COOLDOWNS.get(cat, COOLDOWNS["Mobility"])
    
    if is_home:
        home_exs = HOME_ROUTINES.get(cat, HOME_ROUTINES["Mobility"])
        return {
            "Focus": f"Home {short_code}", "Type": "Home", 
            "Exercises": home_exs, "Core": gym_plan.get("Core", []),
            "Warmup": warmup, "Cooldown": cooldown
        }, short_code, short_code.lower()
        
    return {**gym_plan, "Warmup": warmup, "Cooldown": cooldown}, short_code, short_code.lower()

def ai_coach(day_count, mode, mood):
    if mode == "Infinity Loop (Forever)" and day_count < 180: return "⚠️ **LOGIC ERROR:** You aren't ready for Infinity. Switch to Foundation.", False
    if mood == "Injured / Pain": return "🚨 **INJURY:** Gym Cancelled. Rehab Loaded.", True
    if mood == "Tired / Low Energy": return "📉 **ADJUST:** Reduce weight 20%.", False
    return "✅ **GO MODE:** Attack the tempo.", False

# --- MAIN APP UI ---
def main():
    st.title("🛡️ Bulletproof Athlete v10.0")
    
    # NAVIGATION TABS
    tab_workout, tab_bible, tab_history = st.tabs(["🏋️ Daily Protocol", "📖 The Iron Bible", "📜 History"])

    # --- SIDEBAR: SETTINGS ---
    st.sidebar.header("⚙️ Profile")
    days_active = st.sidebar.number_input("Days Active", min_value=1, value=1)
    location = st.sidebar.radio("📍 Location", ["Gym", "Home"])
    mode = st.sidebar.selectbox("Mode", ["Foundation (First 6 Months)", "Infinity Loop (Forever)"])
    
    # Data Selection
    current_data = FOUNDATION_PHASES["Phase 1: Structural Repair"]
    is_hybrid = False
    
    if mode == "Infinity Loop (Forever)":
        loop_style = st.sidebar.radio("Infinity Style", ["Seasonal (Focus)", "Hybrid (Weekly Mix)"])
        if loop_style == "Seasonal (Focus)":
            season = st.sidebar.selectbox("Season", list(INFINITY_SEASONS.keys()))
            current_data = INFINITY_SEASONS[season]
        else:
            is_hybrid = True
            st.sidebar.info("🔥 Hybrid Active: Mon=Build, Wed=Shred, Fri=Flow")
    
    # --- SIDEBAR: MEDS ---
    st.sidebar.divider()
    st.sidebar.header("💊 Stack")
    with st.sidebar.expander("Morning (Empty)"): st.checkbox("L-Carnitine"); st.checkbox("NMN")
    with st.sidebar.expander("Breakfast (Fat)"): st.checkbox("Omega3"); st.checkbox("B12/C"); st.checkbox("Vit E")
    with st.sidebar.expander("Night"): st.checkbox("Magnesium"); st.checkbox("Zinc")

    # --- TAB 1: WORKOUT ---
    with tab_workout:
        streak = get_streak(load_history())
        col1, col2 = st.columns([1,3])
        col1.metric("🔥 Streak", f"{streak}")
        
        mood = col2.selectbox("Daily Status", ["Neutral", "Great / Strong", "Tired / Low Energy", "Injured / Pain"])
        msg, override = ai_coach(days_active, mode, mood)
        if override: st.error(msg)
        else: st.info(msg)
        
        if st.button("✅ Log Workout Complete"):
            save_history(datetime.date.today(), mode, mood, "Yes")
            st.success("Streak Updated!")
            
        today_name = datetime.datetime.now().strftime("%A")
        st.header(f"📅 {today_name} Protocol")
        
        # DETERMINE PLAN
        plan = {}
        theme = ""
        css = ""

        if override:
            plan = {"Focus": "Injury Rehab", "Type": "Rehab", "Exercises": HOME_ROUTINES["Rehab"], "Core": []}
            theme = "Emergency Protocol"
            css = "repair"
        elif is_hybrid:
            plan, theme, css = get_hybrid_plan(today_name, location == "Home")
            theme = f"Hybrid Mode: {theme}"
        else:
            plan = get_daily_plan(current_data, today_name, location == "Home")
            if plan:
                theme = current_data.get("Theme", "Foundation")
                css = current_data.get("Class", "repair") if plan["Type"] in ["Gym", "Home"] else "recovery"

        # RENDER
        if plan:
            st.markdown(f"<div class='banner {css}'><h3>{plan['Focus']}</h3><p>{theme}</p></div>", unsafe_allow_html=True)
            
            if plan["Type"] != "Recovery" and not override:
                with st.expander("🔥 Dynamic Warmup", expanded=True):
                    for w in plan["Warmup"]: st.checkbox(f"**{w['name']}** ({w['time']})")
            
            st.subheader(f"🏋️ {plan['Type']} Session")
            for i, ex in enumerate(plan["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3,2,1])
                    link = get_youtube_link(ex['name'])
                    c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                    if "alt" in ex and ex["alt"] != "-": c1.markdown(f"<span class='alt-text'>Busy? {ex['alt']}</span>", unsafe_allow_html=True)
                    c2.markdown(f"**Sets:** {ex.get('sets','?')} | **Tempo:** <span class='tempo-tag'>{ex.get('tempo','-')}</span>", unsafe_allow_html=True)
                    if "note" in ex: c2.caption(f"💡 {ex['note']}")
                    c3.checkbox("Done", key=f"ex_{i}")
                    st.markdown("---")
            
            if plan.get("Core"):
                st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
                for c in plan["Core"]: st.checkbox(f"**{c['name']}** ({c['sets']})")
                st.markdown("</div>", unsafe_allow_html=True)
                
            if plan["Type"] != "Recovery" and not override:
                st.subheader("❄️ Targeted Cooldown")
                for c in plan["Cooldown"]: 
                     st.checkbox(f"**{c['name']}** ({c['time']}) - *Targets: {c.get('target','')}*")

    # --- TAB 2: IRON BIBLE ---
    with tab_bible:
        st.header("📖 The Exercise Encyclopedia")
        search = st.text_input("🔍 Search (e.g., Squat, Bicep)", "")
        
        # ANATOMY REFERENCE - UPDATED LINKS
        with st.expander("🖼️ Anatomy Reference (Click to Expand)"):
            c1, c2 = st.columns(2)
            c1.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Anterior_view_of_muscles.svg/400px-Anterior_view_of_muscles.svg.png", caption="Front View")
            c2.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Posterior_view_of_muscles.svg/400px-Posterior_view_of_muscles.svg.png", caption="Back View")

        results = {k: v for k, v in EXERCISE_BIBLE.items() if search.lower() in k.lower()}
        if not results: st.warning("No exercises found. Showing all.")
        
        # Use full list if search is empty
        display_data = results if search else EXERCISE_BIBLE
        
        for name, data in display_data.items():
            st.markdown(f"""
            <div class="bible-card">
                <h4>{name}</h4>
                <p><strong>💪 Muscle:</strong> {data['Muscle']}</p>
                <p><strong>🧘 Stretch:</strong> {data['Stretch']}</p>
                <p><strong>💡 Cue:</strong> <em>"{data['Cue']}"</em></p>
                <a href="{get_youtube_link(name)}" target="_blank">📺 Watch Demo</a>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 3: HISTORY ---
    with tab_history:
        st.header("📜 Workout Log")
        df = load_history()
        if df.empty: st.info("No workouts yet.")
        else: st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
