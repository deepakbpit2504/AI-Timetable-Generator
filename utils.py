from io import BytesIO
import pandas as pd

# -------- CREATE TIME SLOTS --------
def create_time_slots(start, end, duration):
    slots = []
    current = start

    while current < end:
        total = current.hour * 60 + current.minute + duration
        h = total // 60
        m = total % 60

        slots.append(f"{current.strftime('%H:%M')} - {h:02}:{m:02}")
        current = current.replace(hour=h, minute=m)

    return slots


# -------- EXPORT TO EXCEL (FIXED) --------
def export_to_excel(tt, faculty_tt):
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sec, df in tt.items():
            df.to_excel(writer, sheet_name=f"Section_{sec}")

        faculty_df = pd.DataFrame(
            dict([(k, pd.Series(v)) for k, v in faculty_tt.items()])
        )
        faculty_df.to_excel(writer, sheet_name="Faculty")

    output.seek(0)
    return output.getvalue()   # ✅ IMPORTANT FIX