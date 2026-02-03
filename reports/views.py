from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import get_monthly_summary




class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = get_monthly_summary(request.user)
        return Response(data)
