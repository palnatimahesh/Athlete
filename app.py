import streamlit as st
import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Bulletproof Athlete", page_icon="💪", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .banner { padding: 15px; border-radius: 10px; color: white; margin-bottom: 20px; text-align: center; }
    .build { background-color: #2E7D32; } /* Green */
    .shred { background-color: #D32F2F; } /* Red */
    .flow { background-color: #1976D2; } /* Blue */
    .repair { background-color: #F57C00; } /* Orange */
    .stCheckbox { padding: 5px; }
</style>
""", unsafe_allow_html=True)

# --- DATA: FOUNDATION PHASES (DAYS 1-180) ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair (Days 1-30)": {
        "Theme": "Fix Back. Fire Adductors. Detox.",
        "Class": "repair",
        "Routine": {
            "Monday": [
                {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "note": "Top knee on bench. Lift hips high."}, 
                {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "note": "Elevate heels. Torso vertical."}, 
                {"name": "Cable Pull-Throughs", "sets": "3 x 15", "note": "Hinge hips back. Squeeze glutes."}, 
                {"name": "Adductor Machine", "sets": "3 x 15", "note": "Squeeze legs together hard."}
            ],
            "Tuesday": [
                {"name": "Seated DB Press", "sets": "3 x 10", "note": "Sit down to protect spine."}, 
                {"name": "Incline DB Press", "sets": "3 x 12", "note": "Control the negative (3s down)."}, 
                {"name": "Deadbugs", "sets": "3 x 10/side", "note": "Lower back glued to floor."}
            ],
            "Thursday": [
                {"name": "Lying Leg Curls", "sets": "3 x 12", "note": "Full stretch at bottom."}, 
                {"name": "DB RDL (Light)", "sets": "3 x 10", "note": "Push hips back. Stop at shins."}, 
                {"name": "Back Extensions", "sets": "3 x 15", "note": "Squeeze glutes at top. Don't hyperextend."}
            ],
            "Friday": [
                {"name": "Chest Supported Row", "sets": "3 x 10", "note": "Chest against pad. Squeeze back."}, 
                {"name": "Face Pulls", "sets": "4 x 15", "note": "Pull to forehead. Fix posture."}, 
                {"name": "Pallof Press", "sets": "3 x 15s", "note": "Resist rotation. Core tight."}
            ]
        }
    },
    "Phase 2: Hypertrophy (Days 31-90)": {
        "Theme": "Build Muscle. Load the Spine.",
        "Class": "build",
        "Routine": {
            "Monday": [
                {"name": "Trap Bar Deadlift", "sets": "3 x 6", "note": "Chest up. Drive with legs."}, 
                {"name": "Walking Lunges", "sets": "3 x 12", "note": "Knee over toe is okay."}, 
                {"name": "Copenhagen Plank (Straight)", "sets": "3 x 30s", "note": "Legs straight. Advanced."}
            ],
            "Tuesday": [
                {"name": "Overhead Press", "sets": "4 x 6", "note": "Standing. Brace abs."}, 
                {"name": "Weighted Dips", "sets": "3 x 8", "note": "Lean forward for chest."}, 
                {"name": "Hanging Leg Raises", "sets": "3 x Failure", "note": "Control the swing."}
            ],
            "Thursday": [
                {"name": "Front Squats", "sets": "3 x 8", "note": "Bar on shoulders. Elbows high."}, 
                {"name": "Nordic Curl Negatives", "sets": "3 x 5", "note": "Lower slowly. Catch yourself."}, 
                {"name": "Calf Raises", "sets": "4 x 15", "note": "Full range of motion."}
            ],
            "Friday": [
                {"name": "Weighted Pullups", "sets": "4 x 6", "note": "Full stretch at bottom."}, 
                {"name": "DB Rows", "sets": "3 x 10", "note": "Flat back. Pull to hip."}, 
                {"name": "Farmers Carry", "sets": "3 x 40m", "note": "Heavy. Don't lean sideways."}
            ]
        }
    },
    "Phase 3: The Athlete (Days 91-180)": {
        "Theme": "Power & Speed.",
        "Class": "shred",
        "Routine": {
            "Monday": [
                {"name": "Power Cleans", "sets": "5 x 3", "note": "Explosive hip snap."}, 
                {"name": "Box Jumps", "sets": "3 x 5", "note": "Land soft."}, 
                {"name": "Sled Push", "sets": "5 Rounds", "note": "Sprint intensity."}
            ],
            "Tuesday": [
                {"name": "Push Press", "sets": "4 x 5", "note": "Use leg drive to launch weight."}, 
                {"name": "Plyo Pushups", "sets": "3 x 8", "note": "Explode off ground."}, 
                {"name": "Med Ball Slams", "sets": "3 x 15", "note": "Full body slam."}
            ],
            "Thursday": [
                {"name": "Sprints", "sets": "10 x 50m", "note": "Walk back recovery."}, 
                {"name": "Kettlebell Swings", "sets": "4 x 20", "note": "Snap hips forward."}, 
                {"name": "Jump Lunges", "sets": "3 x 10", "note": "Switch legs in air."}
            ],
            "Friday": [
                {"name": "Heavy Farmers Walk", "sets": "4 laps", "note": "Grip strength."}, 
                {"name": "Pullups (Explosive)", "sets": "5 x 5", "note": "Pull fast. Control down."}, 
                {"name": "Ab Wheel", "sets": "3 x 10", "note": "Don't let back sag."}
            ]
        }
    }
}

# --- DATA: INFINITY LOOP (DAY 181+) ---
INFINITY_SEASONS = {
    "BUILD (Strength Focus)": {
        "Theme": "Heavy Loads. Maximum Force.",
        "Class": "build",
        "Routine": {
            "Monday": [{"name": "Trap Bar Deadlift", "sets": "5 x 3", "note": "Heavy triples."}, {"name": "Weighted Dips", "sets": "5 x 5", "note": "Add weight belt."}, {"name": "Pendlay Rows", "sets": "4 x 8", "note": "Strict form."}],
            "Wednesday": [{"name": "Back Squat", "sets": "5 x 5", "note": "Main lift."}, {"name": "Overhead Press", "sets": "5 x 5", "note": "Strict press."}, {"name": "Chin Ups", "sets": "4 x Max", "note": "Palms facing you."}],
            "Friday": [{"name": "Incline Bench", "sets": "4 x 8", "note": "Upper chest."}, {"name": "RDL", "sets": "4 x 8", "note": "Hamstrings."}, {"name": "Arms/Accessory", "sets": "3 x 12", "note": "Biceps/Triceps."}]
        }
    },
    "SHRED (Athlete Focus)": {
        "Theme": "Speed. Agility. Fat Burn.",
        "Class": "shred",
        "Routine": {
            "Monday": [{"name": "Power Cleans", "sets": "5 x 3", "note": "Explosive."}, {"name": "Box Jumps", "sets": "4 x 5", "note": "Land soft."}, {"name": "Sprints", "sets": "6 x 100m", "note": "All out."}],
            "Wednesday": [{"name": "Plyo Pushups", "sets": "4 x 10", "note": "Clap pushups."}, {"name": "Pullups (Fast)", "sets": "4 x 8", "note": "Explosive."}, {"name": "Burpees", "sets": "3 x 15", "note": "Engine builder."}],
            "Friday": [{"name": "Kettlebell Swings", "sets": "4 x 20", "note": "Hips."}, {"name": "Goblet Squat Jumps", "sets": "4 x 10", "note": "Jump with weight."}, {"name": "Battle Ropes", "sets": "4 x 30s", "note": "Finisher."}]
        }
    },
    "FLOW (Mobility Focus)": {
        "Theme": "Joint Health. Recovery.",
        "Class": "flow",
        "Routine": {
            "Monday": [{"name": "ATG Split Squat", "sets": "4 x 10/leg", "note": "Knee over toe."}, {"name": "Jefferson Curl", "sets": "3 x 10", "note": "Very light weight."}, {"name": "Copenhagen Plank", "sets": "3 x 45s", "note": "Adductors."}],
            "Wednesday": [{"name": "Ring Pushups", "sets": "4 x 12", "note": "Stabilization."}, {"name": "Face Pulls", "sets": "4 x 20", "note": "Rear delts."}, {"name": "Skin The Cat", "sets": "3 x 5", "note": "Shoulder mobility."}],
            "Friday": [{"name": "Single Leg RDL", "sets": "3 x 10/leg", "note": "Balance."}, {"name": "Cosack Squats", "sets": "3 x 10/side", "note": "Side lunges."}, {"name": "Q-L Side Bends", "sets": "3 x 15/side", "note": "Lower back armor."}]
        }
    }
}

HOME_ROUTINE = [
    {"name": "Pillow Glute Bridge", "sets": "3 x 15", "note": "Squeeze pillow HARD. Fixes adductors."},
    {"name": "Prone Cobra", "sets": "3 x 45s", "note": "Fixes Hunching. Thumbs up."},
    {"name": "Bird-Dog Squares", "sets": "3 x 6/side", "note": "Draw squares with hand/foot."},
    {"name": "Wall Sit", "sets": "3 x Failure", "note": "Mental toughness."}
]

def get_hybrid_workout(day_name):
    """Logic for the Hybrid Weekly Mix"""
    if day_name == "Monday":
        return INFINITY_SEASONS["BUILD (Strength Focus)"], "BUILD (Strength Focus)"
    elif day_name == "Wednesday":
        return INFINITY_SEASONS["SHRED (Athlete Focus)"], "SHRED (Athlete Focus)"
    elif day_name == "Friday":
        return INFINITY_SEASONS["FLOW (Mobility Focus)"], "FLOW (Mobility Focus)"
    else:
        return None, None

def main():
    st.title("🏆 Bulletproof Athlete Manager")
    
    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("⚙️ Settings")
    
    # 1. Mode Selection
    mode = st.sidebar.radio("Select Training Mode:", 
                            ["Foundation (First 6 Months)", "Infinity Loop (Forever)"],
                            index=0)
    
    # 2. Phase/Season Logic
    selected_routine = {}
    current_theme = ""
    current_class = ""
    
    if mode == "Foundation (First 6 Months)":
        phase_name = st.sidebar.selectbox("Current Phase:", list(FOUNDATION_PHASES.keys()))
        phase_data = FOUNDATION_PHASES[phase_name]
        selected_routine = phase_data["Routine"]
        current_theme = phase_data["Theme"]
        current_class = phase_data["Class"]
        
    else: # Infinity Loop
        loop_style = st.sidebar.radio("Loop Style:", ["Seasonal (4 Months)", "Hybrid (Weekly Mix)"])
        
        if loop_style == "Seasonal (4 Months)":
            season_name = st.sidebar.selectbox("Current Season:", list(INFINITY_SEASONS.keys()))
            season_data = INFINITY_SEASONS[season_name]
            selected_routine = season_data["Routine"]
            current_theme = season_data["Theme"]
            current_class = season_data["Class"]
        else:
            # Hybrid Mode Logic
            today = datetime.datetime.now().strftime("%A")
            season_data, season_name = get_hybrid_workout(today)
            if season_data:
                selected_routine = season_data["Routine"]
                current_theme = f"Hybrid Mode: {season_name}"
                current_class = season_data["Class"]
            else:
                selected_routine = {} # Rest day logic handles this

    # 3. Medication Tracker
    st.sidebar.divider()
    st.sidebar.header("💊 Daily Stack")
    days_active = st.sidebar.number_input("Days Active:", min_value=1, value=1)
    
    with st.sidebar.expander("Morning (Empty Stomach)", expanded=True):
        st.checkbox("L-Carnitine")
        st.checkbox("NMN")
        if days_active > 100 and days_active % 90 == 0:
            st.error("⚠️ CYCLE OFF: L-Carnitine")

    with st.sidebar.expander("Breakfast (With Fat)"):
        st.checkbox("Ubiquinol + Omega3")
        st.checkbox("Vit B12 + C")
        if days_active > 90:
            st.error("🛑 STOP: Vitamin E")
        else:
            st.checkbox("Vitamin E")
            
    with st.sidebar.expander("Night"):
        st.checkbox("Magnesium")
        st.checkbox("Zinc (After Dinner)")

    # --- MAIN CONTENT ---
    today = datetime.datetime.now().strftime("%A")
    st.subheader(f"📅 Today is {today}")
    
    # Banner
    if current_theme:
        st.markdown(f"<div class='banner {current_class}'><h3>{current_theme}</h3></div>", unsafe_allow_html=True)

    # Workout Display Logic
    missed_gym = st.checkbox("🚨 Missed Gym / Home Rescue Mode")
    
    if missed_gym:
        st.warning("House Rescue Routine Active")
        for ex in HOME_ROUTINE:
            st.checkbox(f"**{ex['name']}** - {ex['note']}")
            
    elif today in selected_routine:
        st.success("Gym Protocol Active")
        for ex in selected_routine[today]:
            with st.container():
                cols = st.columns([3, 1])
                cols[0].markdown(f"**{ex['name']}**")
                cols[0].caption(ex.get('note', ex['sets']))
                cols[1].checkbox("Done", key=ex['name'])
                st.divider()
    else:
        st.info("🔄 Active Recovery / Rest Day")
        st.markdown("""
        * **Steps:** Walk 8k-10k steps
        * **Mobility:** Do the Morning Repair Routine
        * **Diet:** Keep protein high, carbs low
        """)

    # Desk Fix Button (Always visible)
    st.divider()
    if st.button("💻 Sitting Too Long? (Click for Back Fix)"):
        st.info("1. Push hands into chair armrests -> Lift butt (Decompress)")
        st.info("2. Stand up -> Squeeze Glutes Hard (Reset Hips)")

if __name__ == "__main__":
    main()
