import numpy as np
from src.simcore.atmosphere import isa_density

G = 9.71 # in units of m/s^2
def derivatives(state, t, drag_coeff=0.02, thrust_n=0, burn_time_s=0, dry_mass_kg=1.0, propellant_mass_kg=0.0):
    x, y, vx, vy = state
    speed = np.sqrt(vx**2 + vy**2)
    rho = isa_density(y)
    rho0 = isa_density(0)  # sea-level reference
    density_ratio = rho / rho0

    # Calculate mass and thrust based on burn time
    if t < burn_time_s and burn_time_s > 0:
        mass = dry_mass_kg + propellant_mass_kg * (1 - t / burn_time_s)
        thrust = thrust_n
    else:
        mass = dry_mass_kg
        thrust = 0

    # Calculate directional thrust components
    if speed > 0:
        thrust_x = thrust * (vx / speed) / mass
        thrust_y = thrust * (vy / speed) / mass 
    else:
        thrust_x, thrust_y = 0, 0

    # Calculate drag force components
    drag_x = -drag_coeff * density_ratio * speed * vx
    drag_y = -drag_coeff * density_ratio * speed * vy

    ax = drag_x + thrust_x
    ay = drag_y + thrust_y - 9.81

    return np.array([vx, vy, ax, ay])

def rk4_step(state, t, dt, drag_coeff=0.02, thrust_n=0.0,
             burn_time_s=0.0, dry_mass_kg=1.0, propellant_mass_kg=0.0):
    """Single classical RK4 step."""    
    args = (drag_coeff, thrust_n, burn_time_s, dry_mass_kg, propellant_mass_kg)

    k1 = derivatives(state,               t,          *args)
    k2 = derivatives(state + 0.5*dt*k1,   t + 0.5*dt, *args)
    k3 = derivatives(state + 0.5*dt*k2,   t + 0.5*dt, *args)
    k4 = derivatives(state +     dt*k3,   t +     dt, *args)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate(v0, angle_deg, dt=0.01, drag_coeff=0.02,
             thrust_n=0.0, burn_time_s=0.0,
             dry_mass_kg=1.0, propellant_mass_kg=0.0):
    """
    Integrate the trajectory until the projectile hits the ground (y < 0).

    Returns
    -------
    ts, xs, ys : ndarrays
    """    
    angle = np.radians(angle_deg)
    state = np.array([0.0, 0.0,
                      v0 * np.cos(angle),
                      v0 * np.sin(angle)])
    t = 0.0
    ts, xs, ys = [t], [state[0]], [state[1]] # initialize time and position lists
    while state[1] >= 0: # continue until the projectile hits the ground
        state = rk4_step(state, t, dt,
                         drag_coeff=drag_coeff,
                         thrust_n=thrust_n,
                         burn_time_s=burn_time_s,
                         dry_mass_kg=dry_mass_kg,
                         propellant_mass_kg=propellant_mass_kg)
        t += dt # increment time
        ts.append(t) # store time
        xs.append(state[0]) # store x position
        ys.append(state[1]) # store y position
    return np.array(ts), np.array(xs), np.array(ys)