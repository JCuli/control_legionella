from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.db import transaction
from datetime import date, datetime
from .models import Measure, Area
from .forms import *

def home_view(request):
	year 					= datetime.now().year
	measure_query 			= Measure.objects.filter(date_created__year=year)
	measure_point_query 	= Measure_point.objects.all()
	area_all 				= measure_query.values_list('measure_point__area', flat=True).distinct()
	area_all 				= Area.objects.filter(id__in=area_all)
	context 				= {	'measure_query':measure_query,
								'measure_point_query':measure_point_query,
								'range': range(1,5),
								'year':year,
								'area_all':Area.objects.all()
							}

	return render(request, 'control/list.html', context)


def select_point_view(request):
	
	form 		= Select_point_form(request.GET or None)
	error 		= ""
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
				'error':error
	}
	return render (request, 'control/select_point.html', context)


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
								'form':form
							}
			return render(request, 'control/select_type.html', context)

		context 	= {'form':form,
					'measure_point':measure_point,
					'type_measure':type_measure
		}
	else:
			return redirect('home')

	if request.POST:
		
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user_created = request.user
			instance.save()
			if "seguent" in request.POST:
				current_weight = measure_point.weight
				while current_weight < Measure_point.objects.all().aggregate(Max('weight'))['weight__max']:
					print(current_weight)
					print(Measure_point.objects.all().aggregate(Max('weight'))['weight__max'])
					try:
						next_measure_point = Measure_point.objects.get(weight=current_weight+1)
						url = reverse('create_measure') + f"?measure_point={next_measure_point.number}"
						return redirect(url)
					except:
						current_weight = current_weight +1
				
				else:
					error= "Aquest es l'ultim punt."
			return redirect('select_point')
	
	return render(request, 'control/create_measure.html', context)

def select_area_view(request):
	form 		= Select_area_form()
	context = {
				'form':form
	}
	return render (request, 'control/select_area.html', context)

# def select_point_view(request):
# 	areas 		= request.GET.getlist('area')
	
# 	areas_qs 	= Area.objects.filter(id__in=areas)
	
# 	queryset= Measure_point.objects.filter(area__in=areas_qs)
	
# 	form 		= Select_point_form()
# 	form.fields['id'].queryset = queryset
# 	context = {
# 				'form':form
# 	}
# 	return render (request, 'control/select_point.html', context)

def create_measure_point_view(request,*arg, **kwargs):
	form = Create_measure_point_form(request.POST or None, initial= {
									'number': Measure_point.objects.all().aggregate(Max('number'))['number__max']+1
									})
	if form.is_valid():
		instance = form.save(commit=False)
		instance.weight = 	Measure_point.objects.all().aggregate(Max('weight'))['weight__max']+1
		instance.save()
		form.save_m2m()
		form = Create_measure_point_form(initial= {
									'number': Measure_point.objects.all().aggregate(Max('number'))['number__max']+1
									})

	context 	= { 'form':form
	}
	return render(request, 'control/create_measure_point.html', context)


def create_area_view(request,*arg, **kwargs):
	form = Create_area_form(request.POST or None)
	if form.is_valid():
		form.save()
		form = Create_area_form()
	context 	= { 'form':form,
					'areas': Area.objects.all()
	}
	return render(request, 'control/create_area.html', context)

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

def edit_mesure_point_view(request,*args,**kwargs):

	area_all 				= Area.objects.all()
	measure_point_orphan 	= Measure_point.objects.filter(area__isnull=True)
	
	context 	= { 'area_all':area_all,
					'measure_point_orphan': measure_point_orphan

	}
	return render(request, 'control/edit_mesure_point.html', context)
	


def edit_mesure_point2_view(request, *args, **kwargs):
	point_id 			= request.GET.get('point')
	point_instance 		= Measure_point.objects.filter(id=point_id)
	if point_instance:
		point_instance 	= Measure_point.objects.get(id=point_id)
	else:
		return redirect('edit_point')

	form 				= Create_measure_point_form(request.POST or None, instance=point_instance )
	if form.is_valid():
		if "delete" in request.POST:
			form.instance.delete()
			return redirect('edit_point')
		else:
			form.save()
			
			return redirect('edit_point')
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
					if element[0] == "area":
						area = element[1]
						if area == "None":
							area = None
						else:
							area = Area.objects.filter(id = area)
							if area:
								area = Area.objects.get(id = area)
							else:
								break
					if element[0] == "point":
						point_id = element[1]
						point_measure_instance = Measure_point.objects.filter(id=point_id)
						if point_measure_instance:
							point_measure_instance = Measure_point.objects.get(id=point_id)
							point_measure_instance.weight = weight
							weight += 1
							point_measure_instance.area = area
							point_measure_instance.save()



		
	return JsonResponse({'data':'OK','error':error})