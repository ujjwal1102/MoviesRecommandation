from rest_framework import viewsets
from .models import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer, RegisterSerializer
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Movie, Review
from . import recommandations
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 10
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Review API",
        default_version='v1',
        description="API documentation for the Movie Review application",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def recommendations(self, request, pk=None):
        try:
            movie_id = int(pk)
            similar_ids = recommandations.find_similar_movies(movie_id, k=10)
            recommended_movies = Movie.objects.filter(id__in=similar_ids)
            serializer = MovieSerializer(recommended_movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

