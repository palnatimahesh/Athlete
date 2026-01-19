import streamlit as st
import datetime
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Bulletproof Athlete v2", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .banner { padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; text-align: center; }
    .build { background-color: #2E7D32; }
    .shred { background-color: #D32F2F; }
    .flow { background-color: #1976D2; }
    .repair { background-color: #F57C00; }
    .alt-text { color: #d32f2f; font-size: 0.9em; font-style: italic; }
    .core-box { background-color: #f8f9fa; border-left: 5px solid #6c757d; padding: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- GLOBAL WARMUP & COOLDOWN ---
WARMUP_ROUTINE = [
    {"name": "90/90 Hip Switch", "time": "2 mins", "note": "Unlock hips."},
    {"name": "Cat-Cow", "time": "1 min", "note": "Spine lube."},
    {"name": "World's Greatest Stretch", "time": "5 reps/side", "note": "Full body opener."},
    {"name": "Glute Bridges", "time": "15 reps", "note": "Wake up glutes."}
]

COOLDOWN_ROUTINE = [
    {"name": "Dead Hang", "time": "1 min", "note": "Decompress spine."},
    {"name": "Deep Squat Hold", "time": "1 min", "note": "Hip mobility."},
    {"name": "Child's Pose", "time": "2 mins", "note": "Relax lower back."}
]

# --- DATA: FOUNDATION PHASES ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair (Days 1-30)": {
        "Theme": "Fix Back. Fire Adductors. Detox.",
        "Class": "repair",
        "Routine": {
            "Monday": {
                "Focus": "Lower Body A (Adductor/Glute)",
                "Exercises": [
                    {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "tempo": "Hold", "note": "Squeeze legs hard.", "alt": "Side Plank with leg lift"},
                    {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "tempo": "3-1-1", "note": "Torso vertical.", "alt": "Leg Press (Feet high & wide)"},
                    {"name": "Cable Pull-Throughs", "sets": "3 x 15", "tempo": "2-0-1", "note": "Hinge hips back.", "alt": "Dumbbell RDL (Light)"},
                    {"name": "Adductor Machine", "sets": "3 x 15", "tempo": "3-0-1", "note": "Control eccentric.", "alt": "Cable Adduction (Ankle strap)"}
                ],
                "Core": [{"name": "Deadbugs", "sets": "3 x 10/side"}]
            },
            "Tuesday": {
                "Focus": "Upper Body Push",
                "Exercises": [
                    {"name": "Seated DB Press", "sets": "3 x 10", "tempo": "2-1-1", "note": "Protect spine.", "alt": "Machine Shoulder Press"},
                    {"name": "Incline DB Press", "sets": "3 x 12", "tempo": "3-0-1", "note": "Upper chest.", "alt": "Incline Machine Press"},
                    {"name": "Chest Fly (Cable/Machine)", "sets": "3 x 15", "tempo": "2-1-1", "note": "Squeeze at center.", "alt": "Dumbbell Flys"}
                ],
                "Core": [{"name": "Pallof Press", "sets": "3 x 15s/side"}]
            },
            "Thursday": {
                "Focus": "Lower Body B (Hamstring/Back)",
                "Exercises": [
                    {"name": "Lying Leg Curls", "sets": "3 x 12", "tempo": "3-0-1", "note": "Control down.", "alt": "Seated Leg Curl"},
                    {"name": "DB RDL (Light)", "sets": "3 x 10", "tempo": "3-1-1", "note": "Stop at shins.", "alt": "45-Degree Back Extension"},
                    {"name": "Back Extensions", "sets": "3 x 15", "tempo": "2-1-1", "note": "Glutes only.", "alt": "Bird-Dog (Weighted)"}
                ],
                "Core": [{"name": "McGill Curl Up", "sets": "5 x 10s"}]
            },
            "Friday": {
                "Focus": "Upper Body Pull (Posture)",
                "Exercises": [
                    {"name": "Chest Supported Row", "sets": "3 x 10", "tempo": "2-1-1", "note": "Squeeze back.", "alt": "Seated Cable Row"},
                    {"name": "Face Pulls", "sets": "4 x 15", "tempo": "2-1-2", "note": "Fix posture.", "alt": "Reverse Pec Deck"},
                    {"name": "Lat Pulldowns", "sets": "3 x 12", "tempo": "2-0-1", "note": "Elbows down.", "alt": "Assisted Pull-up Machine"}
                ],
                "Core": [{"name": "Plank Shoulder Taps", "sets": "3 x 45s"}]
            }
        }
    }
    # (Phases 2 and 3 would follow similar structure - shortened here for brevity but logic holds)
}

# --- HELPER FUNCTIONS ---
def get_daily_plan(phase_data, day_name):
    if day_name in phase_data["Routine"]:
        return phase_data["Routine"][day_name]
    return None

def main():
    st.title("🛡️ Bulletproof Athlete Manager v2")
    
    # --- SIDEBAR ---
    st.sidebar.header("⚙️ Controls")
    mode = st.sidebar.radio("Mode", ["Foundation (Rehab)", "Infinity (Future)"])
    
    # Medication Tracker (Preserved)
    st.sidebar.divider()
    st.sidebar.header("💊 Stack Tracker")
    st.sidebar.caption("Morning: L-Carnitine + NMN (Empty Stomach)")
    st.sidebar.caption("Breakfast: Ubiquinol + Omega3 + B12")
    st.sidebar.caption("Night: Magnesium + Zinc")
    
    # --- MAIN LOGIC ---
    if mode == "Foundation (Rehab)":
        phase_name = "Phase 1: Structural Repair (Days 1-30)" # Default for now
        phase_data = FOUNDATION_PHASES[phase_name]
        
        # WEEKLY PREVIEW BUTTON
        with st.expander("📅 View Full Weekly Schedule"):
            week_data = []
            for d, data in phase_data["Routine"].items():
                ex_list = ", ".join([e["name"] for e in data["Exercises"]])
                week_data.append({"Day": d, "Focus": data["Focus"], "Main Lifts": ex_list})
            st.table(pd.DataFrame(week_data))

        today = datetime.datetime.now().strftime("%A")
        plan = get_daily_plan(phase_data, today)
        
        st.header(f"Today is {today}")
        
        if plan:
            st.markdown(f"<div class='banner repair'><h3>{plan['Focus']}</h3></div>", unsafe_allow_html=True)
            
            # 1. WARMUP SECTION
            st.subheader("🔥 Warmup (10 Mins)")
            for wu in WARMUP_ROUTINE:
                st.checkbox(f"**{wu['name']}** ({wu['time']}) - {wu['note']}", key=wu['name'])
            
            st.divider()
            
            # 2. MAIN WORKOUT SECTION
            st.subheader("🏋️ Main Workout (40 Mins)")
            st.info("💡 **Rest Rule:** Rest 2-3 minutes between sets. If you don't need the rest, the weight is too light.")
            
            for i, ex in enumerate(plan["Exercises"]):
                with st.container():
                    c1, c2, c3 = st.columns([3, 2, 1])
                    
                    # Exercise Name & Alternative
                    c1.markdown(f"**{i+1}. {ex['name']}**")
                    if "alt" in ex:
                        c1.markdown(f"<span class='alt-text'>Gym Busy? Use: {ex['alt']}</span>", unsafe_allow_html=True)
                    
                    # Details
                    c2.caption(f"Sets: {ex['sets']} | Tempo: {ex['tempo']}")
                    c2.caption(f"💡 {ex['note']}")
                    
                    # Checkbox
                    c3.checkbox("Done", key=f"ex_{i}")
                    st.markdown("---")

            # 3. CORE FINISHER SECTION
            st.markdown("<div class='core-box'><h4>🧱 Core Finisher (10 Mins)</h4>", unsafe_allow_html=True)
            for core in plan["Core"]:
                st.checkbox(f"**{core['name']}** ({core['sets']})", key=core['name'])
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.divider()

            # 4. COOLDOWN SECTION
            st.subheader("❄️ Cooldown (5 Mins)")
            for cd in COOLDOWN_ROUTINE:
                st.checkbox(f"**{cd['name']}** ({cd['time']}) - {cd['note']}", key=cd['name'])

        else:
            st.info("🔄 Active Recovery Day")
            st.markdown("""
            * **Morning:** Do the Daily Repair Routine (90/90 Hip Switch).
            * **Cardio:** Walk 8,000 steps.
            * **Hydration:** Drink 4 Liters of water.
            """)
            
            # Fallback Home Routine for Rest Days if needed
            if st.button("I feel stiff, give me a light routine"):
                st.write("**Do 3 rounds of:**")
                st.write("- Cat Cow x 10")
                st.write("- Bird Dog x 6/side")
                st.write("- Plank x 45s")

if __name__ == "__main__":
    main()
