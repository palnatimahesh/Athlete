# data.py

# ==========================================
# 1. DYNAMIC WARMUPS & COOLDOWNS
# ==========================================
WARMUPS = {
    "Lower": [{"name": "High Knees", "time": "30s", "note": "Get heart rate up."}, {"name": "Jumping Jacks", "time": "30s", "note": "Full body warmth."}, {"name": "Leg Swings", "time": "15/side", "note": "Loose hips."}],
    "Push": [{"name": "Arm Circles", "time": "30s", "note": "Big circles."}, {"name": "Plank to Down Dog", "time": "10 reps", "note": "Shoulder mobility."}, {"name": "Jumping Jacks", "time": "30s", "note": "Cardio."}],
    "Pull": [{"name": "Seal Jacks", "time": "30s", "note": "Open chest."}, {"name": "Cat-Cow", "time": "1 min", "note": "Spine flow."}, {"name": "Torso Twists", "time": "20 reps", "note": "Rotation."}],
    "Mobility": [{"name": "Boxer Shuffle", "time": "2 mins", "note": "Light bounce."}, {"name": "Joint Circles", "time": "2 mins", "note": "Wrists/Ankles."}],
    "Runtastic": [{"name": "Jumping Jacks", "time": "60s", "note": "Classic warmup."}, {"name": "High Knees", "time": "30s", "note": "Drive knees up."}, {"name": "Lunge Twist", "time": "10 reps", "note": "Step and twist."}]
}

COOLDOWNS = {
    "Lower": [{"name": "Quad Stretch", "time": "1 min/side", "target": "Quads"}, {"name": "Pigeon Pose", "time": "2 mins/side", "target": "Glutes"}],
    "Push": [{"name": "Chest Opener", "time": "1 min", "target": "Pecs"}, {"name": "Child's Pose", "time": "2 mins", "target": "Shoulders/Back"}],
    "Pull": [{"name": "Lat Stretch", "time": "1 min/side", "target": "Lats"}, {"name": "Forward Fold", "time": "2 mins", "target": "Hamstrings/Back"}],
    "Mobility": [{"name": "Deep Breathing", "time": "3 mins", "target": "Recovery"}],
    "Runtastic": [{"name": "Cobra Stretch", "time": "1 min", "target": "Abs"}, {"name": "Down Dog", "time": "1 min", "target": "Calves/Hams"}, {"name": "Butterfly", "time": "2 mins", "target": "Groin"}]
}

# ==========================================
# 2. FOUNDATION PHASE (LIFE PROTOCOL - PRESERVED)
# ==========================================
# (Keeping this here so the 'Life Protocol' mode still works if you switch back)
HOME_REPAIR = {
    "Monday": [{"name": "Pillow Squeeze", "sets": "4x15s", "tempo": "Max", "alt":"-", "note":"Adductors."}, {"name": "Copenhagen Plank", "sets": "3x20s", "tempo": "Hold", "alt":"-", "note":"Groin."}],
    "Thursday": [{"name": "Superman", "sets": "4x30s", "tempo": "Hold", "alt":"-", "note":"Back."}, {"name": "Bird Dog", "sets": "3x10", "tempo": "Hold", "alt":"-", "note":"Core."}],
    "Push": [{"name": "Pushups", "sets": "3xF", "tempo": "2-0-1", "alt":"-", "note":"Chest."}],
    "Pull": [{"name": "Door Row", "sets": "4x15", "tempo": "Squeeze", "alt":"-", "note":"Back."}]
}

FOUNDATION_PHASES = {
    "Phase 1: Structural Repair": {
        "Theme": "Fix Back.", "Class": "repair",
        "Routine": {
            "Monday": {"Focus": "Repair", "Type": "Home", "Category": "Lower", "Home_Map": "Monday", "Exercises": HOME_REPAIR["Monday"], "Core": []},
            "Tuesday": {"Focus": "Push", "Type": "Home", "Category": "Push", "Home_Map": "Push", "Exercises": HOME_REPAIR["Push"], "Core": []},
            "Thursday": {"Focus": "Back", "Type": "Home", "Category": "Lower", "Home_Map": "Thursday", "Exercises": HOME_REPAIR["Thursday"], "Core": []},
            "Friday": {"Focus": "Pull", "Type": "Home", "Category": "Pull", "Home_Map": "Pull", "Exercises": HOME_REPAIR["Pull"], "Core": []}
        }
    }
}

# ==========================================
# 3. THE 6-WEEK RUNTASTIC LEGACY COURSE
# ==========================================
# High Volume | Circuits | Cardio Elements

COURSE_DATA = {
    # --- WEEKS 1-2: INIT (Conditioning Base) ---
    1: {"Phase": "Weeks 1-2: The Initiation", "Theme": "phase1", "Schedule": {
            "Day 1": {"Focus": "Full Body Alpha", "Exercises": [
                {"name": "Jumping Jacks", "sets": "50 Reps", "tempo": "Fast", "note": "Continuous motion."},
                {"name": "Bodyweight Squats", "sets": "20 Reps", "tempo": "Steady", "note": "Full depth."},
                {"name": "Pushups", "sets": "10 Reps", "tempo": "Steady", "note": "Knees if needed."},
                {"name": "Sit-Ups", "sets": "15 Reps", "tempo": "Control", "note": "Touch toes."},
                {"name": "Mountain Climbers", "sets": "20 Reps (Total)", "tempo": "Fast", "note": "Knees to chest."}
            ]},
            "Day 2": {"Focus": "Lower Burn", "Exercises": [
                {"name": "High Knees", "sets": "30s", "tempo": "Sprint", "note": "Knees to hip height."},
                {"name": "Reverse Lunges", "sets": "20 Reps", "tempo": "Steady", "note": "Alternating legs."},
                {"name": "Glute Bridges", "sets": "20 Reps", "tempo": "Squeeze", "note": "Hips high."},
                {"name": "Squat Hold", "sets": "30s", "tempo": "Hold", "note": "Sit in the chair."}
            ]},
            "Day 3": {"Focus": "Core & Cardio", "Exercises": [
                {"name": "Bicycle Crunches", "sets": "30 Reps", "tempo": "Control", "note": "Elbow to opposite knee."},
                {"name": "Plank", "sets": "45s", "tempo": "Hold", "note": "Flat back."},
                {"name": "Leg Raises", "sets": "12 Reps", "tempo": "Slow", "note": "Hands under hips if needed."},
                {"name": "Boxer Shuffle", "sets": "2 mins", "tempo": "Bounce", "note": "Keep moving."}
            ]},
            "Day 4": {"Focus": "The Bravo Circuit", "Exercises": [
                {"name": "Burpees (No Pushup)", "sets": "10 Reps", "tempo": "Steady", "note": "Jump back, jump up."},
                {"name": "Pushups", "sets": "12 Reps", "tempo": "Steady", "note": "Chest to floor."},
                {"name": "Lunges", "sets": "20 Reps", "tempo": "Steady", "note": "Total reps."},
                {"name": "Plank Jacks", "sets": "20 Reps", "tempo": "Fast", "note": "Plank position, feet jump out/in."}
            ]}
    }},
    
    # --- WEEKS 3-4: TRANSFORMATION (Volume Increase) ---
    3: {"Phase": "Weeks 3-4: Transformation", "Theme": "phase2", "Schedule": {
            "Day 1": {"Focus": "Endurance Charlie", "Exercises": [
                {"name": "Prisoner Squats", "sets": "30 Reps", "tempo": "Fast", "note": "Hands behind head."},
                {"name": "Close Grip Pushups", "sets": "15 Reps", "tempo": "Steady", "note": "Elbows tight."},
                {"name": "High Knees", "sets": "40 Reps", "tempo": "Sprint", "note": "Count one leg."},
                {"name": "Superman Pull", "sets": "15 Reps", "tempo": "Hold 1s", "note": "Squeeze back."}
            ]},
            "Day 2": {"Focus": "Ab Destruction", "Exercises": [
                {"name": "Sit-Ups", "sets": "25 Reps", "tempo": "Steady", "note": "Full ROM."},
                {"name": "Russian Twists", "sets": "40 Reps", "tempo": "Fast", "note": "Total reps, feet up."},
                {"name": "Mountain Climbers", "sets": "40 Reps", "tempo": "Sprint", "note": "Burnout."},
                {"name": "Side Plank", "sets": "45s/side", "tempo": "Hold", "note": "Hips high."}
            ]},
            "Day 3": {"Focus": "Legs Delta", "Exercises": [
                {"name": "Jump Squats", "sets": "15 Reps", "tempo": "Explosive", "note": "Leave the ground."},
                {"name": "Forward Lunges", "sets": "24 Reps", "tempo": "Steady", "note": "Alternating."},
                {"name": "Calf Raises", "sets": "30 Reps", "tempo": "Quick", "note": "Burnout."},
                {"name": "Wall Sit", "sets": "60s", "tempo": "Hold", "note": "Don't quit."}
            ]},
            "Day 4": {"Focus": "Metabolic Echo", "Exercises": [
                {"name": "Burpees (Full)", "sets": "12 Reps", "tempo": "Steady", "note": "Chest to floor pushup included."},
                {"name": "Tricep Dips", "sets": "15 Reps", "tempo": "Control", "note": "Use chair."},
                {"name": "Squats", "sets": "40 Reps", "tempo": "Fast", "note": "Piston style."},
                {"name": "Jumping Jacks", "sets": "60 Reps", "tempo": "Fast", "note": "Cardio finish."}
            ]}
    }},

    # --- WEEKS 5-6: UNLEASHED (High Intensity) ---
    5: {"Phase": "Weeks 5-6: Unleashed", "Theme": "phase3", "Schedule": {
            "Day 1": {"Focus": "Full Body Foxtrot", "Exercises": [
                {"name": "Burpees", "sets": "20 Reps", "tempo": "Fast", "note": "Max effort."},
                {"name": "Jump Lunges", "sets": "20 Reps", "tempo": "Explosive", "note": "Switch in air."},
                {"name": "Pushups", "sets": "25 Reps", "tempo": "Steady", "note": "Break sets if needed."},
                {"name": "Leg Raises", "sets": "20 Reps", "tempo": "Control", "note": "Don't let heels touch floor."}
            ]},
            "Day 2": {"Focus": "Upper Power", "Exercises": [
                {"name": "Pike Pushups", "sets": "15 Reps", "tempo": "Control", "note": "Shoulders."},
                {"name": "Plank to Pushup", "sets": "15 Reps", "tempo": "Steady", "note": "Up, Up, Down, Down."},
                {"name": "Wide Pushups", "sets": "20 Reps", "tempo": "Steady", "note": "Chest focus."},
                {"name": "Door Rows", "sets": "25 Reps", "tempo": "Squeeze", "note": "Back endurance."}
            ]},
            "Day 3": {"Focus": "Core Inferno", "Exercises": [
                {"name": "Scissor Kicks", "sets": "40 Reps", "tempo": "Steady", "note": "Legs straight."},
                {"name": "Bicycle Crunches", "sets": "50 Reps", "tempo": "Fast", "note": "Total count."},
                {"name": "Plank", "sets": "90s", "tempo": "Hold", "note": "Mental toughness."},
                {"name": "Mountain Climbers", "sets": "60 Reps", "tempo": "Sprint", "note": "Gas tank empty."}
            ]},
            "Day 4": {"Focus": "The Final Test (Zulu)", "Exercises": [
                {"name": "High Knees", "sets": "50 Reps", "tempo": "Sprint", "note": "Start."},
                {"name": "Squats", "sets": "50 Reps", "tempo": "Fast", "note": "Keep moving."},
                {"name": "Pushups", "sets": "30 Reps", "tempo": "Steady", "note": "Grind."},
                {"name": "Sit-Ups", "sets": "40 Reps", "tempo": "Steady", "note": "Core."},
                {"name": "Burpees", "sets": "15 Reps", "tempo": "Max", "note": "Finish."}
            ]}
    }}
}

# MAP WEEKS (2->1, 4->3, 6->5)
COURSE_DATA[2] = COURSE_DATA[1]
COURSE_DATA[4] = COURSE_DATA[3]
COURSE_DATA[6] = COURSE_DATA[5]

# ==========================================
# 4. IRON BIBLE (ENHANCED FOR BODYWEIGHT)
# ==========================================
EXERCISE_BIBLE = {
    # CARDIO / PLYO
    "Jumping Jacks": {"Muscle": "Full Body", "Stretch": "Calf Stretch", "Cue": "Touch hands at top."},
    "Burpees": {"Muscle": "Full Body", "Stretch": "Quad/Chest", "Cue": "Drop fast, explode up."},
    "High Knees": {"Muscle": "Hip Flexors/Cardio", "Stretch": "Quad Stretch", "Cue": "Knees to belly button height."},
    "Mountain Climbers": {"Muscle": "Core/Cardio", "Stretch": "Cobra Pose", "Cue": "Keep hips low. Drive knees."},
    # LEGS
    "Bodyweight Squats": {"Muscle": "Quads", "Stretch": "Quad Stretch", "Cue": "Hips back first."},
    "Lunges": {"Muscle": "Legs", "Stretch": "Lunge Stretch", "Cue": "90 degree angles."},
    "Jump Squats": {"Muscle": "Explosiveness", "Stretch": "Quad Stretch", "Cue": "Soft landing."},
    "Pistol Squat": {"Muscle": "Legs (Advanced)", "Stretch": "Hamstring Fold", "Cue": "Balance on one foot."},
    # PUSH
    "Pushups": {"Muscle": "Chest/Tri", "Stretch": "Chest Opener", "Cue": "Chest to floor."},
    "Diamond Pushups": {"Muscle": "Triceps", "Stretch": "Overhead Tricep", "Cue": "Hands make a diamond."},
    "Pike Pushups": {"Muscle": "Shoulders", "Stretch": "Cross Body", "Cue": "Look at feet."},
    # CORE
    "Sit-Ups": {"Muscle": "Abs", "Stretch": "Cobra Pose", "Cue": "Curl up, don't yank neck."},
    "Leg Raises": {"Muscle": "Lower Abs", "Stretch": "Cobra Pose", "Cue": "Hands under hips for support."},
    "Russian Twists": {"Muscle": "Obliques", "Stretch": "Side Bend", "Cue": "Follow hands with eyes."},
    "Plank": {"Muscle": "Core Stability", "Stretch": "Child's Pose", "Cue": "Squeeze glutes."}
}
