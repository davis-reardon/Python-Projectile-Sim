from src.simcore.projectile import simulate
t, x, y = simulate(v0 = 30, angle_deg = 45)

print(f"Max height: {y.max():.2f} m")
print(f"Range: {x[-1]:.2f} m")
print(f"Time of flight: {t[-1]:.2f} s")