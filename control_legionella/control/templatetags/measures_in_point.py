from django import template

register = template.Library()


@register.simple_tag
def measures_in_point(measures_qs, measure_point, type_measure, month):
    return measures_qs.filter(measure_point=measure_point, type_measure=type_measure, month=month)


@register.simple_tag
def add_to_counter(counter,reset):
	if reset == "reset":
		return 0
	else:
		if counter:
			return int(counter)+1
		else:
			return 1


@register.simple_tag
def filter_cell(measures_qs, j, t, month):
	
	cell_qs=[]
	cell_display=[]
	cell_hidden=[]
	for measure in measures_qs:
		if measure['measure_point_id'] == j and measure['type_measure_id'] == t  and measure['month'] == month:
			cell_qs.append(measure)
			# print("len:",len(cell_qs), cell_qs)
	if len(cell_qs)>2:
		cell_display=[cell_qs[-1]]
		cell_hidden= cell_qs[0:-1]
		cell=[cell_display,cell_hidden]
		# print(cell[1])
	elif len(cell_qs)==2:
		cell_display=[cell_qs[-1]]
		cell_hidden= [cell_qs[0]]
		cell=[cell_display,cell_hidden]
		# print(cell)
	elif len(cell_qs)==1:
		cell=[[cell_qs[0]],[]]
		# print(cell)
	else:
		cell=[[],[]]
	# print(cell)
	return cell

@register.simple_tag
def filter_cell_list(measures_qs, j, t):
	
	cell_qs=[]
	for measure in measures_qs:
		if measure['measure_point_id'] == j and measure['type_measure_id'] == t:
			cell_qs.append(measure)
			# print("len:",len(cell_qs), cell_qs)
	return cell_qs


				