import io
import xlsxwriter


def sample_xlsx():
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()

    # workbook
    wb = xlsxwriter.Workbook(output, {"in_memory": True})
    ws = wb.add_worksheet()

    # sheet
    ws.write(0, 0, "Hello World")
    ws.write(1, 0, "結果はっぴょー")

    # close workbook
    wb.close()

    # rewind the buffer
    output.seek(0)

    # create xlsx
    create_file = output.getvalue()
    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    file_name = "sample.xlsx"
    return create_file, mime_type, file_name
