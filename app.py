import streamlit as st
import datetime
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Bulletproof Athlete: Ultimate", page_icon="🛡️", layout="wide")

# --- INITIALIZE HISTORY (CSV) ---
HISTORY_FILE = "workout_history.csv"

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
    return f"https://www.youtube.com/results?search_query={name.replace(' ', '+')}+exercise+form"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .banner { padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; text-align: center; }
    .build { background-color: #2E7D32; }
    .shred { background-color: #D32F2F; }
    .flow { background-color: #1976D2; }
    .repair { background-color: #F57C00; }
    .recovery { background-color: #607D8B; }
    .alt-text { color: #d32f2f; font-size: 0.9em; font-style: italic; }
    .core-box { background-color: #f8f9fa; border-left: 5px solid #6c757d; padding: 10px; margin-top: 10px; }
    a { text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- MASTER DATABASE ---
WARMUP_ROUTINE = [{"name": "90/90 Hip Switch", "time": "2 mins"}, {"name": "Cat-Cow", "time": "1 min"}, {"name": "World's Greatest Stretch", "time": "5 reps/side"}, {"name": "Glute Bridges", "time": "15 reps"}]
COOLDOWN_ROUTINE = [{"name": "Dead Hang", "time": "1 min"}, {"name": "Deep Squat Hold", "time": "1 min"}, {"name": "Child's Pose", "time": "2 mins"}]

FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Duration": 30, "Theme": "Fix Back. Fire Adductors. Detox.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Lower Body A", "Type": "Gym", "Exercises": [
                {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "tempo": "Hold", "note": "Squeeze legs hard.", "alt": "Side Plank with Leg Lift"},
                {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "tempo": "3-1-1", "note": "Torso vertical.", "alt": "Leg Press (Feet High)"},
                {"name": "Cable Pull-Throughs", "sets": "3 x 15", "tempo": "2-0-1", "note": "Hinge hips back.", "alt": "DB RDL (Light)"},
                {"name": "Adductor Machine", "sets": "3 x 15", "tempo": "3-0-1", "note": "Control eccentric.", "alt": "Cable Adduction"}
            ], "Core": [{"name": "Deadbugs", "sets": "3 x 10"}]},
            "Tuesday": {"Focus": "Upper Push", "Type": "Gym", "Exercises": [
                {"name": "Seated DB Press", "sets": "3 x 10", "tempo": "2-1-1", "note": "Protect spine.", "alt": "Machine Shoulder Press"},
                {"name": "Incline DB Press", "sets": "3 x 12", "tempo": "3-0-1", "note": "Upper chest.", "alt": "Incline Machine Press"},
                {"name": "Chest Fly", "sets": "3 x 15", "tempo": "2-1-1", "note": "Squeeze at center.", "alt": "Pec Deck / DB Fly"}
            ], "Core": [{"name": "Pallof Press", "sets": "3 x 15s"}]},
            "Wednesday": {"Focus": "Active Recovery", "Type": "Recovery", "Exercises": [{"name": "Incline Walk", "sets": "30 mins", "tempo": "Zone 2", "note": "12% Incline, No Running.", "alt": "-"}], "Core": []},
            "Thursday": {"Focus": "Lower Body B", "Type": "Gym", "Exercises": [
                {"name": "Lying Leg Curls", "sets": "3 x 12", "tempo": "3-0-1", "note": "Control down.", "alt": "Seated Leg Curl"},
                {"name": "DB RDL (Light)", "sets": "3 x 10", "tempo": "3-1-1", "note": "Stop at shins.", "alt": "45-Degree Back Extension"},
                {"name": "Back Extensions", "sets": "3 x 15", "tempo": "2-1-1", "note": "Glutes only.", "alt": "Bird-Dog (Weighted)"}
            ], "Core": [{"name": "McGill Curl Up", "sets": "5 x 10s"}]},
            "Friday": {"Focus": "Upper Pull", "Type": "Gym", "Exercises": [
                {"name": "Chest Supported Row", "sets": "3 x 10", "tempo": "2-1-1", "note": "Squeeze back.", "alt": "Seated Cable Row"},
                {"name": "Face Pulls", "sets": "4 x 15", "tempo": "Hold", "note": "Fix posture.", "alt": "Reverse Pec Deck"},
                {"name": "Lat Pulldowns", "sets": "3 x 12", "tempo": "2-0-1", "note": "Elbows down.", "alt": "Assisted Pull-up"}
            ], "Core": [{"name": "Plank Shoulder Taps", "sets": "3 x 45s"}]},
            "Saturday": {"Focus": "Outdoor", "Type": "Recovery", "Exercises": [{"name": "Hike/Swim", "sets": "60m", "tempo": "Fun", "note": "Move.", "alt": "-"}], "Core": []},
            "Sunday": {"Focus": "Rest", "Type": "Recovery", "Exercises": [{"name": "Vitamin D3", "sets": "1 Sachet", "tempo": "-", "note": "With Fat.", "alt": "-"}], "Core": []}
        }
    }
}

INFINITY_SEASONS = {
    "BUILD (Strength Focus)": {
        "Theme": "Heavy Loads.", "Class": "build",
        "Routine": {
            "Monday": {"Focus": "Max Lower", "Type": "Gym", "Exercises": [{"name": "Trap Bar DL", "sets": "5x3", "tempo": "X-1-X", "note": "Heavy", "alt": "Sumo DL"}, {"name": "Split Squat", "sets": "3x8", "tempo": "3-0-1", "note": "Deep", "alt": "Lunge"}, {"name": "Leg Press", "sets": "3x10", "tempo": "2-0-1", "note": "Heavy", "alt": "Hack Squat"}], "Core": [{"name": "Weighted Plank", "sets": "3x45s"}]},
            "Wednesday": {"Focus": "Max Upper", "Type": "Gym", "Exercises": [{"name": "OH Press", "sets": "5x5", "tempo": "2-0-1", "note": "Strict", "alt": "DB Press"}, {"name": "Wt Pullup", "sets": "4x6", "tempo": "2-1-1", "note": "Full", "alt": "Lat Pull"}, {"name": "Inc Bench", "sets": "4x8", "tempo": "3-0-1", "note": "Upper", "alt": "DB Inc"}], "Core": [{"name": "Leg Raise", "sets": "3x10"}]},
            "Friday": {"Focus": "Hypertrophy", "Type": "Gym", "Exercises": [{"name": "Front Squat", "sets": "3x8", "tempo": "3-1-1", "note": "Quads", "alt": "Goblet"}, {"name": "RDL", "sets": "3x10", "tempo": "3-1-1", "note": "Hams", "alt": "Curl"}, {"name": "Dips", "sets": "3xF", "tempo": "Slow", "note": "Chest", "alt": "Pushup"}], "Core": [{"name": "Ab Wheel", "sets": "3x10"}]}
        }
    },
    "SHRED (Athlete Focus)": {
        "Theme": "Speed & Agility.", "Class": "shred",
        "Routine": {
            "Monday": {"Focus": "Power", "Type": "Gym", "Exercises": [{"name": "Power Clean", "sets": "5x3", "tempo": "Fast", "note": "Snap", "alt": "DB Snatch"}, {"name": "Box Jump", "sets": "4x5", "tempo": "Fast", "note": "Soft", "alt": "Broad Jump"}, {"name": "Sled Push", "sets": "5x", "tempo": "Max", "note": "Drive", "alt": "Sprint"}], "Core": [{"name": "Slams", "sets": "3x15"}]},
            "Wednesday": {"Focus": "Athletic Upper", "Type": "Gym", "Exercises": [{"name": "Plyo Pushup", "sets": "4x8", "tempo": "Fast", "note": "Explode", "alt": "Throw"}, {"name": "Fast Pullup", "sets": "4x8", "tempo": "Fast", "note": "Speed", "alt": "Lat Pull"}, {"name": "Ropes", "sets": "4x30s", "tempo": "Max", "note": "Burn", "alt": "Burpee"}], "Core": [{"name": "Twist", "sets": "3x20"}]},
            "Friday": {"Focus": "Conditioning", "Type": "Gym", "Exercises": [{"name": "KB Swing", "sets": "4x20", "tempo": "Fast", "note": "Hips", "alt": "DB Swing"}, {"name": "Jump Lunge", "sets": "3x15", "tempo": "Fast", "note": "Burn", "alt": "Step Up"}, {"name": "Farm Carry", "sets": "4x40m", "tempo": "Fast", "note": "Grip", "alt": "Suitcase"}], "Core": [{"name": "Climbers", "sets": "3x45s"}]}
        }
    },
    "FLOW (Mobility Focus)": {
        "Theme": "Joint Health.", "Class": "flow",
        "Routine": {
            "Monday": {"Focus": "Hip Mob", "Type": "Gym", "Exercises": [{"name": "ATG Split", "sets": "3x10", "tempo": "Slow", "note": "Knee>Toe", "alt": "Lunge"}, {"name": "Jeff Curl", "sets": "3x10", "tempo": "5-1-5", "note": "Light", "alt": "RDL"}, {"name": "Copenhagen", "sets": "3x45s", "tempo": "Hold", "note": "Adduct", "alt": "Side Plk"}], "Core": [{"name": "Side Bend", "sets": "3x15"}]},
            "Wednesday": {"Focus": "Shoulder Mob", "Type": "Gym", "Exercises": [{"name": "Ring Pushup", "sets": "3x12", "tempo": "2-2-1", "note": "Stab", "alt": "DB Press"}, {"name": "Face Pull", "sets": "4x20", "tempo": "Hold", "note": "Rear", "alt": "Band"}, {"name": "Skin Cat", "sets": "3x5", "tempo": "Slow", "note": "Mob", "alt": "Hang"}], "Core": [{"name": "Hollow Hold", "sets": "3x45s"}]},
            "Friday": {"Focus": "Spine Mob", "Type": "Gym", "Exercises": [{"name": "SL RDL", "sets": "3x10", "tempo": "3-1-1", "note": "Bal", "alt": "B-Stance"}, {"name": "Cosack", "sets": "3x8", "tempo": "Slow", "note": "Side", "alt": "Lat Lunge"}, {"name": "Back Ext", "sets": "3x20", "tempo": "Hold", "note": "Endure", "alt": "Superman"}], "Core": [{"name": "Pallof", "sets": "3x15s"}]}
        }
    }
}

HOME_REHAB = [{"name": "Pillow Squeeze Bridge", "sets": "3x15", "note": "Fixes Adductors."}, {"name": "Prone Cobra", "sets": "3x45s", "note": "Fixes Posture."}, {"name": "Bird Dog", "sets": "3x10", "note": "Fixes Core."}]

# --- LOGIC FUNCTIONS ---
def get_daily_plan(data_source, day_name):
    if day_name in data_source["Routine"]: return data_source["Routine"][day_name]
    if day_name in ["Tuesday", "Thursday", "Saturday", "Sunday"]:
         return {"Focus": "Active Recovery", "Type": "Recovery", "Exercises": [{"name": "Walk/Mobility", "sets": "30m", "tempo": "-", "note": "Recover", "alt": "-"}], "Core": []}
    return None

def get_hybrid_plan(day_name):
    if day_name == "Monday": return INFINITY_SEASONS["BUILD (Strength Focus)"]["Routine"]["Monday"], "BUILD", "build"
    elif day_name == "Wednesday": return INFINITY_SEASONS["SHRED (Athlete Focus)"]["Routine"]["Wednesday"], "SHRED", "shred"
    elif day_name == "Friday": return INFINITY_SEASONS["FLOW (Mobility Focus)"]["Routine"]["Friday"], "FLOW", "flow"
    else: return {"Focus": "Active Recovery", "Type": "Recovery", "Exercises": [{"name": "Walk/Mobility", "sets": "30m", "tempo": "-", "note": "Recover", "alt": "-"}], "Core": []}, "Recovery", "recovery"

def ai_coach_logic(day_count, mode, mood, loop_style):
    advice = ""
    override = False
    if mode == "Infinity Loop (Forever)" and day_count < 180: advice += "⚠️ **LOGIC ERROR:** You selected 'Infinity Loop' but are on Day " + str(day_count) + ". Switch back to 'Foundation'.\n\n"
    if mood == "Injured / Pain":
        advice += "🚨 **INJURY MODE:** Gym Workout CANCELLED. Home Rehab Loaded."
        override = True
    elif mood == "Tired / Low Energy": advice += "📉 **ADJUSTMENT:** Reduce weights by 20%. Just move."
    else: advice += "✅ **GO MODE:** Focus on tempo and squeeze."
    return advice, override

# --- MAIN APP UI ---
def main():
    st.title("🛡️ Bulletproof Athlete: Ultimate")
    
    # 1. SIDEBAR
    st.sidebar.header("⚙️ Profile")
    days_active = st.sidebar.number_input("Day #", min_value=1, value=1)
    progress = min(days_active / 30, 1.0)
    st.sidebar.write(f"Phase Progress: {int(progress*100)}%")
    st.sidebar.progress(progress)
    
    st.sidebar.divider()
    mode = st.sidebar.radio("Mode", ["Foundation (First 6 Months)", "Infinity Loop (Forever)"])
    
    current_data = {}
    is_hybrid = False
    if mode == "Foundation (First 6 Months)":
        current_data = FOUNDATION_PHASES["Phase 1: Structural Repair"]
    else:
        loop_style = st.sidebar.radio("Loop Style", ["Seasonal", "Hybrid (Weekly Mix)"])
        if loop_style == "Seasonal":
            season = st.sidebar.selectbox("Season", list(INFINITY_SEASONS.keys()))
            current_data = INFINITY_SEASONS[season]
        else: is_hybrid = True

    # Medication Tracker
    st.sidebar.divider()
    st.sidebar.header("💊 Stack")
    st.sidebar.caption("Morning: L-Carnitine + NMN")
    st.sidebar.caption("Food: Ubiquinol, Omega3, B12")
    if days_active > 90: st.sidebar.error("🛑 STOP: Vitamin E")
    else: st.sidebar.caption("Breakfast: Vitamin E")

    # 2. TOP SECTION (Streak + Check-in)
    history_df = load_history()
    streak = get_streak(history_df)
    col1, col2 = st.columns([1, 2])
    col1.metric("🔥 Streak", f"{streak} Days")
    
    with col2:
        mood = st.selectbox("Daily Check-In: How are you?", ["Neutral", "Great / Strong", "Tired / Low Energy", "Injured / Pain"])
        coach_msg, override = ai_coach_logic(days_active, mode, mood, is_hybrid)
        st.info(f"🤖 **Coach:** {coach_msg}")

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    if st.button("✅ Log Workout"):
        save_history(today_str, mode, mood, "Yes")
        st.success("Logged!")
        st.rerun()

    st.divider()

    # 3. WORKOUT DISPLAY
    today_name = datetime.datetime.now().strftime("%A")
    st.header(f"📅 {today_name} Protocol")
    
    # Determine Plan
    plan = {}
    theme = ""
    css = ""

    if override:
        plan = {"Focus": "Injury Rehab", "Type": "Rehab", "Exercises": HOME_REHAB, "Core": []}
        theme = "Recover"
        css = "repair"
    elif is_hybrid:
        plan, theme, css = get_hybrid_plan(today_name)
        theme = f"Hybrid: {theme}"
    else:
        plan = get_daily_plan(current_data, today_name)
        if plan:
            theme = current_data.get("Theme", "Focus")
            css = current_data.get("Class", "repair") if plan["Type"] == "Gym" else "recovery"

    # Render
    if plan:
        st.markdown(f"<div class='banner {css}'><h3>{plan['Focus']}</h3><p>{theme}</p></div>", unsafe_allow_html=True)
        
        # Warmup
        if plan["Type"] == "Gym":
            with st.expander("🔥 Warmup (Mandatory)"):
                for w in WARMUP_ROUTINE: st.checkbox(f"**{w['name']}** ({w['time']})")
        
        # Exercises
        st.subheader("🏋️ Main Lift")
        if plan["Type"] == "Gym": st.caption("💡 **Rest:** 3 mins for compounds, 90s for others.")
        
        for i, ex in enumerate(plan["Exercises"]):
            with st.container():
                c1, c2, c3 = st.columns([3, 2, 1])
                c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({get_youtube_link(ex['name'])})")
                if "alt" in ex and ex["alt"] != "-": 
                    c1.markdown(f"<span class='alt-text'>Gym Busy? Use: {ex['alt']}</span>", unsafe_allow_html=True)
                
                if "sets" in ex: c2.caption(f"Sets: {ex['sets']} | Tempo: {ex.get('tempo','-')}")
                if "note" in ex: c2.caption(f"💡 {ex['note']}")
                c3.checkbox("Done", key=f"ex_{i}")
                st.markdown("---")

        # Core
        if "Core" in plan and plan["Core"]:
            st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
            for c in plan["Core"]: st.checkbox(f"**{c['name']}** ({c['sets']})")
            st.markdown("</div>", unsafe_allow_html=True)

        # Cooldown
        if plan["Type"] == "Gym":
            st.subheader("❄️ Cooldown")
            for c in COOLDOWN_ROUTINE: st.checkbox(f"**{c['name']}** ({c['time']})")

if __name__ == "__main__":
    main()
