import pandas as pd
import random

def generate_timetable(sections, days, slots, subjects, faculty_map, rooms):
    timetable = {sec: pd.DataFrame("", index=days, columns=slots) for sec in sections}

    faculty_schedule = {}
    room_schedule = {}

    # Initialize tracking
    for day in days:
        for slot in slots:
            faculty_schedule[(day, slot)] = set()
            room_schedule[(day, slot)] = set()

    # PRIORITY: shuffle subjects (smart distribution)
    subjects = subjects.copy()
    random.shuffle(subjects)

    for section in sections:
        for subject in subjects:
            faculty = faculty_map[subject]

            attempts = 0
            assigned = False

            while not assigned and attempts < 200:
                day = random.choice(days)
                slot = random.choice(slots)
                room = random.choice(rooms)

                if timetable[section].loc[day, slot] == "":
                    if faculty not in faculty_schedule[(day, slot)]:
                        if room not in room_schedule[(day, slot)]:

                            timetable[section].loc[day, slot] = (
                                f"{subject}\n({faculty})\n[{room}]"
                            )

                            faculty_schedule[(day, slot)].add(faculty)
                            room_schedule[(day, slot)].add(room)

                            assigned = True

                attempts += 1

    return timetable


def detect_conflicts(timetable):
    conflicts = []

    for section, df in timetable.items():
        for day in df.index:
            row = list(df.loc[day])
            if len(row) != len(set(row)):
                conflicts.append(f"Duplicate in {section} on {day}")

    return conflicts