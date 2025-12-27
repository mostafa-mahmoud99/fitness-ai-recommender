import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Fitness Pro | Smart Advisor",
    page_icon="🏃‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. THE KNOWLEDGE BASE ---
# Structured by (Body Category, Fitness Objective)
rec_database = {
    ('obease', 'cardio'): {
        'ex': ["Low-impact walking", "Water aerobics", "Seated cycling"],
        'diet': "Focus on high-fiber, low-calorie density meals. Increase water intake to 3L daily.",
        'rec': "Start with 10-minute sessions to protect joints. Gradually increase to 20 minutes."
    },
    ('overweight', 'cardio'): {
        'ex': ["Brisk walking", "Elliptical trainer", "Incline walking"],
        'diet': "Balance lean proteins with complex carbohydrates like oats and brown rice.",
        'rec': "Maintain a steady heart rate zone for at least 30 minutes for optimal fat oxidation."
    },
    ('normal', 'strength'): {
        'ex': ["Barbell Squats", "Deadlifts", "Bench Press", "Pull-ups"],
        'diet': "Slight caloric surplus. Aim for 1.6g of protein per kg of body weight.",
        'rec': "Focus on progressive overload—aim to increase weight or reps every week."
    },
    ('underweight', 'strength'): {
        'ex': ["Push-ups", "Dumbbell lunges", "Plank", "Bodyweight squats"],
        'diet': "High protein and healthy fats. Incorporate nutrient-dense snacks between meals.",
        'rec': "Focus on movement quality and form over heavy weights initially."
    }
}

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3048/3048344.png", width=100)
st.sidebar.title("User Profile")

# BMI-based category selection
u_body = st.sidebar.selectbox(
    "Body Composition", 
    ["Normal", "Overweight", "Obease", "Underweight"],
    help="Select the category that best matches your current BMI/Profile."
).lower()

u_goal = st.sidebar.selectbox(
    "Fitness Objective", 
    ["Cardio", "Strength"],
    help="What is your primary training goal?"
).lower()

st.sidebar.divider()
st.sidebar.write("📡 **Sensor Connectivity: ACTIVE**")
st.sidebar.caption("Connected to PAMAP2 IMU Sensors")

# --- 4. MAIN DASHBOARD ---
st.title("🏃‍♂️ AI Smart Fitness Dashboard")
st.markdown("---")

# Top row: Activity Metrics
col1, col2, col3 = st.columns(3)

if st.button('🚀 RUN REAL-TIME SENSOR ANALYSIS', use_container_width=True):
    with st.spinner('Synchronizing with wearable sensors...'):
        time.sleep(1.2) # Simulating Random Forest inference time
        
        # Simulated Prediction based on PAMAP2 categories
        activities = ["Sitting", "Walking", "Running", "Standing", "Cycling"]
        detected = random.choice(activities)
        hr = random.randint(70, 160)
        
        # Row 1: Vital Metrics
        with col1:
            st.metric(label="Detected Movement", value=detected)
        with col2:
            st.metric(label="Simulated Heart Rate", value=f"{hr} BPM")
        with col3:
            # Active Status Logic: Filtering Sedentary vs Active
            status = "Sedentary" if detected in ["Sitting", "Lying", "Standing"] else "Active"
            st.metric(label="Activity Status", value=status)

        st.divider()

        # Row 2: Recommendation & Diet
        c_left, c_right = st.columns([2, 1])

        # --- SMART LOOKUP LOGIC ---
        key = (u_body, u_goal)
        if key not in rec_database:
            fallback_options = [k for k in rec_database.keys() if k[0] == u_body]
            plan = rec_database[fallback_options[0]] if fallback_options else rec_database[('normal', 'strength')]
        else:
            plan = rec_database[key]

        with c_left:
            st.subheader("📋 Personalized Workout Plan")
            
            if status == "Sedentary":
                st.warning(f"⚠️ **Motion Alert:** You have been '{detected}' for too long. Time to move!")
            else:
                st.success(f"🔥 **Intensity Match:** Your current activity ({detected}) aligns with your fitness goals.")
            
            st.markdown(f"### **Expert Recommendation:**")
            st.write(plan['rec'])
            
            # --- ADAPTIVE PRESCRIPTION LOGIC ---
            st.markdown("#### **Suggested Exercises:**")
            
            # Volume and Intensity shift based on Objective
            if u_goal == "strength":
                rep_scheme = ["5 Sets of 5", "4 Sets of 8", "4 Sets of 6", "3 Sets of 8", "3 Sets of 10"]
            else:
                rep_scheme = ["3 Sets of 15", "3 Sets of 20", "2 Sets of 15", "3 Sets of 12", "3 Sets of 20"]
            
            ex_data = pd.DataFrame({
                "Exercise Name": plan['ex'], 
                "Sets/Reps": rep_scheme[:len(plan['ex'])] 
            })
            st.table(ex_data)

        with c_right:
            st.subheader("🥗 Nutrition & Recovery")
            st.info(plan['diet'])
            
            st.subheader("📉 Burn Forecast")
            st.write("Estimated Intensity:")
            progress_val = 75 if u_goal == "cardio" else 45
            st.progress(progress_val)
            st.caption(f"Intensity Level: {progress_val}%")

else:
    st.info("👋 Welcome! Adjust your profile in the sidebar and click the button above to start your AI analysis.")

# --- 5. FOOTER ---
st.markdown("---")
st.caption("Classical Machine Learning Activity Recognition v2.0 | Developed for Research & Fitness Optimization")