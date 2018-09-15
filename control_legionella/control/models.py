from django.db import models
from django.conf import settings
from datetime import date

User= settings.AUTH_USER_MODEL

class Area(models.Model):
	area				= models.CharField(max_length=50, null=False, unique=True, error_messages={'unique':"Ja existeix!"})
	weight 				= models.IntegerField(null=True, unique=False) 

	class Meta:
		verbose_name 		= 'Area'
		verbose_name_plural = 'Areas'
		ordering 			= ['weight','id']
	def __str__(self): return str(self.area)

class Type_measure(models.Model):
	type_measure		= models.CharField(max_length=50, null=True, unique=False)

	class Meta:
		verbose_name 		= 'Tipus de mesura'
		verbose_name_plural = 'Tipus de mesures'
	def __str__(self): return str(self.type_measure)



class Measure_point_group(models.Model):
	group 				= models.CharField(max_length=50, null=True, unique=True, error_messages={'unique':"Ja existeix!"})
	weight 				= models.IntegerField(null=True, unique=False) 

	class Meta:
		verbose_name 		= 'Group'
		verbose_name_plural = 'Groups'
		ordering 			= ['weight','id']
		
	def __str__(self): return str(self.group)




class Measure_point(models.Model):

	area				= models.ForeignKey(Area, null=True,on_delete=models.SET_NULL)
	group 				= models.ForeignKey(Measure_point_group, null=True,on_delete=models.SET_NULL)
	type_measure 		= models.ManyToManyField(Type_measure, blank=True)
	name 				= models.CharField(max_length=50, null=False, unique=False)
	number 				= models.IntegerField(null=False, unique=True)
	weight 				= models.IntegerField(null=True, unique=False)
	note 				= models.CharField(max_length=500, null=True, blank=True)


	class Meta:
		ordering 			= ['weight']
		verbose_name 		= 'Punt de mesura'
		verbose_name_plural = 'Punts de mesura'
	def __str__(self): return str(self.name)

	



class Measure(models.Model):

	temperature			= models.DecimalField(max_digits=3, decimal_places=1, null=True)
	chloride			= models.DecimalField(max_digits=2, decimal_places=1, null=True)
	measure_point		= models.ForeignKey(Measure_point, blank=False, null=False,on_delete=models.CASCADE)
	type_measure 		= models.ForeignKey(Type_measure, blank=False, null=False,on_delete=models.PROTECT)
	date_created		= models.DateTimeField(auto_now=False, auto_now_add=True, null=True)	
	date_modified		= models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
	user_created		= models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	status_OK 			= models.BooleanField()
	month				= models.IntegerField(null=False, unique=False)
	note 				= models.CharField(max_length=500, null=True, blank=True)

	class Meta:
		verbose_name		 	= 'Mesure'
		verbose_name_plural 	= 'Mesures'

	def __str__(self): return str(self.id)

