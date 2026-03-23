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

# -------- UTILS --------
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


def generate_tt(sections, days, slots, subjects, faculty, locked):
    tt = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}
    faculty_schedule = {}

    for sub, data in subjects.items():

        # THEORY
        for _ in range(data["theory"]):
            for _ in range(30):
                sec = random.choice(sections)
                day = random.choice(days)
                slot = random.choice(slots)
                fac = faculty[sub]

                if (
                    tt[sec].loc[day, slot] == "" and
                    (fac, day, slot) not in faculty_schedule and
                    f"{day}-{slot}" not in locked
                ):
                    tt[sec].loc[day, slot] = f"{sub}\n({fac})"
                    faculty_schedule[(fac, day, slot)] = True
                    break

        # PRACTICAL
        for _ in range(data["practical"]):
            for _ in range(30):
                sec = random.choice(sections)
                day = random.choice(days)
                fac = faculty[sub]

                for i in range(len(slots)-1):
                    s1, s2 = slots[i], slots[i+1]

                    if (
                        tt[sec].loc[day, s1] == "" and
                        tt[sec].loc[day, s2] == "" and
                        (fac, day, s1) not in faculty_schedule and
                        (fac, day, s2) not in faculty_schedule and
                        f"{day}-{s1}" not in locked and
                        f"{day}-{s2}" not in locked
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


def evaluate(tt):
    score = 0
    for sec, df in tt.items():
        score += (df == "").sum().sum()
    return score


def detect_conflicts(tt):
    conflicts = []
    faculty_map = {}

    for sec, df in tt.items():
        for d in df.index:
            for s in df.columns:
                val = df.loc[d, s]
                if "(" in val:
                    fac = val.split("(")[-1].replace(")", "")
                    key = (fac, d, s)
                    if key in faculty_map:
                        conflicts.append(f"{fac} clash at {d} {s}")
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
- Saves time  
- Reduces errors  
- Handles multiple sections  
- Balanced workload  
- Smart optimization  

## 📚 Uses
- Colleges  
- Schools  
- Coaching  
- Faculty scheduling  
- Complex timetables  
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

    # -------- STEPS --------
    if st.session_state.step == 1:

        st.header("Course Setup")

        sections = st.multiselect("Sections", ["A","B","C"], default=["A"])

        if st.button("Next"):
            st.session_state.sections = sections
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:

        st.header("Subjects")

        num = st.number_input("Subjects", 1, 10, 3)

        subjects, faculty = {}, {}

        for i in range(num):
            sub = st.text_input(f"Subject {i}")
            th = st.number_input(f"Theory {i}", 1, 5, 3)
            pr = st.number_input(f"Practical {i}", 0, 5, 1)
            fac = st.text_input(f"Faculty {i}")

            if sub:
                subjects[sub] = {"theory": th, "practical": pr}
                faculty[sub] = fac

        if st.button("Next"):
            st.session_state.subjects = subjects
            st.session_state.faculty = faculty
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:

        st.header("Time Setup")

        start = st.time_input("Start")
        end = st.time_input("End")
        duration = st.slider("Duration", 30, 120, 60)

        if st.button("Next"):
            st.session_state.start = start
            st.session_state.end = end
            st.session_state.duration = duration
            st.session_state.step = 4
            st.rerun()

    elif st.session_state.step == 4:

        st.header("Dashboard")

        days = ["Mon","Tue","Wed","Thu","Fri"]
        slots = create_slots(
            st.session_state.start,
            st.session_state.end,
            st.session_state.duration
        )

        # 🔒 LOCK SLOTS
        locked = st.multiselect(
            "Lock Slots",
            [f"{d}-{s}" for d in days for s in slots]
        )

        tab1, tab2, tab3 = st.tabs(["Generate","View","Analytics"])

        # -------- GENERATE --------
        with tab1:
            if st.button("Generate Best Timetable"):

                best, best_score = None, float("inf")

                for _ in range(20):
                    tt = generate_tt(
                        st.session_state.sections,
                        days,
                        slots,
                        st.session_state.subjects,
                        st.session_state.faculty,
                        locked
                    )
                    score = evaluate(tt)

                    if score < best_score:
                        best_score = score
                        best = tt

                st.session_state.tt = best
                st.success(f"Best Score: {best_score}")

        # -------- VIEW --------
        with tab2:
            if "tt" in st.session_state:
                tt = st.session_state.tt

                for sec, df in tt.items():
                    st.dataframe(df)

                conflicts = detect_conflicts(tt)
                if conflicts:
                    st.error(conflicts)
                else:
                    st.success("No conflicts")

                file = export_excel(tt)
                st.download_button("Download Excel", file, "tt.xlsx")

        # -------- ANALYTICS --------
        with tab3:
            if "tt" in st.session_state:
                tt = st.session_state.tt

                counts = {}
                for sec, df in tt.items():
                    for d in df.index:
                        counts[d] = counts.get(d, 0) + (df.loc[d] != "").sum()

                fig, ax = plt.subplots()
                ax.bar(counts.keys(), counts.values())
                st.pyplot(fig)

        if st.button("Restart"):
            st.session_state.clear()
            st.rerun()