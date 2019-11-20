#from django.conf.urls import url
from django.conf.urls import url,include
from django.contrib import admin
from django.urls import path
import rest_framework.authtoken.views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='杰普商城 API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 15
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^login/', obtain_jwt_token),  #jwt验证方式
    url(r'^api/', schema_view),
    url(r'^demo/', include('demo.urls', namespace='demo')),
    # 15!
    path(r'goods/',include('goods.urls',namespace='goods')),  #goods
    path(r'operations/',include('operations.urls',namespace='operations')),#operations
    path(r'users/',include('users.urls',namespace='users')),  #users

]