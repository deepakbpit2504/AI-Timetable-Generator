import streamlit as st
import pandas as pd
from auth import login, logout
from scheduler import generate_timetable, detect_conflicts
from utils import create_time_slots, export_to_excel

st.set_page_config(page_title="AI Timetable", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.main {background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);color:white;}
h1,h2,h3{color:#00e6e6;}
.stButton>button{border-radius:10px;background:#00c6ff;color:white;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 AI Timetable Generator</h1>", unsafe_allow_html=True)

st.info("🧠 Heuristic-based scheduling with iterative optimization")

# ---------- LOGIN ----------
if not login():
    st.stop()

logout()

# ---------- NAV ----------
menu = st.sidebar.radio("Navigation", ["Dashboard","Generator","Analytics"])

# ---------- INPUT ----------
course = st.sidebar.selectbox("Course", ["B.Tech","BBA","MBA","BSc"])
branch = st.sidebar.selectbox("Branch", ["CSE","IT","ECE","EEE"])
shift = st.sidebar.selectbox("Shift", ["Shift 1","Shift 2"])
sections = st.sidebar.multiselect("Sections", ["A","B","C"], default=["A"])
rooms = st.sidebar.multiselect("Rooms", ["Room 101","Room 102","Lab 1"], default=["Room 101"])

num = st.sidebar.number_input("Subjects",1,10,5)

subjects=[]
faculty_map={}

for i in range(num):
    s=st.sidebar.text_input(f"Sub {i+1}",key=i)
    f=st.sidebar.text_input(f"Fac {i+1}",key=i+100)
    if s:
        subjects.append(s)
        faculty_map[s]=f if f else "TBD"

start=st.sidebar.time_input("Start")
end=st.sidebar.time_input("End")
duration=st.sidebar.slider("Duration",30,120,60)

days=["Mon","Tue","Wed","Thu","Fri"]

# ---------- DASHBOARD ----------
if menu=="Dashboard":
    st.metric("Subjects",len(subjects))
    st.metric("Sections",len(sections))
    st.metric("Rooms",len(rooms))

# ---------- GENERATOR ----------
if menu=="Generator":

    if st.button("Generate"):
        slots=create_time_slots(start,end,duration)
        tt=generate_timetable(sections,days,slots,subjects,faculty_map,rooms)
        st.session_state.tt=tt

    if st.button("🔄 Regenerate Better"):

        best=None
        min_conf=999

        for _ in range(5):
            slots=create_time_slots(start,end,duration)
            tt=generate_timetable(sections,days,slots,subjects,faculty_map,rooms)
            conf=detect_conflicts(tt)

            if len(conf)<min_conf:
                min_conf=len(conf)
                best=tt

        st.session_state.tt=best
        st.success(f"Optimized! Conflicts: {min_conf}")

    if "tt" in st.session_state:
        tt=st.session_state.tt

        for sec,df in tt.items():
            st.subheader(sec)
            st.dataframe(df)

        conflicts=detect_conflicts(tt)

        st.subheader("Conflicts")
        if conflicts:
            for c in conflicts:
                st.write(c)
        else:
            st.success("No conflicts!")

        if st.button("Export"):
            export_to_excel(tt)
            with open("timetable.xlsx","rb") as f:
                st.download_button("Download",f)

# ---------- ANALYTICS ----------
if menu=="Analytics":
    if "tt" in st.session_state:
        tt=st.session_state.tt
        rc={}
        for df in tt.values():
            for val in df.values.flatten():
                if val:
                    r=val.split("[")[-1].replace("]","")
                    rc[r]=rc.get(r,0)+1
        st.bar_chart(pd.DataFrame.from_dict(rc,orient='index',columns=['Usage']))