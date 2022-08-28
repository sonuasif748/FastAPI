from math import sin, cos, sqrt, atan2, radians

def distancefinder(myloc, loc):
    R = 6373.0
    lat1 = radians(float(myloc[0]))
    lon1 = radians(float(myloc[1]))
    lat2 = radians(float(loc[0]))
    lon2 = radians(float(loc[1]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance