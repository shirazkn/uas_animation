(cd ~ && ffmpeg -r 14 -i 'frames/default_drone_camera_1_camera_link_camera(1)-%4d.jpg' -c:v libx264 -vf fps=20 -pix_fmt yuv420p test_vid_both.mp4 -y)
(cd ~ && firefox test_vid_both.mp4)