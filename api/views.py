import csv

from django.http import HttpResponse
from rest_framework.views import APIView
from api.models import ApiUser, TodoItem


class GetCsvApiview(APIView):
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['name', 'city', 'title', 'completed'])

        queryset = TodoItem.objects.select_related('owner').order_by('owner')

        for item in queryset:
            writer.writerow([
                item.owner,
                item.owner.city,
                item.title,
                item.completed
            ])

        return response
