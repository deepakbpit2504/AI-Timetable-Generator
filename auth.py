import streamlit as st

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}


# -------- LANDING PAGE --------
def landing_page():
    st.title("🤖 AI Timetable Generator")

    st.markdown("""
### 🚀 Smart Academic Scheduling System

Automatically generate optimized, conflict-free timetables.

### 🎯 Advantages:
- Saves time ⏱️
- Reduces errors 📉
- Handles complex scheduling ⚡
- Balanced workload 📊

### 🧠 Uses:
- Colleges
- Schools
- Coaching Institutes

---
""")

    col1, col2 = st.columns(2)

    if col1.button("📝 Register"):
        st.session_state.page = "register"
        st.rerun()

    if col2.button("🔐 Login"):
        st.session_state.page = "login"
        st.rerun()


# -------- REGISTER --------
def register_page():
    st.markdown("## 📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if u in st.session_state.users:
            st.error("User exists ❌")
        elif u == "" or p == "":
            st.warning("Fill all fields ⚠️")
        else:
            st.session_state.users[u] = p
            st.success("Registered 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "landing"
        st.rerun()


# -------- LOGIN --------
def login_page():
    st.markdown("## 🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in st.session_state.users and st.session_state.users[u] == p:
            st.session_state.logged_in = True
            st.success("Login success ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

    if st.button("⬅️ Back"):
        st.session_state.page = "landing"
        st.rerun()


# -------- MAIN CONTROL --------
def login():

    if "page" not in st.session_state:
        st.session_state.page = "landing"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        if st.session_state.page == "landing":
            landing_page()

        elif st.session_state.page == "register":
            register_page()

        elif st.session_state.page == "login":
            login_page()

        return False

    return True


# -------- LOGOUT --------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "landing"
        st.rerun()