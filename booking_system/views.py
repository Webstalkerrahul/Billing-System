from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from booking_system.models import Resources, Bookings
from booking_system.serializer import ResourcesSerializer, BookingsSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username or not password:
            return render(
                request,
                'login.html',
                {'error': 'Please enter both username and password.'}
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('resources-list')  # Redirect to the resources API endpoint
        else:
            return render(
                request,
                'login.html',
                {'error': 'Invalid credentials.'}
            )

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ResourcesViewSet(ModelViewSet):
    queryset = Resources.objects.all()
    serializer_class = ResourcesSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        resources = Resources.objects.filter(available_quantity__gt=0)
        resources_not_available = Resources.objects.filter(available_quantity__lt=1)
        serializer = self.get_serializer(resources, many=True)
        stock_serializer = self.get_serializer(resources_not_available, many=True)
        return Response({
            'message': 'Resources fetched successfully',
            'resources': serializer.data,
            'out of stock resources': stock_serializer.data
        })

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def availability(self, request, pk=None):
        try:
            resource = Resources.objects.get(id=pk)
            serializer = self.get_serializer(resource)
            return Response({
                'message': 'Resource availability fetched successfully',
                'resource': serializer.data
            })
        except Resources.DoesNotExist:
            return Response({
                'message': 'Resource not found',
                'error': f'Resource with id {pk} does not exist'
            }, status=status.HTTP_404_NOT_FOUND)


class BookingsViewSet(ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_bookings(self, request):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response({
            'message': 'Bookings fetched successfully',
            'bookings': serializer.data
        })

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'register':
            return UserSerializer
        return self.serializer_class

    @action(detail=False, methods=['POST'], permission_classes=[IsAdminUser ])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            return Response({'message': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'message': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': f'Username "{username}" is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'message': f'Email "{email}" is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(
                username=username,
                email=email,
                password=make_password(password)  # Hash the password
            )
            return Response({
                'message': 'User created successfully.',
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Error creating user.', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
