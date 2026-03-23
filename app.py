import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from auth import login, logout
from scheduler import generate_timetable, evaluate_timetable, build_faculty_timetable
from utils import create_time_slots, export_to_excel

st.set_page_config(layout="wide")

# Optional: hide full error trace
st.set_option('client.showErrorDetails', False)

# -------- LOGIN --------
if not login():
    st.stop()

logout()

# -------- STEP CONTROL --------
if "step" not in st.session_state:
    st.session_state.step = 1

# -------- STEP 1 --------
if st.session_state.step == 1:

    st.header("📘 Academic Setup")

    course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
    branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
    sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

    rooms = {"Room 101":60, "Room 102":40, "Lab 1":30}

    students = {}
    for sec in sections:
        students[sec] = st.number_input(f"Students {sec}", 10,100,60)

    combined = st.multiselect("Combined Sections", sections)

    if st.button("Next"):
        st.session_state.update(locals())
        st.session_state.step = 2
        st.rerun()

# -------- STEP 2 --------
elif st.session_state.step == 2:

    st.header("👨‍🏫 Subjects")

    num = st.number_input("Number of Subjects", 1, 10, 5)

    subjects = {}
    faculty_map = {}

    for i in range(num):
        name = st.text_input(f"Subject {i}")
        theory = st.number_input(f"Theory Hours {i}", 1, 5, 3)
        practical = st.number_input(f"Practical Hours {i}", 0, 5, 1)
        fac = st.text_input(f"Faculty {i}")

        if name:
            subjects[name] = {"theory": theory, "practical": practical}
            faculty_map[name] = fac

    if st.button("Next"):
        st.session_state.subjects = subjects
        st.session_state.faculty_map = faculty_map
        st.session_state.step = 3
        st.rerun()

# -------- STEP 3 --------
elif st.session_state.step == 3:

    st.header("⏰ Timing Setup")

    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    duration = st.slider("Period Duration (minutes)", 30, 120, 60)

    if st.button("Next"):
        st.session_state.start = start
        st.session_state.end = end
        st.session_state.duration = duration
        st.session_state.step = 4
        st.rerun()

# -------- FINAL DASHBOARD --------
elif st.session_state.step == 4:

    st.header("🚀 Dashboard")

    menu = st.selectbox("Menu", ["Generate","View","Analytics"])

    days = ["Mon","Tue","Wed","Thu","Fri"]
    slots = create_time_slots(
        st.session_state.start,
        st.session_state.end,
        st.session_state.duration
    )

    # 🔒 LOCK SLOTS
    locked = st.multiselect(
        "🔒 Lock Slots",
        [f"{d}-{s}" for d in days for s in slots]
    )

    # -------- GENERATE --------
    if menu == "Generate":

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

                score, _ = evaluate_timetable(tt)

                if score < best_score:
                    best_score = score
                    best = tt

            st.session_state.tt = best
            st.success(f"🔥 Best Score: {best_score}")

    # -------- VIEW --------
    elif menu == "View":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            for sec, df in tt.items():
                st.subheader(f"Section {sec}")
                st.dataframe(df, use_container_width=True)

            score, _ = evaluate_timetable(tt)
            st.metric("📊 Score", score)

            faculty_tt = build_faculty_timetable(tt)
            file = export_to_excel(tt, faculty_tt)

            if file:
                st.download_button(
                    label="⬇️ Download Excel",
                    data=file,
                    file_name="timetable.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    # -------- ANALYTICS --------
    elif menu == "Analytics":

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

            st.subheader("📊 Lectures per Day")

            fig, ax = plt.subplots()
            ax.bar(data["Day"], data["Lectures"])
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Lectures")
            ax.set_title("Lectures Distribution")
            st.pyplot(fig)

        else:
            st.warning("Generate timetable first ⚠️")