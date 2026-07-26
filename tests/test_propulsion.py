from src.simcore.projectile import simulate

def test_thrust_increases_range():
    _, x_no_thrust, _ = simulate(v0=30, angle_deg=45, thrust_n=0)
    _, x_thrust, _ = simulate(v0=30, angle_deg=45, thrust_n=500, burn_time_s=2.0,
                                dry_mass_kg=5.0, propellant_mass_kg=2.0)
    assert x_thrust[-1] > x_no_thrust[-1]