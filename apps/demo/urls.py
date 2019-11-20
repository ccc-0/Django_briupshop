from django.conf.urls import url
from apps.demo import views
app_name = '[demo]'

urlpatterns = [
    url(r'^index/', views.index, name='index'),

    url(r'^index_class/', views.IndexClass.as_view(), name='index_class'),

]