def trunc_coordinates(coordinates):
	"""
	This function truncates longitude and latitude coordinates of a user's
	location.

	Inputs:
		- coordinates: a tuple (longitude, latitude)

	Outputs:
		- coordinates: a tuple (longitude, latitude) with values truncated

	"""
	l = []
	for coordinate in coordinates:
		l.append('%.3f'%(coordinate))
	new_coordinates = tuple(l)
	return new_coordinates
