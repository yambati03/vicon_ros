To run the Vicon publisher node, complete the following steps.
* First, build the `vicon` and `vicon_msgs` packages using `colon build --symlink-install`
* Make sure that Vicon Tracker is set up to publish a UDP object stream to `192.168.10.2:51001`
* Run `ros2 run vicon publish_vicon_update`. Updates will be published to the `/vicon` topic.