import streamlit as st
import datetime
import pandas as pd
import os

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(page_title="Bulletproof Athlete v14", page_icon="🛡️", layout="wide")

HISTORY_FILE = "workout_history.csv"

# --- HISTORY FUNCTIONS ---
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(columns=["Date", "Phase", "Mood", "Completed"])
    return pd.read_csv(HISTORY_FILE)

def save_history(date, phase, mood, completed):
    df = load_history()
    df["Date"] = df["Date"].astype(str)
    if date in df["Date"].values:
        df.loc[df["Date"] == date, ["Phase", "Mood", "Completed"]] = [phase, mood, completed]
    else:
        new_row = pd.DataFrame({"Date": [date], "Phase": [phase], "Mood": [mood], "Completed": [completed]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        return True
    return False

def get_streak(df):
    if df.empty: return 0
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    today = pd.to_datetime(datetime.date.today())
    is_today_logged = not df[df["Date"] == today].empty
    streak = 0
    current_date = today if is_today_logged else today - datetime.timedelta(days=1)
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
    .repair { background: linear-gradient(135deg, #F57C00, #E65100); }
    .recovery { background: linear-gradient(135deg, #607D8B, #455A64); }
    .alt-text { color: #d32f2f !important; font-size: 0.9em; font-weight: bold; display: block; margin-top: 5px; }
    .tempo-tag { background-color: #e3f2fd; color: #1565c0 !important; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
    .bible-card { background-color: #f1f8e9; color: #1a1a1a !important; padding: 15px; border-radius: 10px; border-left: 5px solid #558b2f; margin-bottom: 10px; }
    .bible-card h4 { color: #2e7d32 !important; margin: 0 0 5px 0; }
    .bible-card p { color: #1a1a1a !important; margin: 5px 0; }
    .core-box { background-color: #e9ecef; color: #1a1a1a !important; border-left: 5px solid #343a40; padding: 15px; border-radius: 0 8px 8px 0; margin-top: 20px; }
    .core-box h4 { color: #1a1a1a !important; margin: 0 0 10px 0; }
    a { text-decoration: none; font-weight: bold; color: #0288D1 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
WARMUPS = {
    "Lower": [{"name": "90/90 Hip Switch", "time": "2 mins"}, {"name": "Cat-Cow", "time": "1 min"}, {"name": "Glute Bridges", "time": "20 reps"}],
    "Push": [{"name": "Arm Circles", "time": "30 secs"}, {"name": "Band Pull-Aparts", "time": "20 reps"}, {"name": "Scapular Pushups", "time": "15 reps"}],
    "Pull": [{"name": "Cat-Cow", "time": "1 min"}, {"name": "Dead Hang", "time": "30 secs"}, {"name": "Bird-Dog", "time": "10 reps"}],
    "Mobility": [{"name": "Light Walk", "time": "5 mins"}, {"name": "Joint Circles", "time": "2 mins"}]
}

COOLDOWNS = {
    "Lower": [{"name": "Deep Squat Hold", "time": "1 min", "target": "Hips"}, {"name": "Couch Stretch", "time": "2 mins/side", "target": "Quads"}, {"name": "Pigeon Pose", "time": "2 mins/side", "target": "Glutes"}],
    "Push": [{"name": "Doorway Pec Stretch", "time": "1 min/side", "target": "Chest"}, {"name": "Overhead Tricep", "time": "1 min/side", "target": "Triceps"}],
    "Pull": [{"name": "Child's Pose", "time": "2 mins", "target": "Lower Back"}, {"name": "Lat Stretch", "time": "1 min/side", "target": "Lats"}],
    "Mobility": [{"name": "Corpse Pose", "time": "5 mins", "target": "CNS Reset"}]
}

# ==========================================
# 3. DATABASES
# ==========================================

# --- HOME REPAIR ROUTINES (Logic: Matches Gym Biomechanics) ---
HOME_REPAIR = {
    # MONDAY: ADDUCTOR REPAIR (Replacing Gym Adductor Machine)
    "Monday": [
        {"name": "Seated Pillow Squeeze", "sets": "4 x 15s", "tempo": "Max Effort", "alt":"-", "note": "Sit on chair. Squeeze pillow between knees 100% effort. Fires Adductors."},
        {"name": "Copenhagen Plank (Floor)", "sets": "3 x 20s", "tempo": "Hold", "alt":"-", "note": "Top knee on chair. Lift hips. Gold standard for groin strength."},
        {"name": "Bulgarian Split Squat", "sets": "3 x 10/leg", "tempo": "3-1-1", "alt":"-", "note": "Stretches hip flexor while strengthening glute."},
        {"name": "Glute Bridge March", "sets": "3 x 20", "tempo": "Slow", "alt":"-", "note": "Hips up. Lift one leg at a time without hips dropping."}
    ],
    # THURSDAY: LOWER BACK ARMOUR (Replacing Gym Back Extensions)
    "Thursday": [
        {"name": "Superman Hold", "sets": "4 x 30s", "tempo": "Hold", "alt":"-", "note": "Lie on belly. Lift chest and thighs. Squeezes spinal erectors."},
        {"name": "Single Leg RDL (Bodyweight)", "sets": "3 x 12/leg", "tempo": "3-1-1", "alt":"-", "note": "Soft knee. Reach to floor. Forces QL muscle to balance spine."},
        {"name": "Bird-Dog (High Tension)", "sets": "3 x 10/side", "tempo": "Hold 5s", "alt":"-", "note": "Make a fist. Kick heel back hard. Brace core like getting punched."},
        {"name": "Doorframe Rows", "sets": "4 x 15", "tempo": "Squeeze", "alt":"-", "note": "Upper back posture fix."}
    ],
    # UPPER BODY DAYS (Standard Push/Pull)
    "Push": [{"name": "Decline Pushups", "sets": "4xF", "tempo": "2-0-1", "alt":"-", "note": "Feet on couch."}, {"name": "Pike Pushups", "sets": "3x10", "tempo": "Slow", "alt":"-", "note": "Shoulders."}, {"name": "Door Flys", "sets": "3x15", "tempo": "Squeeze", "alt":"-", "note": "Chest."}],
    "Pull": [{"name": "Door Towel Row", "sets": "4x15", "tempo": "Squeeze", "alt":"-", "note": "Lats."}, {"name": "Prone W-Raise", "sets": "3x15", "tempo": "Hold", "alt":"-", "note": "Upper Back."}, {"name": "Scap Retract", "sets": "3x20", "tempo": "Hold", "alt":"-", "note": "Posture."}]
}

# --- GYM FOUNDATION ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Theme": "Fix Back. Fire Adductors. Detox.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Adductor & Glute Repair", "Type": "Gym", "Category": "Lower", "Home_Map": "Monday", "Exercises": [
                {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "tempo": "Hold", "note": "Squeeze legs hard.", "alt": "Side Plank on floor"},
                {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "tempo": "3-1-1", "note": "Torso vertical.", "alt": "Leg Press (Feet High)"},
                {"name": "Cable Pull-Throughs", "sets": "3 x 15", "tempo": "2-0-1", "note": "Hinge hips back.", "alt": "DB RDL (Light)"},
                {"name": "Adductor Machine", "sets": "3 x 15", "tempo": "3-0-1", "note": "Control eccentric.", "alt": "Cable Adduction or Band Squeeze"}
            ], "Core": [{"name": "Deadbugs", "sets": "3 x 10"}]},
            
            "Tuesday": {"Focus": "Upper Push", "Type": "Gym", "Category": "Push", "Home_Map": "Push", "Exercises": [
                {"name": "Seated DB Press", "sets": "3 x 10", "tempo": "2-1-1", "note": "Protect spine.", "alt": "Machine Shoulder Press"},
                {"name": "Incline DB Press", "sets": "3 x 12", "tempo": "3-0-1", "note": "Upper chest.", "alt": "Incline Machine Press"},
                {"name": "Chest Fly", "sets": "3 x 15", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Pec Deck Machine"}
            ], "Core": [{"name": "Pallof Press", "sets": "3 x 15s"}]},
            
            "Wednesday": {"Focus": "Active Recovery", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Mobility", "Exercises": [{"name": "Incline Walk", "sets": "30m", "tempo": "Zone 2", "note": "No run.", "alt": "-"}], "Core": []},
            
            "Thursday": {"Focus": "Lower Back Armour", "Type": "Gym", "Category": "Lower", "Home_Map": "Thursday", "Exercises": [
                {"name": "Lying Leg Curls", "sets": "3 x 12", "tempo": "3-0-1", "note": "Control.", "alt": "Seated Leg Curl"},
                {"name": "DB RDL (Light)", "sets": "3 x 10", "tempo": "3-1-1", "note": "Stop at shins.", "alt": "45-Degree Back Extension"},
                {"name": "Back Extensions", "sets": "3 x 15", "tempo": "2-1-1", "note": "Glutes only.", "alt": "Bird-Dog (Weighted)"}
            ], "Core": [{"name": "McGill Curl Up", "sets": "5 x 10s"}]},
            
            "Friday": {"Focus": "Upper Pull", "Type": "Gym", "Category": "Pull", "Home_Map": "Pull", "Exercises": [
                {"name": "Chest Supp Row", "sets": "3 x 10", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Seated Cable Row"},
                {"name": "Face Pulls", "sets": "4 x 15", "tempo": "Hold", "note": "Posture.", "alt": "Reverse Pec Deck"},
                {"name": "Lat Pulldowns", "sets": "3 x 12", "tempo": "2-0-1", "note": "Elbows.", "alt": "Assisted Pull-up Machine"}
            ], "Core": [{"name": "Plank Taps", "sets": "3 x 45s"}]},
            
            "Saturday": {"Focus": "Outdoor", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Mobility", "Exercises": [{"name": "Hike/Swim", "sets": "60m", "tempo": "Fun", "note": "Move.", "alt": "-"}], "Core": []},
            "Sunday": {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Mobility", "Exercises": [{"name": "Vitamin D3", "sets": "1 Sachet", "tempo": "-", "note": "With Fat.", "alt": "-"}], "Core": []}
        }
    }
}

# --- IRON BIBLE ---
EXERCISE_BIBLE = {
    # QUADS & GLUTES
    "Goblet Squat": {"Muscle": "Quads/Core", "Stretch": "Couch Stretch", "Cue": "Elbows inside knees. Chest up."},
    "Bulgarian Split Squat": {"Muscle": "Glutes/Quads", "Stretch": "Couch Stretch", "Cue": "Torso forward for glutes. Upright for quads."},
    "Leg Press": {"Muscle": "Quads", "Stretch": "Quad Stretch", "Cue": "Don't lock knees at top."},
    # POSTERIOR CHAIN
    "Trap Bar Deadlift": {"Muscle": "Full Body", "Stretch": "Hamstring Fold", "Cue": "Push floor away. Hips low."},
    "RDL": {"Muscle": "Hamstrings", "Stretch": "Toe Touch", "Cue": "Hips back. Soft knees."},
    "Lying Leg Curls": {"Muscle": "Hamstrings", "Stretch": "Seated Hamstring Stretch", "Cue": "Hips glued to pad."},
    "Superman Hold": {"Muscle": "Lower Back", "Stretch": "Child's Pose", "Cue": "Lift chest and thighs."},
    # ADDUCTORS
    "Copenhagen Plank": {"Muscle": "Adductors", "Stretch": "Butterfly", "Cue": "Lift hips high. Squeeze top leg."},
    "Seated Pillow Squeeze": {"Muscle": "Adductors", "Stretch": "Butterfly", "Cue": "Crush the pillow 100% effort."},
    # PUSH
    "Seated DB Press": {"Muscle": "Shoulders", "Stretch": "Clasped Hands Back", "Cue": "Ribs down. Press slightly forward."},
    "Incline DB Press": {"Muscle": "Upper Chest", "Stretch": "Door Pec Stretch", "Cue": "Elbows 45 degrees."},
    "Pushups": {"Muscle": "Chest", "Stretch": "Chest Opener", "Cue": "Arrow shape arms."},
    "Dips": {"Muscle": "Lower Chest", "Stretch": "Overhead Tricep Stretch", "Cue": "Lean forward."},
    # PULL
    "Chest Supported Row": {"Muscle": "Upper Back", "Stretch": "Dead Hang", "Cue": "Squeeze spine."},
    "Lat Pulldown": {"Muscle": "Lats", "Stretch": "Dead Hang", "Cue": "Elbows to pockets."},
    "Face Pulls": {"Muscle": "Rear Delts", "Stretch": "Cross Body", "Cue": "Thumbs back."},
    # ARMS
    "Hammer Curl": {"Muscle": "Biceps/Brachialis", "Stretch": "Wrist Extension", "Cue": "Thumbs up."},
    "Tricep Pushdown": {"Muscle": "Triceps", "Stretch": "Overhead Stretch", "Cue": "Elbows glued to side."},
    # CORE
    "Deadbug": {"Muscle": "Deep Core", "Stretch": "Cobra", "Cue": "Back glued to floor."},
    "Pallof Press": {"Muscle": "Anti-Rotation", "Stretch": "Side Bend", "Cue": "Resist the turn."},
    "McGill Curl Up": {"Muscle": "Spine Stability", "Stretch": "None", "Cue": "Hands under lower back."}
}

# --- LOGIC FUNCTIONS ---
def get_daily_plan(data_source, day_name, is_home):
    gym_plan = data_source["Routine"].get(day_name, {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Mobility", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-"}], "Core": []})
    
    cat = gym_plan.get("Category", "Mobility")
    warmup = WARMUPS.get(cat, WARMUPS["Mobility"])
    cooldown = COOLDOWNS.get(cat, COOLDOWNS["Mobility"])

    if is_home and gym_plan["Type"] == "Gym":
        home_key = gym_plan.get("Home_Map", "Mobility")
        home_exs = HOME_REPAIR.get(home_key, HOME_REPAIR["Monday"]) 
        return {
            "Focus": f"Home Repair: {gym_plan['Focus']}", 
            "Type": "Home", 
            "Exercises": home_exs, 
            "Core": gym_plan.get("Core", []), 
            "Warmup": warmup, 
            "Cooldown": cooldown
        }
    
    return {**gym_plan, "Warmup": warmup, "Cooldown": cooldown}

def ai_coach(day_count, mode, mood):
    if mode == "Infinity Loop (Forever)" and day_count < 180: return "⚠️ **LOGIC ERROR:** Stick to Foundation Phase 1.", False
    if mood == "Injured / Pain": return "🚨 **INJURY:** Gym Cancelled. Rehab Loaded.", True
    if mood == "Tired / Low Energy": return "📉 **ADJUST:** Reduce weight 20%.", False
    return "✅ **GO MODE:** Focus on structure.", False

# --- MAIN APP ---
def main():
    st.title("🛡️ Bulletproof Athlete v14")
    
    tab_workout, tab_bible, tab_history = st.tabs(["🏋️ Daily Protocol", "📖 The Iron Bible", "📜 History"])

    # SIDEBAR
    st.sidebar.header("⚙️ Settings")
    days_active = st.sidebar.number_input("Days Active", min_value=1, value=1)
    
    # RESTORED: Phase Progress Bar
    phase_progress = min(days_active / 30, 1.0)
    st.sidebar.write(f"**Phase 1 Completion:** {int(phase_progress*100)}%")
    st.sidebar.progress(phase_progress)
    
    st.sidebar.divider()
    location = st.sidebar.radio("📍 Location", ["Gym", "Home"])
    mode = "Foundation (First 6 Months)" 
    st.sidebar.info(f"Mode Locked: {mode}")
    
    if st.sidebar.button("🗑️ Clear History Log"):
        if clear_history():
            st.sidebar.success("Log Deleted.")
            st.rerun()

    # Meds
    st.sidebar.divider()
    st.sidebar.header("💊 Stack")
    with st.sidebar.expander("Morning"): st.checkbox("L-Carnitine"); st.checkbox("NMN")
    with st.sidebar.expander("Breakfast"): 
        st.checkbox("Ubiquinol + Omega3")
        st.checkbox("B12 + C")
        st.checkbox("Vit E")
        st.checkbox("Vit D3 (Sundays Only)")
    with st.sidebar.expander("Night"): st.checkbox("Magnesium"); st.checkbox("Zinc")

    # TAB 1: WORKOUT
    with tab_workout:
        streak = get_streak(load_history())
        col1, col2 = st.columns([1,3])
        col1.metric("🔥 Streak", f"{streak}")
        mood = col2.selectbox("Status", ["Neutral", "Great / Strong", "Tired / Low Energy", "Injured / Pain"])
        
        msg, override = ai_coach(days_active, mode, mood)
        if override: st.error(msg)
        else: st.info(msg)
        
        if st.button("✅ Log Workout"):
            save_history(datetime.date.today(), mode, mood, "Yes")
            st.success("Logged!")

        today_name = datetime.datetime.now().strftime("%A")
        st.header(f"📅 {today_name}")
        
        # Get Plan
        plan = {}
        if override:
            plan = {"Focus": "Emergency Rehab", "Type": "Rehab", "Exercises": HOME_REPAIR["Thursday"], "Core": [], "Warmup": [], "Cooldown": []} 
        else:
            plan = get_daily_plan(FOUNDATION_PHASES["Phase 1: Structural Repair"], today_name, location == "Home")

        st.markdown(f"<div class='banner repair'><h3>{plan['Focus']}</h3></div>", unsafe_allow_html=True)

        # Warmup
        if plan.get("Warmup"):
            with st.expander("🔥 Warmup"):
                for w in plan["Warmup"]: st.checkbox(f"**{w['name']}** ({w['time']})")

        # Exercises
        st.subheader("🏋️ Routine")
        for i, ex in enumerate(plan["Exercises"]):
            with st.container():
                c1, c2, c3 = st.columns([3,2,1])
                link = get_youtube_link(ex['name'])
                c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                
                # ALTERNATIVE DISPLAY (GYM ONLY)
                if plan["Type"] == "Gym" and "alt" in ex and ex["alt"] != "-":
                    c1.markdown(f"<span class='alt-text'>Gym Busy? Use: {ex['alt']}</span>", unsafe_allow_html=True)
                
                c2.markdown(f"**Sets:** {ex.get('sets','?')} | **Tempo:** <span class='tempo-tag'>{ex.get('tempo','-')}</span>", unsafe_allow_html=True)
                if "note" in ex: c2.caption(f"💡 {ex['note']}")
                c3.checkbox("Done", key=f"ex_{i}")
                st.markdown("---")

        # Core
        if plan.get("Core"):
            st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
            for c in plan["Core"]: st.checkbox(f"{c['name']} ({c['sets']})")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Cooldown
        if plan.get("Cooldown"):
             st.subheader("❄️ Cooldown")
             for c in plan["Cooldown"]: st.checkbox(f"**{c['name']}** ({c['time']})")

    # TAB 2: BIBLE
    with tab_bible:
        st.header("📖 Exercise Encyclopedia")
        search = st.text_input("🔍 Search", "")
        
        display_data = {k: v for k, v in EXERCISE_BIBLE.items() if search.lower() in k.lower()} if search else EXERCISE_BIBLE
        for name, data in display_data.items():
            st.markdown(f"""
            <div class="bible-card">
                <h4>{name}</h4>
                <p><strong>Muscle:</strong> {data['Muscle']} | <strong>Stretch:</strong> {data['Stretch']}</p>
                <p><em>"{data['Cue']}"</em></p>
                <a href="{get_youtube_link(name)}" target="_blank">📺 Demo</a>
            </div>
            """, unsafe_allow_html=True)

    # TAB 3: HISTORY
    with tab_history:
        st.header("📜 Log")
        st.dataframe(load_history().sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
