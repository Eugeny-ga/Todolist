from django.contrib.auth import login, authenticate, logout
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import exceptions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.serializers import *

@extend_schema_view(
    post=extend_schema(description='Registration view for new users', summary='User registration')
)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


@extend_schema_view(
    post=extend_schema(description='Login view for users', summary='User login')
)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)
        if not user:
            raise exceptions.AuthenticationFailed

        login(request=request, user=user)

        return Response(ProfileSerializer(user).data)

@extend_schema_view(
    get=extend_schema(description='Get all information about user', summary='User retrieve'),

    put=extend_schema(description='Update all user\'s information', summary='User update'),

    patch=extend_schema(description='Update partial user\'s information', summary='User update partial'),

    delete=extend_schema(description='Logout user from system', summary='User Logout'),
)
class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
          logout(self.request)


@extend_schema_view(
    put=extend_schema(description='Update user password', summary='Password update')
)
class UpdatePasswordView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
