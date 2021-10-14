ffmpeg -r 25 -i 'frames/default_drone_camera_1_camera_link_camera(1)-%4d.jpg' -c:v libx264 -vf fps=25 -pix_fmt yuv420p test_vid1.mp4
