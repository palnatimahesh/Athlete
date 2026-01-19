import streamlit as st
import datetime
import pandas as pd
import os

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(page_title="Bulletproof Athlete v8", page_icon="🛡️", layout="wide")

HISTORY_FILE = "workout_history.csv"

# --- HELPER: HISTORY MANAGEMENT ---
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(columns=["Date", "Phase", "Mood", "Completed"])
    return pd.read_csv(HISTORY_FILE)

def save_history(date, phase, mood, completed):
    df = load_history()
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
    streak = 0
    current_date = today if not df[df["Date"] == today].empty else today - datetime.timedelta(days=1)
    
    for date in df["Date"]:
        if date == current_date:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        elif date > current_date: continue
        else: break
    return streak

def get_youtube_link(name):
    clean_name = name.split("(")[0].strip()
    return f"https://www.youtube.com/results?search_query={clean_name.replace(' ', '+')}+exercise+form"

# --- CSS STYLING ---
st.markdown("""
<style>
    .banner { padding: 20px; border-radius: 12px; color: white; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .build { background: linear-gradient(135deg, #2E7D32, #1B5E20); }
    .shred { background: linear-gradient(135deg, #C62828, #B71C1C); }
    .flow { background: linear-gradient(135deg, #1565C0, #0D47A1); }
    .repair { background: linear-gradient(135deg, #F57C00, #E65100); }
    .recovery { background: linear-gradient(135deg, #607D8B, #455A64); }
    .alt-text { color: #d32f2f; font-size: 0.85em; font-style: italic; display: block; }
    .tempo-tag { background-color: #e3f2fd; color: #1565c0; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
    .bible-card { background-color: #f1f8e9; padding: 15px; border-radius: 10px; border-left: 5px solid #558b2f; margin-bottom: 10px; }
    .core-box { background-color: #f8f9fa; border-left: 5px solid #343a40; padding: 15px; border-radius: 0 8px 8px 0; margin-top: 20px; }
    a { text-decoration: none; font-weight: bold; color: #0288D1; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
# Based on the Category of the day (Lower, Push, Pull)

WARMUPS = {
    "Lower": [ # For Leg Days
        {"name": "90/90 Hip Switch", "time": "2 mins"},
        {"name": "Leg Swings (Front/Side)", "time": "15 reps"},
        {"name": "World's Greatest Stretch", "time": "5 reps/side"},
        {"name": "Glute Bridges", "time": "20 reps"}
    ],
    "Push": [ # For Chest/Shoulder Days
        {"name": "Arm Circles", "time": "30 secs"},
        {"name": "Band Pull-Aparts", "time": "20 reps"},
        {"name": "Thoracic Rotations", "time": "10 reps/side"},
        {"name": "Scapular Pushups", "time": "15 reps"}
    ],
    "Pull": [ # For Back Days
        {"name": "Cat-Cow", "time": "1 min"},
        {"name": "Dead Hang", "time": "30 secs"},
        {"name": "Band Pass-Throughs", "time": "15 reps"},
        {"name": "Bird-Dog", "time": "10 reps"}
    ],
    "Mobility": [ # For Rest/Recovery
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
# 3. THE "IRON BIBLE" (Knowledge Bank)
# ==========================================
# This maps exercises to their target muscles and specific stretches
EXERCISE_BIBLE = {
    "Goblet Squat": {"Muscle": "Quads & Glutes", "Stretch": "Couch Stretch", "Cue": "Elbows inside knees. Chest up."},
    "Trap Bar Deadlift": {"Muscle": "Posterior Chain", "Stretch": "Seated Hamstring Fold", "Cue": "Hips low. Drive floor away."},
    "Copenhagen Plank": {"Muscle": "Adductors (Inner Thigh)", "Stretch": "Butterfly Stretch", "Cue": "Squeeze top leg UP into bench."},
    "Seated DB Press": {"Muscle": "Front Delts", "Stretch": "Hands-Clasped Behind Back", "Cue": "Ribcage down. Don't arch back."},
    "Face Pulls": {"Muscle": "Rear Delts / Rotator Cuff", "Stretch": "Cross-Body Arm Stretch", "Cue": "Pull to forehead. Thumbs back."},
    "Chest Supported Row": {"Muscle": "Lats & Rhomboids", "Stretch": "Dead Hang", "Cue": "Drive elbows back. Squeeze spine."},
    "Cable Pull-Throughs": {"Muscle": "Glutes & Hams", "Stretch": "Pigeon Pose", "Cue": "Reach through legs. Snap hips forward."}
}

# --- HOME ALTERNATIVES (Bodyweight) ---
HOME_ROUTINES = {
    "Lower": [{"name": "BW Squat (Slow)", "sets": "4x20", "tempo": "3-1-1", "alt":"-"}, {"name": "Lunges", "sets": "3x15", "tempo": "2-0-1", "alt":"-"}, {"name": "Glute Bridge", "sets": "3x20", "tempo": "Hold", "alt":"-"}],
    "Push": [{"name": "Pushups", "sets": "4xF", "tempo": "2-0-1", "alt":"-"}, {"name": "Pike Pushups", "sets": "3x10", "tempo": "Slow", "alt":"-"}, {"name": "Dips", "sets": "3x15", "tempo": "Slow", "alt":"-"}],
    "Pull": [{"name": "Door Row", "sets": "4x15", "tempo": "Squeeze", "alt":"-"}, {"name": "Superman", "sets": "3x45s", "tempo": "Hold", "alt":"-"}, {"name": "Scap Retract", "sets": "3x20", "tempo": "Hold", "alt":"-"}]
}

# --- WORKOUT DATA (FOUNDATION) ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Theme": "Fix Back. Fire Adductors.", "Class": "repair",
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
    }
    # (Shred and Flow seasons hidden for brevity but logic remains same)
}

# --- LOGIC FUNCTIONS ---
def get_daily_plan(data_source, day_name, is_home):
    gym_plan = data_source["Routine"].get(day_name, {"Focus": "Active Recovery", "Type": "Recovery", "Category": "Mobility", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-"}], "Core": []})
    
    # Dynamic Warmup/Cooldown Selection
    cat = gym_plan.get("Category", "Mobility")
    warmup = WARMUPS.get(cat, WARMUPS["Mobility"])
    cooldown = COOLDOWNS.get(cat, COOLDOWNS["Mobility"])

    if is_home and gym_plan["Type"] == "Gym":
        home_exs = HOME_ROUTINES.get(cat, [{"name": "Mobility Flow", "sets": "20m", "tempo": "-", "alt": "-"}])
        return {"Focus": f"Home: {gym_plan['Focus']}", "Type": "Home", "Exercises": home_exs, "Core": gym_plan.get("Core", []), "Warmup": warmup, "Cooldown": cooldown}
    
    return {**gym_plan, "Warmup": warmup, "Cooldown": cooldown}

def ai_coach(day_count, mode, mood):
    if mode == "Infinity Loop (Forever)" and day_count < 180: return "⚠️ **LOGIC ERROR:** You aren't ready for Infinity. Switch to Foundation.", False
    if mood == "Injured / Pain": return "🚨 **INJURY:** Gym Cancelled. Rehab Loaded.", True
    if mood == "Tired / Low Energy": return "📉 **ADJUST:** Reduce weight 20%.", False
    return "✅ **GO MODE:** Attack the tempo.", False

# --- MAIN APP ---
def main():
    st.title("🛡️ Bulletproof Athlete v8.0")
    
    # TABS FOR MAIN NAVIGATION
    tab_workout, tab_bible, tab_history = st.tabs(["🏋️ Daily Workout", "📖 The Iron Bible", "📜 History"])

    # --- SIDEBAR ---
    st.sidebar.header("⚙️ Profile")
    days_active = st.sidebar.number_input("Days Active", min_value=1, value=1)
    location = st.sidebar.radio("📍 Location", ["Gym", "Home"])
    mode = st.sidebar.selectbox("Mode", ["Foundation (First 6 Months)", "Infinity Loop (Forever)"])
    
    # Select Data
    current_data = FOUNDATION_PHASES["Phase 1: Structural Repair"]
    if mode == "Infinity Loop (Forever)":
        current_data = INFINITY_SEASONS["BUILD (Strength)"] # Default for demo
    
    # Meds
    st.sidebar.divider()
    st.sidebar.header("💊 Stack")
    with st.sidebar.expander("Morning"): st.checkbox("L-Carnitine"); st.checkbox("NMN")
    with st.sidebar.expander("Breakfast"): st.checkbox("Omega3"); st.checkbox("B12/C"); st.checkbox("Vit E")
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
        
        if st.button("Log Workout"):
            save_history(datetime.date.today(), mode, mood, "Yes")
            st.success("Saved!")

        today_name = datetime.datetime.now().strftime("%A")
        st.header(f"📅 {today_name} Protocol")
        
        plan = get_daily_plan(current_data, today_name, location == "Home")
        
        # Banner
        css = "repair" if plan["Type"] != "Recovery" else "recovery"
        st.markdown(f"<div class='banner {css}'><h3>{plan['Focus']}</h3></div>", unsafe_allow_html=True)

        if override:
            st.write("### 🚑 Emergency Rehab Routine")
            st.write("1. Pillow Squeeze Bridge (3x15)\n2. Prone Cobra (3x45s)\n3. Bird Dog (3x10)")
        else:
            # DYNAMIC WARMUP
            if plan["Type"] != "Recovery":
                with st.expander("🔥 Dynamic Warmup (Specific)", expanded=True):
                    for w in plan["Warmup"]: st.checkbox(f"**{w['name']}** ({w['time']})")

            # EXERCISES
            st.subheader("🏋️ Routine")
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
            
            # CORE
            if plan["Core"]:
                st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
                for c in plan["Core"]: st.checkbox(f"{c['name']} ({c['sets']})")
                st.markdown("</div>", unsafe_allow_html=True)

            # DYNAMIC COOLDOWN
            if plan["Type"] != "Recovery":
                st.subheader("❄️ Targeted Cooldown")
                st.caption(f"Stretches specifically for {plan.get('Category', 'Full Body')}")
                for c in plan["Cooldown"]: 
                    st.checkbox(f"**{c['name']}** ({c['time']}) - *Targets: {c.get('target','')}*")

    # --- TAB 2: THE IRON BIBLE ---
    with tab_bible:
        st.header("📖 The Exercise Encyclopedia")
        st.caption("Search for any movement to see the target muscle and the specific 'Counter-Stretch'.")
        
        search = st.text_input("🔍 Search Exercise (e.g., Squat, Deadlift)", "")
        
        # Filter Bible
        results = {k: v for k, v in EXERCISE_BIBLE.items() if search.lower() in k.lower()}
        
        if not results:
            st.warning("No exercises found. Try searching 'Squat' or 'Press'.")
        
        for name, data in results.items():
            st.markdown(f"""
            <div class="bible-card">
                <h3>{name}</h3>
                <p><strong>💪 Target Muscle:</strong> {data['Muscle']}</p>
                <p><strong>🧘 Specific Counter-Stretch:</strong> {data['Stretch']}</p>
                <p><strong>💡 Pro Cue:</strong> <em>"{data['Cue']}"</em></p>
                <a href="{get_youtube_link(name)}" target="_blank">📺 Watch Demo Video</a>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("---")
        st.write("### 🖼️ Anatomical Reference")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Anterior_view_of_muscles.svg/800px-Anterior_view_of_muscles.svg.png", caption="Front Anatomy", width=300)

    # --- TAB 3: HISTORY ---
    with tab_history:
        st.header("📜 Workout Log")
        df = load_history()
        if df.empty:
            st.info("No workouts logged yet.")
        else:
            st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
