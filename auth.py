import streamlit as st

USERS = {"admin": "1234"}

def login():

    # ✅ ADD THIS (ONLY CHANGE YOU NEED)
    st.title("🤖 AI Timetable Generator")
    st.subheader("Intelligent Scheduling System")

    st.markdown("""
- Generate optimized timetables  
- Avoid conflicts automatically  
- Save time and effort  
""")

    # 🔐 LOGIN FORM (keep your existing code)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()