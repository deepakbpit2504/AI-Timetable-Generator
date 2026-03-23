import streamlit as st

# -------- USER STORAGE --------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

# -------- INITIAL STATE --------
if "page" not in st.session_state:
    st.session_state.page = "landing"   # ✅ START FROM WELCOME

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -------- PAGE 1: WELCOME --------
def landing_page():
    st.title("🤖 AI Timetable Generator")

    st.markdown("""
### 🚀 Intelligent Scheduling System

Generate **conflict-free, optimized academic timetables** easily.

### 🎯 Advantages:
- Saves time ⏱️
- Reduces manual errors 📉
- Handles complex scheduling ⚡
- Balanced workload 📊

### 🧠 Uses:
- Colleges & Universities
- Schools & Institutes

---
""")

    col1, col2 = st.columns(2)

    if col1.button("📝 Register"):
        st.session_state.page = "register"
        st.rerun()

    if col2.button("🔐 Login"):
        st.session_state.page = "login"
        st.rerun()


# -------- PAGE 2: REGISTER --------
def register_page():
    st.markdown("## 📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username in st.session_state.users:
            st.error("User already exists ❌")
        elif username == "" or password == "":
            st.warning("Fill all fields ⚠️")
        else:
            st.session_state.users[username] = password
            st.success("Account created 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "landing"
        st.rerun()


# -------- PAGE 3: LOGIN --------
def login_page():
    st.markdown("## 🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

    if st.button("⬅️ Back"):
        st.session_state.page = "landing"
        st.rerun()


# -------- MAIN CONTROL --------
def login():

    # 👉 If NOT logged in → show pages
    if not st.session_state.logged_in:

        if st.session_state.page == "landing":
            landing_page()

        elif st.session_state.page == "register":
            register_page()

        elif st.session_state.page == "login":
            login_page()

        return False   # ❌ STOP app here

    return True  # ✅ Continue app


# -------- LOGOUT --------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "landing"  # back to welcome
        st.rerun()