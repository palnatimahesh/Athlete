# app.py
import streamlit as st
import datetime
import pandas as pd
import os
import data # Importing the file above

# ==========================================
# 1. CONFIGURATION
# ==========================================
st.set_page_config(page_title="Bulletproof Athlete v16", page_icon="🛡️", layout="wide")
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
    if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE); return True
    return False

def get_streak(df):
    if df.empty: return 0
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    today = pd.to_datetime(datetime.date.today())
    streak = 0
    current_date = today if not df[df["Date"] == today].empty else today - datetime.timedelta(days=1)
    for date in df["Date"]:
        if date == current_date: streak += 1; current_date -= datetime.timedelta(days=1)
        elif date > current_date: continue
        else: break
    return streak

def get_youtube_link(name):
    return f"https://www.youtube.com/results?search_query={name.split('(')[0].strip().replace(' ', '+')}+exercise+form"

# ==========================================
# 2. STYLING
# ==========================================
st.markdown("""
<style>
    .banner { padding: 20px; border-radius: 12px; color: white; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .phase1 { background: linear-gradient(135deg, #FF9800, #F57C00); }
    .phase2 { background: linear-gradient(135deg, #4CAF50, #2E7D32); }
    .phase3 { background: linear-gradient(135deg, #2196F3, #1565C0); }
    .repair { background: linear-gradient(135deg, #F57C00, #E65100); }
    .recovery { background: linear-gradient(135deg, #607D8B, #455A64); }
    
    .tempo-tag { background-color: #e3f2fd; color: #1565c0 !important; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .alt-text { color: #d32f2f !important; font-size: 0.9em; font-weight: bold; }
    
    .bible-card { background-color: #f1f8e9; color: #1a1a1a !important; padding: 15px; border-radius: 10px; border-left: 5px solid #558b2f; margin-bottom: 10px; }
    .bible-card h4 { margin: 0 0 5px 0; color: #2e7d32 !important; }
    
    a { text-decoration: none; font-weight: bold; color: #0288D1 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOGIC
# ==========================================
def get_life_plan(day_name, is_home):
    # This grabs the "Repair" plan from data.py
    gym_plan = data.FOUNDATION_PHASES["Phase 1: Structural Repair"]["Routine"].get(day_name, {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Exercises": [], "Core": []})
    
    cat = gym_plan.get("Category", "Mobility")
    warmup = data.WARMUPS.get(cat, data.WARMUPS["Mobility"])
    cooldown = data.COOLDOWNS.get(cat, data.COOLDOWNS["Mobility"])

    if is_home and gym_plan["Type"] == "Gym":
        home_key = gym_plan.get("Home_Map", "Monday")
        # Ensure we fetch the list from the HOME_REPAIR dictionary
        home_exs = data.HOME_REPAIR.get(home_key, data.HOME_REPAIR["Monday"])
        return {"Focus": f"Home: {gym_plan['Focus']}", "Type": "Home", "Exercises": home_exs, "Core": [], "Warmup": warmup, "Cooldown": cooldown}
    
    return {**gym_plan, "Warmup": warmup, "Cooldown": cooldown}

# ==========================================
# 4. MAIN APP
# ==========================================
def main():
    st.title("🛡️ Bulletproof Athlete v16")
    
    # --- Sidebar ---
    mode = st.sidebar.selectbox("Select Mode", ["Life Protocol (Repair)", "6-Week Runtastic Course"])
    
    st.sidebar.divider()
    st.sidebar.header("⚙️ Settings")
    
    # Settings based on Mode
    if mode == "Life Protocol (Repair)":
        days_active = st.sidebar.number_input("Days Active", 1, 365, 1)
        st.sidebar.progress(min(days_active/30, 1.0))
        location = st.sidebar.radio("Location", ["Gym", "Home"])
        selected_week = 0 # Not used
        selected_day = 0 # Not used
    else:
        st.sidebar.info("Course Mode: High Intensity")
        selected_week = st.sidebar.selectbox("Week", [1,2,3,4,5,6])
        selected_day = st.sidebar.radio("Day", ["Day 1", "Day 2", "Day 3", "Day 4"])
        location = "Home" # Runtastic is usually home based
        days_active = 0 # Not used

    if st.sidebar.button("🗑️ Clear Logs"):
        clear_history(); st.rerun()

    # Meds
    st.sidebar.divider()
    st.sidebar.header("💊 Stack")
    with st.sidebar.expander("Supplements"):
        st.checkbox("L-Carnitine")
        st.checkbox("Ubiquinol + Omega3")
        st.checkbox("Vitamin D3 (Sunday)")
        st.checkbox("Magnesium")

    # --- Tabs ---
    tab_workout, tab_bible, tab_history = st.tabs(["🏋️ Daily Workout", "📖 Iron Bible", "📜 History"])

    # --- WORKOUT TAB ---
    with tab_workout:
        streak = get_streak(load_history())
        col1, col2 = st.columns([1,3])
        col1.metric("🔥 Streak", f"{streak}")
        mood = col2.selectbox("Status", ["Neutral", "Strong", "Tired", "Injured"])
        
        if mood == "Injured": st.error("🚨 INJURY MODE: Do Rehab exercises only.")
        
        if st.button("✅ Log Complete"):
            key = f"Week {selected_week} {selected_day}" if mode == "6-Week Runtastic Course" else datetime.date.today().strftime("%Y-%m-%d")
            save_history(key, mode, mood, "Yes")
            st.success("Logged!")

        # RENDER: LIFE PROTOCOL
        if mode == "Life Protocol (Repair)":
            today = datetime.datetime.now().strftime("%A")
            st.header(f"📅 {today}")
            plan = get_life_plan(today, location == "Home")
            
            st.markdown(f"<div class='banner repair'><h3>{plan['Focus']}</h3></div>", unsafe_allow_html=True)
            
            if plan.get("Warmup"):
                with st.expander("🔥 Warmup"):
                    for w in plan["Warmup"]: st.checkbox(f"**{w['name']}** ({w['time']})")
            
            for i, ex in enumerate(plan["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3,2,1])
                    link = get_youtube_link(ex['name'])
                    c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                    if "alt" in ex and ex["alt"] != "-": c1.markdown(f"<span class='alt-text'>Busy? {ex['alt']}</span>", unsafe_allow_html=True)
                    c2.markdown(f"**Sets:** {ex.get('sets','?')} | **Tempo:** <span class='tempo-tag'>{ex.get('tempo','-')}</span>", unsafe_allow_html=True)
                    c2.caption(f"💡 {ex.get('note','')}")
                    c3.checkbox("Done", key=f"lp_{i}")
                    st.markdown("---")
            
            if plan.get("Cooldown"):
                st.subheader("❄️ Cooldown")
                for c in plan["Cooldown"]: st.checkbox(f"**{c['name']}** ({c['time']})")

        # RENDER: 6-WEEK COURSE
        else:
            c_data = data.COURSE_DATA[selected_week]
            w_data = c_data["Schedule"][selected_day]
            
            st.markdown(f"<div class='banner {c_data['Theme']}'><h2>Week {selected_week} - {selected_day}</h2><p>{c_data['Phase']} | Focus: {w_data['Focus']}</p></div>", unsafe_allow_html=True)
            
            # Course Warmup (Generic)
            with st.expander("🔥 Warmup"):
                st.checkbox("Jumping Jacks (60s)")
                st.checkbox("High Knees (30s)")
                st.checkbox("Arm Circles (30s)")

            for i, ex in enumerate(w_data["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3,2,1])
                    link = get_youtube_link(ex['name'])
                    c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                    c2.markdown(f"**Sets:** {ex['sets']} | **Tempo:** <span class='tempo-tag'>{ex['tempo']}</span>", unsafe_allow_html=True)
                    c2.caption(f"💡 {ex['note']}")
                    c3.checkbox("Done", key=f"wc_{selected_week}_{i}")
                    st.markdown("---")

    # --- BIBLE TAB ---
    with tab_bible:
        st.header("📖 Exercise Encyclopedia")
        search = st.text_input("🔍 Search", "")
        # Filter logic
        res = {k:v for k,v in data.EXERCISE_BIBLE.items() if search.lower() in k.lower()} if search else data.EXERCISE_BIBLE
        
        for name, info in res.items():
            st.markdown(f"""
            <div class="bible-card">
                <h4>{name}</h4>
                <p><strong>Muscle:</strong> {info['Muscle']} | <strong>Stretch:</strong> {info['Stretch']}</p>
                <p><em>"{info['Cue']}"</em></p>
                <a href="{get_youtube_link(name)}" target="_blank">📺 Demo</a>
            </div>
            """, unsafe_allow_html=True)

    # --- HISTORY TAB ---
    with tab_history:
        st.header("📜 Log")
        st.dataframe(load_history().sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
