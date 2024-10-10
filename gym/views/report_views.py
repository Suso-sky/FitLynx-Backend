from gym.models import Attendance, Gym
from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import time, date
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from gym.permissions import IsAdminUser
from datetime import datetime

class ReportView(View):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        gym_id = self.kwargs.get('gym_id') 
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')     
         
        try:
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            else:
                start_date = None
                end_date = None

            gym = get_object_or_404(Gym, gym_id=gym_id)
            attendances = Attendance.objects.filter(gym=gym)

            if start_date and end_date:
                attendances = attendances.filter(date__range=[start_date, end_date])

            data = {
                'Nombre': [attendance.user.username for attendance in attendances],
                'Programa': [attendance.user.program for attendance in attendances],
                'Código': [attendance.user.student_code for attendance in attendances],
                'Fecha': [attendance.date.strftime('%Y-%m-%d') if isinstance(attendance.date, date) else attendance.date for attendance in attendances],
                'Hora': [attendance.time.strftime('%H:%M:%S') if isinstance(attendance.time, time) else attendance.time for attendance in attendances],
                'Módulo': [attendance.gym.name.split(' ')[0] for attendance in attendances],
            }

            df = pd.DataFrame(data)
            
            wb = Workbook()
            ws = wb.active
            for row in dataframe_to_rows(df, index=False, header=True):
                ws.append(row)

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

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=attendance_report.xlsx'
            wb.save(response)

            return response

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}', status=500)