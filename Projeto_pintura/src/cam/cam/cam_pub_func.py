#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Autor: Guyuehome (www.guyuehome.com)
@Descrição: tópico ROS2 exemplo de publicação de imagem tópico
"""

import rclpy                        # Biblioteca de interface ROS2 Python
from rclpy.node import Node         # Classe de nó ROS2
from sensor_msgs.msg import Image   # Tipo de mensagem de imagem
from cv_bridge import CvBridge      # Classe de conversão de imagem ROS e OpenCV
import cv2                          # Biblioteca de processamento de imagem Opencv

"""
Crie um nó de editor
"""
class ImagePublisher(Node):

    def __init__(self, name):
        super().__init__(name)                                           # Inicialização da classe pai do nó ROS2
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)  #Criar objeto editor (tipo de mensagem, nome do tópico, comprimento da fila)
        self.timer = self.create_timer(0.1, self.timer_callback)         # Crie um cronômetro (período em segundos, função de retorno de chamada para execução agendada)
        self.cap = cv2.VideoCapture(2)                                   # Crie um objeto de captura de vídeo e conduza a câmera para capturar imagens (número do dispositivo da câmera)
        self.cv_bridge = CvBridge()                                      # Crie um objeto de conversão de imagem para converter posteriormente imagens OpenCV em mensagens de imagem ROS

    def timer_callback(self):
        ret, frame = self.cap.read()                                     # Leia as imagens quadro a quadro
        
        if ret == True:                                                  # Se a imagem for lida com sucesso
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame, 'bgr8'))             # Postar mensagem de imagem

        self.get_logger().info('Publishing video frame')                 # Informações de log de saída, indicando que a publicação do tópico de imagem foi concluída

def main(args=None):                                 # Função principal da entrada principal do nó ROS2
    rclpy.init(args=args)                            # Inicialização da interface ROS2 Python
    node = ImagePublisher("topic_webcam_pub")        # Crie um objeto de nó ROS2 e inicialize-o
    rclpy.spin(node)                                 # Loop aguardando a saída do ROS2
    node.destroy_node()                              # Destruir objeto de nó
    rclpy.shutdown()                                 # Feche a interface ROS2 Python

