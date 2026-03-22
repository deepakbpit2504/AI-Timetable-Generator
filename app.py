import streamlit as st
import pandas as pd
from auth import login, logout
from scheduler import generate_timetable, detect_conflicts
from utils import create_time_slots, export_to_excel

st.set_page_config(page_title="AI Timetable", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.main {background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);color:white;}
h1,h2,h3{color:#00e6e6;}
.stButton>button{border-radius:10px;background:#00c6ff;color:white;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 AI Timetable Generator</h1>", unsafe_allow_html=True)

# ---------- LOGIN ----------
if not login():
    st.stop()

logout()

# ---------- STEP CONTROL ----------
if "step" not in st.session_state:
    st.session_state.step = 1

# ---------- STEP 1 ----------
if st.session_state.step == 1:

    st.header("📘 Step 1: Academic Configuration")

    st.info("""
📚 This step defines the academic structure of your institution.

Why this matters:
- Helps organize courses and departments  
- Enables structured scheduling  
- Supports multi-section management  
""")

    course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
    branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
    shift = st.selectbox("Shift", ["Shift 1","Shift 2"])
    sections = st.multiselect("Sections", ["A","B","C"], default=["A"])
    rooms = st.multiselect("Rooms", ["Room 101","Room 102","Lab 1"], default=["Room 101"])

    if st.button("Next ➡️"):
        st.session_state.course = course
        st.session_state.branch = branch
        st.session_state.shift = shift
        st.session_state.sections = sections
        st.session_state.rooms = rooms
        st.session_state.step = 2
        st.rerun()

# ---------- STEP 2 ----------
elif st.session_state.step == 2:

    st.header("👨‍🏫 Step 2: Subjects & Faculty Mapping")

    st.info("""
🧠 This step assigns subjects and faculty members.

Advantages:
- Ensures proper faculty allocation  
- Prevents teaching conflicts  
- Maintains academic consistency  
""")

    num = st.number_input("Number of Subjects",1,10,5)

    subjects = []
    faculty_map = {}

    for i in range(num):
        s = st.text_input(f"Subject {i+1}", key=f"s{i}")
        f = st.text_input(f"Faculty {i+1}", key=f"f{i}")

        if s:
            subjects.append(s)
            faculty_map[s] = f if f else "TBD"

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

    st.header("⏰ Step 3: Time Configuration")

    st.info("""
⏳ This step defines scheduling constraints.

Benefits:
- Ensures proper time allocation  
- Avoids overlapping sessions  
- Supports flexible scheduling  
""")

    start = st.time_input("Start Time")
    end = st.time_input("End Time")
    duration = st.slider("Period Duration",30,120,60)

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
📊 This dashboard allows you to generate and analyze timetables.

Key Capabilities:
- Smart timetable generation  
- Conflict detection  
- Resource optimization  
""")

    menu = st.radio("Choose Action", ["Generate","View Timetable","Analytics"])

    days = ["Mon","Tue","Wed","Thu","Fri"]

    # ---------- GENERATE ----------
    if menu == "Generate":

        st.write("⚡ Generate a smart timetable using heuristic optimization")

        if st.button("🚀 Generate Timetable"):

            slots = create_time_slots(
                st.session_state.start,
                st.session_state.end,
                st.session_state.duration
            )

            tt = generate_timetable(
                st.session_state.sections,
                days,
                slots,
                st.session_state.subjects,
                st.session_state.faculty_map,
                st.session_state.rooms
            )

            st.session_state.tt = tt
            st.success("Timetable Generated!")
            st.balloons()

        if st.button("🔄 Regenerate Better"):

            best = None
            min_conf = 999

            for _ in range(5):
                slots = create_time_slots(
                    st.session_state.start,
                    st.session_state.end,
                    st.session_state.duration
                )

                temp = generate_timetable(
                    st.session_state.sections,
                    days,
                    slots,
                    st.session_state.subjects,
                    st.session_state.faculty_map,
                    st.session_state.rooms
                )

                conf = detect_conflicts(temp)

                if len(conf) < min_conf:
                    min_conf = len(conf)
                    best = temp

            st.session_state.tt = best
            st.success(f"Optimized! Conflicts: {min_conf}")

    # ---------- VIEW ----------
    elif menu == "View Timetable":

        st.write("📅 View generated timetable with conflict insights")

        if "tt" in st.session_state:
            for sec, df in st.session_state.tt.items():
                st.subheader(f"Section {sec}")
                st.dataframe(df)

            conflicts = detect_conflicts(st.session_state.tt)

            st.subheader("🚨 Conflicts")
            if conflicts:
                for c in conflicts:
                    st.write(c)
            else:
                st.success("No conflicts!")

            if st.button("Export"):
                export_to_excel(st.session_state.tt)
                with open("timetable.xlsx","rb") as f:
                    st.download_button("Download", f)

        else:
            st.warning("Generate timetable first")

    # ---------- ANALYTICS ----------
    elif menu == "Analytics":

        st.write("📊 Analyze room utilization and scheduling efficiency")

        if "tt" in st.session_state:
            tt = st.session_state.tt

            room_count = {}

            for df in tt.values():
                for val in df.values.flatten():
                    if val:
                        room = val.split("[")[-1].replace("]", "")
                        room_count[room] = room_count.get(room, 0) + 1

            st.bar_chart(pd.DataFrame.from_dict(
                room_count, orient='index', columns=['Usage']
            ))

        else:
            st.warning("Generate timetable first")