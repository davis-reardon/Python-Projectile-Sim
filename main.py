import yaml
from src.simcore.projectile import simulate

with open("config.yaml") as f:
    config = yaml.safe_load(f)

params = config["simulation"]
t, x, y = simulate(
    v0=params["v0"],
    angle_deg=params["angle_deg"],
    dt=params["dt"],
    drag_coeff=params["drag_coeff"]
)

print(f"Maximum height: {max(y):.2f} m")
print(f"Range: {x[-1]:.2f} m")
print(f"Time of flight: {t[-1]:.2f} s")
