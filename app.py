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


# -------- UTIL --------
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
    faculty_schedule = {}

    for sub, data in subjects.items():

        # THEORY
        for _ in range(data["theory"]):
            for _ in range(20):
                sec = random.choice(sections)
                day = random.choice(days)
                slot = random.choice(slots)

                fac = faculty[sub]

                if tt[sec].loc[day, slot] == "" and (fac, day, slot) not in faculty_schedule:
                    tt[sec].loc[day, slot] = f"{sub}\n({fac})"
                    faculty_schedule[(fac, day, slot)] = True
                    break

        # PRACTICAL (LAB - consecutive)
        for _ in range(data["practical"]):
            for _ in range(20):
                sec = random.choice(sections)
                day = random.choice(days)

                for i in range(len(slots)-1):
                    s1, s2 = slots[i], slots[i+1]
                    fac = faculty[sub]

                    if (
                        tt[sec].loc[day, s1] == "" and
                        tt[sec].loc[day, s2] == "" and
                        (fac, day, s1) not in faculty_schedule and
                        (fac, day, s2) not in faculty_schedule
                    ):
                        tt[sec].loc[day, s1] = f"{sub} LAB"
                        tt[sec].loc[day, s2] = f"{sub} LAB"

                        faculty_schedule[(fac, day, s1)] = True
                        faculty_schedule[(fac, day, s2)] = True
                        break
                else:
                    continue
                break

    return tt


def detect_conflicts(tt):
    conflicts = []
    faculty_map = {}

    for sec, df in tt.items():
        for day in df.index:
            for slot in df.columns:
                val = df.loc[day, slot]

                if "(" in val:
                    fac = val.split("(")[-1].replace(")", "")
                    key = (fac, day, slot)

                    if key in faculty_map:
                        conflicts.append(f"{fac} clash at {day} {slot}")
                    else:
                        faculty_map[key] = sec

    return conflicts


def export_excel(tt):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sec, df in tt.items():
            df.to_excel(writer, sheet_name=sec)
    output.seek(0)
    return output.getvalue()


# -------- WELCOME --------
if st.session_state.page == "welcome":

    st.title("🤖 AI Timetable Generator")
    st.subheader("Intelligent Academic Scheduling System")

    st.markdown("""
## 🚀 Advantages
1. Saves time  
2. Reduces errors  
3. Handles multiple sections  
4. Balanced faculty workload  
5. Smart optimization  

## 📚 Uses
1. Colleges  
2. Schools  
3. Coaching institutes  
4. Faculty scheduling  
5. Complex timetable handling  
""")

    if st.button("➡️ Continue"):
        st.session_state.page = "login"
        st.rerun()


# -------- LOGIN --------
elif st.session_state.page == "login":

    st.title("🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.session_state.page = "app"
            st.rerun()
        else:
            st.error("Invalid credentials")


# -------- MAIN APP --------
elif st.session_state.page == "app":

    if not st.session_state.logged_in:
        st.session_state.page = "login"
        st.rerun()

    st.title("📊 Timetable System")

    # STEP 1
    if st.session_state.step == 1:

        st.header("Step 1: Course Setup")

        course = st.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
        branch = st.selectbox("Branch", ["CSE","IT","ECE","EEE"])
        shift = st.selectbox("Shift", ["Shift 1","Shift 2"])
        sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

        if st.button("Next"):
            st.session_state.sections = sections
            st.session_state.step = 2
            st.rerun()

    # STEP 2
    elif st.session_state.step == 2:

        st.header("Step 2: Subjects & Faculty")

        num = st.number_input("Subjects", 1, 10, 3)

        subjects = {}
        faculty = {}

        for i in range(num):
            sub = st.text_input(f"Subject {i}")
            theory = st.number_input(f"Theory {i}", 1, 5, 3)
            practical = st.number_input(f"Practical {i}", 0, 5, 1)
            fac = st.text_input(f"Faculty {i}")

            if sub:
                subjects[sub] = {"theory": theory, "practical": practical}
                faculty[sub] = fac

        if st.button("Next"):
            st.session_state.subjects = subjects
            st.session_state.faculty = faculty
            st.session_state.step = 3
            st.rerun()

    # STEP 3
    elif st.session_state.step == 3:

        st.header("Step 3: Time Setup")

        start = st.time_input("Start Time")
        end = st.time_input("End Time")
        duration = st.slider("Duration", 30, 120, 60)

        if st.button("Next"):
            st.session_state.start = start
            st.session_state.end = end
            st.session_state.duration = duration
            st.session_state.step = 4
            st.rerun()

    # STEP 4
    elif st.session_state.step == 4:

        st.header("Step 4: Generate")

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

            # CONFLICTS
            conflicts = detect_conflicts(tt)
            if conflicts:
                st.error("⚠️ Conflicts Found")
                for c in conflicts:
                    st.write(c)
            else:
                st.success("✅ No conflicts")

            # DOWNLOAD
            file = export_excel(tt)
            st.download_button("Download Excel", file, "timetable.xlsx")

            # ANALYTICS
            counts = {}
            for sec, df in tt.items():
                for d in df.index:
                    counts[d] = counts.get(d, 0) + (df.loc[d] != "").sum()

            fig, ax = plt.subplots()
            ax.bar(counts.keys(), counts.values())
            st.pyplot(fig)

        if st.button("🔄 Restart"):
            st.session_state.clear()
            st.rerun()