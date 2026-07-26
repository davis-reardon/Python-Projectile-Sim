import yaml
from src.simcore.projectile import simulate

with open("config.yaml") as f:
    config = yaml.safe_load(f)

sim_params = config["simulation"]
prop_params = config["propulsion"]

t, x, y = simulate(
    v0=sim_params["v0"],
    angle_deg=sim_params["angle_deg"],
    dt=sim_params["dt"],
    drag_coeff=sim_params["drag_coeff"],
    thrust_n=prop_params["thrust_n"],
    burn_time_s=prop_params["burn_time_s"],
    dry_mass_kg=prop_params["dry_mass_kg"],
    propellant_mass_kg=prop_params["propellant_mass_kg"]
)

print(f"Maximum height: {max(y):.2f} m")
print(f"Range: {x[-1]:.2f} m")
print(f"Time of flight: {t[-1]:.2f} s")
