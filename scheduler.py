import pandas as pd
import random

def generate_timetable(sections, days, slots, subjects, faculty_map, rooms):
    timetable = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}

    faculty_usage = {}
    room_usage = {}

    for day in days:
        for slot in slots:
            faculty_usage[(day, slot)] = set()
            room_usage[(day, slot)] = set()

    for section in sections:
        for subject in subjects:
            faculty = faculty_map.get(subject, "TBD")

            for _ in range(100):  # try multiple times
                day = random.choice(days)
                slot = random.choice(slots)
                room = random.choice(rooms)

                if timetable[section].loc[day, slot] == "":
                    if faculty not in faculty_usage[(day, slot)]:
                        if room not in room_usage[(day, slot)]:

                            timetable[section].loc[day, slot] = f"{subject}\n({faculty})\n[{room}]"

                            faculty_usage[(day, slot)].add(faculty)
                            room_usage[(day, slot)].add(room)
                            break

    return timetable


def detect_conflicts(timetable):
    conflicts = []
    faculty_usage = {}
    room_usage = {}

    for section, df in timetable.items():
        for day in df.index:
            for slot in df.columns:
                val = df.loc[day, slot]

                if not val:
                    conflicts.append(f"⚠️ Empty slot in {section} on {day} ({slot})")
                    continue

                try:
                    subject, rest = val.split("\n", 1)
                    faculty = rest.split("\n")[0].replace("(", "").replace(")", "")
                    room = val.split("[")[-1].replace("]", "")
                except:
                    continue

                key = (day, slot, faculty)
                if key in faculty_usage:
                    conflicts.append(f"❌ Faculty clash: {faculty} on {day} {slot}")
                else:
                    faculty_usage[key] = True

                key2 = (day, slot, room)
                if key2 in room_usage:
                    conflicts.append(f"❌ Room clash: {room} on {day} {slot}")
                else:
                    room_usage[key2] = True

    return conflicts