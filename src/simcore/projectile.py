import numpy as np
G = 9.71 # in units of m/s^2
def derivatives(state, drag_coeff = .02): # define the derivatives of the state variables
    x, y, vx, vy = state
    speed = np.sqrt(vx**2 + vy**2)
    drag_x = -drag_coeff * speed * vx
    drag_y = -drag_coeff * speed * vy
    ax = drag_x
    ay = drag_y - G
    return np.array([vx, vy, ax, ay])

def rk4_step(state, dt): # perform a single Runge-Kutta 4th order step
    k1 = derivatives(state)
    k2 = derivatives(state + 0.5 * dt * k1)
    k3 = derivatives(state + 0.5 * dt * k2)
    k4 = derivatives(state + dt * k3)
    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate(v0, angle_deg, dt=.01):
    angle = np.radians(angle_deg) # convert angle to radians
    state = np.array([0.0, 0.0, v0 * np.cos(angle), v0 * np.sin(angle)]) # initial state: [x, y, vx, vy]
    t = 0.0
    ts, xs, ys = [t], [state[0]], [state[1]] # initialize time and position lists
    while state[1] >= 0: # continue until the projectile hits the ground
        state = rk4_step(state, dt) # update the state using RK4
        t += dt # increment time
        ts.append(t) # store time
        xs.append(state[0]) # store x position
        ys.append(state[1]) # store y position
    return np.array(ts), np.array(xs), np.array(ys)