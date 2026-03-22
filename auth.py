import streamlit as st

if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

def show_welcome():
    st.title("🎓 AI Timetable Generator")

    st.markdown("""
### 🚀 Welcome to Intelligent Timetable System

Generate optimized, conflict-free academic timetables with ease.

### ✨ Features:
- Multi-section scheduling
- Faculty allocation
- Room management
- Conflict detection
- AI-based optimization
""")

    col1, col2 = st.columns(2)

    if col1.button("🔐 Login"):
        st.session_state.page = "login"

    if col2.button("📝 Register"):
        st.session_state.page = "register"


def register():
    st.markdown("## 📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        if u in st.session_state.users:
            st.error("User exists")
        elif u == "" or p == "":
            st.warning("Fill all fields")
        else:
            st.session_state.users[u] = p
            st.success("Registered 🎉")
            st.session_state.page = "login"
            st.rerun()

    if st.button("⬅️ Back"):
        st.session_state.page = "welcome"
        st.rerun()


def login():
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.page == "welcome":
        show_welcome()
        return False

    elif st.session_state.page == "register":
        register()
        return False

    elif st.session_state.page == "login":

        st.markdown("## 🔐 Login")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u in st.session_state.users and st.session_state.users[u] == p:
                st.session_state.logged_in = True
                st.success("Login success ✅")
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("⬅️ Back"):
            st.session_state.page = "welcome"
            st.rerun()

        return False

    return True


def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "welcome"
        st.rerun()