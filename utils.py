import pandas as pd

def create_time_slots(start, end, duration):
    slots = []
    current = start

    while current < end:
        total = current.hour*60 + current.minute + duration
        h = total // 60
        m = total % 60

        slots.append(f"{current.strftime('%H:%M')} - {h:02}:{m:02}")
        current = current.replace(hour=h, minute=m)

    return slots


def export_to_excel(tt, faculty_tt):
    with pd.ExcelWriter("timetable.xlsx") as writer:

        for sec, df in tt.items():
            df.to_excel(writer, sheet_name=sec)

        pd.DataFrame(dict([(k, pd.Series(v)) for k,v in faculty_tt.items()])).to_excel(writer, sheet_name="Faculty")