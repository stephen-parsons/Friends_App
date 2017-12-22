from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	url(r'^friends$', views.index),
	url(r'^user/(?P<user_id>\d+)/send_request$', views.send_request),
	url(r'^user/(?P<user_id>\d+)/cancel_request$', views.cancel_request),
	url(r'^user/(?P<user_id>\d+)/cancel_recieved_request$', views.cancel_recieved_request),
	url(r'^user/(?P<user_id>\d+)/friend$', views.add_friend),
	url(r'^user/(?P<user_id>\d+)/unfriend$', views.un_friend),
	url(r'^user/(?P<user_id>\d+)$', views.user_profile),
	url(r'^user/upload_picture$', views.upload_picture),
	url(r'^user/upload/delete_img$', views.delete_picture)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)