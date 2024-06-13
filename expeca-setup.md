# Setup ExPECA

Deploy a cross traffic setup by following [this](https://github.com/KTH-EXPECA/examples/blob/main/crosstraffic.md).

Reserve worker-06 for the server
Reserve worker-09 and adv-router-07 for the client

Run server node
```
publicnet = chi.network.get_network("serverpublic")
edgenet = chi.network.get_network("edge-net")
container_name = "ros-latency-server-node"
chi.container.create_container(
    name = container_name,
    image = "bryandony/ros:melodic-voxblox-edge-expeca",
    reservation_id = worker_reservation_id,
    environment = {
        "DNS_IP":"8.8.8.8",
        "GATEWAY_IP":"130.237.11.97",
        "PASS":"expeca"
    },
    mounts = [],
    nets = [
        { "network" : publicnet['id'] },
        { "network" : edgenet['id'] },
    ],
    labels = {
        "networks.1.interface":"ens1f1",
        "networks.1.ip":"130.237.11.122/27",
        "networks.1.gateway":"130.237.11.97",
        "networks.2.interface":"eno12399np0",
        "networks.2.ip":"10.70.70.211/24",
        "networks.2.routes":"172.16.0.0/16-10.70.70.1",
        "capabilities.privileged":"true",
    },
)
chi.container.wait_for_active(container_name)
logger.success(f"created {container_name} container.")
```

ssh the server node and clone this repo.
```
ssh root@130.237.11.122
git clone https://github.com/samiemostafavi/ros-latency-pr3d.git
source /root/catkin_ws/devel/setup.bash
ros_master
roscore &
sleep 2
rostopic echo /head_front_camera/depth/color/points > /dev/null 2>&1 &
```

Run client node
```
publicnet = chi.network.get_network("serverpublic")
advnet = chi.network.get_network("adv-07-netw")
name = "ros-latency-client-node"
chi.container.create_container(
    name = name,
    image = "bryandony/ros:melodic-voxblox-edge-expeca",
    reservation_id = worker_reservation_id,
    environment = {"SERVER_DIR":"/tmp/"},
    nets = [
        { "network" : publicnet['id'] },
        { "network" : advnet['id'] },
    ],
    labels = {
        "networks.1.interface":"ens1",
        "networks.1.ip":"130.237.11.123/27",
        "networks.1.gateway":"130.237.11.97",
        "networks.2.interface":"eno12409",
        "networks.2.ip":"10.42.3.2/24",
        "networks.2.routes":"10.70.70.0/24-10.42.3.1",
        "capabilities.privileged":"true",
    },
)
chi.container.wait_for_active(name)
logger.success(f"created {name} container.")
```
Add the default route via console: `ip route add default via 130.237.11.97`.
Add nameserver via console: `echo nameserver 8.8.8.8 > /etc/resolv.conf`

ssh the client node and clone this repo.
```
ssh root@130.237.11.123
source /root/catkin_ws/devel/setup.bash
ros_slave 10.70.70.211
git clone https://github.com/samiemostafavi/ros-latency-pr3d.git
cd ros-latency-pr3d/
rosbag play -l ari_realsense_sample-2024-04-13-11-14-20.bag --topics /head_front_camera/depth/color/points
```





