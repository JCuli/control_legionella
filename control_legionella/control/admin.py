from django.contrib import admin
from .models import Measure_point,\
					Type_measure,\
					Measure,\
					Area,\
					Measure_point_group
admin.site.register(Measure_point)
admin.site.register(Type_measure)
admin.site.register(Measure)
admin.site.register(Area)
admin.site.register(Measure_point_group)