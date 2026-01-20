# data.py

# ==========================================
# 1. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
WARMUPS = {
    "Lower": [
        {"name": "Jumping Jacks", "time": "60 secs", "note": "Get heart rate up."},
        {"name": "High Knees", "time": "45 secs", "note": "Drive knees to chest."},
        {"name": "Bodyweight Squats", "time": "20 reps", "note": "Fast tempo."},
        {"name": "Lunge with Twist", "time": "10 reps/side", "note": "Open hips."}
    ],
    "Push": [
        {"name": "Arm Circles", "time": "30 secs", "note": "Big circles."},
        {"name": "Plank to Down-Dog", "time": "10 reps", "note": "Shoulder mobility."},
        {"name": "Wall Pushups", "time": "15 reps", "note": "Activation."},
        {"name": "Jumping Jacks", "time": "60 secs", "note": "Blood flow."}
    ],
    "Pull": [
        {"name": "Jumping Jacks", "time": "60 secs", "note": "Warmup."},
        {"name": "Arm Cross Swings", "time": "30 secs", "note": "Chest opener."},
        {"name": "Cat-Cow", "time": "1 min", "note": "Spine."},
        {"name": "Superman Pulses", "time": "15 reps", "note": "Wake up back."}
    ],
    "Mobility": [
        {"name": "Light Jog/March", "time": "3 mins", "note": "Gentle."},
        {"name": "Hip Circles", "time": "1 min", "note": "Loosen up."}
    ]
}

COOLDOWNS = {
    "Lower": [
        {"name": "Quad Stretch (Standing)", "time": "1 min/side", "target": "Quads"},
        {"name": "Deep Lunge Hold", "time": "1 min/side", "target": "Hip Flexors"},
        {"name": "Butterfly Stretch", "time": "2 mins", "target": "Adductors"}
    ],
    "Push": [
        {"name": "Chest Opener against Wall", "time": "1 min/side", "target": "Pecs"},
        {"name": "Child's Pose", "time": "2 mins", "target": "Shoulders/Back"},
        {"name": "Tricep Overhead Stretch", "time": "1 min/side", "target": "Triceps"}
    ],
    "Pull": [
        {"name": "Cat-Cow (Slow)", "time": "2 mins", "target": "Spine"},
        {"name": "Seated Forward Fold", "time": "2 mins", "target": "Hamstrings/Back"},
        {"name": "Neck Rolls", "time": "1 min", "target": "Neck"}
    ],
    "Mobility": [
        {"name": "Corpse Pose", "time": "5 mins", "target": "Total Relaxation"}
    ]
}

# ==========================================
# 2. RUNTASTIC 6-WEEK TRANSFORMATION DATA
# ==========================================
# Logic: 4 Days/Week. Circuit Style.
# Day 1: Full Body Alpha
# Day 2: Core & Cardio
# Day 3: Lower Body Power
# Day 4: The "Runtastic" Challenge (High Reps)

COURSE_DATA = {
    # --- WEEKS 1-2: THE IGNITION (Adaptation) ---
    1: {"Phase": "Phase 1: Ignition", "Theme": "phase1", "Schedule": {
        "Day 1": {"Focus": "Full Body Tone", "Exercises": [
            {"name": "Pushups", "sets": "3 Rounds x 12", "tempo": "Steady", "note": "Chest to floor."},
            {"name": "Squats", "sets": "3 Rounds x 20", "tempo": "Fast", "note": "Deep depth."},
            {"name": "Lunges", "sets": "3 Rounds x 14", "tempo": "Steady", "note": "Alternating legs."},
            {"name": "Plank", "sets": "3 Rounds x 45s", "tempo": "Hold", "note": "Keep back flat."}
        ]},
        "Day 2": {"Focus": "Abs & Cardio", "Exercises": [
            {"name": "Mountain Climbers", "sets": "3 x 40s", "tempo": "Fast", "note": "Knees to chest."},
            {"name": "High Knees", "sets": "3 x 40s", "tempo": "Sprint", "note": "Run in place."},
            {"name": "Bicycle Crunches", "sets": "3 x 20", "tempo": "Control", "note": "Elbow to opposite knee."},
            {"name": "Leg Raises", "sets": "3 x 15", "tempo": "Slow", "note": "Don't arch back."}
        ]},
        "Day 3": {"Focus": "Lower Body Burn", "Exercises": [
            {"name": "Sumo Squats", "sets": "4 x 15", "tempo": "Steady", "note": "Feet wide, toes out."},
            {"name": "Glute Bridges", "sets": "4 x 20", "tempo": "Squeeze", "note": "Pause at top."},
            {"name": "Wall Sit", "sets": "3 x 60s", "tempo": "Hold", "note": "Thighs parallel."},
            {"name": "Calf Raises", "sets": "3 x 25", "tempo": "Fast", "note": "Burnout."}
        ]},
        "Day 4": {"Focus": "The Challenge (No Rest)", "Exercises": [
            {"name": "Jumping Jacks", "sets": "50 Reps", "tempo": "Non-stop", "note": "Warm up."},
            {"name": "Bodyweight Squats", "sets": "40 Reps", "tempo": "Non-stop", "note": "Burn the legs."},
            {"name": "Pushups", "sets": "30 Reps", "tempo": "Non-stop", "note": "Break if needed."},
            {"name": "Sit-ups", "sets": "20 Reps", "tempo": "Non-stop", "note": "Full range."},
            {"name": "Burpees", "sets": "10 Reps", "tempo": "Max Effort", "note": "Finish strong."}
        ]}
    }},

    # --- WEEKS 3-4: ACCELERATION (Intensity Up) ---
    2: {"Phase": "Phase 2: Acceleration", "Theme": "phase2", "Schedule": {
        "Day 1": {"Focus": "Full Body Power", "Exercises": [
            {"name": "Plyo Pushups", "sets": "3 x 10", "tempo": "Explosive", "note": "Hands leave ground."},
            {"name": "Jump Squats", "sets": "3 x 15", "tempo": "Explosive", "note": "Land soft."},
            {"name": "Commandos", "sets": "3 x 12", "tempo": "Steady", "note": "Plank to Pushup position."},
            {"name": "Side Plank Dips", "sets": "3 x 15/side", "tempo": "Steady", "note": "Obliques."}
        ]},
        "Day 2": {"Focus": "Core Crusher", "Exercises": [
            {"name": "Russian Twists", "sets": "3 x 40s", "tempo": "Fast", "note": "Feet off ground."},
            {"name": "Plank Jacks", "sets": "3 x 40s", "tempo": "Fast", "note": "Plank + Jumping Jack legs."},
            {"name": "Flutter Kicks", "sets": "3 x 40s", "tempo": "Fast", "note": "Legs straight."},
            {"name": "Superman Hold", "sets": "3 x 45s", "tempo": "Hold", "note": "Squeeze lower back."}
        ]},
        "Day 3": {"Focus": "Legs & Lungs", "Exercises": [
            {"name": "Jump Lunges", "sets": "4 x 16 (Total)", "tempo": "Fast", "note": "Switch in air."},
            {"name": "Single Leg RDL", "sets": "3 x 12/leg", "tempo": "Slow", "note": "Balance."},
            {"name": "Curtsy Lunges", "sets": "3 x 15/side", "tempo": "Steady", "note": "Target glutes."},
            {"name": "Burpees", "sets": "3 x 12", "tempo": "Steady", "note": "Pace yourself."}
        ]},
        "Day 4": {"Focus": "The 300 Challenge", "Exercises": [
            {"name": "Squats", "sets": "100 Reps", "tempo": "Time", "note": "As fast as possible."},
            {"name": "Pushups", "sets": "50 Reps", "tempo": "Time", "note": "Chest to floor."},
            {"name": "Lunges", "sets": "50 Reps", "tempo": "Time", "note": "Total count."},
            {"name": "Situps", "sets": "50 Reps", "tempo": "Time", "note": "Core burner."},
            {"name": "Burpees", "sets": "50 Reps", "tempo": "Time", "note": "The finisher."}
        ]}
    }},

    # --- WEEKS 5-6: PEAK PERFORMANCE (Max Effort) ---
    3: {"Phase": "Phase 3: Peak Performance", "Theme": "phase3", "Schedule": {
        "Day 1": {"Focus": "Tabata Style (20s Work/10s Rest)", "Exercises": [
            {"name": "Burpees", "sets": "8 Rounds", "tempo": "Max Effort", "note": "Tabata Protocol."},
            {"name": "Pushups", "sets": "8 Rounds", "tempo": "Max Effort", "note": "Tabata Protocol."},
            {"name": "Jump Squats", "sets": "8 Rounds", "tempo": "Max Effort", "note": "Tabata Protocol."},
            {"name": "Situps", "sets": "8 Rounds", "tempo": "Max Effort", "note": "Tabata Protocol."}
        ]},
        "Day 2": {"Focus": "Strength Endurance", "Exercises": [
            {"name": "Decline Pushups", "sets": "4 x Failure", "tempo": "Control", "note": "Feet on chair."},
            {"name": "Pistol Squat (Box)", "sets": "4 x 8/leg", "tempo": "Slow", "note": "Single leg sit/stand."},
            {"name": "Tricep Dips", "sets": "4 x 20", "tempo": "Pump", "note": "Chair dips."},
            {"name": "V-Ups", "sets": "4 x 15", "tempo": "Snap", "note": "Touch toes."}
        ]},
        "Day 3": {"Focus": "Agility & Speed", "Exercises": [
            {"name": "Sprints (In Place)", "sets": "10 x 30s", "tempo": "Sprint", "note": "High knees fast."},
            {"name": "Lateral Jumps", "sets": "3 x 45s", "tempo": "Bounding", "note": "Skater jumps."},
            {"name": "Spiderman Pushups", "sets": "3 x 12", "tempo": "Control", "note": "Knee to elbow."},
            {"name": "Plank to Squat", "sets": "3 x 15", "tempo": "Flow", "note": "Mobility + Speed."}
        ]},
        "Day 4": {"Focus": "The Final Exam", "Exercises": [
            {"name": "Burpees", "sets": "100 Reps", "tempo": "For Time", "note": "Do them all. No time limit."},
            {"name": "Squats", "sets": "100 Reps", "tempo": "For Time", "note": "Legs will burn."},
            {"name": "Pushups", "sets": "100 Reps", "tempo": "For Time", "note": "Break into sets."},
            {"name": "Plank", "sets": "Max Hold", "tempo": "Failure", "note": "Until you drop."}
        ]}
    }}
}

# Clone weeks to fill the 6-week schedule
COURSE_DATA[2] = COURSE_DATA[1]
COURSE_DATA[4] = COURSE_DATA[2]
COURSE_DATA[6] = COURSE_DATA[3]

# ==========================================
# 3. LIFE PROTOCOL DATA (Shared from previous)
# ==========================================
# (Keeping your Life Protocol intact so you have both options)
HOME_REPAIR = {
    "Monday": [{"name": "Seated Pillow Squeeze", "sets": "4x15s", "tempo": "Max", "alt":"-", "note":"Adductor"}, {"name": "Copenhagen Plank", "sets": "3x20s", "tempo":"Hold", "alt":"-", "note":"Adductor"}, {"name": "Split Squat", "sets": "3x10", "tempo":"3-1-1", "alt":"-", "note":"Glute"}],
    "Thursday": [{"name": "Superman", "sets": "4x30s", "tempo":"Hold", "alt":"-", "note":"Back"}, {"name": "Single Leg RDL", "sets": "3x12", "tempo":"3-1-1", "alt":"-", "note":"Hinge"}, {"name": "Bird Dog", "sets": "3x10", "tempo":"Hold", "alt":"-", "note":"Core"}],
    "Push": [{"name": "Pike Pushups", "sets": "3x10", "tempo":"Slow", "alt":"-", "note":"Shoulders"}, {"name": "Pushups", "sets": "3xF", "tempo":"2-0-1", "alt":"-", "note":"Chest"}],
    "Pull": [{"name": "Towel Row", "sets": "4x15", "tempo":"Squeeze", "alt":"-", "note":"Back"}, {"name": "Scap Retract", "sets": "3x20", "tempo":"Hold", "alt":"-", "note":"Posture"}]
}

FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Theme": "Fix Back.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Adductors", "Type": "Gym", "Category": "Lower", "Home_Map": "Monday", "Exercises": [{"name": "Adductor Machine", "sets": "3x15", "tempo": "3-0-1", "alt": "Cable", "note": "Squeeze."}], "Core": []},
            "Tuesday": {"Focus": "Push", "Type": "Gym", "Category": "Push", "Home_Map": "Push", "Exercises": [{"name": "DB Press", "sets": "3x10", "tempo": "2-1-1", "alt": "Machine", "note": "Press."}], "Core": []},
            "Wednesday": {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Monday", "Exercises": [{"name": "Walk", "sets": "30m", "tempo": "-", "alt": "-", "note": "Walk"}], "Core": []},
            "Thursday": {"Focus": "Back", "Type": "Gym", "Category": "Lower", "Home_Map": "Thursday", "Exercises": [{"name": "Back Ext", "sets": "3x15", "tempo": "2-1-1", "alt": "Bird Dog", "note": "Hinge."}], "Core": []},
            "Friday": {"Focus": "Pull", "Type": "Gym", "Category": "Pull", "Home_Map": "Pull", "Exercises": [{"name": "Row", "sets": "3x10", "tempo": "2-1-1", "alt": "Cable", "note": "Row."}], "Core": []},
            "Saturday": {"Focus": "Fun", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Monday", "Exercises": [{"name": "Hike", "sets": "60m", "tempo": "-", "alt": "-", "note": "Move"}], "Core": []},
            "Sunday": {"Focus": "Rest", "Type": "Recovery", "Category": "Mobility", "Home_Map": "Monday", "Exercises": [{"name": "Rest", "sets": "-", "tempo": "-", "alt": "-", "note": "Rest"}], "Core": []},
        }
    }
}

EXERCISE_BIBLE = {
    "Burpees": {"Muscle": "Full Body", "Stretch": "Child's Pose", "Cue": "Chest to floor, jump high."},
    "Mountain Climbers": {"Muscle": "Core/Cardio", "Stretch": "Cobra", "Cue": "Keep hips low, knees fast."},
    "Jump Squats": {"Muscle": "Legs/Power", "Stretch": "Quad Stretch", "Cue": "Explode up, land soft."},
    "Pushups": {"Muscle": "Chest", "Stretch": "Chest Opener", "Cue": "Elbows back, core tight."},
    "Plank": {"Muscle": "Core", "Stretch": "Cobra", "Cue": "Squeeze glutes, don't sag."},
    "High Knees": {"Muscle": "Cardio", "Stretch": "Quad Stretch", "Cue": "Knees above hips."},
    "Seated Pillow Squeeze": {"Muscle": "Adductors", "Stretch": "Butterfly", "Cue": "Crush it."},
    "Superman Hold": {"Muscle": "Lower Back", "Stretch": "Child's Pose", "Cue": "Lift everything."}
}
