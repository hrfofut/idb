import math


def unbinary(s):
    """Removes the first two characters and the last character of a string, then adds necessary info for browser to see b64 image.
    Useful because encoding a binary to b64 adds "b'" to the front and "'" to the back.
    """
    return 'data:image/jpeg;base64,' + s[2:-1]


def real_dist(lat1, lng1, lat2, lng2):
    """
    Calculates distance between two co-ordinates and returns it in meters.
    """
    R = 6371e3  # metres
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lng2 - lng1)

    a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) * math.sin(Δλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c
    return d
