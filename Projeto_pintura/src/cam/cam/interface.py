import tkinter 
from tkinter import ttk 
import sv_ttk
import cv2
from PIL import Image, ImageTk
import time
import os, subprocess, re
import socket
import json
import threading as th
from datetime import datetime

janela = tkinter.Tk()
janela.title("Gerenciamento Darwini")

sv_ttk.set_theme("dark")

class functions():
    def ros(self):
        subprocess.call('ros2 run cam joy_sub', shell=True)
        
    def limp_tela(self):
        self.coord_e.delete(0,'end')
    
    def limp_tela2(self):
        self.alt_e.delete(0,'end')
        self.lar_e.delete(0,'end')
        
    def quit(self):
        self.janela.destroy()

    def salv_video(self):
        if self.estado.get():
            
            if self.com:
                self.counter = -75600
                self.clock = ttk.Label(self.cam_f, text="Iniciando")
                self.clock.place(relx = 0.8, rely = 0.9)
                tc = th.Thread(target=self.timer)
                tc.daemon
                tc.start()
                
                filename = time.strftime("%Y%m%d-%H%M%S")
                if os.path.isdir('/home/'+self.user+'/Documents/Galeria'): 
                    self.out = cv2.VideoWriter("/home/"+self.user+"/Documents/Galeria/video"+filename+".avi",cv2.VideoWriter_fourcc(*'MJPG'), 20.0, (640,480))
                else :
                    os.mkdir('/home/'+self.user+'/Documents/Galeria')
                    self.out = cv2.VideoWriter("/home/"+self.user+"/Documents/Galeria/video"+filename+".avi",cv2.VideoWriter_fourcc(*'MJPG'), 20.0, (640,480))
                self.com = False
            else:
                self.out.write(self.frame)

        elif not self.estado.get() and not self.com:
            self.out.release()
            self.clock.destroy()
            self.message_salv()
            self.gal()
            self.com = True
    
    def timer(self):
        if self.estado.get():
            self.counter += 1
            tt = datetime.fromtimestamp(self.counter)
            display = tt.strftime('%H:%M:%S')
            self.clock.config(text=display)
            self.clock.after(1000, self.timer)
    
    def env_mensagem(self):
        if self.coord_e.get():
            itens = self.coord_e.get()
            itens = re.sub('[(,)]',' ',itens)
            lst = [int(item) for item in itens.split()]    
            self.x, self.y = lst

        if self.alt_e.get() and self.lar_e.get():
            alt = int(self.alt_e.get())
            lar = int(self.lar_e.get()) 
            
        elif self.alt_e.get() or self.lar_e.get():
            mensagem = ttk.Label(self.aba1, text="Incompleto")
            mensagem.place(relx = 0.2, rely = 0.88)
            mensagem.after(1500, mensagem.destroy)               
        
    
    def open_camera(self): 
    
        # Capture the video frame by frame 
        _, self.frame = self.vid.read() 
        
        self.salv_video()
        
        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA) 
        
        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 
        
        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 
    
        # Displaying photoimage in the label 
        self.label_widget.photo_image = photo_image 
    
        # Configure image in the label 
        self.label_widget.configure(image=photo_image) 

        # Repeat the same process after every 10 seconds 
        self.label_widget.after(10, self.open_camera) 

    def salv_foto(self):
        filename = time.strftime("%Y%m%d-%H%M%S")
        if os.path.isdir('/home/'+self.user+'/Documents/Galeria'):
            cv2.imwrite("/home/"+self.user+"/Documents/Galeria/foto"+filename+".png", self.frame)
        else :
            os.mkdir('/home/'+self.user+'/Documents/Galeria')
            cv2.imwrite("/home/"+self.user+"/Documents/Galeria/foto"+filename+".png", self.frame)
        self.message_salv()
        self.gal()

    def open_file(self, event):
        cs = self.lbox.curselection()
        msge = self.lbox.get(cs[0])
        #open("/home/"+self.user+"/Documents/Galeria/"+msge)
        subprocess.call(('xdg-open', "/home/"+self.user+"/Documents/Galeria/"+msge))
        #plt.imshow(mpimg.imread("/home/"+self.user+"/Documents/Galeria/"+msge))
        #plt.show()
    
    def leitura_controle(self):
        while True:
            self.conn.send(b' ')
            data = json.loads(self.conn.recv(1024).decode())
            self.bots = data.get("bots")
            self.joys = data.get("joys")
    
    def message_salv(self):
        mensagem = ttk.Label(self.cam_f, text="Salvo")
        mensagem.place(relx = 0.8, rely = 0.9)
        mensagem.after(1500, mensagem.destroy)
        
    def at_proj(self): 
        while True:
            self.block = [True, True, True, True]
            if self.rect:
                for a in self.rect:
                    if self.x <= self.canvas.coords(a)[2] and self.x >= self.canvas.coords(a)[0]:
                        if self.y-1 == self.canvas.coords(a)[3]:
                            self.block[0] = False
                        if self.y+1 == self.canvas.coords(a)[1]:
                            self.block[1] = False
                    if self.y <= self.canvas.coords(a)[3] and self.y >= self.canvas.coords(a)[1]:
                        if self.x-1 == self.canvas.coords(a)[2]:
                            self.block[2] = False
                        if self.x+1 == self.canvas.coords(a)[0]:
                            self.block[3] = False

                    
            
            if self.block[0] and (self.bots[1] == 1 or self.joys[1] > 0.5):
                self.y = self.y-1
            elif self.block[1] and (self.bots[2] == 1 or self.joys[1] < -0.5):
                self.y = self.y+1

            if self.block[2] and (self.bots[3] == 1 or self.joys[0] > 0.5):
                self.x = self.x-1
            elif self.block[3] and (self.bots[4] == 1 or self.joys[0] < -0.5):
                self.x = self.x+1

            
            x_atual, y_atual, _, _ = self.canvas.coords(self.esfera)
            
            if self.bots[0] == 1 :
                self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill='blue')
            
            self.canvas.move(self.esfera, self.x - x_atual-10, self.y - y_atual-10)
            
            for linha in self.linhas:
                self.canvas.coords(linha, self.x, self.y, self.canvas.coords(linha)[2], self.canvas.coords(linha)[3])

    def callback0(self,e):
        if self.click:
            coord_x = e.x
            coord_y = e.y
            if coord_x < self.coordx_i:
                if coord_y < self.coordy_i: 
                    self.canvas.coords(self.ret, coord_x, coord_y, self.coordx_i, self.coordy_i)                
                else:
                    self.canvas.coords(self.ret, coord_x, self.coordy_i, self.coordx_i, coord_y)
            else:
                if coord_y < self.coordy_i: 
                    self.canvas.coords(self.ret, self.coordx_i, coord_y, coord_x, self.coordy_i)                
                else:
                    self.canvas.coords(self.ret, self.coordx_i, self.coordy_i, coord_x, coord_y)
    
    def callback1(self,e):
        if self.click:
            coordx_f = e.x
            coordy_f = e.y
            self.click = False
            self.rect.append(self.canvas.create_rectangle(self.canvas.coords(self.ret), outline='red'))
            self.canvas.delete(self.ret)
           
        else:
            self.coordx_i = e.x
            self.coordy_i = e.y
            self.ret = self.canvas.create_rectangle(self.coordx_i, self.coordy_i, self.coordx_i, self.coordy_i, outline='red')
            self.click = True   
    
    def callback2(self,e):
        if self.click:
            print(e)
            coordx_f = e.x
            coordy_f = e.y
            self.click = False
            self.rect.append(self.canvas.create_rectangle(self.canvas.coords(self.ret), outline='purple'))
            self.canvas.delete(self.ret)
           
        else:
            self.coordx_i = e.x
            self.coordy_i = e.y
            self.ret = self.canvas.create_rectangle(self.coordx_i, self.coordy_i, self.coordx_i, self.coordy_i, outline='purple')
            self.click = True 
    
    def undo(self):
        if self.rect:
            delet = self.rect.pop()
            self.canvas.delete(delet)
          
                
class aplication(functions):
    def __init__(self):
        try:
            self.i=0    
            self.start()
            self.janela = janela
            #self.janela.configure(background = 'gray')
            self.tela()
            self.menu()
            self.frames()
            t2 = th.Thread(target = self.proj)
            t2.daemon = True
            t2.start()
            self.abas()
            self.gal()
            self.widgets()
            janela.mainloop()
            
        except:
            self.quit()
    
    def start(self):
        self.user = os.environ.get('USER')
        self.estado = tkinter.BooleanVar()
        self.estado.set(False)
        self.com = True
        self.click = False
        self.rect = []
        self.rect2 = []

        self.x, self.y = 10,10
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 5555))
        s.listen(1)
        
        t0 = th.Thread(target = self.ros)
        t0.daemon = True
        t0.start()
        
        self.conn, _ = s.accept()

        t1 = th.Thread(target = self.leitura_controle)
        t1.daemon = True
        t1.start()
        
        self.bots = [0, 0, 0, 0, 0]
        self.joys = [0.0, 0.0]
            
    def tela(self):
        self.janela.geometry("1080x720")
        self.janela.resizable(True, True)
        self.janela.minsize(width=540, height = 360)
        
    def menu(self):
        menubar = tkinter.Menu(self.janela)
        self.janela.config(menu=menubar)
        menu_conf = tkinter.Menu(menubar)
        
        menubar.add_cascade(label = "Opções", menu= menu_conf)
        menu_conf.add_command(label= "Mudar Tema", command = sv_ttk.toggle_theme)
        menu_conf.add_command(label= "Sair", command = quit)
            
    def frames(self):
        self.proj_f = ttk.Frame(self.janela)
        self.proj_f.place(relx = 0.01, rely = 0.01, relwidth=0.48, relheight=0.98)
        
        self.canvas = tkinter.Canvas(self.proj_f, width=200, height=200)
        self.canvas.place(relx = 0, rely = 0, relwidth=1, relheight=1)
        
        self.cam_f = ttk.Frame(self.janela)
        self.cam_f.place(relx = 0.51, rely = 0.01, relwidth=0.48, relheight=0.48)
        
        self.vid = cv2.VideoCapture(0) 
        self.width, self.height = 640, 480
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height) 
        self.label_widget = ttk.Label(self.cam_f) 
        self.label_widget.place(relx = 0, rely = 0, relwidth=1, relheight=1)
        self.open_camera()
        
        self.dados_f = ttk.Frame(self.janela)
        self.dados_f.place(relx = 0.51, rely = 0.51, relwidth=0.48, relheight=0.48)
    
    def proj(self):
        self.canvas.create_rectangle(10, 10, 510, 580, fill='white')
        self.linhas = []
        for i, j in [(10, 10), (10, 580), (510, 10), (510, 580)]:
            self.canvas.create_rectangle(i - 5, j - 5, i + 5, j + 5, fill='blue')
            linha = self.canvas.create_line(510/2, 580/2, i, j, fill='gray')
            self.linhas.append(linha)
        self.esfera = self.canvas.create_oval(510/2 - 10, 580/2 - 10, 510/2 + 10, 580/2 + 10, fill='red') 
        self.at_proj()
         
    def abas(self):
        self.abas = ttk.Notebook(self.dados_f)
        self.aba1 = ttk.Frame(self.abas)
        self.aba2 = ttk.Frame(self.abas)
        self.aba3 = ttk.Frame(self.abas)
        self.abas.add(self.aba1, text = "Configurar")
        self.abas.add(self.aba2, text = "Dados")
        self.abas.add(self.aba3, text = "Galeria")
        self.abas.place(relx = 0, rely = 0, relwidth=1, relheight=1)
    
    def gal(self):
        flist = os.listdir('/home/'+self.user+'/Documents/Galeria')
        self.lbox = tkinter.Listbox(self.aba3)
        for item in flist:
            self.lbox.insert(tkinter.END, item)
        self.lbox.place(relx = 0, rely = 0, relwidth=1, relheight=1)
        
        self.reca_b = ttk.Button(self.aba3, text= "Recarregar", style="Accent.TButton", command = self.gal)
        self.reca_b.place(relx = 0.78, rely = 0.03, relwidth=0.2, relheight=0.1)
        
        self.lbox.bind('<Double-Button>', self.open_file)
        
    def widgets(self):
        #Botões
        self.enviar_coord_b = ttk.Button(self.proj_f, text= "Enviar", style="Accent.TButton", command=self.env_mensagem)
        self.enviar_coord_b.place(relx = 0.68, rely = 0.93, relwidth=0.15, relheight=0.05)
        
        self.limpar_coord_b = ttk.Button(self.proj_f, text= "Apagar", style="Accent.TButton", command = self.limp_tela)
        self.limpar_coord_b.place(relx = 0.84, rely = 0.93, relwidth=0.15, relheight=0.05)
        
        self.undo_b = ttk.Button(self.proj_f, text= "Undo", style="Accent.TButton", command = self.undo)
        self.undo_b.place(relx = 0.84, rely = 0.88, relwidth=0.15, relheight=0.04)
        
        self.foto_b = ttk.Button(self.cam_f, text= "Fotografar", style="Accent.TButton", command = self.salv_foto)
        self.foto_b.place(relx = 0.3, rely = 0.88, relwidth=0.2, relheight=0.1)
        
        self.video_b = ttk.Checkbutton(self.cam_f, text= "Filmar", style="Toggle.TButton",var = self.estado)
        self.video_b.place(relx = 0.51, rely = 0.88, relwidth=0.15, relheight=0.1)
        
        self.enviar_dim_b = ttk.Button(self.aba1, text= "Enviar", style="Accent.TButton", command=self.env_mensagem)
        self.enviar_dim_b.place(relx = 0.34, rely = 0.88, relwidth=0.15, relheight=0.1)
        
        self.limpar_dim_b = ttk.Button(self.aba1, text= "Apagar", style="Accent.TButton", command = self.limp_tela2)
        self.limpar_dim_b.place(relx = 0.51, rely = 0.88, relwidth=0.15, relheight=0.1)
        
        
        #Campos de escrita
        self.coord_n = ttk.Label(self.proj_f, text = "Coodenadas (x,y)")
        self.coord_n.place(relx = 0.025, rely = 0.9)
        self.coord_e = ttk.Entry(self.proj_f)
        self.coord_e.place(relx = 0.02, rely = 0.93, relwidth=0.65, relheight=0.05)
        
        self.alt_n = ttk.Label(self.aba1, text = "Altura")
        self.alt_n.place(relx = 0.015, rely = 0.1)
        self.alt_e = ttk.Entry(self.aba1)
        self.alt_e.place(relx = 0.01, rely = 0.17, relwidth=0.49, relheight=0.1)
        
        self.lar_n = ttk.Label(self.aba1, text = "Largura")
        self.lar_n.place(relx = 0.515, rely = 0.1)
        self.lar_e = ttk.Entry(self.aba1)
        self.lar_e.place(relx = 0.51, rely = 0.17, relwidth=0.49, relheight=0.1)
        
        #Mouse
        self.canvas.bind('<Motion>',self.callback0)
        self.canvas.bind('<Button-1>', self.callback1)
        self.canvas.bind('<Button-3>', self.callback2)
        
        #Teclado
        self.aba1.bind('Return', self.env_mensagem)
        
if __name__ == "__main__":    
    aplication()