from django.conf.urls import url
from django.views.generic.base import RedirectView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .capability_statement import capability_statement

from api import views

schema_view = get_schema_view(
    openapi.Info(
        title="CALC API",
        default_version='v2',
        description="CALC API DOCUMENTATION",
        contact=openapi.Contact(email="calc@gsa.gov"),
    ),
    public=True,
)

urlpatterns = [
    url(r'^rates/$', views.GetRates.as_view()),
    url(r'^rates/csv/$', views.GetRatesCSV.as_view()),
    url(r'^search/$', views.GetAutocomplete.as_view()),
    url(r'^schedules/$', views.ScheduleMetadataList.as_view()),
    url(r'^docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^$', RedirectView.as_view(pattern_name='api-docs:docs-index')),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^contract/capability_statement/(?P<contractnumber>[\w-]+)/$',
        capability_statement.get_capability_statment),  # after login
    url(r'^contract/capability_statement/url/(?P<contractnumberlist>[\w,-]+)/$',
        capability_statement.get_bulk_capability_statment),
]
