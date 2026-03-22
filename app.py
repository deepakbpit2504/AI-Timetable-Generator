import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from auth import login, logout
from scheduler import generate_timetable, evaluate_timetable, build_faculty_timetable
from utils import create_time_slots, export_to_excel

st.set_page_config(layout="wide")

st.title("🤖 AI Timetable Generator")

# ---------- LOGIN ----------
if not login():
    st.stop()

logout()

# ---------- STEP CONTROL ----------
if "step" not in st.session_state:
    st.session_state.step = 1

# ---------- STEP 1 ----------
if st.session_state.step == 1:

    st.header("📘 Academic Setup")

    st.info("""
Define course structure, sections, and classroom capacity.
This ensures proper allocation and avoids overcrowding.
""")

    course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
    branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
    shift = st.selectbox("Shift", ["Shift 1","Shift 2"])

    sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

    rooms = {
        "Room 101": 60,
        "Room 102": 40,
        "Lab 1": 30
    }

    students = {}
    for sec in sections:
        students[sec] = st.number_input(f"Students in {sec}", 10,100,60)

    combined = st.multiselect("Combined Sections", sections)

    if st.button("Next ➡️"):
        st.session_state.update(locals())
        st.session_state.step = 2
        st.rerun()

# ---------- STEP 2 ----------
elif st.session_state.step == 2:

    st.header("👨‍🏫 Subjects & Faculty")

    st.info("""
Assign subjects with theory/practical hours and map faculty.
This helps maintain balanced teaching workload.
""")

    num = st.number_input("Number of Subjects",1,10,5)

    subjects = {}
    faculty_map = {}

    for i in range(num):
        name = st.text_input(f"Subject {i+1}", key=f"s{i}")
        theory = st.number_input(f"Theory hrs {i+1}",1,5,3, key=f"t{i}")
        practical = st.number_input(f"Practical hrs {i+1}",0,5,1, key=f"p{i}")
        fac = st.text_input(f"Faculty {i+1}", key=f"f{i}")

        if name:
            subjects[name] = {"theory": theory, "practical": practical}
            faculty_map[name] = fac if fac else "TBD"

    if st.button("Next ➡️"):
        st.session_state.subjects = subjects
        st.session_state.faculty_map = faculty_map
        st.session_state.step = 3
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.step = 1
        st.rerun()

# ---------- STEP 3 ----------
elif st.session_state.step == 3:

    st.header("⏰ Timing Setup")

    st.info("""
Define working hours and period duration.
Ensures proper scheduling without overlaps.
""")

    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    duration = st.slider("Period Duration (minutes)",30,120,60)

    if st.button("Next ➡️"):
        st.session_state.start = start
        st.session_state.end = end
        st.session_state.duration = duration
        st.session_state.step = 4
        st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.step = 2
        st.rerun()

# ---------- FINAL DASHBOARD ----------
elif st.session_state.step == 4:

    st.header("🚀 Timetable Dashboard")

    st.info("""
Generate optimized timetable, view weekly schedule,
analyze conflicts, and export data.
""")

    menu = st.radio("Menu", ["Generate","View","Analytics"])

    days = ["Mon","Tue","Wed","Thu","Fri"]
    slots = create_time_slots(
        st.session_state.start,
        st.session_state.end,
        st.session_state.duration
    )

    locked = st.multiselect("🔒 Lock Slots", [f"{d}-{s}" for d in days for s in slots])

    # ---------- GENERATE ----------
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

    # ---------- VIEW ----------
    elif menu == "View":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            st.subheader("📅 Weekly Timetable")

            for sec, df in tt.items():
                st.markdown(f"## Section {sec}")
                st.dataframe(df, use_container_width=True)

                st.markdown("### 📌 Day-wise Breakdown")
                for day in df.index:
                    st.write(f"**{day}**")
                    for slot, val in df.loc[day].items():
                        st.write(f"{slot} → {val if val else 'Free'}")
                    st.divider()

            # SCORE
            score, conflicts = evaluate_timetable(tt)
            st.metric("📊 Timetable Score", score)

            # CONFLICTS
            st.subheader("🚨 Issues")
            if conflicts:
                for c in conflicts:
                    st.write("⚠️", c)
            else:
                st.success("Perfect Week Schedule 💀")

            # FACULTY VIEW
            faculty_tt = build_faculty_timetable(tt)
            st.subheader("👨‍🏫 Faculty Timetable")
            st.write(faculty_tt)

            # EXPORT (FIXED)
            if st.button("📥 Download Excel"):
                file = export_to_excel(tt, faculty_tt)

                st.download_button(
                    label="⬇️ Download Timetable",
                    data=file,
                    file_name="timetable.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        else:
            st.warning("Generate timetable first")

    # ---------- ANALYTICS ----------
    elif menu == "Analytics":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            st.subheader("📊 Conflict Heatmap")

            heat = sum([df.isnull().astype(int) for df in tt.values()])

            fig, ax = plt.subplots()
            sns.heatmap(heat, annot=True, ax=ax)
            st.pyplot(fig)

        else:
            st.warning("Generate timetable first")