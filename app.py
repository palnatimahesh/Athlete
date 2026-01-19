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
    .info-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 10px; }
    .stCheckbox { padding: 5px; }
</style>
""", unsafe_allow_html=True)

# --- DATA: FOUNDATION PHASES (DAYS 1-180) ---
FOUNDATION_PHASES = {
    "Phase 1: Structural Repair (Days 1-30)": {
        "Theme": "Fix Back. Fire Adductors. Detox.",
        "Description": "We limit volume to 4 exercises to ensure 100% focus. Your connective tissue (tendons/discs) heals 5x slower than muscle. We are building the chassis before the engine.",
        "Class": "repair",
        "Routine": {
            "Monday": [
                {"name": "Copenhagen Plank (Knee)", "sets": "3 x 20s", "tempo": "Hold", "note": "TOP QUALITY. Squeeze legs together like cracking a nut. If hips drop, stop."}, 
                {"name": "Goblet Squat (Heels High)", "sets": "4 x 12", "tempo": "3-1-1", "note": "3s Down. 1s Pause at bottom. Explode Up. Keep torso vertical."}, 
                {"name": "Cable Pull-Throughs", "sets": "3 x 15", "tempo": "2-0-1", "note": "Hinge hips back until hamstrings stretch. Squeeze glutes to stand."}, 
                {"name": "Adductor Machine", "sets": "3 x 15", "tempo": "3-0-1", "note": "Control the opening (eccentric) for 3 seconds. Don't let it snap back."}
            ],
            "Tuesday": [
                {"name": "Seated DB Press", "sets": "3 x 10", "tempo": "2-1-1", "note": "Sit firmly. Brace abs before pressing. Don't arch lower back."}, 
                {"name": "Incline DB Press", "sets": "3 x 12", "tempo": "3-0-1", "note": "3 seconds down. Feel the stretch in upper chest."}, 
                {"name": "Deadbugs", "sets": "3 x 10/side", "tempo": "Slow", "note": "CRITICAL: Keep lower back glued to floor. If it lifts, you failed."}
            ],
            "Thursday": [
                {"name": "Lying Leg Curls", "sets": "3 x 12", "tempo": "3-0-1", "note": "Don't swing. Control the weight on the way down."}, 
                {"name": "DB RDL (Light)", "sets": "3 x 10", "tempo": "3-1-1", "note": "Push hips back. Feel hamstring stretch. Stop at mid-shin."}, 
                {"name": "Back Extensions", "sets": "3 x 15", "tempo": "2-1-1", "note": "Lift using GLUTES, not lower back. Pause at top for 1s."}
            ],
            "Friday": [
                {"name": "Chest Supported Row", "sets": "3 x 10", "tempo": "2-1-1", "note": "Chest against pad to protect spine. Squeeze shoulder blades."}, 
                {"name": "Face Pulls", "sets": "4 x 15", "tempo": "2-1-2", "note": "Pull to forehead. Hold for 1s. Rotates shoulders back."}, 
                {"name": "Pallof Press", "sets": "3 x 15s", "tempo": "Hold", "note": "Anti-Rotation. Fight the cable pulling you sideways."}
            ]
        }
    },
    "Phase 2: Hypertrophy (Days 31-90)": {
        "Theme": "Build Muscle. Load the Spine.",
        "Description": "Now that the structure is fixed, we introduce heavy loading. We use compound movements to stimulate testosterone and muscle density.",
        "Class": "build",
        "Routine": {
            "Monday": [{"name": "Trap Bar Deadlift", "sets": "3 x 6", "tempo": "X-1-X", "note": "Explosive up. Control down."}, {"name": "Walking Lunges", "sets": "3 x 12", "tempo": "2-0-1", "note": "Deep lunge."}, {"name": "Copenhagen Plank (Straight)", "sets": "3 x 30s", "tempo": "Hold", "note": "Advanced version."}],
            "Tuesday": [{"name": "Overhead Press", "sets": "4 x 6", "tempo": "2-0-1", "note": "Standing."}, {"name": "Weighted Dips", "sets": "3 x 8", "tempo": "3-0-1", "note": "Lean forward."}, {"name": "Hanging Leg Raises", "sets": "3 x Failure", "tempo": "Controlled", "note": "No swinging."}],
            "Thursday": [{"name": "Front Squats", "sets": "3 x 8", "tempo": "3-1-1", "note": "Upright torso."}, {"name": "Nordic Curl Negatives", "sets": "3 x 5", "tempo": "5-0-X", "note": "As slow as possible down."}, {"name": "Calf Raises", "sets": "4 x 15", "tempo": "2-1-1", "note": "Full stretch."}],
            "Friday": [{"name": "Weighted Pullups", "sets": "4 x 6", "tempo": "2-0-1", "note": "Full ROM."}, {"name": "DB Rows", "sets": "3 x 10", "tempo": "2-0-1", "note": "Heavy."}, {"name": "Farmers Carry", "sets": "3 x 40m", "tempo": "Walk", "note": "Grip strength."}]
        }
    },
    "Phase 3: The Athlete (Days 91-180)": {
        "Theme": "Power & Speed.",
        "Description": "Focus shifts to Rate of Force Development (RFD). Moving weights fast to become athletic and explosive.",
        "Class": "shred",
        "Routine": {
            "Monday": [{"name": "Power Cleans", "sets": "5 x 3", "tempo": "Explosive", "note": "Snap hips."}, {"name": "Box Jumps", "sets": "3 x 5", "tempo": "Explosive", "note": "Soft land."}, {"name": "Sled Push", "sets": "5 Rounds", "tempo": "Max Effort", "note": "Drive."}],
            "Tuesday": [{"name": "Push Press", "sets": "4 x 5", "tempo": "X-0-1", "note": "Leg drive."}, {"name": "Plyo Pushups", "sets": "3 x 8", "tempo": "Explosive", "note": "Leave ground."}, {"name": "Med Ball Slams", "sets": "3 x 15", "tempo": "Max Effort", "note": "Slam hard."}],
            "Thursday": [{"name": "Sprints", "sets": "10 x 50m", "tempo": "Sprint", "note": "Max speed."}, {"name": "Kettlebell Swings", "sets": "4 x 20", "tempo": "X-0-X", "note": "Hip hinge."}, {"name": "Jump Lunges", "sets": "3 x 10", "tempo": "Continuous", "note": "Burnout."}],
            "Friday": [{"name": "Heavy Farmers Walk", "sets": "4 laps", "tempo": "Walk", "note": "Heavy."}, {"name": "Pullups (Explosive)", "sets": "5 x 5", "tempo": "Fast", "note": "Chest to bar."}, {"name": "Ab Wheel", "sets": "3 x 10", "tempo": "3-0-1", "note": "Core stability."}]
        }
    }
}

# --- DATA: INFINITY LOOP (DAY 181+) ---
INFINITY_SEASONS = {
    "BUILD (Strength Focus)": {
        "Theme": "Heavy Loads. Maximum Force.",
        "Class": "build",
        "Description": "High tension. Low reps. We are forcing the muscle fibers to thicken.",
        "Routine": {
            "Monday": [{"name": "Trap Bar Deadlift", "sets": "5 x 3", "tempo": "X-1-X", "note": "Heavy triples."}, {"name": "Weighted Dips", "sets": "5 x 5", "tempo": "2-0-1", "note": "Add weight belt."}, {"name": "Pendlay Rows", "sets": "4 x 8", "tempo": "Explosive", "note": "Strict form."}],
            "Wednesday": [{"name": "Back Squat", "sets": "5 x 5", "tempo": "3-1-1", "note": "Main lift."}, {"name": "Overhead Press", "sets": "5 x 5", "tempo": "2-0-1", "note": "Strict press."}, {"name": "Chin Ups", "sets": "4 x Max", "tempo": "2-0-1", "note": "Palms facing you."}],
            "Friday": [{"name": "Incline Bench", "sets": "4 x 8", "tempo": "3-0-1", "note": "Upper chest."}, {"name": "RDL", "sets": "4 x 8", "tempo": "3-1-1", "note": "Hamstrings."}, {"name": "Arms/Accessory", "sets": "3 x 12", "tempo": "2-0-1", "note": "Biceps/Triceps."}]
        }
    },
    "SHRED (Athlete Focus)": {
        "Theme": "Speed. Agility. Fat Burn.",
        "Class": "shred",
        "Description": "Conditioning focus. High heart rate. Plyometrics to improve elasticity.",
        "Routine": {
            "Monday": [{"name": "Power Cleans", "sets": "5 x 3", "tempo": "Fast", "note": "Explosive."}, {"name": "Box Jumps", "sets": "4 x 5", "tempo": "Fast", "note": "Land soft."}, {"name": "Sprints", "sets": "6 x 100m", "tempo": "Fast", "note": "All out."}],
            "Wednesday": [{"name": "Plyo Pushups", "sets": "4 x 10", "tempo": "Fast", "note": "Clap pushups."}, {"name": "Pullups (Fast)", "sets": "4 x 8", "tempo": "Fast", "note": "Explosive."}, {"name": "Burpees", "sets": "3 x 15", "tempo": "Continuous", "note": "Engine builder."}],
            "Friday": [{"name": "Kettlebell Swings", "sets": "4 x 20", "tempo": "Fast", "note": "Hips."}, {"name": "Goblet Squat Jumps", "sets": "4 x 10", "tempo": "Fast", "note": "Jump with weight."}, {"name": "Battle Ropes", "sets": "4 x 30s", "tempo": "Fast", "note": "Finisher."}]
        }
    },
    "FLOW (Mobility Focus)": {
        "Theme": "Joint Health. Recovery.",
        "Class": "flow",
        "Description": "Loaded stretching. We build strength at the end-ranges of motion to bulletproof joints.",
        "Routine": {
            "Monday": [{"name": "ATG Split Squat", "sets": "4 x 10/leg", "tempo": "3-1-1", "note": "Knee over toe."}, {"name": "Jefferson Curl", "sets": "3 x 10", "tempo": "5-1-5", "note": "Very light weight."}, {"name": "Copenhagen Plank", "sets": "3 x 45s", "tempo": "Hold", "note": "Adductors."}],
            "Wednesday": [{"name": "Ring Pushups", "sets": "4 x 12", "tempo": "2-1-1", "note": "Stabilization."}, {"name": "Face Pulls", "sets": "4 x 20", "tempo": "2-1-2", "note": "Rear delts."}, {"name": "Skin The Cat", "sets": "3 x 5", "tempo": "Slow", "note": "Shoulder mobility."}],
            "Friday": [{"name": "Single Leg RDL", "sets": "3 x 10/leg", "tempo": "3-1-1", "note": "Balance."}, {"name": "Cosack Squats", "sets": "3 x 10/side", "tempo": "2-1-1", "note": "Side lunges."}, {"name": "Q-L Side Bends", "sets": "3 x 15/side", "tempo": "2-0-1", "note": "Lower back armor."}]
        }
    }
}

HOME_ROUTINE = [
    {"name": "Pillow Glute Bridge", "sets": "3 x 15", "tempo": "Hold 3s", "note": "Squeeze pillow HARD between knees while lifting hips. Fires adductors."},
    {"name": "Prone Cobra", "sets": "3 x 45s", "tempo": "Hold", "note": "Lie on stomach. Lift chest. Thumbs up. Fixes Hunching."},
    {"name": "Bird-Dog Squares", "sets": "3 x 6/side", "tempo": "Slow", "note": "Draw squares in air with hand/foot. Core stability."},
    {"name": "Wall Sit", "sets": "3 x Failure", "tempo": "Hold", "note": "Back flat against wall. Thighs parallel to floor."}
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
    
    # --- SIDEBAR: EDUCATION & SETTINGS ---
    st.sidebar.header("📘 Methodology (Read First)")
    with st.sidebar.expander("Why only 4 exercises?"):
        st.write("""
        **1. Signal-to-Noise Ratio:** If you do 8 exercises, your focus drops by the end. Your weak links (Back/Adductors) fail, and you compensate with bad form. We want 4 perfect exercises, not 8 junk ones.
        
        **2. Connective Tissue:** Muscles adapt fast. Tendons and Discs adapt slowly. We are repairing the 'Chassis' (Skeleton) before upgrading the 'Engine' (Muscles).
        """)
    
    with st.sidebar.expander("How to Read Tempo (3-1-1)"):
        st.write("""
        **Example: 3-1-1**
        * **3s:** Lower the weight (Eccentric). Count '1-Mississippi, 2-Mississippi...'
        * **1s:** Pause at the bottom (Stretch).
        * **1s:** Explode Up (Concentric).
        
        *If it says 'Hold', just hold the position statically.*
        """)

    st.sidebar.divider()
    st.sidebar.header("⚙️ Training Mode")
    
    # 1. Mode Selection
    mode = st.sidebar.radio("Select Phase:", 
                            ["Foundation (First 6 Months)", "Infinity Loop (Forever)"],
                            index=0)
    
    selected_routine = {}
    current_theme = ""
    current_class = ""
    current_desc = ""
    
    if mode == "Foundation (First 6 Months)":
        phase_name = st.sidebar.selectbox("Current Phase:", list(FOUNDATION_PHASES.keys()))
        phase_data = FOUNDATION_PHASES[phase_name]
        selected_routine = phase_data["Routine"]
        current_theme = phase_data["Theme"]
        current_desc = phase_data.get("Description", "")
        current_class = phase_data["Class"]
        
    else: # Infinity Loop
        loop_style = st.sidebar.radio("Loop Style:", ["Seasonal (4 Months)", "Hybrid (Weekly Mix)"])
        
        if loop_style == "Seasonal (4 Months)":
            season_name = st.sidebar.selectbox("Current Season:", list(INFINITY_SEASONS.keys()))
            season_data = INFINITY_SEASONS[season_name]
            selected_routine = season_data["Routine"]
            current_theme = season_data["Theme"]
            current_desc = season_data.get("Description", "")
            current_class = season_data["Class"]
        else:
            # Hybrid Mode Logic
            today = datetime.datetime.now().strftime("%A")
            season_data, season_name = get_hybrid_workout(today)
            if season_data:
                selected_routine = season_data["Routine"]
                current_theme = f"Hybrid Mode: {season_name}"
                current_desc = "Mixing Strength, Speed, and Mobility in one week."
                current_class = season_data["Class"]
            else:
                selected_routine = {} 

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
        st.markdown(f"<div class='banner {current_class}'><h3>{current_theme}</h3><p>{current_desc}</p></div>", unsafe_allow_html=True)

    # Workout Display Logic
    missed_gym = st.checkbox("🚨 Missed Gym / Home Rescue Mode")
    
    if missed_gym:
        st.warning("House Rescue Routine Active")
        st.write("*Do this circuit 3 times. Rest 60s between rounds.*")
        for ex in HOME_ROUTINE:
            with st.container():
                cols = st.columns([2, 1, 2, 1])
                cols[0].markdown(f"**{ex['name']}**")
                cols[1].markdown(f"*{ex['sets']}*")
                cols[2].caption(f"💡 {ex['note']}")
                cols[3].checkbox("Done", key=f"home_{ex['name']}")
                st.divider()
            
    elif today in selected_routine:
        st.success("Gym Protocol Active")
        st.info("🔥 **Intensity Rule:** If the last rep isn't a struggle, you are going too light or too fast.")
        
        for ex in selected_routine[today]:
            with st.container():
                cols = st.columns([2, 1, 1, 2, 1])
                # Name
                cols[0].markdown(f"**{ex['name']}**")
                # Sets/Reps
                cols[1].markdown(f"Sets: {ex['sets']}")
                # Tempo
                cols[2].markdown(f"⏱️ {ex['tempo']}")
                # Notes
                cols[3].caption(f"💡 {ex['note']}")
                # Checkbox
                cols[4].checkbox("Done", key=ex['name'])
                st.divider()
    else:
        st.info("🔄 Active Recovery / Rest Day")
        st.markdown("""
        * **Steps:** Walk 8k-10k steps
        * **Mobility:** Do the Morning Repair Routine (90/90 Hip Switch)
        * **Diet:** Keep protein high, carbs low
        """)

    # Desk Fix Button (Always visible)
    st.divider()
    if st.button("💻 Sitting Too Long? (Click for Back Fix)"):
        st.info("1. Push hands into chair armrests -> Lift butt (Decompress)")
        st.info("2. Stand up -> Squeeze Glutes Hard (Reset Hips)")

if __name__ == "__main__":
    main()
