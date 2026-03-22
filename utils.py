from io import BytesIO
import pandas as pd

def export_to_excel(tt, faculty_tt):

    output = BytesIO()

    writer = pd.ExcelWriter(output, engine='openpyxl')

    # Section sheets
    for sec, df in tt.items():
        df.to_excel(writer, sheet_name=f"Section_{sec}")

    # Faculty sheet
    faculty_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in faculty_tt.items()]))
    faculty_df.to_excel(writer, sheet_name="Faculty")

    writer.close()   # IMPORTANT ✅

    output.seek(0)

    return output