import pygame
import random
import winsound

pygame.init()

ANCHO = 900
ALTO = 550
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Arcade Retro")

reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Arial", 35)

estado = "menu"

# ---------------- MENU ----------------
def dibujar_menu():
    t1 = fuente.render("MINI ARCADE RETRO", True, (255,255,255))
    t2 = fuente.render("1 - Atrapa la Estrella", True, (255,255,0))
    t3 = fuente.render("2 - Esquiva Obstaculos", True, (0,255,255))
    t4 = fuente.render("ESC - Salir", True, (255,100,100))

    pantalla.blit(t1, (260,120))
    pantalla.blit(t2, (280,230))
    pantalla.blit(t3, (280,290))
    pantalla.blit(t4, (340,400))

# ---------------- JUEGO 1 ----------------
jugador = pygame.Rect(430, 420, 40, 40)
estrella = pygame.Rect(
    random.randint(50, 800),
    random.randint(50, 350),
    30,
    30
)
puntos1 = 0

# ---------------- JUEGO 2 ----------------
jugador2 = pygame.Rect(430, 450, 50, 50)
obstaculos = []
puntos2 = 0
velocidad = 6

corriendo = True

while corriendo:
    reloj.tick(60)

    color = (
        (pygame.time.get_ticks()//7) % 255,
        (pygame.time.get_ticks()//5) % 255,
        (pygame.time.get_ticks()//3) % 255
    )
    pantalla.fill(color)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:

            if estado == "menu":
                if evento.key == pygame.K_1:
                    estado = "estrella"
                if evento.key == pygame.K_2:
                    estado = "esquivar"
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False

    teclas = pygame.key.get_pressed()

    # ---------- MENU ----------
    if estado == "menu":
        dibujar_menu()

    # ---------- ATRAPA LA ESTRELLA ----------
    elif estado == "estrella":

        if teclas[pygame.K_LEFT]:
            jugador.x -= 7
        if teclas[pygame.K_RIGHT]:
            jugador.x += 7
        if teclas[pygame.K_UP]:
            jugador.y -= 7
        if teclas[pygame.K_DOWN]:
            jugador.y += 7

        pygame.draw.rect(pantalla, (0,255,255), jugador)
        pygame.draw.circle(
            pantalla,
            (255,255,0),
            estrella.center,
            20
        )

        if jugador.colliderect(estrella):
            puntos1 += 1
            winsound.Beep(1000,100)

            estrella.x = random.randint(50,800)
            estrella.y = random.randint(50,400)

        nivel = "Facil"
        if puntos1 >= 5:
            nivel = "Medio"
        if puntos1 >= 10:
            nivel = "Dificil"

        txt = fuente.render(
            f"Puntos: {puntos1}   Nivel: {nivel}",
            True,
            (255,255,255)
        )
        pantalla.blit(txt,(20,20))

        volver = fuente.render(
            "M - Menu",
            True,
            (255,255,255)
        )
        pantalla.blit(volver,(20,70))

        if teclas[pygame.K_m]:
            estado = "menu"

    # ---------- ESQUIVAR ----------
    elif estado == "esquivar":

        if teclas[pygame.K_LEFT]:
            jugador2.x -= 8
        if teclas[pygame.K_RIGHT]:
            jugador2.x += 8

        if random.randint(1,25) == 1:
            obstaculos.append(
                pygame.Rect(
                    random.randint(0,850),
                    -50,
                    40,
                    40
                )
            )

        for o in obstaculos[:]:
            o.y += velocidad
            pygame.draw.rect(
                pantalla,
                (255,0,0),
                o
            )

            if o.y > 550:
                obstaculos.remove(o)
                puntos2 += 1
                winsound.Beep(700,60)

            if jugador2.colliderect(o):
                winsound.Beep(300,500)
                estado = "menu"
                puntos2 = 0
                obstaculos.clear()

        pygame.draw.rect(
            pantalla,
            (0,255,0),
            jugador2
        )

        nivel = "Facil"
        velocidad = 6

        if puntos2 >= 10:
            nivel = "Medio"
            velocidad = 9

        if puntos2 >= 20:
            nivel = "Dificil"
            velocidad = 12

        txt = fuente.render(
            f"Puntos: {puntos2}   Nivel: {nivel}",
            True,
            (255,255,255)
        )
        pantalla.blit(txt,(20,20))

        volver = fuente.render(
            "M - Menu",
            True,
            (255,255,255)
        )
        pantalla.blit(volver,(20,70))

        if teclas[pygame.K_m]:
            estado = "menu"

    pygame.display.update()

pygame.quit()