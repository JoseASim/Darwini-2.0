Deve-se rodar o comando para iniciar o micro-ROS e substituir PORTA pela respectiva no arduino IDE

```sh
source install/local_setup.bash
ros2 run micro_ros_agent micro_ros_agent serial -D /dev/<PORTA>
```
