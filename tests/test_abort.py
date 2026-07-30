from src.simcore.projectile import simulate

def test_abort():
    """After abort + latency, thrust should redirect vertical and the sim
    should terminate at apogee rather than continuing to ground impact."""
    _, x_normal, y_normal, _, _ = simulate(
        v0=50, angle_deg=45, thrust_n=500, burn_time_s=5.0,
        dry_mass_kg=5.0, propellant_mass_kg=3.0)

    _, x_abort, y_abort, _, _ = simulate(
        v0=50, angle_deg=45, thrust_n=500, burn_time_s=5.0,
        dry_mass_kg=5.0, propellant_mass_kg=3.0,
        abort_command_time_s=1.0, command_latency_s=0.2)

    # Aborted flight should end earlier (at apogee, y still > 0)
    assert y_abort[-1] > 0
    # Aborted flight should travel less downrange than the un-aborted one
    assert x_abort[-1] < x_normal[-1]