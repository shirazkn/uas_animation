Animating a UAS in Gazebo using time-series data generated using Python/Matlab code (i.e. ignores ros physics)

Requires: ros1-noetic, Gazebo11. I couldn't get ros1/2 to work on MacOSX but works fine on Ubuntu (and presumably Mojave).

1. Use `catkin build` inside workspace directory. (Might need you to install additional dependency)
2. Source the setup `. ./devel/setup.<shell>`
3. `roslaunch animate animate.launch`

`catkin clean` reverts the build.
