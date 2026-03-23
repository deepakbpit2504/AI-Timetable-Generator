import streamlit as st

# -------- USERS --------
USERS = {"admin": "1234"}

# -------- LOGIN FUNCTION --------
def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        # 💀 INTRO CONTENT (WELCOME INSIDE LOGIN)
        st.title("🤖 AI Timetable Generator")

        st.markdown("""
### 🚀 Intelligent Academic Scheduling System

Automatically generate optimized, conflict-free timetables.

---

### 🎯 Advantages:
- Saves time ⏱️
- Reduces manual errors 📉
- Handles complex scheduling ⚡
- Balanced workload 📊

---

### 🧠 Uses:
- Colleges & Universities
- Schools
- Coaching Institutes

---
""")

        st.markdown("## 🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

        return False

    return True


# -------- LOGOUT --------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()