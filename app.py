# app.py
import streamlit as st
import datetime
import pandas as pd
import os
import data # Importing the data file we just created

# ==========================================
# 1. CONFIGURATION & HISTORY LOGIC
# ==========================================
st.set_page_config(page_title="Bulletproof Athlete Ultimate", page_icon="🛡️", layout="wide")

HISTORY_FILE = "workout_history.csv"

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

# ==========================================
# 2. STYLING
# ==========================================
st.markdown("""
<style>
    .banner { padding: 20px; border-radius: 12px; color: white; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    /* Life Protocol Colors */
    .repair { background: linear-gradient(135deg, #F57C00, #E65100); }
    .recovery { background: linear-gradient(135deg, #607D8B, #455A64); }
    /* 6-Week Course Colors */
    .phase1 { background: linear-gradient(135deg, #FF9800, #F57C00); }
    .phase2 { background: linear-gradient(135deg, #4CAF50, #2E7D32); }
    .phase3 { background: linear-gradient(135deg, #2196F3, #1565C0); }
    
    .alt-text { color: #d32f2f !important; font-size: 0.9em; font-weight: bold; display: block; margin-top: 5px; }
    .tempo-tag { background-color: #e3f2fd; color: #1565c0 !important; padding: 2px 8px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }
    
    /* Bible Card */
    .bible-card { background-color: #f1f8e9; color: #1a1a1a !important; padding: 15px; border-radius: 10px; border-left: 5px solid #558b2f; margin-bottom: 10px; }
    .bible-card h4 { color: #2e7d32 !important; margin: 0 0 5px 0; }
    .bible-card p { color: #1a1a1a !important; margin: 5px 0; }
    
    /* Core Box */
    .core-box { background-color: #e9ecef; color: #1a1a1a !important; border-left: 5px solid #343a40; padding: 15px; border-radius: 0 8px 8px 0; margin-top: 20px; }
    .core-box h4 { color: #1a1a1a !important; margin: 0 0 10px 0; }
    a { text-decoration: none; font-weight: bold; color: #0288D1 !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOGIC FUNCTIONS
# ==========================================
def get_daily_plan(data_source, day_name, is_home):
    gym_plan = data_source["Routine"].get(day_name, {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Mobility", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-"}], "Core": []})
    
    cat = gym_plan.get("Category", "Mobility")
    warmup = data.WARMUPS.get(cat, data.WARMUPS["Mobility"])
    cooldown = data.COOLDOWNS.get(cat, data.COOLDOWNS["Mobility"])

    if is_home and gym_plan["Type"] == "Gym":
        home_key = gym_plan.get("Home_Map", "Mobility")
        home_exs = data.HOME_REPAIR.get(home_key, data.HOME_REPAIR["Monday"]) 
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
    if mood == "Injured / Pain": return "🚨 **INJURY:** Gym Cancelled. Rehab Loaded.", True
    if mood == "Tired / Low Energy": return "📉 **ADJUST:** Reduce weight 20%.", False
    return "✅ **GO MODE:** Focus on structure.", False

# ==========================================
# 4. MAIN UI
# ==========================================
def main():
    st.title("🛡️ Bulletproof Athlete Ultimate")
    
    # MODE SELECTION
    mode = st.sidebar.selectbox("Select Training Mode", ["Life Protocol (Foundation)", "6-Week Alpha Course"])
    
    tab_workout, tab_bible, tab_history = st.tabs(["🏋️ Workout Of The Day", "📖 Iron Bible", "📜 History"])

    # --- SIDEBAR ---
    st.sidebar.divider()
    st.sidebar.header("⚙️ Settings")
    
    if mode == "Life Protocol (Foundation)":
        days_active = st.sidebar.number_input("Days Active", min_value=1, value=1)
        phase_progress = min(days_active / 30, 1.0)
        st.sidebar.write(f"**Phase 1 Progress:** {int(phase_progress*100)}%")
        st.sidebar.progress(phase_progress)
        location = st.sidebar.radio("Location", ["Gym", "Home"])
    else:
        # Course settings
        st.sidebar.info("Course Mode: Runtastic Style")
        selected_week = st.sidebar.selectbox("Select Week", [1,2,3,4,5,6])
        selected_day = st.sidebar.radio("Select Day", ["Day 1", "Day 2", "Day 3", "Day 4"])
        location = "Gym" # Default for course

    if st.sidebar.button("🗑️ Clear Logs"):
        clear_history()
        st.sidebar.success("Logs Cleared")
        st.rerun()

    # Meds
    st.sidebar.divider()
    st.sidebar.header("💊 Daily Stack")
    with st.sidebar.expander("Morning"): st.checkbox("L-Carnitine"); st.checkbox("NMN")
    with st.sidebar.expander("Breakfast"): 
        st.checkbox("Ubiquinol + Omega3")
        st.checkbox("B12 + C")
        st.checkbox("Vit E")
        st.checkbox("Vit D3 (Sundays Only)")
    with st.sidebar.expander("Night"): st.checkbox("Magnesium"); st.checkbox("Zinc")

    # --- TAB 1: WORKOUT DISPLAY ---
    with tab_workout:
        streak = get_streak(load_history())
        col1, col2 = st.columns([1,3])
        col1.metric("🔥 Streak", f"{streak}")
        mood = col2.selectbox("Daily Status", ["Neutral", "Great / Strong", "Tired / Low Energy", "Injured / Pain"])
        
        msg, override = ai_coach(1, mode, mood)
        if override: st.error(msg)
        else: st.info(msg)

        if st.button("✅ Log Complete"):
            log_key = f"Week {selected_week} {selected_day}" if mode == "6-Week Alpha Course" else datetime.date.today().strftime("%Y-%m-%d")
            save_history(log_key, mode, mood, "Yes")
            st.success("Workout Logged!")

        # === RENDER: LIFE PROTOCOL ===
        if mode == "Life Protocol (Foundation)":
            today_name = datetime.datetime.now().strftime("%A")
            st.header(f"📅 {today_name}")
            
            plan = {}
            if override:
                plan = {"Focus": "Emergency Rehab", "Type": "Rehab", "Exercises": data.HOME_REPAIR["Thursday"], "Core": [], "Warmup": [], "Cooldown": []} 
            else:
                plan = get_daily_plan(data.FOUNDATION_PHASES["Phase 1: Structural Repair"], today_name, location == "Home")

            st.markdown(f"<div class='banner repair'><h3>{plan['Focus']}</h3></div>", unsafe_allow_html=True)
            
            if plan.get("Warmup"):
                with st.expander("🔥 Warmup"):
                    for w in plan["Warmup"]: st.checkbox(f"**{w['name']}** ({w['time']})")
            
            st.subheader("🏋️ Routine")
            for i, ex in enumerate(plan["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3,2,1])
                    link = get_youtube_link(ex['name'])
                    c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                    if plan["Type"] == "Gym" and "alt" in ex and ex["alt"] != "-": c1.markdown(f"<span class='alt-text'>Gym Busy? {ex['alt']}</span>", unsafe_allow_html=True)
                    c2.markdown(f"**Sets:** {ex.get('sets','?')} | **Tempo:** <span class='tempo-tag'>{ex.get('tempo','-')}</span>", unsafe_allow_html=True)
                    if "note" in ex: c2.caption(f"💡 {ex['note']}")
                    c3.checkbox("Done", key=f"ex_{i}")
                    st.markdown("---")
            
            if plan.get("Core"):
                st.markdown("<div class='core-box'><h4>🧱 Core Finisher</h4>", unsafe_allow_html=True)
                for c in plan["Core"]: st.checkbox(f"{c['name']} ({c['sets']})")
                st.markdown("</div>", unsafe_allow_html=True)
            
            if plan.get("Cooldown"):
                 st.subheader("❄️ Cooldown")
                 for c in plan["Cooldown"]: st.checkbox(f"**{c['name']}** ({c['time']})")

        # === RENDER: 6-WEEK COURSE ===
        else:
            c_data = data.COURSE_DATA[selected_week]
            w_data = c_data["Schedule"][selected_day]
            st.markdown(f"<div class='banner {c_data['Theme']}'><h2>Week {selected_week} - {selected_day}</h2><p>{c_data['Phase']} | Focus: {w_data['Focus']}</p></div>", unsafe_allow_html=True)
            
            for i, ex in enumerate(w_data["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3,2,1])
                    link = get_youtube_link(ex['name'])
                    c1.markdown(f"**{i+1}. {ex['name']}** [[📺 Demo]]({link})")
                    c2.markdown(f"**Sets:** {ex['sets']} | **Tempo:** <span class='tempo-tag'>{ex['tempo']}</span>", unsafe_allow_html=True)
                    c2.caption(f"💡 {ex['note']}")
                    c3.checkbox("Done", key=f"wc_{i}")
                    st.markdown("---")

    # --- TAB 2: BIBLE ---
    with tab_bible:
        st.header("📖 Exercise Encyclopedia")
        search = st.text_input("🔍 Search", "")
        display_data = {k: v for k, v in data.EXERCISE_BIBLE.items() if search.lower() in k.lower()} if search else data.EXERCISE_BIBLE
        for name, data_entry in display_data.items():
            st.markdown(f"""
            <div class="bible-card">
                <h4>{name}</h4>
                <p><strong>Muscle:</strong> {data_entry['Muscle']} | <strong>Stretch:</strong> {data_entry['Stretch']}</p>
                <p><em>"{data_entry['Cue']}"</em></p>
                <a href="{get_youtube_link(name)}" target="_blank">📺 Demo</a>
            </div>
            """, unsafe_allow_html=True)

    # --- TAB 3: HISTORY ---
    with tab_history:
        st.header("📜 Log")
        st.dataframe(load_history().sort_values("Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
