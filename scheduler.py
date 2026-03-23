import pandas as pd
import random

def generate_timetable(sections, days, slots, subjects, faculty_map, rooms, students, combined, locked):

    timetable = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}

    faculty_usage = {}
    room_usage = {}

    for d in days:
        for s in slots:
            faculty_usage[(d,s)] = set()
            room_usage[(d,s)] = set()

    for subject, info in subjects.items():

        faculty = faculty_map.get(subject, "TBD")
        hours = info["theory"] + info["practical"]

        for _ in range(hours):

            for _ in range(200):
                day = random.choice(days)
                slot = random.choice(slots)

                if f"{day}-{slot}" in locked:
                    continue

                room = random.choice(list(rooms.keys()))
                target = combined if combined else sections

                valid = True
                for sec in target:
                    if rooms[room] < students[sec]:
                        valid = False

                if not valid:
                    continue

                conflict = False

                for sec in target:
                    if timetable[sec].loc[day, slot] != "":
                        conflict = True

                if faculty in faculty_usage[(day,slot)]:
                    conflict = True

                if room in room_usage[(day,slot)]:
                    conflict = True

                if not conflict:
                    for sec in target:
                        timetable[sec].loc[day, slot] = f"{subject}\n({faculty})\n[{room}]"

                    faculty_usage[(day,slot)].add(faculty)
                    room_usage[(day,slot)].add(room)
                    break

    return timetable


def evaluate_timetable(tt):
    score = 0
    conflicts = []

    faculty_used = {}
    room_used = {}

    for sec, df in tt.items():
        for d in df.index:
            for s in df.columns:
                val = df.loc[d,s]

                if not val:
                    score += 5
                    continue

                faculty = val.split("\n")[1].replace("(","").replace(")","")
                room = val.split("[")[-1].replace("]","")

                if (d,s,faculty) in faculty_used:
                    score += 20
                    conflicts.append(f"Faculty clash {faculty}")
                else:
                    faculty_used[(d,s,faculty)] = True

                if (d,s,room) in room_used:
                    score += 15
                    conflicts.append(f"Room clash {room}")
                else:
                    room_used[(d,s,room)] = True

    return score, conflicts


def build_faculty_timetable(tt):
    faculty_tt = {}

    for sec, df in tt.items():
        for d in df.index:
            for s in df.columns:
                val = df.loc[d,s]
                if val:
                    fac = val.split("\n")[1].replace("(","").replace(")","")
                    faculty_tt.setdefault(fac, []).append(f"{d} {s} ({sec})")

    return faculty_tt