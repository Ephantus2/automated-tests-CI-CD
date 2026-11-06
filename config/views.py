from django.db import connection, DatabaseError
from django.http import JsonResponse
from django.views import View

class HealthCheckView(View):
    def get(self, request):
        try:
            # attempt a simple query against the database

            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return JsonResponse({
                "status": "healthy",
                "database": "connected"
            })

        except DatabaseError:
            return JsonResponse({
                "status": "unhealthy",
                "database": "unavailable"
            },
            status = 503
            )