from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('output', views.output,name='generate'),
    path('texttospeech',views.texttospeech,name='texttospeech'),
    # path('texttotranslate',views.texttotranslate,name='texttotranslate'),
    path('new_page/', views.new_page, name='new_page'),
]
