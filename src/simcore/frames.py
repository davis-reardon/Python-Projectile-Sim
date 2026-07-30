import numpy as np

def range_to_enu(x, y, az_deg):
    """
    Convert range coordinates (x, y) to East-North-Up (ENU) coordinates
    given a launch azimuth angle.

    Parameters:
    x : downrange distance (m)
    y : altitude (m)
    az_deg : launch azimuth, compass bearing, 0=North, 90=East

    Returns:
    E, N, U : East, North, Up components (m)
    """
    az_rad = np.radians(az_deg)
    E = x * np.sin(az_rad)
    N = x * np.cos(az_rad)
    U = y
    return E, N, U