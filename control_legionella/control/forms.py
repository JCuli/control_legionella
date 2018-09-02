from django import forms
from django.contrib.auth.models import User
from .models import *
from .validators import validate_point


class Create_measure_form(forms.ModelForm):
	measure_point 		= forms.ModelChoiceField(
							queryset=Measure_point.objects.all(),
							label= "",
							widget = forms.Select(attrs={
									'class':"d-none"})
							)
	type_measure 		= forms.ModelChoiceField(
							queryset=Type_measure.objects.all(),
							label= "",
							widget = forms.Select(attrs={
									'class':"d-none"})
							)
	temperature 		= forms.DecimalField(
							required=True,
							label= "Temperatura",
							widget = forms.NumberInput(attrs={
									'placeholder':"ºC",
									'class':"form-control"})
							)
	status_OK 			=forms.BooleanField(
							required= False,
							label="Conservacio correcta?",
							widget = forms.CheckboxInput(attrs={
									'class':"form-check-input ml-2"})
							)

	class Meta:
		model 	= Measure
		fields	= [
			'measure_point',
			'type_measure',
			'temperature',
			'status_OK'
		]

# Create_measure_FormSet = forms.modelformset_factory(Measure,form=Create_measure_form, extra=0)

class Select_area_form(forms.ModelForm):
	
	c=Area.objects.all().order_by("area")
	area = forms.ModelMultipleChoiceField(
				queryset= c,
				required=False,
				label="Category",
				widget=forms.CheckboxSelectMultiple(attrs={
							
							# 'class':'form-check-input',		
							
				})
	)
	class Meta:
		model 	= Area
		fields	= [
			'area'
		]


class Select_point_form(forms.Form):
	measure_point 	=forms.IntegerField(
				validators =[validate_point],
				label="Numero",
				required=True,
				widget=forms.NumberInput(attrs={
							'class':'form-control',
							'placeholder':'#Punt de mesura'
				})
	)


class Select_type_form(forms.ModelForm):
	
	c=Type_measure.objects.all()
	type_measure = forms.ModelChoiceField(
				queryset= c,
				label="",
				empty_label=None,
				widget = forms.Select(attrs={
									'class':"d-none"})				
	)
	class Meta:
		model 	= Type_measure
		fields	= [
			'type_measure'
		]

class Create_measure_point_form(forms.ModelForm):

	number 	=forms.IntegerField(
				label="Numero",
				required=True,
				widget=forms.NumberInput(attrs={
							'class':'form-control',
							'placeholder':'#Punt de mesura'
				})
	)
	name 		= forms.CharField(
						max_length=50,
						label="Nom",
						required=True,
						widget=forms.TextInput(attrs={
							'class':'form-control',
							'placeholder':'Aixeta...',
							})
						)
	area 		= forms.ModelChoiceField(
							queryset=Area.objects.all(),
							required=False,
							label = "Zona",
							widget = forms.Select(attrs={
								'class':"form-control",
							})
				)
	type_measure 		= forms.ModelMultipleChoiceField(
							queryset=Type_measure.objects.all(),
							required=True,
							label = "Tipus",
							widget = forms.CheckboxSelectMultiple(attrs={
								'class':"form-check-input",
							})
				)

	class Meta:
		model 	= Measure_point
		fields	= [
			'number',
			'name',
			'area',
			'type_measure'
		]

class Create_area_form(forms.ModelForm):

	area 	= forms.CharField(
						max_length=50,
						label="Zona",
						required=True,
						widget=forms.TextInput(attrs={
							'class':'form-control',
							'placeholder':'area...',
							})
						)
	class Meta:
		model 	= Area
		fields	= [
			'area'
		]

class Delete_area_form(forms.ModelForm):


	class Meta:
		model 	= Area
		fields	= [
			
		]