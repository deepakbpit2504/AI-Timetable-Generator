import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(layout="wide")

# -------- INIT --------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "step" not in st.session_state:
    st.session_state.step = 1


# -------- UTIL FUNCTIONS --------
def create_slots(start, end, duration):
    slots = []
    current = start
    while current < end:
        total = current.hour*60 + current.minute + duration
        h = total // 60
        m = total % 60
        slots.append(f"{current.strftime('%H:%M')} - {h:02}:{m:02}")
        current = current.replace(hour=h, minute=m)
    return slots


def generate_tt(sections, days, slots, subjects, faculty):
    tt = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}

    for sub, hrs in subjects.items():
        for _ in range(hrs):
            sec = random.choice(sections)
            day = random.choice(days)
            slot = random.choice(slots)
            tt[sec].loc[day, slot] = f"{sub}\n({faculty[sub]})"

    return tt


def export_excel(tt):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sec, df in tt.items():
            df.to_excel(writer, sheet_name=sec)
    output.seek(0)
    return output.getvalue()


# -------- PAGE 1: WELCOME --------
if st.session_state.page == "welcome":

    st.title("🤖 AI Timetable Generator")

    st.markdown("""
### Intelligent Academic Scheduling System

- Avoid clashes  
- Save time  
- Optimize schedules  
""")

    if st.button("➡️ Continue"):
        st.session_state.page = "login"
        st.rerun()


# -------- PAGE 2: LOGIN --------
elif st.session_state.page == "login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.session_state.page = "app"
            st.session_state.step = 1
            st.rerun()
        else:
            st.error("Invalid credentials")


# -------- PAGE 3: MAIN APP --------
elif st.session_state.page == "app":

    if not st.session_state.logged_in:
        st.session_state.page = "login"
        st.rerun()

    st.title("📊 Timetable System")

    # -------- STEP 1 --------
    if st.session_state.step == 1:

        st.header("Step 1: Course & Structure")

        course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
        branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
        shift = st.selectbox("Shift", ["Shift 1","Shift 2"])
        sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

        if st.button("Next"):
            st.session_state.course = course
            st.session_state.branch = branch
            st.session_state.shift = shift
            st.session_state.sections = sections
            st.session_state.step = 2
            st.rerun()

    # -------- STEP 2 --------
    elif st.session_state.step == 2:

        st.header("Step 2: Subjects & Faculty")

        num = st.number_input("Number of Subjects", 1, 10, 3)

        subjects = {}
        faculty = {}

        for i in range(num):
            sub = st.text_input(f"Subject {i}")
            hrs = st.number_input(f"Hours {i}", 1, 5, 2)
            fac = st.text_input(f"Faculty {i}")

            if sub:
                subjects[sub] = hrs
                faculty[sub] = fac

        if st.button("Next"):
            st.session_state.subjects = subjects
            st.session_state.faculty = faculty
            st.session_state.step = 3
            st.rerun()

    # -------- STEP 3 --------
    elif st.session_state.step == 3:

        st.header("Step 3: Time Configuration")

        start = st.time_input("Start Time")
        end = st.time_input("End Time")
        duration = st.slider("Slot Duration", 30, 120, 60)

        if st.button("Next"):
            st.session_state.start = start
            st.session_state.end = end
            st.session_state.duration = duration
            st.session_state.step = 4
            st.rerun()

    # -------- STEP 4 --------
    elif st.session_state.step == 4:

        st.header("Step 4: Generate & Analyze")

        days = ["Mon","Tue","Wed","Thu","Fri"]
        slots = create_slots(
            st.session_state.start,
            st.session_state.end,
            st.session_state.duration
        )

        if st.button("Generate Timetable"):
            tt = generate_tt(
                st.session_state.sections,
                days,
                slots,
                st.session_state.subjects,
                st.session_state.faculty
            )
            st.session_state.tt = tt

        if "tt" in st.session_state:

            tt = st.session_state.tt

            for sec, df in tt.items():
                st.subheader(f"Section {sec}")
                st.dataframe(df)

            # Download
            file = export_excel(tt)
            st.download_button("Download Excel", file, "timetable.xlsx")

            # Analytics
            counts = {}
            for sec, df in tt.items():
                for d in df.index:
                    counts[d] = counts.get(d, 0) + (df.loc[d] != "").sum()

            fig, ax = plt.subplots()
            ax.bar(counts.keys(), counts.values())
            st.pyplot(fig)

        if st.button("🔙 Restart"):
            st.session_state.clear()
            st.rerun()