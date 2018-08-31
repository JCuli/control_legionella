from django.core.exceptions import ValidationError
from .models import Measure_point


def validate_point(value):
	query = Measure_point.objects.filter(number= value)
	if not query:
		error_message ="Aquest punt de mesura no existeix"
		raise ValidationError(error_message)