from rest_framework import viewsets
from ..serializers import UserNameUpdateSerializer
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from django.http import JsonResponse

class UserUpdateView(viewsets.ViewSet):
    serializer_class = UserNameUpdateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def update(self, request, pk=None):
        user = request.user
        print(user)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
    "success" : True,
    "message" : "Data updated successfully"
})#{'success':True,"data":serializer.data}, status=200)
        return JsonResponse(serializer.errors)#, status=400)
