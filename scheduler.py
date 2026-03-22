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

                # Capacity check
                valid = True
                for sec in target:
                    if rooms[room] < students[sec]:
                        valid = False

                if not valid:
                    continue

                # Conflict checks
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


def evaluate_timetable(timetable):
    score = 0
    conflicts = []

    faculty_usage = {}
    room_usage = {}
    faculty_load = {}
    subject_day_count = {}

    for sec, df in timetable.items():
        for day in df.index:

            prev_empty = False

            for slot in df.columns:
                val = df.loc[day, slot]

                if not val:
                    score += 5
                    if prev_empty:
                        score += 2
                    prev_empty = True
                    continue

                prev_empty = False

                subject, rest = val.split("\n", 1)
                faculty = rest.split("\n")[0].replace("(", "").replace(")", "")
                room = val.split("[")[-1].replace("]", "")

                faculty_load[faculty] = faculty_load.get(faculty, 0) + 1

                key_sd = (sec, day, subject)
                subject_day_count[key_sd] = subject_day_count.get(key_sd, 0) + 1

                if subject_day_count[key_sd] > 2:
                    score += 10

                key1 = (day, slot, faculty)
                if key1 in faculty_usage:
                    score += 25
                else:
                    faculty_usage[key1] = True

                key2 = (day, slot, room)
                if key2 in room_usage:
                    score += 20
                else:
                    room_usage[key2] = True

    if faculty_load:
        avg = sum(faculty_load.values()) / len(faculty_load)
        for load in faculty_load.values():
            if load > avg + 2:
                score += 10

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