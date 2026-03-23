import streamlit as st

USERS = {"admin": "1234"}

def login():

    # 🔥 FORCE RESET BUTTON (VERY IMPORTANT)
    if st.sidebar.button("🔄 Reset App"):
        st.session_state.clear()
        st.rerun()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # 👉 ALWAYS SHOW THIS IF NOT LOGGED IN
    if not st.session_state.logged_in:

        st.title("🤖 AI Timetable Generator")

        st.markdown("""
## 🚀 Intelligent Academic Scheduling System

This system generates **optimized, conflict-free timetables** automatically.

---

### 🎯 Advantages
- Saves time ⏱️  
- Reduces errors 📉  
- Handles multiple sections ⚡  
- Balanced workload 📊  

---

### 📚 Uses
- Colleges  
- Schools  
- Coaching institutes  

---

### 🔐 Why Login?

Login ensures:
- Secure access  
- Data protection  
- Personalized scheduling  

---
""")

        st.markdown("## 🔐 Login to Continue")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

        return False

    return True


def logout():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()   # 💀 FULL RESET
        st.rerun()