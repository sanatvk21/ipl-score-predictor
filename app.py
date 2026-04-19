import streamlit as st
import numpy as np
import pickle
import pandas as pd  
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
# ===== HEADER =====
st.markdown("""
<div style='text-align:center; padding:10px; background: linear-gradient(90deg,#ff4b4b,#ffcc00); border-radius:10px;'>
    <h1 style='color:white;'>🏏 IPL Live Score Predictor</h1>
    <p style='color:white;'>Real-time match analytics by Sanat Mishra</p>
</div>
""", unsafe_allow_html=True)
teams = ["MI", "CSK", "RCB", "KKR", "SRH", "DC", "RR", "PBKS", "GT", "LSG"]

colA, colB = st.columns(2)

with colA:

    batting_team = st.selectbox("🏏 Batting Team", teams)

with colB:

    bowling_team = st.selectbox("🎯 Bowling Team", teams)
    st.markdown("#### Match Situation")

col1, col2 = st.columns(2)

with col1:
    overs = st.number_input("Overs (e.g., 10.3)", 0.0, 20.0, 10.0, step=0.1)
    current_score = st.number_input("Score", 0, 300, 80)

with col2:
    wickets = st.slider("Wickets", 0, 10, 2)

    overs_int = int(overs)
balls = int((overs - overs_int) * 10)

if balls > 5:
    st.error("Invalid overs format! Use x.y where y ≤ 5")

total_balls = overs_int * 6 + balls
balls_left = 120 - total_balls
run_rate = current_score / overs if overs > 0 else 0

st.markdown(f"""
<div style='background-color:#1e1e1e; padding:15px; border-radius:10px;'>
    <h2 style='color:#ffcc00;'>{batting_team}</h2>
    <h1 style='color:white;'>{current_score}/{wickets}</h1>
    <p style='color:#aaa;'>Overs: {overs} | RR: {round(run_rate,2)}</p>
</div>
""", unsafe_allow_html=True)

progress = int((total_balls / 120) * 100)
st.progress(progress)
st.caption(f"Innings Progress: {progress}%")
if st.button(" Predict Final Score"):

    X = np.array([[overs, current_score, run_rate, wickets, 10-wickets, balls_left]])
    prediction = model.predict(X)[0]

    # 🎯 MAIN RESULT CARD
    st.markdown(f"""
    <div style='background: linear-gradient(90deg,#ff4b4b,#ffcc00); padding:20px; border-radius:10px; text-align:center;'>
        <h2 style='color:white;'>Predicted Final Score</h2>
        <h1 style='color:white;'>{int(prediction)}</h1>
    </div>
    """, unsafe_allow_html=True)

    # 📊 RANGE
    st.info(f"Expected Range: {int(prediction-10)} - {int(prediction+10)}")

    # 🔥 MATCH INSIGHT
    if prediction > 190:
        st.success(" High Scoring Thriller!")
    elif prediction > 160:
        st.warning(" Competitive Match")
    else:
        st.error(" Low Scoring Game")

    # 📉 GRAPH
    import pandas as pd
    overs_range = list(range(1, int(overs)+1))
    scores = [current_score * (i/overs) for i in overs_range]

    df_plot = pd.DataFrame({"Overs": overs_range, "Score": scores})
    st.line_chart(df_plot.set_index("Overs"))
    st.markdown("""
<div style='text-align:center; margin-top:30px; padding:10px; border-top:1px solid #444;'>
    <p style='color:#aaa;'>
         Built with ❤️ by <span style='color:#ffcc00; font-weight:bold;'>Sanat Mishra</span>
    </p>
</div>
""", unsafe_allow_html=True)

