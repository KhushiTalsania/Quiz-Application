from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from projects.models import Result
from .serializers import ResultSerializer

@api_view(['GET'])
def getroutes(request):
    routes = [
        {'GET': '/api/home'},
        {'GET': '/api/department/id'},
    ]
    return Response(routes)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getresults(request):
    print("User: ", request.user)
    participants = Result.objects.all()
    serializers = ResultSerializer(participants, many = True)
    return Response(serializers.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def getresult(request, id):
    result = Result.objects.get(id = id)
    serializers = ResultSerializer(result, many = False)
    print("User: ", request.user)
    print("Value: ", request.data['value'])
    return Response(serializers.data)