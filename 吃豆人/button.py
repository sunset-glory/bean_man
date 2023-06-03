import pygame.font

class playbutton():
    def __init__(self,screen,text):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        #必要的按键参数
        self.width,self.height = 200.50
        self.buttoncolor = (0,255,0)
        self.textcolor = (255,255,255)
        self.font = pygame.font.SysFont(None,48)
        #按键居中显示
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self.presenttext(text)               #按键仅一次创建即可

    def presenttext(self, text):          #将文本显示在按钮中央
        self.text_image = self.font.render(text,True,self.textcolor,self.buttoncolor)
        self.text_image_rect = self.msg_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self.screen.fill(self.buttoncolor,self.rect)
        self.screen.blit(self.text_image,self.text_image_rect)
