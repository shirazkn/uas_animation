Animating a UAS in Gazebo using time-series data generated through Python/Matlab simulations
Requires: ros1-noetic, Gazebo11. I couldn't get ros1/2 to work on MacOSX but works fine on Ubuntu (and presumably Mojave).

1. Use `catkin build` inside workspace directory. (Needs some dependency that doesn't come with ros)
2. Source the setup `. ./devel/setup.<shell>`
3. `roslaunch visnet visnet.launch`  (I need to rename this...)
