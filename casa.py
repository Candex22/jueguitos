import pygame
import sys
import random

pygame.init()

width, height = 720, 480
pantalla = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tateti')

fuente = pygame.font.Font(None, 28)


fondo_imagen = pygame.image.load("fondo.jpg")
fondo_imagen = pygame.transform.scale(fondo_imagen, (width * 2 // 3, height))

color_boton = (0, 200, 0)
color_boton_borde = (0, 150, 0)
color_fondo_marcador = (200, 200, 200)
color_texto_marcador = (0, 0, 0)
color_fondo_menú = (255, 255, 255)
color_texto_boton = (255, 255, 255)

class Tablero:
    def __init__(self):
        self.puntuacion_x = 0
        self.puntuacion_o = 0
        self.resetear()
        self.modo = None

    def resetear(self):
        self.tablero = [[None for _ in range(3)] for _ in range(3)]
        self.jugador_actual = 'X'
        self.juego_terminado = False
        self.ganador = None

    def dibujar_lineas(self):
        tablero_ancho = width * 2 // 3
        tablero_alto = height
        cuadro_ancho = tablero_ancho // 3
        inicio_x = 0
        inicio_y = 0

        pantalla.blit(fondo_imagen, (0, 0))

        pygame.draw.rect(pantalla, (255, 255, 255), (tablero_ancho, 0, width - tablero_ancho, height))

        for x in range(1, 3):
            pygame.draw.line(pantalla, (0, 0, 0), (inicio_x + x * cuadro_ancho, inicio_y),
                             (inicio_x + x * cuadro_ancho, inicio_y + tablero_alto), 5)
        for x in range(1, 3):
            pygame.draw.line(pantalla, (0, 0, 0), (inicio_x, inicio_y + x * (tablero_alto // 3)),
                             (inicio_x + tablero_ancho, inicio_y + x * (tablero_alto // 3)), 5)

        pygame.draw.line(pantalla, (0, 0, 0), (tablero_ancho, 0), (tablero_ancho, height), 5)

        self.dibujar_puntuacion()

    def dibujar_marcaciones(self):
        tablero_ancho = width * 2 // 3
        tablero_alto = height
        cuadro_ancho = tablero_ancho // 3
        inicio_x = 0
        inicio_y = 0

        for fila in range(3):
            for columna in range(3):
                x = inicio_x + columna * cuadro_ancho
                y = inicio_y + fila * (tablero_alto // 3)
                centro_x = x + cuadro_ancho // 2
                centro_y = y + (tablero_alto // 3) // 2
                radio = cuadro_ancho // 2 - 30

                if self.tablero[fila][columna] == 'X':
                    pygame.draw.line(pantalla, (0, 0, 255), (x + 20, y + 20),
                                     (x + cuadro_ancho - 20, y + (tablero_alto // 3) - 20), 7)
                    pygame.draw.line(pantalla, (0, 0, 255), (x + cuadro_ancho - 20, y + 20),
                                     (x + 20, y + (tablero_alto // 3) - 20), 7)
                elif self.tablero[fila][columna] == 'O':
                    pygame.draw.circle(pantalla, (255, 0, 0), (centro_x, centro_y),
                                       radio, 7)

        pygame.display.update()

    def dibujar_puntuacion(self):
        marcador_ancho = 280
        marcador_alto = 120
        marcador_x = width * 2 // 3 + 20
        marcador_y = 20

        pygame.draw.rect(pantalla, color_fondo_marcador, pygame.Rect(marcador_x - 10, marcador_y - 10, marcador_ancho + 20, marcador_alto + 20), border_radius=10)

        texto = fuente.render(f"Ta Te Ti!", True, color_texto_marcador)
        pantalla.blit(texto, (marcador_x + 10, marcador_y + 10))

        texto_x = fuente.render(f'Jugador X: {self.puntuacion_x}', True, color_texto_marcador)
        texto_o = fuente.render(f'Jugador O: {self.puntuacion_o}', True, color_texto_marcador)
        pantalla.blit(texto_x, (marcador_x + 10, marcador_y + 60))
        pantalla.blit(texto_o, (marcador_x + 10, marcador_y + 100))

        pygame.display.update()

    def hacer_movimiento(self, fila, columna):
        if not self.juego_terminado and self.tablero[fila][columna] is None:
            self.tablero[fila][columna] = self.jugador_actual
            self.ganador = self.verificar_ganador()
            if self.ganador:
                if self.ganador == 'X':
                    self.puntuacion_x += 1
                elif self.ganador == 'O':
                    self.puntuacion_o += 1
                self.juego_terminado = True
            elif self.esta_lleno():
                self.juego_terminado = True
            else:
                if self.modo == 'contra_maquina' and self.jugador_actual == 'X':
                    self.jugador_actual = 'O'
                    self.movimiento_maquina()
                else:
                    self.jugador_actual = 'O' if self.jugador_actual == 'X' else 'X'

    def verificar_ganador(self):
        for i in range(3):
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] and self.tablero[i][0] is not None:
                return self.tablero[i][0]
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] and self.tablero[0][i] is not None:
                return self.tablero[0][i]

        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] and self.tablero[0][0] is not None:
            return self.tablero[0][0]
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] and self.tablero[0][2] is not None:
            return self.tablero[0][2]

        return None

    def esta_lleno(self):
        return all(celda is not None for fila in self.tablero for celda in fila)

    def mostrar_mensaje(self, mensaje):
        pantalla.fill(color_fondo_menú)
        self.dibujar_lineas()
        self.dibujar_marcaciones()

        mensaje_ancho, mensaje_alto = 300, 80
        mensaje_rect = pygame.Rect((width - mensaje_ancho) // 2, height // 2 - 40, mensaje_ancho, mensaje_alto)
        pygame.draw.rect(pantalla, color_boton, mensaje_rect, border_radius=10)

        texto = fuente.render(mensaje, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=mensaje_rect.center)
        pantalla.blit(texto, texto_rect)

        self.dibujar_boton_reinicio()
        pygame.display.update()

    def dibujar_boton_reinicio(self):
        boton_ancho, boton_alto = 180, 50
        boton_rect = pygame.Rect((width - boton_ancho) // 2, height - boton_alto - 20, boton_ancho, boton_alto)
        pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=10)
        pygame.draw.rect(pantalla, color_boton_borde, boton_rect, width=2, border_radius=10)
        texto = fuente.render('Reiniciar', True, color_texto_boton)
        texto_rect = texto.get_rect(center=boton_rect.center)
        pantalla.blit(texto, texto_rect)

    def verificar_boton_reinicio(self, pos):
        boton_ancho, boton_alto = 180, 50
        boton_rect = pygame.Rect((width - boton_ancho) // 2, height - boton_alto - 20, boton_ancho, boton_alto)
        return boton_rect.collidepoint(pos)

    def dibujar_botones_modo(self):
        boton_ancho, boton_alto = 200, 40
        boton_2_jugadores = pygame.Rect((width * 2 // 3 + 20), height // 2 - 70, boton_ancho, boton_alto)
        pygame.draw.rect(pantalla, color_boton, boton_2_jugadores, border_radius=10)
        pygame.draw.rect(pantalla, color_boton_borde, boton_2_jugadores, width=2, border_radius=10)
        texto_2_jugadores = fuente.render('2 Jugadores', True, color_texto_boton)
        texto_rect_2_jugadores = texto_2_jugadores.get_rect(center=boton_2_jugadores.center)
        pantalla.blit(texto_2_jugadores, texto_rect_2_jugadores)

        boton_contra_maquina = pygame.Rect((width * 2 // 3 + 20), height // 2 - 10, boton_ancho, boton_alto)
        pygame.draw.rect(pantalla, color_boton, boton_contra_maquina, border_radius=10)
        pygame.draw.rect(pantalla, color_boton_borde, boton_contra_maquina, width=2, border_radius=10)
        texto_contra_maquina = fuente.render('Contra Máquina', True, color_texto_boton)
        texto_rect_contra_maquina = texto_contra_maquina.get_rect(center=boton_contra_maquina.center)
        pantalla.blit(texto_contra_maquina, texto_rect_contra_maquina)

        pygame.display.update()

    def verificar_boton_modo(self, pos):
        boton_ancho, boton_alto = 200, 40
        boton_2_jugadores = pygame.Rect((width * 2 // 3 + 20), height // 2 - 70, boton_ancho, boton_alto)
        boton_contra_maquina = pygame.Rect((width * 2 // 3 + 20), height // 2 - 10, boton_ancho, boton_alto)

        if boton_2_jugadores.collidepoint(pos):
            self.modo = 'dos_jugadores'
            self.resetear()
            return True
        elif boton_contra_maquina.collidepoint(pos):
            self.modo = 'contra_maquina'
            self.resetear()
            return True
        return False

    def movimiento_maquina(self):
        opciones = [(fila, columna) for fila in range(3) for columna in range(3) if self.tablero[fila][columna] is None]
        if opciones:
            fila, columna = random.choice(opciones)
            self.hacer_movimiento(fila, columna)

def main():
    tablero = Tablero()
    en_modo_seleccion = True

    while en_modo_seleccion:
        tablero.dibujar_botones_modo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if tablero.verificar_boton_modo(evento.pos):
                    en_modo_seleccion = False
                    tablero.dibujar_lineas()
                    tablero.dibujar_marcaciones()
                    tablero.dibujar_puntuacion()
                    tablero.dibujar_botones_modo()
                    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if tablero.juego_terminado:
                    if tablero.verificar_boton_reinicio(evento.pos):
                        tablero.resetear()
                        tablero.dibujar_lineas()
                        tablero.dibujar_marcaciones()
                        tablero.dibujar_puntuacion()
                    continue

                x, y = evento.pos
                tablero_ancho = width * 2 // 3
                cuadro_ancho = tablero_ancho // 3
                inicio_x = 0
                inicio_y = 0
                fila = (y - inicio_y) // (height // 3)
                columna = (x - inicio_x) // cuadro_ancho
                if 0 <= fila < 3 and 0 <= columna < 3:
                    tablero.hacer_movimiento(fila, columna)

                if tablero.juego_terminado:
                    if tablero.ganador:
                        tablero.mostrar_mensaje(f'¡Jugador {tablero.ganador} gana!')
                        print(f"Puntuación - X: {tablero.puntuacion_x}, O: {tablero.puntuacion_o}")
                    else:
                        tablero.mostrar_mensaje('¡Empate!')
                else:
                    tablero.dibujar_lineas()
                    tablero.dibujar_marcaciones()
                    tablero.dibujar_puntuacion()

        if tablero.modo == 'contra_maquina' and not tablero.juego_terminado and tablero.jugador_actual == 'O':
            tablero.movimiento_maquina()

        pygame.display.update()

main()