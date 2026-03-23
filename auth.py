import streamlit as st

# -------- INIT --------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "initialized" not in st.session_state:
    st.session_state.page = "landing"
    st.session_state.logged_in = False
    st.session_state.initialized = True


# -------- LANDING --------
def landing_page():
    st.title("🤖 AI Timetable Generator")

    st.markdown("""
### 🚀 Intelligent Academic Scheduling System

Generate optimized, conflict-free timetables automatically.

### 🎯 Advantages:
- Saves time ⏱️
- Reduces human errors 📉
- Handles complex scheduling ⚡
- Balanced workload 📊

### 🧠 Uses:
- Colleges
- Schools
- Coaching institutes
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
            st.error("User already exists ❌")
        elif u == "" or p == "":
            st.warning("Fill all fields ⚠️")
        else:
            st.session_state.users[u] = p
            st.success("Account created 🎉")
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
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

    if st.button("⬅️ Back"):
        st.session_state.page = "landing"
        st.rerun()


# -------- MAIN --------
def login():
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