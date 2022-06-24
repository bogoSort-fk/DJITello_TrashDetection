import math
import re
R = 6371000

def distanceBearing(latitude, longitude, distance, bearing):

    latitude = math.radians(latitude)
    longitude = math.radians(longitude)
    angularD = distance / R
    latitude2 = math.asin(math.sin(latitude) * math.cos(angularD) + 
    math.cos(latitude) * math.sin(angularD) * math.cos(bearing))

    longitude2 = longitude + math.atan2(math.sin(bearing) * math.sin(angularD)
     * math.cos(latitude), math.cos(angularD) - math.sin(latitude) * math.sin(latitude2))

    dlongitude = longitude - longitude2
    y = math.sin(dlongitude) * math.cos(latitude)
    x = math.cos(latitude2) * math.sin(latitude) - math.sin(latitude2) * math.cos(latitude) * math.cos(dlongitude)
    z = math.atan2(y,x)
    
    finalBearing = math.degrees(z + math.pi)

    return round(math.degrees(latitude2), 7),  round(math.degrees(longitude2), 7)

def latlonDegreeConverter(longitude, latitude):

    # math.modf() splits whole number and decimal into tuple
    split_degx = math.modf(longitude)
    
    # the whole number [index 1] is the degrees
    degrees_x = int(split_degx[1])

    # split the whole number part of the total as the minutes: 20
    # abs() absoulte value - no negative
    minutes_x = abs(int(math.modf(split_degx[0] * 60)[1]))

    # multiply the decimal part of the split above by 60 to get the seconds
    # abs() absoulte value - no negative
    seconds_x = abs(round(math.modf(split_degx[0] * 60)[0] * 60,2))

    # repeat for latitude
    split_degy = math.modf(latitude)
    degrees_y = int(split_degy[1])
    minutes_y = abs(int(math.modf(split_degy[0] * 60)[1]))
    seconds_y = abs(round(math.modf(split_degy[0] * 60)[0] * 60,2))

    # account for E/W & N/S
    if degrees_x < 0:
        EorW = "W"
    else:
        EorW = "E"

    if degrees_y < 0:
        NorS = "S"
    else:
        NorS = "N"

    # abs() remove negative from degrees, was only needed for if-else above
    print(str(abs(degrees_x)) + u"\u00b0" + str(minutes_x) + "'" + str(seconds_x) + "\"" + EorW)
    print(str(abs(degrees_y)) + u"\u00b0" + str(minutes_y) + "'" + str(seconds_y) + "\"" + NorS)

def toDegree(var):
    split_degx = math.modf(var)
    
    # the whole number [index 1] is the degrees
    degrees_x = int(split_degx[1])

    # multiply the decimal part by 60: 0.3478 * 60 = 20.868
    # split the whole number part of the total as the minutes: 20
    # abs() absoulte value - no negative
    minutes_x = abs(int(math.modf(split_degx[0] * 60)[1]))

    seconds_x = abs(round(math.modf(split_degx[0] * 60)[0] * 60,2))

    return str(abs(degrees_x)) + u"\u00b0" + str(minutes_x) + "'" + str(seconds_x)