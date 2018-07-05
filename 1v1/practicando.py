import pygame,sys



pygame.init()
juego=pygame.display.set_mode((360,360))
pygame.display.set_caption("Prueba")

claro=(120,120,120)
normal=(160,160,160)

#fuente=pygame.font.Font(None,40)
#texto=fuente.render("Ajedrez",0,(250,250,250))
#jugador=fuente.render("1 vs 1",0,(250,250,250),(120,120,120))
#compu=fuente.render("AI vs 1",0,(250,250,250,),(120,120,120))

def pagina_inicio():
    inicio=True
    while inicio:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
        fondo=pygame.image.load("fondo.jpg")
        posX,posY=0,0
        juego.blit(fondo,(posX,posY))
        fuente=pygame.font.Font(None,60)
        texto=fuente.render("Ajedrez",0,(250,250,250))
        juego.blit(texto,(110,50))
        mouse=pygame.mouse.get_pos()
        if 30+110>mouse[0]>30 and 140+55>mouse[1]>140:
            pygame.draw.rect(juego,claro,(30,140,110,55),0)
        else:
            pygame.draw.rect(juego,normal,(30,140,110,55),0)
        fuente2=pygame.font.Font(None,30)
        texto2=fuente2.render("1 vs 1",0,(250,250,250))
        juego.blit(texto2,(50,160))

        if 230+110>mouse[0]>230 and 140+55>mouse[1]>140:
            pygame.draw.rect(juego,claro,(230,140,110,55),0)
        else:
            pygame.draw.rect(juego,normal,(230,140,110,55),0)
        texto3=fuente2.render("1 vs AI",0,(250,250,250))
        juego.blit(texto3,(250,160))

        pygame.display.update()
def button(x,y,w,h,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0]==1 and action!=None:
            if action == "play":
                game_loop()
            elif action=="quit":
                pygame.quit()
#while True:
    #for i in pygame.event.get():
        #if i.type==QUIT:
         #   pygame.quit()
          #  sys.exit()
    #juego.blit(texto,(130,50))
    #juego.blit(jugador,(50,110))
    #juego.blit(compu,(230,110))
    #pygame.display.update()

pagina_inicio()
