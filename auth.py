import streamlit as st

# -------- DEFAULT USER --------
USERS = {"admin": "1234"}


def login():

    # 🔄 RESET BUTTON (VERY IMPORTANT)
    if st.sidebar.button("🔄 Reset App"):
        st.session_state.clear()
        st.rerun()

    # INIT STATE
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # -------- SHOW INTRO + LOGIN --------
    if not st.session_state.logged_in:

        # 🎯 MAIN TITLE
        st.title("🤖 AI Timetable Generator")

        # 📄 INTRO CONTENT
        st.markdown("""
## 🚀 Intelligent Academic Scheduling System

This system automatically generates **optimized and conflict-free timetables** 
for educational institutions.

---

### 🎯 Advantages
- ⏱️ Saves time compared to manual scheduling  
- 📉 Reduces human errors  
- ⚡ Handles multiple sections efficiently  
- 📊 Balanced workload distribution  
- 🧠 Smart optimization using scoring  

---

### 📚 Uses
- 🏫 Colleges & Universities  
- 🏫 Schools  
- 📖 Coaching Institutes  
- 🧑‍🏫 Faculty scheduling  

---

### 🔐 Why Login?

Login ensures:
- 🔒 Secure and authorized access  
- 💾 Protection of user data  
- 👤 Personalized timetable generation  
- 📊 System integrity and reliability  

---
""")

        # 🔐 LOGIN SECTION
        st.markdown("## 🔐 Login to Continue")

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
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()   # FULL RESET
        st.rerun()