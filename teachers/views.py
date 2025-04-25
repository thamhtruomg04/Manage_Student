from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Teacher
from .serializers import TeacherSerializer
from django.contrib.auth.models import User

class TeacherListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to list all teachers or create a new teacher.
    - GET: Return a list of all teachers.
    - POST: Create a new teacher (requires admin authentication).
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Ensure only admins can create teachers
        if not self.request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to create a teacher."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Create a new User instance for the teacher
        user_data = self.request.data.get('user')
        if user_data:
            user = User.objects.create_user(
                username=user_data.get('username'),
                password=user_data.get('password'),
                email=user_data.get('email', '')
            )
            serializer.save(user=user)
        else:
            return Response(
                {"detail": "User data is required to create a teacher."},
                status=status.HTTP_400_BAD_REQUEST
            )

class TeacherRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a teacher.
    - GET: Return details of a specific teacher.
    - PUT/PATCH: Update a teacher's details (requires admin authentication).
    - DELETE: Delete a teacher (requires admin authentication).
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Ensure only admins can update teachers
        if not self.request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to update a teacher."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Update user data if provided
        user_data = self.request.data.get('user')
        if user_data:
            user = self.get_object().user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            if user_data.get('password'):
                user.set_password(user_data['password'])
            user.save()
        serializer.save()

    def perform_destroy(self, instance):
        # Ensure only admins can delete teachers
        if not self.request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to delete a teacher."},
                status=status.HTTP_403_FORBIDDEN
            )
        # Delete the associated User instance
        instance.user.delete()
        instance.delete()