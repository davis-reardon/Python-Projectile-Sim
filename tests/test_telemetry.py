import csv
import os
import numpy as np
from src.simcore.telemetry import write_telemetry_csv, TELEMETRY_COLUMNS


def test_write_telemetry_csv(tmp_path):
    filepath = tmp_path / "telemetry.csv"
    t = np.array([0.0, 1.0])
    x = np.array([0.0, 100.0])
    y = np.array([0.0, 50.0])
    e = np.array([0.0, 0.0])
    n = np.array([0.0, 100.0])
    u = np.array([0.0, 50.0])

    write_telemetry_csv(filepath, t, x, y, e, n, u)

    with open(filepath) as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    assert header == TELEMETRY_COLUMNS
    assert len(rows) == 2
    assert rows[1] == ["1.0", "100.0", "50.0", "0.0", "100.0", "50.0"]