import PySimpleGUI as sg
from tkinter import filedialog
import cv2


def getBiggerSize(img):
    if(img.shape[0] < img.shape[1]):
        return img.shape[0]
    else:
        return img.shape[1]
    


    
def cutImage(img, initial):
    w = img.shape[0]
    h = img.shape[1]
    if(w == h):
        return img
    if(h > w):
        img = img[0:initial+w,initial:initial+w]
    else:
        img = img[initial:initial+h,0:initial+h]
    
    return img
    

def printImage(image, time):
    cv2.imshow("imagem", image)
    key = cv2.waitKey(time)
    if key == 27:
        cv2.destroyAllWindows()
        return -1


def transformImageInBlackAndGray(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def putFilterBlackWhite(imagem, limiar):
    ret,imgT = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    #imgT = apply_brightness_contrast(imagem,brightness, contrast)
    return imgT
    
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def editImage(imagem, limiar):
    imagem = transformImageInBlackAndGray(imagem)
    imagem = putFilterBlackWhite(imagem, limiar)
    return imagem

class TelaPython():
    def __init__(self):
        #Layout
        layout = [
            [sg.Text("Escolha uma imagem quadrada de preferencia")],
            [sg.Button('Load image', key="loadImage")],  
            [sg.Text("W = 10000 H = 10000", key="textSizeImage",font = 'arial')], 
            [sg.Text("Pinos: ", key="pinos"),sg.Input(size=(10,0), key="pinosQtd", default_text="250")], 
            [sg.Text("iterações: ", key="iteracoes"),sg.Input(size=(10,0), key="iteracoesQtd", default_text="1800")],
            [sg.Text("Limiar: ", key="textContrast"),sg.Slider(range=(0,130),default_value = 80, orientation='h', key="sliderContrast",change_submits=True)],
            [sg.Text("Adjust: ", key="adjustImage"), sg.Slider(range=(0,255),default_value =0, orientation='h', key="sliderCutWidth",change_submits=True)],  
            [sg.Image(filename='', key='image')],   
            [sg.Button('OK')]
            
        ]
        #Janela
        self.janela = sg.Window('String art', finalize=True).layout(layout)
        
                
    def iniciar(self):
        
        while True: 
            self.events,self.values = self.janela.Read()
            if(self.events== "loadImage"):
                imagemPath = filedialog.askopenfilename()
                imagem = cv2.imread(imagemPath, 1)
               
                
                
                #self.janela["textLimiar"].update(visible=True)
                #self.janela["sliderContrast"].update(visible=True)
                #self.janela["sliderCutWidth"].update(visible=True)
                #self.janela["textSizeImage"].update(visible=True)
                #self.janela["adjustImage"].update(visible=True)
                self.janela["sliderCutWidth"].update(range=(0, abs(imagem.shape[0]-imagem.shape[1])))
                
                text = "W = {} H = {}".format(imagem.shape[1],imagem.shape[0])
                self.janela["textSizeImage"].update(value = text)
                
                imagemCrop = cutImage(imagem,0)
                imagemBG = transformImageInBlackAndGray(imagem)
                
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderContrast"])
                imagem = cutImage(imagem,getBiggerSize(imagem))
                imagem = cv2.resize(imagem, (500,500), 1.5,1.5,interpolation = cv2.INTER_CUBIC )
                
                #Essa parte é pra resolver um bug
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderContrast"])
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"]+1)) 
                imagem = cv2.resize(imagem, (500,500), 1.5,1.5,interpolation = cv2.INTER_CUBIC) 
                 
                imgbytes = cv2.imencode('.png', imagemBG)[1].tobytes()  # ditto 
                self.janela["image"].update(data=imgbytes)
                
                
            if (self.events == '-GRAPH-'):
                if mouse == (None, None):
                    continue 
                print(mouse[0], mouse[1])
            if(self.events == sg.WINDOW_CLOSED):
                break
            
            if(self.events == 'sliderContrast' or self.events == 'sliderBrightness'):
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderContrast"] )
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"]))
                imagem = cv2.resize(imagem, (500,500))  
                
            if(self.events == 'OK'):
                return [imagem, imagemPath,
                        self.values["pinosQtd"],
                        self.values['iteracoesQtd'],
                        self.values['sliderContrast']]
               
            if(self.events == "sliderCutWidth"):
                imagem = putFilterBlackWhite(imagemBG, self.values["sliderContrast"])
                imagem = cutImage(imagem,int(self.values["sliderCutWidth"])) 
                imagem = cv2.resize(imagem, (500,500)) 
            
            imgbytes = cv2.imencode('.png', imagem)[1].tobytes()  # ditto 
            self.janela["image"].update(data=imgbytes)  
              
            
            
                
               
                
            
def qtdBlack(image):
    size = image.shape
    qtd = 0
    for i in range(0,size[0]):
        for y in range(0,size[1]):
            if(image.item(i,y) == 0):
                qtd += 1
    return qtd

#tela = TelaPython()
#tela.iniciar()

print("done")
