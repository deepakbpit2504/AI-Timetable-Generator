import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from auth import login, logout
from scheduler import generate_timetable, evaluate_timetable, build_faculty_timetable
from utils import create_time_slots, export_to_excel

st.set_page_config(layout="wide")

# -------- CLEAN UI --------
st.markdown("""
<style>
.block-container {max-width: 1100px; margin:auto;}
h1,h2,h3{text-align:center;}
.stButton>button {width:100%; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# -------- LOGIN FLOW --------
if not login():
    st.stop()

logout()

# -------- STEP CONTROL --------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------- STEP 1 --------
if st.session_state.step == 1:

    st.markdown("## 📘 Academic Setup")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
        branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])

    with col2:
        sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

    rooms = {"Room 101":60, "Room 102":40, "Lab 1":30}

    students = {}
    for sec in sections:
        students[sec] = st.number_input(f"Students {sec}", 10,100,60)

    combined = st.multiselect("Combined Sections", sections)

    if st.button("Next ➡️"):
        st.session_state.update(locals())
        st.session_state.step = 2
        st.rerun()

# -------- STEP 2 --------
elif st.session_state.step == 2:

    st.markdown("## 👨‍🏫 Subjects")
    st.divider()

    num = st.number_input("Subjects",1,10,5)

    subjects = {}
    faculty_map = {}

    for i in range(num):
        name = st.text_input(f"Subject {i}")
        theory = st.number_input(f"Theory {i}",1,5,3)
        practical = st.number_input(f"Practical {i}",0,5,1)
        fac = st.text_input(f"Faculty {i}")

        if name:
            subjects[name]={"theory":theory,"practical":practical}
            faculty_map[name]=fac

    if st.button("Next ➡️"):
        st.session_state.subjects=subjects
        st.session_state.faculty_map=faculty_map
        st.session_state.step=3
        st.rerun()

# -------- STEP 3 --------
elif st.session_state.step == 3:

    st.markdown("## ⏰ Timing Setup")
    st.divider()

    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    duration = st.slider("Period Duration (minutes)",30,120,60)

    if st.button("Next ➡️"):
        st.session_state.start=start
        st.session_state.end=end
        st.session_state.duration=duration
        st.session_state.step=4
        st.rerun()

# -------- FINAL DASHBOARD --------
elif st.session_state.step == 4:

    st.markdown("## 🚀 Timetable Dashboard")
    st.divider()

    menu = st.selectbox("Choose Action", ["Generate","View","Analytics"])

    days=["Mon","Tue","Wed","Thu","Fri"]
    slots = create_time_slots(
        st.session_state.start,
        st.session_state.end,
        st.session_state.duration
    )

    # ✅ LOCKED SLOTS BACK
    locked = st.multiselect("🔒 Lock Slots", [f"{d}-{s}" for d in days for s in slots])

    # -------- GENERATE --------
    if menu=="Generate":

        if st.button("💀 Optimize Timetable"):

            best = None
            best_score = float("inf")

            for _ in range(15):
                tt = generate_timetable(
                    st.session_state.sections,
                    days,
                    slots,
                    st.session_state.subjects,
                    st.session_state.faculty_map,
                    st.session_state.rooms,
                    st.session_state.students,
                    st.session_state.combined,
                    locked
                )

                score,_ = evaluate_timetable(tt)

                if score < best_score:
                    best_score = score
                    best = tt

            st.session_state.tt = best
            st.success(f"🔥 Best Score: {best_score}")

    # -------- VIEW --------
    elif menu=="View":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            for sec, df in tt.items():
                st.markdown(f"### Section {sec}")
                st.dataframe(df, use_container_width=True)

            score,_ = evaluate_timetable(tt)
            st.metric("📊 Timetable Score", score)

            faculty_tt = build_faculty_timetable(tt)

            file = export_to_excel(tt, faculty_tt)

            if file:
                st.download_button(
                    "⬇️ Download Excel",
                    data=file,
                    file_name="timetable.xlsx"
                )

    # -------- ANALYTICS --------
    elif menu=="Analytics":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            day_counts = {}

            for sec, df in tt.items():
                for day in df.index:
                    count = (df.loc[day] != "").sum()
                    day_counts[day] = day_counts.get(day, 0) + count

            data = pd.DataFrame({
                "Day": list(day_counts.keys()),
                "Lectures": list(day_counts.values())
            })

            fig, ax = plt.subplots()
            ax.bar(data["Day"], data["Lectures"])
            ax.set_title("Lectures per Day")
            st.pyplot(fig)

        else:
            st.warning("Generate timetable first")