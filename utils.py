import pandas as pd

def create_time_slots(start, end, duration):
    slots = []
    current = start

    while current < end:
        next_minutes = current.hour * 60 + current.minute + duration
        hour = next_minutes // 60
        minute = next_minutes % 60

        slot = f"{current.strftime('%H:%M')} - {hour:02}:{minute:02}"
        slots.append(slot)

        current = current.replace(hour=hour, minute=minute)

    return slots


def export_to_excel(timetable):
    with pd.ExcelWriter("timetable.xlsx") as writer:
        for section, df in timetable.items():
            df.to_excel(writer, sheet_name=f"Section_{section}")