from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^wall$', views.index),
	url(r'^wall/submit_message$', views.submit_message),
	url(r'^wall/submit_comment$', views.submit_comment),
	url(r'^wall/delete_msg$', views.delete_msg),
	url(r'^wall/delete_comment$', views.delete_comment)
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)