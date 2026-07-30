import numpy as np
from src.simcore.atmosphere import isa_density

G = 9.71  # in units of m/s^2

def derivatives(state, t, drag_coeff=0.02, thrust_n=0, burn_time_s=0,
                 dry_mass_kg=5.0, propellant_mass_kg=0, moment_of_inertia=0.1,
                 wind_accel_z=0.0):
    x, y, z, vx, vy, vz, theta, omega = state
    speed = np.sqrt(vx**2 + vy**2 + vz**2)
    rho = isa_density(y)
    rho0 = isa_density(0)
    density_ratio = rho / rho0
    torque = 0.0
    alpha = torque / moment_of_inertia

    if t < burn_time_s and burn_time_s > 0:
        mass = dry_mass_kg + propellant_mass_kg * (1 - t / burn_time_s)
        thrust = thrust_n
    else:
        mass = dry_mass_kg
        thrust = 0

    if speed > 0:
        thrust_x = thrust * (vx / speed) / mass
        thrust_y = thrust * (vy / speed) / mass
        thrust_z = thrust * (vz / speed) / mass
    else:
        thrust_x, thrust_y, thrust_z = 0, 0, 0

    drag_x = -drag_coeff * density_ratio * speed * vx
    drag_y = -drag_coeff * density_ratio * speed * vy
    drag_z = -drag_coeff * density_ratio * speed * vz

    ax = drag_x + thrust_x
    ay = drag_y + thrust_y - 9.81
    az = drag_z + thrust_z + wind_accel_z

    return np.array([vx, vy, vz, ax, ay, az, omega, alpha])


def rk4_step(state, t, dt, drag_coeff=0.02, thrust_n=0.0,
             burn_time_s=0.0, dry_mass_kg=1.0, propellant_mass_kg=0.0,
             wind_accel_z=0.0):
    """Single classical RK4 step."""
    args = (drag_coeff, thrust_n, burn_time_s, dry_mass_kg, propellant_mass_kg,
            0.1, wind_accel_z)

    k1 = derivatives(state,               t,          *args)
    k2 = derivatives(state + 0.5*dt*k1,   t + 0.5*dt, *args)
    k3 = derivatives(state + 0.5*dt*k2,   t + 0.5*dt, *args)
    k4 = derivatives(state +     dt*k3,   t +     dt, *args)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def simulate(v0, angle_deg, dt=0.01, drag_coeff=0.02,
             thrust_n=0.0, burn_time_s=0.0,
             dry_mass_kg=1.0, propellant_mass_kg=0.0,
             wind_accel_z=0.0):
    """
    Integrate the trajectory until the projectile hits the ground (y < 0).

    Returns
    -------
    ts, xs, ys, zs, theta_final : ndarrays / float
    """
    angle = np.radians(angle_deg)
    state = np.array([0.0, 0.0, 0.0,
                      v0 * np.cos(angle), v0 * np.sin(angle), 0.0,
                      0.0, 0.1])  # x, y, z, vx, vy, vz, theta, omega
    t = 0.0
    ts, xs, ys, zs = [t], [state[0]], [state[1]], [state[2]]
    while state[1] >= 0:
        state = rk4_step(state, t, dt,
                         drag_coeff=drag_coeff,
                         thrust_n=thrust_n,
                         burn_time_s=burn_time_s,
                         dry_mass_kg=dry_mass_kg,
                         propellant_mass_kg=propellant_mass_kg,
                         wind_accel_z=wind_accel_z)
        t += dt
        ts.append(t)
        xs.append(state[0])
        ys.append(state[1])
        zs.append(state[2])
    return np.array(ts), np.array(xs), np.array(ys), np.array(zs), np.array(state[6])