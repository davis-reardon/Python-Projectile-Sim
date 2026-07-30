import matplotlib.pyplot as plt
from src.simcore.projectile import simulate

t, x, y, z, theta = simulate(v0=50, angle_deg=45, thrust_n=500,
                               burn_time_s=3.0, dry_mass_kg=5.0,
                               propellant_mass_kg=2.0, wind_accel_z=1.5)

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, z, y, linewidth=2)
ax.scatter(x[0], z[0], y[0], color='green', s=50, label='Launch')
ax.scatter(x[-1], z[-1], y[-1], color='red', s=50, label='Impact')

ax.set_xlabel('Downrange (m)')
ax.set_ylabel('Cross-range (m)')
ax.set_zlabel('Altitude (m)')
ax.set_title('Projectile Trajectory')
ax.view_init(elev=20, azim=-60)
ax.legend()

ax.view_init(elev=20, azim=-60)
plt.tight_layout()
plt.savefig('data/results/trajectory_3d.png', dpi=150)
print("Saved plot to data/results/trajectory_3d.png")
plt.show()