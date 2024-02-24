import subprocess
import time
import threading

def ler():
    while True:
        print("Rodando")
        time.sleep(0.5)
        
def ros():
    subprocess.call('ros2 run cam joy_sub', shell=True)

def main():
    t1 = threading.Thread(target=ros)
    t1.daemon
    t1.start()
    ler()

if __name__ == '__main__':
    main()
