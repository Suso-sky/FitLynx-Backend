from gym.models import Asistencia
from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import time, date

class ReporteView(View):
    def get(self, request, *args, **kwargs):
        # Obtener las asistencias de la base de datos
        asistencias = Asistencia.objects.all()

        # Crear un DataFrame de pandas con los datos de las asistencias
        data = {
            'Nombre': [asistencia.usuario.nombre for asistencia in asistencias],
            'Programa': [asistencia.usuario.programa for asistencia in asistencias],
            'Código Estudiantil': [asistencia.usuario.codigo_estudiantil for asistencia in asistencias],
            'Fecha': [asistencia.fecha.strftime('%Y-%m-%d') if isinstance(asistencia.fecha, date) else asistencia.fecha for asistencia in asistencias],
            'Hora': [asistencia.hora.strftime('%H:%M:%S') if isinstance(asistencia.hora, time) else asistencia.hora for asistencia in asistencias],
            'Cantidad de Horas': [asistencia.cantidad_horas for asistencia in asistencias],
        }

        df = pd.DataFrame(data)

        # Crear un libro de Excel y escribir el DataFrame en una hoja
        wb = Workbook()
        ws = wb.active

        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Configurar las columnas para un mejor formato
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

        # Configurar la respuesta HTTP para la descarga del archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=asistencias.xlsx'
        wb.save(response)

        return response
