import streamlit as st

USERS = {"admin": "1234"}

def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        # FULL PAGE (NOT SPLIT)
        st.title("🤖 AI Timetable Generator")

        st.markdown("""
### 🚀 Intelligent Academic Scheduling System

This system helps institutions automatically generate **conflict-free and optimized timetables**.

---

## 🎯 Advantages
- ⏱️ Saves time compared to manual scheduling  
- 📉 Reduces human errors  
- ⚡ Handles multiple sections easily  
- 📊 Balanced workload distribution  
- 🧠 Smart optimization using scoring  

---

## 📚 Uses
- 🏫 Colleges & Universities  
- 🏫 Schools  
- 📖 Coaching Institutes  
- 🧑‍🏫 Faculty scheduling  

---

## 🔐 Why Login?

Login is required to:
- 🔒 Ensure secure access  
- 💾 Protect user data  
- 👤 Provide personalized timetable generation  
- 📊 Maintain system integrity  

---

### 🔐 Login to Continue
""")

        # LOGIN FORM BELOW CONTENT
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


def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()