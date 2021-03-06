from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Max
from django.db import transaction
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.utils import timezone
import os
from .models import Measure, Area
from .forms import *

@login_required()
def list_view(request):
	year 					= datetime.now().year
	year 					= request.GET.get('year',year)
	measure_query 			= Measure.objects.filter(date_created__year=year)
	measure_query 			= measure_query.values('id','note', 'measure_point_id', 'type_measure_id', 'month','temperature','chloride', 'date_created','status_OK')
	measure_point_query 	= Measure_point.objects.all().order_by('name').prefetch_related('area', 'type_measure')
	area_all 				= Measure_point.objects.all().values_list('area', flat=True)
	area_all 				= Area.objects.filter(id__in=area_all)
	form 					= Select_year_form(initial={'year':year})
	context 				= {	'measure_query':measure_query,
								'measure_point_query':measure_point_query,
								'range': range(1,13),
								'year':year,
								'area_all':area_all,
								'type_measure_all':Type_measure.objects.all(),
								'group_all': Measure_point_group.objects.all(),
								'form':form
							}
	return render(request, 'control/list.html', context)


@login_required()
def month_view(request):
	year 					= datetime.now().year
	year 					= int(request.GET.get('year',year))
	measure_query 			= Measure.objects.filter(date_created__year=year)
	measure_query 			= measure_query.values('id','note','measure_point_id', 'type_measure_id', 'month','temperature','chloride', 'date_created','status_OK')
	measure_point_query 	= Measure_point.objects.all().prefetch_related('area', 'type_measure')
	area_all 				= Measure_point.objects.all().values_list('area', flat=True)
	area_all 				= Area.objects.filter(id__in=area_all)
	form 					= Select_year_form(initial={'year':year})

	month 					= datetime.now().month
	if year == datetime.now().year:
		current_month = month
	else:
		current_month = 13



	context 				= {	'measure_query':measure_query,
								'measure_point_query':measure_point_query,
								'year':year,
								'area_all':area_all,
								'type_measure_all':Type_measure.objects.all(),
								'group_all': Measure_point_group.objects.all(),
								'current_month': current_month,
								'form':form
							}
	return render(request, 'control/list_month.html', context)


@login_required()
def select_point_view(request):
	
	form 			= Select_point_form(request.GET or None)
	error 			= ""
	current_month 	= datetime.now().month
	suggested 		= []
	suggested_qs	= Measure_point.objects.filter(group=current_month)
	for measure_point in suggested_qs:
		for type_measure in measure_point.type_measure.all():
			max_date = measure_point.measure_set.filter(type_measure=type_measure).aggregate(Max('date_created'))
			if max_date.get('date_created__max'):
				if max_date.get('date_created__max') < timezone.now().replace(day=1, hour=0, minute=0, second=0):
					suggested.append({'measure_point': measure_point, 'type_measure':type_measure })

			else:
				suggested.append({'measure_point': measure_point, 'type_measure':type_measure })
	print(suggested)
	if form.is_valid():
		measure_point = int(form.cleaned_data.get('measure_point'))
		measure_point_qs = Measure_point.objects.filter(number=measure_point)
		if measure_point_qs:
			url = reverse('create_measure') + f"?measure_point={measure_point}"
			return redirect(url)
		else:
			error="No hi ha cap punt de mesura amb aquest numero"
	
	context = {
				'form':form,
				'area_all':Area.objects.all(),
				'error':error,
				'suggested':suggested
	}
	return render (request, 'control/select_point.html', context)


@login_required()
def create_measure_view(request,*args,**kwargs):
	
	measure_point 			= request.GET.get('measure_point')
	measure_point_qs 		= Measure_point.objects.filter(number=measure_point)
	type_measure 			= request.GET.get('type_measure')
	

	if measure_point_qs:
		measure_point 		= Measure_point.objects.get(number=measure_point)
		if measure_point and type_measure:
			type_measure 	= Type_measure.objects.get(id=type_measure)
			form 			= Create_measure_form(request.POST or None, initial={'measure_point':measure_point,
																			'type_measure':type_measure})
		elif measure_point.type_measure.count() == 1:
			type_measure 	= measure_point.type_measure.first()
			form 			= Create_measure_form(request.POST or None, initial={'measure_point':measure_point,
																			'type_measure':type_measure})
		elif measure_point.type_measure.count() > 1:
			form = Select_type_form()
			context 		= {'measure_point':measure_point,
								'form':form,
								'current_group':datetime.now().month
							}
			return render(request, 'control/select_type.html', context)

		context 	= {'form':form,
					'measure_point':measure_point,
					'type_measure':type_measure,
					'current_group':datetime.now().month
		}

		if request.POST:
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user_created = request.user
				instance.month = datetime.now().month
				instance.save()
				return redirect('select_point')
		return render(request, 'control/create_measure.html', context)
	else:
		return redirect('month_view')

@login_required()
def edit_measure_view(request, *arg, **kwargs):
	measure_id 		= request.GET.get('measure_id')
	instance 		= Measure.objects.filter(id=measure_id)
	if instance:
		instance 	= Measure.objects.get(id=measure_id)
		form 	 	= Create_measure_form(request.POST or None, instance=instance)
		if "delete" in request.POST:
			print(instance)
			instance.delete()
			return redirect('month_view')
		if form.is_valid():
			form.save()
			return redirect('month_view')

		context = {
				'form':form
		}
		return render (request, 'control/edit_measure.html', context)
	else:
		return redirect('month_view')

	
@login_required()
def measure_view(request):
	measure_id 		= request.GET.get('measure_id')
	instance 		= Measure.objects.filter(id=measure_id)
	if instance:
		instance 	= Measure.objects.get(id=measure_id)
		

		context = {
				'instance':instance
		}
		return render (request, 'control/measure_view.html', context)
	else:
		return redirect('month_view')


@login_required()
def select_area_view(request):
	form 		= Select_area_form()
	context = {
		}
	return render (request, 'control/select_area.html', context)


@login_required()
def create_measure_point_view(request,*arg, **kwargs):

	if request.POST:
		form = Create_measure_point_form(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			try:
				instance.weight = 	Measure_point.objects.all().aggregate(Max('weight'))['weight__max']+1
			except TypeError as error:
				instance.weight = 1
			instance.save()
			form.save_m2m()
		else:
			context 	= { 'form':form
			}
			return render(request, 'control/create_measure_point.html', context)

	
	try:
		if Measure_point.objects.all().order_by('id').last():
			last_point = Measure_point.objects.all().order_by('id').last()
			form = Create_measure_point_form(initial= {
										'number': Measure_point.objects.all().aggregate(Max('number'))['number__max']+1,
										'area': last_point.area.pk,
										})
		else:
			form = Create_measure_point_form(initial= {
										'number': Measure_point.objects.all().aggregate(Max('number'))['number__max']+1,
										})

	except TypeError:
		form = Create_measure_point_form(initial= {
									'number':1,
									})

	context 	= { 'form':form
	}
	return render(request, 'control/create_measure_point.html', context)


@login_required()
def create_area_view(request,*arg, **kwargs):
	form = Create_area_form(request.POST or None)
	if form.is_valid():
		form.save()
		form = Create_area_form()
	context 	= { 'form':form,
					'areas': Area.objects.all()
	}
	return render(request, 'control/create_area.html', context)

@login_required()
def set_area_order_view(request,*args, **kwargs):
	error 	= ""
	if request.is_ajax():
		sort 		= request.POST.get('data')
		element_id 	= request.POST.get('element_id')
		action 		= request.POST.get('action')
		
		if sort:
			sort = sort.split(',')
			with transaction.atomic():
				for i, id_value in enumerate(sort):
					instance = Area.objects.get(id=id_value)
					instance.weight = i
					instance.save()

		elif action == "edit":
			form = Create_area_form(request.POST, instance=Area.objects.get(id=element_id))
			if form.is_valid():
				form.save()
			else:
				error = form.errors['area']
		elif action == "delete":
			print("pre-delete")
			form = Delete_area_form(request.POST, instance=Area.objects.get(id=element_id))
			if form.is_valid():
				Area.objects.get(id=element_id).delete()
				print("delete", element_id)
			else:
				error = form.errors['area']
		
	return JsonResponse({'data':'OK','error':error})

@login_required()
def edit_measure_point_view(request,*args,**kwargs):

	measure_point_group_all = Measure_point_group.objects.all()
	measure_point_orphan 	= Measure_point.objects.filter(group__isnull=True).order_by('number')
	measure_point_all 	 	= Measure_point.objects.all()
	
	context 	= { 'measure_point_group_all':measure_point_group_all,
					'measure_point_all':measure_point_all,
					'measure_point_orphan': measure_point_orphan

	}
	return render(request, 'control/edit_mesure_point.html', context)
	



@login_required()
def edit_measure_point2_view(request, *args, **kwargs):
	point_id 			= request.GET.get('point')
	point_instance 		= Measure_point.objects.filter(id=point_id)
	if "byNumber" in request.GET:
		url_redirect 	= 'edit_measure_point_byNumber'
	else:
		url_redirect 	= 'edit_point'

	if point_instance:
		point_instance 	= Measure_point.objects.get(id=point_id)
	else:
		return redirect(url_redirect)

	form 				= Create_measure_point_form(request.POST or None, instance=point_instance )
	if form.is_valid():
		if "delete" in request.POST:
			form.instance.delete()
			return redirect(url_redirect)
		else:
			form.save()
			
			return redirect(url_redirect)
	else:
		context 			= {
								'form':form
		}
		return render(request, 'control/edit_mesure_point2.html', context)


def set_point_order_view(request,*args, **kwargs):
	error 	= ""
	if request.is_ajax():
		points_array 		= request.POST.get('points_array')
		if points_array:
			points_array = points_array.split(',')
			weight = 1
			with transaction.atomic():
				for element in points_array:
					element = element.split('|')
					# print(element)
					if element[0] == "group":
						group = element[1]
						if group == "None":
							group = None
						else:
							group = Measure_point_group.objects.filter(id = group)
							if group:
								group = Measure_point_group.objects.get(id = group)
							else:
								break
					if element[0] == "point":
						point_id = element[1]
						point_measure_instance = Measure_point.objects.filter(id=point_id)
						if point_measure_instance:
							point_measure_instance = Measure_point.objects.get(id=point_id)
							point_measure_instance.weight = weight
							weight += 1
							point_measure_instance.group = group
							point_measure_instance.save()
		
	return JsonResponse({'data':'OK','error':error})

@login_required()
def edit_measure_point_byNumber_view(request,*args,**kwargs):

	measure_point_all 	 	= Measure_point.objects.all().order_by('number')
	
	context 	= { 'measure_point_all':measure_point_all,	
			}
	return render(request, 'control/edit_mesure_point_byNumber.html', context)

def download_db(request):
	base_dir=settings.BASE_DIR
	with open(os.path.join(base_dir, 'db.sqlite3'),'rb') as f:
		data 	= f.read()

	response = HttpResponse(data, content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=legionella_db_{}.sqlite'.format(datetime.now().strftime('%Y-%m-%d'))
	return response