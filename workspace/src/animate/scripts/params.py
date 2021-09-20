from Simulations import Circle

# Note: Separate instances of this object are created
# for each ros node.

sim = Circle.Simulation(endtime=10)
drone_update_rate = 30
camera_update_rate = 10