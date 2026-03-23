import streamlit as st

# -------- USERS --------
USERS = {"admin": "1234"}

# -------- LOGIN FUNCTION --------
def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        # 🎨 PAGE LAYOUT
        col1, col2 = st.columns([1.5, 1])

        # -------- LEFT SIDE (INFO) --------
        with col1:
            st.title("🤖 AI Timetable Generator")

            st.markdown("""
### 🚀 Smart Academic Scheduling System

Generate **conflict-free, optimized timetables** using intelligent algorithms.

---

### 🎯 Advantages
- ⏱️ Saves huge manual effort  
- 📉 Eliminates scheduling conflicts  
- ⚡ Handles multi-section complexity  
- 📊 Balanced workload distribution  
- 🧠 Smart optimization with scoring  

---

### 📚 Uses
- 🏫 Colleges & Universities  
- 🏫 Schools  
- 📖 Coaching Institutes  
- 🧑‍🏫 Faculty scheduling  

---

### 🔐 Why Login is Required?

Login ensures that:
- 🔒 Only authorized users access the system  
- 💾 User data and configurations are सुरक्षित (secure)  
- 🧑‍💻 Personalized timetable generation is possible  
- 📊 Data integrity and privacy are maintained  

👉 This makes the system **safe, reliable, and user-specific**.

---

💡 *Design smarter schedules, faster than ever.*
""")

        # -------- RIGHT SIDE (LOGIN BOX) --------
        with col2:
            st.markdown("## 🔐 Login Portal")

            st.markdown("""
Enter your credentials to access the system.

- Authorized access only  
- Secure authentication  
- Quick and easy login  
""")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
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