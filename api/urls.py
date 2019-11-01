from django.conf.urls import url
from django.views.generic.base import RedirectView
from rest_framework.documentation import include_docs_urls

from .capability_statement import capability_statement

from api import views

urlpatterns = [
    url(r'^rates/$', views.GetRates.as_view()),
    url(r'^rates/csv/$', views.GetRatesCSV.as_view()),
    url(r'^search/$', views.GetAutocomplete.as_view()),
    url(r'^schedules/$', views.ScheduleMetadataList.as_view()),
    url(r'^docs/', include_docs_urls(
        title='CALC API',
        description=views.DOCS_DESCRIPTION,
    )),
    url(r'^$', RedirectView.as_view(pattern_name='api-docs:docs-index')),
    url(r'^contract/capability_statement/(?P<contractnumber>[\w-]+)/$',
        capability_statement.get_capability_statment),  # after login
    url(r'^contract/capability_statement/url/(?P<contractnumberlist>[\w,-]+)/$',
        capability_statement.get_bulk_capability_statment),
]
