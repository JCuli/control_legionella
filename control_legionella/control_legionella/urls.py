from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout,PasswordChangeView, PasswordChangeDoneView
from django.conf.urls.static import static
from django.conf import settings
from control.views import list_view,\
                            create_measure_view,\
                            select_area_view,\
                            select_point_view,\
                            create_measure_point_view,\
                            create_area_view,\
                            set_area_order_view,\
                            edit_measure_point_view,\
                            edit_measure_point2_view,\
                            set_point_order_view,\
                            month_view,\
                            edit_measure_view,\
                            measure_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^change-password/$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^all_view/$', list_view, name='all_view'),
    url(r'^create_measure/$', create_measure_view, name='create_measure'),
    url(r'^edit_measure/$', edit_measure_view, name='edit_measure'),
    url(r'^measure_view/$', measure_view, name='measure_view'),
    url(r'^create_area/$', create_area_view, name='create_area'),
    url(r'^set_area_order/$', set_area_order_view, name='set_area_order'),
    url(r'^set_point_order/$', set_point_order_view, name='set_point_order'),
    url(r'^create_point/$', create_measure_point_view, name='create_point'),
    url(r'^edit_point/$', edit_measure_point_view, name='edit_point'),
    url(r'^edit_point2/$', edit_measure_point2_view, name='edit_point2'),
    url(r'^select_area/$', select_area_view, name='select_area'),
    url(r'^select_point/$', select_point_view, name='select_point'),
    url(r'^$', month_view, name='month_view')
    
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
