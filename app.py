import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(layout="wide")

# 💀 FORCE START FROM WELCOME EVERY RUN
if "initialized" not in st.session_state:
    st.session_state.clear()
    st.session_state.initialized = True
    st.session_state.page = "welcome"
    st.session_state.logged_in = False


# -------- UTILS --------
def create_time_slots(start, end, duration):
    slots = []
    current = start

    while current < end:
        total = current.hour*60 + current.minute + duration
        h = total // 60
        m = total % 60
        slots.append(f"{current.strftime('%H:%M')} - {h:02}:{m:02}")
        current = current.replace(hour=h, minute=m)

    return slots


def generate_timetable(sections, days, slots, subjects, faculty_map):
    tt = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}

    for sub, hrs in subjects.items():
        for _ in range(hrs):
            sec = random.choice(sections)
            day = random.choice(days)
            slot = random.choice(slots)

            tt[sec].loc[day, slot] = f"{sub}\n({faculty_map[sub]})"

    return tt


def evaluate(tt):
    score = 0
    for sec, df in tt.items():
        score += (df == "").sum().sum()
    return score


def export_excel(tt):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sec, df in tt.items():
            df.to_excel(writer, sheet_name=sec)
    output.seek(0)
    return output.getvalue()


# -------- PAGE 1 --------
if st.session_state.page == "welcome":

    st.title("🤖 AI Timetable Generator")

    st.markdown("""
## 🚀 Intelligent Academic Scheduling System

Automatically generate optimized timetables.

### 🎯 Advantages
- Saves time  
- Reduces errors  
- Handles complexity  

### 📚 Uses
- Colleges  
- Schools  
- Coaching  

---
""")

    if st.button("➡️ Continue"):
        st.session_state.page = "login"
        st.rerun()


# -------- PAGE 2 --------
elif st.session_state.page == "login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid credentials")


# -------- PAGE 3 --------
elif st.session_state.page == "app":

    if not st.session_state.logged_in:
        st.session_state.page = "login"
        st.rerun()

    st.title("🚀 Timetable Dashboard")

    # -------- INPUT --------
    sections = st.multiselect("Sections", ["A","B","C"], default=["A"])
    days = ["Mon","Tue","Wed","Thu","Fri"]

    subjects = {}
    faculty = {}

    num = st.number_input("Subjects", 1, 10, 3)

    for i in range(num):
        sub = st.text_input(f"Subject {i}")
        hrs = st.number_input(f"Hours {i}", 1, 5, 2)
        fac = st.text_input(f"Faculty {i}")

        if sub:
            subjects[sub] = hrs
            faculty[sub] = fac

    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    duration = st.slider("Duration", 30, 120, 60)

    slots = create_time_slots(start, end, duration)

    # -------- GENERATE --------
    if st.button("Generate Timetable"):

        tt = generate_timetable(sections, days, slots, subjects, faculty)
        st.session_state.tt = tt

    # -------- DISPLAY --------
    if "tt" in st.session_state:

        tt = st.session_state.tt

        for sec, df in tt.items():
            st.subheader(f"Section {sec}")
            st.dataframe(df)

        score = evaluate(tt)
        st.metric("Score", score)

        file = export_excel(tt)

        st.download_button("Download Excel", file, "timetable.xlsx")

        # -------- ANALYTICS --------
        counts = {}

        for sec, df in tt.items():
            for d in df.index:
                counts[d] = counts.get(d, 0) + (df.loc[d] != "").sum()

        fig, ax = plt.subplots()
        ax.bar(counts.keys(), counts.values())
        st.pyplot(fig)

    # -------- LOGOUT --------
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()