# 🚀 AI-Powered Timetable Generator using OR-Tools

An AI-based system that automatically generates conflict-free academic timetables using constraint optimization.

---

## 🧠 Features

- ✅ Multi-section timetable generation
- ✅ Faculty clash avoidance
- ✅ Room allocation optimization
- ✅ Practical lab scheduling (consecutive slots)
- ✅ Lunch break handling
- ✅ Excel export
- ✅ Web-based UI using Streamlit

---

## 🏗️ Tech Stack

- Python
- Streamlit
- Google OR-Tools (CP-SAT Solver)
- Pandas
- OpenPyXL

---

## ⚙️ How It Works

The system models timetable generation as a **Constraint Satisfaction Problem (CSP)** and solves it using AI.

### Constraints handled:
- No faculty overlap
- No room clashes
- Fixed course hours
- Labs scheduled in consecutive slots
- Mandatory lunch break

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
