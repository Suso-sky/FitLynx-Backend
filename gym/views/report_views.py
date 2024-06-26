from gym.models import Attendance
from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import time, date

class ReportView(View):
    def get(self, request, *args, **kwargs):
        # Get attendances from the database
        attendances = Attendance.objects.all()

        # Create a pandas DataFrame with attendance data
        data = {
            'Name': [attendance.user.username for attendance in attendances],
            'Program': [attendance.user.program for attendance in attendances],
            'Student Code': [attendance.user.student_code for attendance in attendances],
            'Date': [attendance.date.strftime('%Y-%m-%d') if isinstance(attendance.date, date) else attendance.date for attendance in attendances],
            'Time': [attendance.time.strftime('%H:%M:%S') if isinstance(attendance.time, time) else attendance.time for attendance in attendances],
            'Hours': [attendance.hours_amount for attendance in attendances],
        }

        df = pd.DataFrame(data)

        # Create an Excel workbook and write the DataFrame to a sheet
        wb = Workbook()
        ws = wb.active

        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Adjust columns for better formatting
        for column in ws.columns:
            max_length = 0
            column = [cell for cell in column]
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        # Configure HTTP response for Excel file download
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'
        wb.save(response)

        return response
