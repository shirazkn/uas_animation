from Simulations import Circle, TimeSeries

SLOWDOWN_FACTOR = 3.0
GHOST_STOP_TIME = 34.5  # Debug high value

# Note: Separate instances of this object are created
# for each ros node.

# sim = Circle.Simulation(endtime=10)
sim = TimeSeries.Simulation(filename='data_rkf_rpy.obj', offset=[53, 4, -5], slowdown_factor=SLOWDOWN_FACTOR)

# TimeSeries files: 'data_rkf.obj'

drone_update_rate = 500
ghost_update_rate = 20
camera_update_rate = 20