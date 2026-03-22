import streamlit as st

users = {
    "admin": "1234",
    "faculty": "abcd"
}

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.markdown("## 🔐 Login Page")

        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u in users and users[u] == p:
                st.session_state.logged_in = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        return False
    return True

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()