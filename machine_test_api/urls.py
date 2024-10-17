from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, ClientProjectCreateView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('machine_test_api/', include(router.urls)),
    path('machine_test_api/clients/<int:client_id>/projects/', ClientProjectCreateView.as_view(), name='client-projects'),
    path('machine_test_api-token-auth/', obtain_auth_token, name='api_token_auth'),  # For obtaining auth token
]
