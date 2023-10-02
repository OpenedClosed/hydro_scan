from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .views import (
    BottomViewSet,
    CharacteristicViewSet,
    OrderViewSet,
    download_3d_model,
    download_report,
)


app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title="Dummy API",
        default_version='v1',
        description="Dummy description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@dummy.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

router.register(
    r'bottoms',
    BottomViewSet,
    basename='bottoms'
)

router.register(
    r'characteristics',
    CharacteristicViewSet,
    basename='characteristics'
)

router.register(
    r'orders',
    OrderViewSet,
    basename='orders'
)

urlpatterns = [
    path(
        'orders/<int:order_id>/download_report/',
        download_report, name='shopping_cart'
    ),
    path(
        'orders/<int:order_id>/download_3d_model/',
        download_3d_model, name='shopping_cart'
    ),
    path('', include(router.urls)),
    re_path(
        r'^playground/$',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0
        ),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^docs/$',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='schema-redoc'
    )
]
