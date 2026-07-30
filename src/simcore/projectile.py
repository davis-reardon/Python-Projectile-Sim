import numpy as np
from src.simcore.atmosphere import isa_density
from src.simcore.grain import bates_burn_radius, bates_burn_area

G = 9.71  # in units of m/s^2

def derivatives(state, t, drag_coeff=0.02, thrust_n=0, burn_time_s=0,
                 dry_mass_kg=5.0, propellant_mass_kg=0, moment_of_inertia=0.1,
                 wind_accel_z=0.0, abort_time_s=None,
                 grain_inner_radius0_m=None, grain_outer_radius_m=None,
                 grain_burn_rate_m_s=None, grain_length_m=None,
                 thrust_per_area_n_m2=None, stability_coeff=0.0,
                 gimbal_angle_deg=0.0, moment_arm_m=0.1):
    x, y, z, vx, vy, vz, theta, omega = state
    speed = np.sqrt(vx**2 + vy**2 + vz**2)
    rho = isa_density(y)
    rho0 = isa_density(0)
    density_ratio = rho / rho0

    # Angle of attack: difference between body orientation and velocity direction
    velocity_angle = np.arctan2(vy, vx)
    aoa_raw = theta - velocity_angle
    aoa = np.arctan2(np.sin(aoa_raw), np.cos(aoa_raw))  # wrap to [-pi, pi]

    dynamic_pressure = 0.5 * rho * speed**2
    torque = -stability_coeff * dynamic_pressure * aoa
    alpha = torque / moment_of_inertia


    use_grain = grain_inner_radius0_m is not None

    if t < burn_time_s and burn_time_s > 0:
            mass = dry_mass_kg + propellant_mass_kg * (1 - t / burn_time_s)
            if use_grain:
                r = bates_burn_radius(t, grain_inner_radius0_m,
                                       grain_outer_radius_m, grain_burn_rate_m_s)
                area = bates_burn_area(r, grain_length_m)
                thrust = thrust_per_area_n_m2 * area
            else:
                thrust = thrust_n
    else:
            mass = dry_mass_kg
            thrust = 0

    aborted = abort_time_s is not None and t >= abort_time_s

    if aborted:
            thrust_x, thrust_y, thrust_z = 0.0, thrust / mass, 0.0
            gimbal_torque = 0.0
    else:
            thrust_angle = theta + np.radians(gimbal_angle_deg)
            thrust_x = thrust * np.cos(thrust_angle) / mass
            thrust_y = thrust * np.sin(thrust_angle) / mass
            thrust_z = 0.0
            gimbal_torque = thrust * moment_arm_m * np.sin(np.radians(gimbal_angle_deg))

    torque_total = torque + gimbal_torque
    alpha = torque_total / moment_of_inertia

    drag_x = -drag_coeff * density_ratio * speed * vx
    drag_y = -drag_coeff * density_ratio * speed * vy
    drag_z = -drag_coeff * density_ratio * speed * vz

    ax = drag_x + thrust_x
    ay = drag_y + thrust_y - 9.81
    az = drag_z + thrust_z + wind_accel_z

    return np.array([vx, vy, vz, ax, ay, az, omega, alpha])


def rk4_step(state, t, dt, drag_coeff=0.02, thrust_n=0.0,
             burn_time_s=0.0, dry_mass_kg=1.0, propellant_mass_kg=0.0,
             wind_accel_z=0.0, abort_time_s=None,
             grain_inner_radius0_m=None, grain_outer_radius_m=None,
             grain_burn_rate_m_s=None, grain_length_m=None,
             thrust_per_area_n_m2=None, stability_coeff=0.0,
             gimbal_angle_deg=0.0, moment_arm_m=0.1):
    """Single classical RK4 step."""
    args = (drag_coeff, thrust_n, burn_time_s, dry_mass_kg, propellant_mass_kg,
            0.1, wind_accel_z, abort_time_s,
            grain_inner_radius0_m, grain_outer_radius_m,
            grain_burn_rate_m_s, grain_length_m, thrust_per_area_n_m2,
            stability_coeff, gimbal_angle_deg, moment_arm_m)

    k1 = derivatives(state,               t,          *args)
    k2 = derivatives(state + 0.5*dt*k1,   t + 0.5*dt, *args)
    k3 = derivatives(state + 0.5*dt*k2,   t + 0.5*dt, *args)
    k4 = derivatives(state +     dt*k3,   t +     dt, *args)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


def simulate(v0, angle_deg, dt=0.01, drag_coeff=0.02,
             thrust_n=0.0, burn_time_s=0.0,
             dry_mass_kg=1.0, propellant_mass_kg=0.0,
             wind_accel_z=0.0,
             abort_command_time_s=None, command_latency_s=0.0,
             grain_inner_radius0_m=None, grain_outer_radius_m=None,
             grain_burn_rate_m_s=None, grain_length_m=None,
             thrust_per_area_n_m2=None, stability_coeff=0.0,
             gimbal_angle_deg=0.0, moment_arm_m=0.1):
    angle = np.radians(angle_deg)
    state = np.array([0.0, 0.0, 0.0,
                  v0 * np.cos(angle), v0 * np.sin(angle), 0.0,
                  angle, 0.1])  # x, y, z, vx, vy, vz, theta, omega
    t = 0.0
    ts, xs, ys, zs = [t], [state[0]], [state[1]], [state[2]]

    abort_time_s = None
    if abort_command_time_s is not None:
        abort_time_s = abort_command_time_s + command_latency_s

    aborted = False
    while state[1] >= 0:
        state = rk4_step(state, t, dt,
                         drag_coeff=drag_coeff,
                         thrust_n=thrust_n,
                         burn_time_s=burn_time_s,
                         dry_mass_kg=dry_mass_kg,
                         propellant_mass_kg=propellant_mass_kg,
                         wind_accel_z=wind_accel_z,
                         abort_time_s=abort_time_s,
                         grain_inner_radius0_m=grain_inner_radius0_m,
                         grain_outer_radius_m=grain_outer_radius_m,
                         grain_burn_rate_m_s=grain_burn_rate_m_s,
                         grain_length_m=grain_length_m,
                         thrust_per_area_n_m2=thrust_per_area_n_m2,
                         stability_coeff=stability_coeff,
                         gimbal_angle_deg=gimbal_angle_deg,
                         moment_arm_m=moment_arm_m)
        t += dt
        ts.append(t)
        xs.append(state[0])
        ys.append(state[1])
        zs.append(state[2])

        if abort_time_s is not None and t >= abort_time_s:
            aborted = True

        if aborted and state[4] <= 0:
            break

    return np.array(ts), np.array(xs), np.array(ys), np.array(zs), np.array(state[6])