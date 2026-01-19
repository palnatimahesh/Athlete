import streamlit as st
import datetime
import pandas as pd
import os

# --- CONFIGURATION ---
st.set_page_config(page_title="Bulletproof Athlete v5", page_icon="🛡️", layout="wide")

# --- INITIALIZE HISTORY (CSV) ---
HISTORY_FILE = "workout_history.csv"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame(columns=["Date", "Phase", "Mood", "Completed"])
    return pd.read_csv(HISTORY_FILE)

def save_history(date, phase, mood, completed):
    df = load_history()
    # Check if entry exists for today
    if date in df["Date"].values:
        df.loc[df["Date"] == date, ["Phase", "Mood", "Completed"]] = [phase, mood, completed]
    else:
        new_row = pd.DataFrame({"Date": [date], "Phase": [phase], "Mood": [mood], "Completed": [completed]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

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
    .video-link { font-size: 0.8em; text-decoration: none; color: #007bff; }
</style>
""", unsafe_allow_html=True)

# --- DATABASES ---
WARMUP_ROUTINE = [{"name": "90/90 Hip Switch", "time": "2 mins"}, {"name": "Cat-Cow", "time": "1 min"}, {"name": "World's Greatest Stretch", "time": "5 reps/side"}, {"name": "Glute Bridges", "time": "15 reps"}]
COOLDOWN_ROUTINE = [{"name": "Dead Hang", "time": "1 min"}, {"name": "Deep Squat Hold", "time": "1 min"}, {"name": "Child's Pose", "time": "2 mins"}]

FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Duration": 30, "Theme": "Fix Back. Fire Adductors.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Lower Body A", "Type": "Gym", "Exercises": [{"name": "Copenhagen Plank", "sets": "3x20s", "tempo": "Hold", "note": "Squeeze legs.", "alt": "Side Plank"}, {"name": "Goblet Squat", "sets": "4x12", "tempo": "3-1-1", "note": "Heels High.", "alt": "Leg Press"}, {"name": "Cable Pull-Through", "sets": "3x15", "tempo": "2-0-1", "note": "Hinge.", "alt": "DB RDL"}, {"name": "Adductor Machine", "sets": "3x15", "tempo": "3-0-1", "note": "Control.", "alt": "Cable Add"}], "Core": [{"name": "Deadbugs", "sets": "3x10"}]},
            "Tuesday": {"Focus": "Upper Push", "Type": "Gym", "Exercises": [{"name": "Seated DB Press", "sets": "3x10", "tempo": "2-1-1", "note": "Core tight.", "alt": "Machine Press"}, {"name": "Incline DB Press", "sets": "3x12", "tempo": "3-0-1", "note": "Upper Chest.", "alt": "Inc Machine"}, {"name": "Chest Fly", "sets": "3x15", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Pec Deck"}], "Core": [{"name": "Pallof Press", "sets": "3x15s"}]},
            "Wednesday": {"Focus": "Active Recovery", "Type": "Recovery", "Exercises": [{"name": "Incline Walk", "sets": "30m", "tempo": "Zone 2", "note": "No running.", "alt": "-"}], "Core": []},
            "Thursday": {"Focus": "Lower Body B", "Type": "Gym", "Exercises": [{"name": "Lying Leg Curls", "sets": "3x12", "tempo": "3-0-1", "note": "Control.", "alt": "Seat Curl"}, {"name": "DB RDL", "sets": "3x10", "tempo": "3-1-1", "note": "Light.", "alt": "Back Ext"}, {"name": "Back Extension", "sets": "3x15", "tempo": "2-1-1", "note": "Glutes.", "alt": "Bird Dog"}], "Core": [{"name": "McGill Curl Up", "sets": "5x10s"}]},
            "Friday": {"Focus": "Upper Pull", "Type": "Gym", "Exercises": [{"name": "Chest Supp Row", "sets": "3x10", "tempo": "2-1-1", "note": "Squeeze.", "alt": "Cable Row"}, {"name": "Face Pulls", "sets": "4x15", "tempo": "Hold", "note": "Posture.", "alt": "Rev Pec Deck"}, {"name": "Lat Pulldown", "sets": "3x12", "tempo": "2-0-1", "note": "Elbows.", "alt": "Ast Pullup"}], "Core": [{"name": "Plank Taps", "sets": "3x45s"}]},
            "Saturday": {"Focus": "Outdoor Activity", "Type": "Recovery", "Exercises": [{"name": "Hike/Swim", "sets": "60m", "tempo": "Fun", "note": "Move.", "alt": "-"}], "Core": []},
            "Sunday": {"Focus": "Total Rest", "Type": "Recovery", "Exercises": [{"name": "Vitamin D3", "sets": "1 Sachet", "tempo": "-", "note": "With Fat.", "alt": "-"}], "Core": []}
        }
    }
}
# (Infinity Seasons logic remains same as v4.0, omitted for brevity but should be included)

HOME_REHAB = [{"name": "Pillow Squeeze Bridge", "sets": "3x15", "note": "Fixes Adductors."}, {"name": "Prone Cobra", "sets": "3x45s", "note": "Fixes Posture."}, {"name": "Bird Dog", "sets": "3x10", "note": "Fixes Core."}]

# --- HELPER FUNCTIONS ---
def get_youtube_link(exercise_name):
    query = exercise_name.replace(" ", "+") + "+exercise+form"
    return f"https://www.youtube.com/results?search_query={query}"

def get_streak(df):
    if df.empty: return 0
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    today = pd.to_datetime(datetime.date.today())
    
    streak = 0
    # Check if today is logged
    if not df[df["Date"] == today].empty:
        streak += 1
        current_date = today - datetime.timedelta(days=1)
    else:
        current_date = today - datetime.timedelta(days=1)
        
    for date in df["Date"]:
        if date == current_date:
            streak += 1
            current_date -= datetime.timedelta(days=1)
        elif date > current_date: continue # Skip duplicate entries
        else: break
    return streak

# --- MAIN APP ---
def main():
    st.title("🛡️ Bulletproof Athlete: Smart Tracker")
    
    # LOAD HISTORY
    history_df = load_history()
    streak = get_streak(history_df)
    
    # --- TOP METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Current Streak", f"{streak} Days")
    
    # --- SIDEBAR SETTINGS ---
    st.sidebar.header("⚙️ Profile")
    days_active = st.sidebar.number_input("Day #", min_value=1, value=1)
    
    # Visual Progress Bar
    phase_duration = 30 # Default for Phase 1
    progress = min(days_active / phase_duration, 1.0)
    st.sidebar.write(f"**Phase Progress:** {int(progress*100)}%")
    st.sidebar.progress(progress)
    
    mode = st.sidebar.radio("Mode", ["Foundation", "Infinity"])
    
    # Logic to select data (Same as v4.0)
    current_data = FOUNDATION_PHASES["Phase 1: Structural Repair"] # Defaulting for brevity
    
    # --- CHECK-IN ---
    st.markdown("### 💬 Daily Check-In")
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    
    # Check if already logged today
    already_logged = not history_df[history_df["Date"] == today_str].empty
    
    mood = st.selectbox("How is the body?", ["Neutral", "Great / Strong", "Tired / Low Energy", "Injured / Pain"])
    
    if st.button("✅ Log Workout"):
        save_history(today_str, "Phase 1", mood, "Yes")
        st.success("Workout Logged! Streak Updated.")
        st.rerun()

    if already_logged:
        st.info(f"You have already logged today's session as: **{mood}**")

    st.divider()

    # --- WORKOUT DISPLAY ---
    day_name = datetime.datetime.now().strftime("%A")
    st.header(f"📅 {day_name} Protocol")
    
    # Logic for Rehab Override
    routine = []
    if mood == "Injured / Pain":
        st.warning("🚑 Injury Protocol Active: Home Rehab Only")
        routine = HOME_REHAB
        theme = "Rehab"
        css = "repair"
    else:
        # Fetch routine from FOUNDATION_PHASES (Simulated logic)
        daily_plan = current_data["Routine"].get(day_name)
        if daily_plan:
            routine = daily_plan["Exercises"]
            theme = daily_plan["Focus"]
            css = "repair" if daily_plan["Type"] == "Gym" else "recovery"
        else:
            routine = []

    # RENDER ROUTINE
    if routine:
        st.markdown(f"<div class='banner {css}'><h3>{theme}</h3></div>", unsafe_allow_html=True)
        
        # Warmup (If Gym)
        if "Type" in daily_plan and daily_plan["Type"] == "Gym":
            with st.expander("🔥 Warmup (Click to View)", expanded=False):
                for w in WARMUP_ROUTINE: st.checkbox(f"{w['name']} ({w['time']})")

        # Exercises with Video Links
        st.subheader("🏋️ Exercises")
        for i, ex in enumerate(routine):
            with st.container():
                c1, c2, c3 = st.columns([3, 2, 1])
                # Name + Video Link
                c1.markdown(f"**{i+1}. {ex['name']}** [📺 Demo]({get_youtube_link(ex['name'])})")
                if "alt" in ex and ex["alt"] != "-": 
                    c1.markdown(f"<span class='alt-text'>Alt: {ex['alt']}</span>", unsafe_allow_html=True)
                
                if "sets" in ex: c2.caption(f"Sets: {ex['sets']} | Tempo: {ex.get('tempo','-')}")
                if "note" in ex: c2.caption(f"💡 {ex['note']}")
                
                c3.checkbox("Done", key=f"ex_{i}")
                st.markdown("---")
        
        # Core (If exists)
        if "Core" in daily_plan and daily_plan["Core"]:
            st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
            for c in daily_plan["Core"]: st.checkbox(f"**{c['name']}** ({c['sets']})")
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
