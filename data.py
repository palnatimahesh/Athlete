# data.py

# ==========================================
# 1. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
WARMUPS = {
    "Lower": [
        {"name": "90/90 Hip Switch", "time": "2 mins", "note": "Internal/External rotation."},
        {"name": "Cat-Cow", "time": "1 min", "note": "Segmental spine movement."},
        {"name": "World's Greatest Stretch", "time": "5 reps/side", "note": "Open hips and t-spine."},
        {"name": "Glute Bridges", "time": "20 reps", "note": "Wake up the posterior chain."}
    ],
    "Push": [
        {"name": "Arm Circles", "time": "30 secs", "note": "Small to big circles."},
        {"name": "Band Pull-Aparts", "time": "20 reps", "note": "Retract scapula."},
        {"name": "Thoracic Rotations", "time": "10 reps/side", "note": "Open up chest."},
        {"name": "Scapular Pushups", "time": "15 reps", "note": "Elbows locked, move shoulders."}
    ],
    "Pull": [
        {"name": "Cat-Cow", "time": "1 min", "note": "Spine lube."},
        {"name": "Dead Hang", "time": "30 secs", "note": "Decompress shoulders."},
        {"name": "Band Pass-Throughs", "time": "15 reps", "note": "Shoulder mobility."},
        {"name": "Bird-Dog", "time": "10 reps", "note": "Core activation."}
    ],
    "Mobility": [
        {"name": "Light Walk", "time": "5 mins", "note": "Increase body temp."},
        {"name": "Joint Circles", "time": "2 mins", "note": "Wrists, ankles, neck."}
    ]
}

COOLDOWNS = {
    "Lower": [
        {"name": "Deep Squat Hold", "time": "1 min", "target": "Hips/Ankles"},
        {"name": "Couch Stretch", "time": "2 mins/side", "target": "Quads/Hip Flexors"},
        {"name": "Pigeon Pose", "time": "2 mins/side", "target": "Glutes/Piriformis"}
    ],
    "Push": [
        {"name": "Doorway Pec Stretch", "time": "1 min/side", "target": "Chest/Front Delt"},
        {"name": "Cross-Body Shoulder", "time": "1 min/side", "target": "Rear Delts"},
        {"name": "Overhead Tricep", "time": "1 min/side", "target": "Triceps"}
    ],
    "Pull": [
        {"name": "Child's Pose", "time": "2 mins", "target": "Lower Back/Lats"},
        {"name": "Lat Stretch (Doorframe)", "time": "1 min/side", "target": "Lats"},
        {"name": "Neck Tilts", "time": "1 min", "target": "Traps/Neck"}
    ],
    "Mobility": [
        {"name": "Corpse Pose", "time": "5 mins", "target": "CNS Reset/Breathing"}
    ]
}

# ==========================================
# 2. FOUNDATION PHASE (LIFE PROTOCOL)
# ==========================================
HOME_REPAIR = {
    "Monday": [ # ADDUCTOR REPAIR
        {"name": "Seated Pillow Squeeze", "sets": "4 x 15s", "tempo": "Max Effort", "alt":"-", "note": "Sit on chair. Squeeze pillow between knees 100% effort. Fires Adductors."},
        {"name": "Copenhagen Plank (Floor)", "sets": "3 x 20s", "tempo": "Hold", "alt":"-", "note": "Top knee on chair. Lift hips. Gold standard for groin strength."},
        {"name": "Bulgarian Split Squat", "sets": "3 x 10/leg", "tempo": "3-1-1", "alt":"-", "note": "Stretches hip flexor while strengthening glute."},
        {"name": "Glute Bridge March", "sets": "3 x 20", "tempo": "Slow", "alt":"-", "note": "Hips up. Lift one leg at a time without hips dropping."}
    ],
    "Thursday": [ # LOWER BACK ARMOUR
        {"name": "Superman Hold", "sets": "4 x 30s", "tempo": "Hold", "alt":"-", "note": "Lie on belly. Lift chest and thighs. Squeezes spinal erectors."},
        {"name": "Single Leg RDL (Bodyweight)", "sets": "3 x 12/leg", "tempo": "3-1-1", "alt":"-", "note": "Soft knee. Reach to floor. Forces QL muscle to balance spine."},
        {"name": "Bird-Dog (High Tension)", "sets": "3 x 10/side", "tempo": "Hold 5s", "alt":"-", "note": "Make a fist. Kick heel back hard. Brace core like getting punched."},
        {"name": "Doorframe Rows", "sets": "4 x 15", "tempo": "Squeeze", "alt":"-", "note": "Upper back posture fix."}
    ],
    "Push": [
        {"name": "Decline Pushups", "sets": "4xF", "tempo": "2-0-1", "alt":"-", "note": "Feet on couch. Hits Upper Chest."},
        {"name": "Pike Pushups", "sets": "3x10", "tempo": "Slow", "alt":"-", "note": "Hips high (V-Shape). Hits Shoulders."},
        {"name": "Door Flys", "sets": "3x15", "tempo": "Squeeze", "alt":"-", "note": "Lean through doorframe. Hits Chest."}
    ],
    "Pull": [
        {"name": "Door Towel Row", "sets": "4x15", "tempo": "Squeeze", "alt":"-", "note": "Wrap towel on doorknob. Pull chest to door. Hits Lats."},
        {"name": "Prone W-Raise", "sets": "3x15", "tempo": "Hold", "alt":"-", "note": "Lie on belly. Lift arms in W shape. Hits Rear Delts."},
        {"name": "Scap Retract", "sets": "3x20", "tempo": "Hold", "alt":"-", "note": "Stand against wall. Press elbows back. Fixes Posture."}
    ]
}

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

# ==========================================
# 3. THE 12-WEEK TRANSFORMATION (ADIDAS STYLE)
# ==========================================
COURSE_DATA = {
    # --- PHASE 1: THE FOUNDATION (Weeks 1-4) ---
    1: {"Phase": "Phase 1: Foundation", "Theme": "phase1", "Schedule": {
            "Day 1": {"Focus": "Lower Control", "Exercises": [{"name": "Bodyweight Squat", "sets": "3x15", "tempo": "Slow", "note": "3s down."}, {"name": "Glute Bridges", "sets": "3x15", "tempo": "Hold", "note": "Squeeze glutes."}, {"name": "Plank", "sets": "3x30s", "tempo": "Hold", "note": "Core tight."}]},
            "Day 2": {"Focus": "Upper Push/Pull", "Exercises": [{"name": "Pushups (or Knee)", "sets": "3x10", "tempo": "Control", "note": "Chest to floor."}, {"name": "Door Rows", "sets": "3x15", "tempo": "Squeeze", "note": "Retract scapula."}, {"name": "Superman", "sets": "3x30s", "tempo": "Hold", "note": "Lower back."}]},
            "Day 3": {"Focus": "Active Recovery", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "note": "Zone 2."}, {"name": "World's Greatest Stretch", "sets": "5/side", "tempo": "Flow", "note": "Mobility."}]},
            "Day 4": {"Focus": "Full Body A", "Exercises": [{"name": "Squat to Chair", "sets": "3x20", "tempo": "Touch", "note": "Tap and go."}, {"name": "Incline Pushups", "sets": "3x12", "tempo": "Control", "note": "Hands on couch."}, {"name": "Bird Dog", "sets": "3x10", "tempo": "Hold", "note": "Stability."}]}
    }},
    # --- PHASE 2: THE BUILDER (Weeks 5-8) ---
    5: {"Phase": "Phase 2: Strength Builder", "Theme": "phase2", "Schedule": {
            "Day 1": {"Focus": "Lower Strength", "Exercises": [{"name": "Bulgarian Split Squat", "sets": "3x10/leg", "tempo": "3-1-1", "note": "Deep stretch."}, {"name": "Single Leg RDL", "sets": "3x10/leg", "tempo": "Slow", "note": "Balance."}, {"name": "Side Planks", "sets": "3x45s", "tempo": "Hold", "note": "Obliques."}]},
            "Day 2": {"Focus": "Upper Strength", "Exercises": [{"name": "Decline Pushups", "sets": "3xF", "tempo": "Power", "note": "Feet elevated."}, {"name": "Towel Door Rows", "sets": "4x12", "tempo": "Max Squeeze", "note": "Back width."}, {"name": "Tricep Dips", "sets": "3x15", "tempo": "Control", "note": "Lockout."}]},
            "Day 3": {"Focus": "Conditioning", "Exercises": [{"name": "Jog/Run", "sets": "25m", "tempo": "Steady", "note": "Endurance."}, {"name": "Deadbug", "sets": "3x20", "tempo": "Slow", "note": "Core."}]},
            "Day 4": {"Focus": "Full Body Volume", "Exercises": [{"name": "1.5 Rep Squats", "sets": "3x15", "tempo": "Pump", "note": "Down, half up, down, up."}, {"name": "Spiderman Pushups", "sets": "3x10", "tempo": "Controlled", "note": "Knee to elbow."}, {"name": "Lunges", "sets": "3x20", "tempo": "Continuous", "note": "Total reps."}]}
    }},
    # --- PHASE 3: THE BEAST (Weeks 9-12) ---
    9: {"Phase": "Phase 3: Transformation", "Theme": "phase3", "Schedule": {
            "Day 1": {"Focus": "Explosive Lower", "Exercises": [{"name": "Jump Squats", "sets": "4x15", "tempo": "Explosive", "note": "Land soft."}, {"name": "Jump Lunges", "sets": "3x16", "tempo": "Fast", "note": "Switch in air."}, {"name": "Hollow Body Hold", "sets": "3x45s", "tempo": "Hold", "note": "Iron core."}]},
            "Day 2": {"Focus": "Explosive Upper", "Exercises": [{"name": "Plyo Pushups", "sets": "4x10", "tempo": "Clap", "note": "Explode up."}, {"name": "Mountain Climbers", "sets": "4x60s", "tempo": "Sprint", "note": "Non-stop."}, {"name": "Plank to Pushup", "sets": "3x12", "tempo": "Fast", "note": "Elbows to hands."}]},
            "Day 3": {"Focus": "HIIT & Sprints", "Exercises": [{"name": "Sprints", "sets": "10x40s", "tempo": "Max Effort", "note": "20s rest."}, {"name": "Leg Raises", "sets": "3x20", "tempo": "Control", "note": "No swing."}]},
            "Day 4": {"Focus": "The Finisher", "Exercises": [{"name": "Burpees", "sets": "50", "tempo": "Time", "note": "As fast as possible."}, {"name": "Air Squats", "sets": "100", "tempo": "Time", "note": "Non-stop."}, {"name": "Pushups", "sets": "50", "tempo": "Time", "note": "Good form."}, {"name": "Plank", "sets": "Max", "tempo": "Failure", "note": "Empty the tank."}]}
    }}
}

# --- WEEK MAPPING ---
# Weeks 1-4 use Phase 1 Logic
COURSE_DATA[2] = COURSE_DATA[1]; COURSE_DATA[3] = COURSE_DATA[1]; COURSE_DATA[4] = COURSE_DATA[1]
# Weeks 5-8 use Phase 2 Logic
COURSE_DATA[6] = COURSE_DATA[5]; COURSE_DATA[7] = COURSE_DATA[5]; COURSE_DATA[8] = COURSE_DATA[5]
# Weeks 9-12 use Phase 3 Logic
COURSE_DATA[10] = COURSE_DATA[9]; COURSE_DATA[11] = COURSE_DATA[9]; COURSE_DATA[12] = COURSE_DATA[9]

# ==========================================
# 4. IRON BIBLE (FULL ENCYCLOPEDIA)
# ==========================================
EXERCISE_BIBLE = {
    # LEGS
    "Goblet Squat": {"Muscle": "Quads/Core", "Stretch": "Couch Stretch", "Cue": "Elbows inside knees. Chest up."},
    "Copenhagen Plank": {"Muscle": "Adductors", "Stretch": "Butterfly", "Cue": "Lift hips high. Squeeze top leg."},
    "Seated Pillow Squeeze": {"Muscle": "Adductors", "Stretch": "Butterfly", "Cue": "Crush the pillow 100% effort."},
    "Bulgarian Split Squat": {"Muscle": "Glutes/Quads", "Stretch": "Couch Stretch", "Cue": "Torso forward for glutes. Upright for quads."},
    "Trap Bar Deadlift": {"Muscle": "Full Body", "Stretch": "Hamstring Fold", "Cue": "Push floor away. Hips low."},
    "RDL": {"Muscle": "Hamstrings", "Stretch": "Toe Touch", "Cue": "Hips back. Soft knees."},
    "Superman Hold": {"Muscle": "Lower Back", "Stretch": "Child's Pose", "Cue": "Lift chest and thighs."},
    "Leg Press": {"Muscle": "Quads", "Stretch": "Quad Stretch", "Cue": "Don't lock knees at top."},
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
