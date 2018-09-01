from django import template

register = template.Library()


@register.simple_tag
def measures_in_point(measures_qs, measure_point, type_measure, quarter):
    return measures_qs.filter(measure_point=measure_point, type_measure=type_measure, quarter=quarter)




    # {% measures_in_point measures_qs measure_point type_measure quarter %}