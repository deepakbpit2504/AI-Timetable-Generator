import streamlit as st

# -------- USERS --------
USERS = {"admin": "1234"}

# -------- LOGIN FUNCTION --------
def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        # FULL PAGE (WELCOME + LOGIN TOGETHER)
        st.title("🤖 AI Timetable Generator")

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
        st.session_state.logged_in = False
        st.rerun()