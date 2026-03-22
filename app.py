import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from auth import login, logout
from scheduler import generate_timetable, evaluate_timetable, build_faculty_timetable
from utils import create_time_slots, export_to_excel

st.set_page_config(layout="wide")

if not login():
    st.stop()

logout()

if "step" not in st.session_state:
    st.session_state.step = 1

# STEP 1
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

# STEP 2
elif st.session_state.step == 2:

    st.header("👨‍🏫 Subjects")

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

    if st.button("Next"):
        st.session_state.subjects=subjects
        st.session_state.faculty_map=faculty_map
        st.session_state.step=3
        st.rerun()

# STEP 3
elif st.session_state.step == 3:

    st.header("⏰ Timing")

    start = st.time_input("Start")
    end = st.time_input("End")
    duration = st.slider("Duration",30,120,60)

    if st.button("Next"):
        st.session_state.start=start
        st.session_state.end=end
        st.session_state.duration=duration
        st.session_state.step=4
        st.rerun()

# FINAL
elif st.session_state.step == 4:

    menu = st.radio("Menu", ["Generate","View","Analytics"])

    days=["Mon","Tue","Wed","Thu","Fri"]
    slots = create_time_slots(st.session_state.start, st.session_state.end, st.session_state.duration)

    if menu=="Generate":

        if st.button("Generate"):
            tt = generate_timetable(
                st.session_state.sections, days, slots,
                st.session_state.subjects,
                st.session_state.faculty_map,
                st.session_state.rooms,
                st.session_state.students,
                st.session_state.combined,
                []
            )

            st.session_state.tt = tt

    elif menu=="View":

        if "tt" in st.session_state:
            tt = st.session_state.tt

            for sec, df in tt.items():
                st.dataframe(df)

            faculty_tt = build_faculty_timetable(tt)

            file = export_to_excel(tt, faculty_tt)

            st.download_button(
                label="⬇️ Download Excel",
                data=file,
                file_name="timetable.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    elif menu=="Analytics":

        if "tt" in st.session_state:
            heat = sum([df.isnull().astype(int) for df in st.session_state.tt.values()])

            fig, ax = plt.subplots()
            sns.heatmap(heat, annot=True, ax=ax)
            st.pyplot(fig)