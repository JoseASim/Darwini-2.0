Deve-se executar os comandos

```sh
source install/local_setup.bash
colcon build --packages-select <PASTA>
ros2 run <PASTA> <CONSOLE_SCRIPT>
```
neste caso PASTA é a pasta em src e CONSOLE_SCRIPT é um dos descritos no arquino setup.py
