import streamlit as st
from ortools.sat.python import cp_model
import pandas as pd

# Page config
st.set_page_config(page_title="AI Timetable Generator", layout="wide")

st.title("🚀 AI-Powered Timetable Generator")

st.write("Click the button below to generate a timetable using AI.")

# Button
if st.button("Generate Timetable"):

    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    SLOTS = ["9-10", "10-11", "11-12", "12-1", "LUNCH", "2-3", "3-4"]

    courses = {
        "Math": {"theory": 3, "lab": 0},
        "Physics": {"theory": 2, "lab": 2},
        "DBMS": {"theory": 3, "lab": 2},
        "OS": {"theory": 3, "lab": 0}
    }

    sections = ["A", "B"]

    faculty_map = {
        "Math": "ProfA",
        "Physics": "ProfB",
        "DBMS": "ProfC",
        "OS": "ProfD"
    }

    rooms = ["R1", "R2"]
    labs = ["Lab1"]

    # MODEL
    model = cp_model.CpModel()
    x = {}

    for sec in sections:
        for course in courses:
            for d in range(len(DAYS)):
                for s in range(len(SLOTS)):
                    if SLOTS[s] == "LUNCH":
                        continue
                    for r in rooms + labs:
                        x[(sec, course, d, s, r)] = model.NewBoolVar(
                            f"x_{sec}_{course}_{d}_{s}_{r}"
                        )

    # Course hours constraint
    for sec in sections:
        for course in courses:
            total = courses[course]["theory"] + courses[course]["lab"]
            model.Add(sum(
                x[(sec, course, d, s, r)]
                for d in range(len(DAYS))
                for s in range(len(SLOTS)) if SLOTS[s] != "LUNCH"
                for r in rooms + labs
            ) == total)

    # One class per slot
    for sec in sections:
        for d in range(len(DAYS)):
            for s in range(len(SLOTS)):
                if SLOTS[s] == "LUNCH":
                    continue
                model.Add(sum(
                    x[(sec, c, d, s, r)]
                    for c in courses
                    for r in rooms + labs
                ) <= 1)

    # Faculty clash
    for f in set(faculty_map.values()):
        for d in range(len(DAYS)):
            for s in range(len(SLOTS)):
                if SLOTS[s] == "LUNCH":
                    continue
                model.Add(sum(
                    x[(sec, c, d, s, r)]
                    for sec in sections
                    for c in courses
                    for r in rooms + labs
                    if faculty_map[c] == f
                ) <= 1)

    # Room clash
    for r in rooms + labs:
        for d in range(len(DAYS)):
            for s in range(len(SLOTS)):
                if SLOTS[s] == "LUNCH":
                    continue
                model.Add(sum(
                    x[(sec, c, d, s, r)]
                    for sec in sections
                    for c in courses
                ) <= 1)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    result = solver.Solve(model)

    if result == cp_model.FEASIBLE or result == cp_model.OPTIMAL:
        st.success("✅ Timetable Generated!")

        timetable = {
            sec: {day: {slot: "FREE" for slot in SLOTS} for day in DAYS}
            for sec in sections
        }

        for sec in sections:
            for course in courses:
                for d in range(len(DAYS)):
                    for s in range(len(SLOTS)):
                        if SLOTS[s] == "LUNCH":
                            timetable[sec][DAYS[d]][SLOTS[s]] = "LUNCH"
                            continue
                        for r in rooms + labs:
                            if solver.Value(x[(sec, course, d, s, r)]) == 1:
                                timetable[sec][DAYS[d]][SLOTS[s]] = f"{course} ({faculty_map[course]}) [{r}]"

        # Display
        for sec in sections:
            st.subheader(f"Section {sec}")
            df = pd.DataFrame(timetable[sec]).T
            st.dataframe(df)

        # Download Excel
        file = "timetable.xlsx"
        writer = pd.ExcelWriter(file, engine='openpyxl')

        for sec in sections:
            df = pd.DataFrame(timetable[sec]).T
            df.to_excel(writer, sheet_name=sec)

        writer.close()

        with open(file, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name="timetable.xlsx")

    else:
        st.error("❌ No feasible timetable found!")
      
