# rosrun orb_slam Mono_Inertial \
#   ~/orbslam/orb_slam/data/orb_vocab.txt \
#   ~/orbslam/orb_slam/data/mav0_all_sensor.yaml

# rosrun orb_slam Mono_Inertial \
#   ~/orbslam/orb_slam/data/orb_vocab.txt \
#   ~/orbslam/orb_slam/data/roahmlab_caminfo.yaml \
#   /imu \
#   /rgb/image_raw

rosrun orb_slam RGBD \
  ~/orbslam/orb_slam/data/orb_vocab.txt \
  ~/orbslam/orb_slam/data/roahmlab_caminfo_v2.yaml \
  /rgb/image_raw \
  /depth_to_rgb/image_raw

# rosrun orb_slam RGBD \
#   ~/orbslam/orb_slam/data/orb_vocab.txt \
#   ~/orbslam/orb_slam/data/fetch_caminfo.yaml \
#   /fetch_habitat/head/color/image_raw \
#   /fetch_habitat/head/depth/image_raw

#### RQT RECONFIGURE