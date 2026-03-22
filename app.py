import streamlit as st
import json
import pandas as pd
from auth import login, logout
from scheduler import generate_timetable, detect_conflicts
from utils import create_time_slots, export_to_excel

# ---------- CONFIG ----------
st.set_page_config(page_title="Timetable Generator", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}
h1 { text-align: center; color: #00c6ff; }
.stButton>button {
    border-radius: 10px;
    background-color: #00c6ff;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- WELCOME TITLE (NEW) ----------
st.markdown("""
<h1>🤖 AI Timetable Generator App</h1>
<p style='text-align:center; font-size:18px;'>
Smart Scheduling • Conflict-Free • Automated
</p>
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
if not login():
    st.stop()

logout()

# ---------- MAIN HEADER ----------
st.markdown("<h1>📅 Intelligent Timetable Generator</h1>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Configuration")

course = st.sidebar.selectbox("🎓 Course", ["B.Tech CSE", "BBA", "MBA"])
semester = st.sidebar.selectbox("📘 Semester", ["Sem 1", "Sem 2", "Sem 3"])

sections = st.sidebar.multiselect(
    "🏫 Sections", ["A", "B", "C"], default=["A"]
)

rooms = st.sidebar.multiselect(
    "🏫 Rooms",
    ["Room 101", "Room 102", "Lab 1"],
    default=["Room 101", "Room 102"]
)

# ---------- VALIDATION ----------
if not sections:
    st.warning("Please select at least one section")
    st.stop()

if not rooms:
    st.warning("Please select at least one room")
    st.stop()

# ---------- TIMINGS ----------
st.sidebar.header("⏰ Timings")

start_time = st.sidebar.time_input("Start Time")
end_time = st.sidebar.time_input("End Time")
duration = st.sidebar.slider("Period Duration (min)", 30, 120, 60)

if start_time >= end_time:
    st.error("Start time must be before end time")
    st.stop()

# ---------- DARK MODE ----------
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ---------- LOAD DATA ----------
with open("data.json") as f:
    data = json.load(f)

subjects = data["subjects"]
faculty_map = data["faculty"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# ---------- GENERATE ----------
if st.button("🚀 Generate Timetable"):

    slots = create_time_slots(start_time, end_time, duration)

    if not slots:
        st.error("No time slots generated. Check timings.")
        st.stop()

    timetable = generate_timetable(
        sections, days, slots, subjects, faculty_map, rooms
    )

    st.session_state.timetable = timetable
    st.success("Timetable Generated!")

# ---------- REGENERATE ----------
if st.button("🔄 Regenerate Better"):
    if "timetable" in st.session_state:
        slots = create_time_slots(start_time, end_time, duration)

        if not slots:
            st.error("Invalid slots")
            st.stop()

        timetable = generate_timetable(
            sections, days, slots, subjects, faculty_map, rooms
        )

        st.session_state.timetable = timetable

# ---------- DISPLAY ----------
if "timetable" in st.session_state:

    timetable = st.session_state.timetable

    # ---------- ANALYTICS ----------
    st.subheader("📊 Analytics")

    if timetable:
        first_df = next(iter(timetable.values()))
        st.metric("Total Slots", len(days) * len(first_df.columns))
    else:
        st.metric("Total Slots", 0)

    st.metric("Subjects", len(subjects))

    # ---------- TABS ----------
    tab1, tab2 = st.tabs(["📅 Timetable", "📊 Room Usage"])

    with tab1:
        for sec, df in timetable.items():
            st.subheader(f"Section {sec}")
            st.dataframe(df)

    with tab2:
        room_count = {}

        for df in timetable.values():
            for val in df.values.flatten():
                if val:
                    room = val.split("[")[-1].replace("]", "")
                    room_count[room] = room_count.get(room, 0) + 1

        if room_count:
            st.bar_chart(pd.DataFrame.from_dict(
                room_count, orient='index', columns=['Usage']
            ))
        else:
            st.info("No room usage data available")

    # ---------- CONFLICT CHECK ----------
    conflicts = detect_conflicts(timetable)

    if conflicts:
        st.error("⚠️ Conflicts Found")
        for c in conflicts:
            st.write(c)
    else:
        st.success("✅ No Conflicts")

    # ---------- EXPORT ----------
    if st.button("📥 Export Excel"):
        export_to_excel(timetable)

        with open("timetable.xlsx", "rb") as f:
            st.download_button("Download File", f, "timetable.xlsx")

# ---------- SAVE CONFIG ----------
if st.sidebar.button("💾 Save Config"):
    config = {
        "course": course,
        "semester": semester,
        "sections": sections
    }

    with open("config.json", "w") as f:
        json.dump(config, f)

    st.sidebar.success("Saved!")