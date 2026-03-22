import streamlit as st

# Temporary in-memory user store
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": "1234"
    }

# ---------- WELCOME PAGE ----------
def show_welcome():
    st.title("🎓 AI Timetable Generator")

    st.markdown("""
### 🚀 Welcome to Intelligent Timetable System

This platform helps educational institutions automatically generate **optimized, conflict-free academic timetables**.

### ✨ Key Features:
- 📅 Multi-section scheduling
- 👨‍🏫 Faculty allocation
- 🏫 Room management
- ⚡ Conflict detection
- 📊 Smart optimization scoring

👉 Please **Register or Login** to continue.
""")

    col1, col2 = st.columns(2)

    if col1.button("🔐 Login"):
        st.session_state.page = "login"

    if col2.button("📝 Register"):
        st.session_state.page = "register"


# ---------- REGISTER ----------
def register():
    st.markdown("## 📝 Register")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Register"):
        if username in st.session_state.users:
            st.error("User already exists")
        elif username == "" or password == "":
            st.warning("Please fill all fields")
        else:
            st.session_state.users[username] = password
            st.success("Registration successful 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "welcome"
        st.rerun()


# ---------- LOGIN ----------
def login():

    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # ---------- ROUTING ----------
    if st.session_state.page == "welcome":
        show_welcome()
        return False

    elif st.session_state.page == "register":
        register()
        return False

    elif st.session_state.page == "login":

        st.markdown("## 🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("⬅️ Back"):
            st.session_state.page = "welcome"
            st.rerun()

        return False

    return True


# ---------- LOGOUT ----------
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "welcome"
        st.rerun()