import csv

TELEMETRY_COLUMNS = ["t_s", "x_m", "y_m", "east_m", "north_m", "up_m"]


def write_telemetry_csv(filepath, t, x, y, east, north, up):
    """
    Write simulation telemetry to CSV.
    All inputs are 1D arrays of equal length.
    Columns: t_s, x_m, y_m, east_m, north_m, up_m
    """
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(TELEMETRY_COLUMNS)
        for row in zip(t, x, y, east, north, up):
            writer.writerow(row)