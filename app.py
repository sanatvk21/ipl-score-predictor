import streamlit as st
import numpy as np
import pickle

# Page config
st.set_page_config(
    page_title="IPL Score Predictor",
    page_icon="🏏",
    layout="centered"
)

# Load model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

# Title
st.markdown(
    "<h1 style='text-align: center;'>🏏 IPL Score Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown("### Predict final score based on live match situation")

# Team selection (UI upgrade)
teams = ["MI", "CSK", "RCB", "KKR", "SRH", "DC", "RR", "PBKS", "GT", "LSG"]

colA, colB = st.columns(2)
with colA:
    batting_team = st.selectbox("Batting Team", teams)
with colB:
    bowling_team = st.selectbox("Bowling Team", teams)

st.divider()

# Inputs in columns
col1, col2 = st.columns(2)

with col1:
    overs = st.slider("Overs Completed", 5.0, 19.0, 10.0)
    current_score = st.number_input("Current Score", 0, 300, 80)

with col2:
    wickets = st.slider("Wickets Fallen", 0, 10, 2)

# Calculations
balls_left = int(120 - overs * 6)
run_rate = current_score / overs if overs > 0 else 0

# Match phase indicator
if overs < 6:
    st.info("🔥 Powerplay Phase")
elif overs < 15:
    st.info("⚖️ Middle Overs")
else:
    st.info("💣 Death Overs")

# Match summary
st.markdown(f"""
### 📊 Match Situation
- **Score:** {current_score}/{wickets}
- **Overs:** {overs}
- **Run Rate:** {round(run_rate, 2)}
- **Balls Left:** {balls_left}
""")

# Prediction button
if st.button("Predict Final Score 🚀"):

    X = np.array([[overs, current_score, run_rate, wickets, 10-wickets, balls_left, ]])
    prediction = model.predict(X)[0]

    # Styled output
    st.markdown(
        f"""
        <div style='text-align:center; padding:20px; border-radius:10px; background-color:#1f77b4;'>
            <h2 style='color:white;'>Predicted Final Score</h2>
            <h1 style='color:white;'>{int(prediction)}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Insight message
    if prediction > 180:
        st.success("🔥 High scoring match expected!")
    elif prediction > 150:
        st.warning("⚖️ Competitive total")
    else:
        st.error("🧊 Low scoring match")
