#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Autor: Guyuehome (www.guyuehome.com)
@Descrição: exemplo de tópico ROS2 - inscreva-se no tópico de imagem
"""

import rclpy                            # Biblioteca de interface ROS2 Python
from rclpy.node import Node             # Classe de nó ROS2
from sensor_msgs.msg import Image       # Tipo de mensagem de imagem
from cv_bridge import CvBridge          # Classe de conversão de imagem ROS e OpenCV
import cv2                              # Biblioteca de processamento de imagem Opencv
import pyvirtualcam
import numpy as np
import threading as th
import time

frame = np.zeros((480, 640, 3), np.uint8)  # RGB
lock = th.Lock()

"""
Crie um nó de assinante
"""
class ImageSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)                                  # Inicialização da classe pai do nó ROS2
        self.sub = self.create_subscription(Image, 'image_raw', self.listener_callback, 5)     # Crie um objeto de assinante (tipo de mensagem, nome do tópico, função de retorno de chamada do assinante, comprimento da fila)
        self.cv_bridge = CvBridge()                             # Crie um objeto de conversão de imagem para converter imagens OpenCV e mensagens de imagem ROS entre si.
        
    def listener_callback(self, data):
        global frame, lock
        self.get_logger().info('Receiving video frame')         # Informações de log de saída, indicando que a função de retorno de chamada foi inserida
        image = self.cv_bridge.imgmsg_to_cv2(data, 'bgr8')      # Converta mensagens de imagem ROS em imagens OpenCV        
        lock.acquire()
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #frame=image
        lock.release()
        

def ros(args=None):
    rclpy.init(args=args)                                   # Inicialização da interface ROS2 Python
    node = ImageSubscriber("topic_webcam_sub")              # Crie um objeto de nó ROS2 e inicialize-o
    rclpy.spin(node)                                        # Loop aguardando a saída do ROS2
    node.destroy_node()                                     # Destruir objeto de nó
    rclpy.shutdown()                                        # Feche a interface ROS2 Python

def v_cam():
    global frame, lock
    with pyvirtualcam.Camera(width=640, height=480, fps=20) as cam:
        print(f'Using virtual camera: {cam.device}')
        while True:
            lock.acquire()
            cam.send(frame)
            lock.release()
            cam.sleep_until_next_frame()
      

    
def main(args=None):                                        # Função principal da entrada principal do nó ROS2
    t1 = th.Thread(target = ros)
    t2 = th.Thread(target = v_cam)
    t1.start()
    t2.start()
    
    
if __name__ == "__main__":
    main()
