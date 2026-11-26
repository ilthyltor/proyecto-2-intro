import pygame



anchoPanel = 190
altoBarra = 50
tamañoCelda = 20
fps = 60

colores = {
    0: (238, 240, 243),  # Aire
    1: (211, 177, 111),  # Arena
    2: (55, 133, 220),   # Agua
    3: (112, 119, 130),  # Piedra
}

elementos = [("Aire", 0), ("Arena", 1), ("Agua", 2), ("Piedra", 3)]


def crear_matriz(tamaño):

    matriz = []

    for y in range(tamaño):

        fila = []

        for x in range(tamaño):

            fila.append(0)

        matriz.append(fila)

    return matriz


def dibujar_boton(ventana, fuente, texto, rectangulo, activo=False):

    if activo:

        colorFondo = (80, 102, 135)

    else:

        colorFondo = (48, 57, 72)

    pygame.draw.rect(ventana, colorFondo, rectangulo, border_radius=5)
    imagen = fuente.render(texto, True, (245, 246, 249))
    x, y, ancho, alto = rectangulo
    ventana.blit(imagen, (x + 10, y + (alto - imagen.get_height()) // 2))


def obtener_celda(posicion, tamaño):

    x = (posicion[0] - anchoPanel) // tamañoCelda
    y = (posicion[1] - altoBarra) // tamañoCelda

    if posicion[0] < anchoPanel or posicion[1] < altoBarra:

        return None

    if x < 0 or y < 0 or x >= tamaño or y >= tamaño:

        return None

    return x, y


def dibujar(ventana, fuente, fuentePequena, matriz, tamaño, seleccionado, mensaje):

    ventana.fill((24, 28, 37))
    pygame.draw.rect(ventana, (37, 44, 57), (0, 0, ventana.get_width(), altoBarra))
    ventana.blit(fuente.render("SANDBOX", True, (245, 246, 249)), (14, 14))

    pygame.draw.rect(ventana, (31, 37, 48), (0, altoBarra, anchoPanel, ventana.get_height()))
    ventana.blit(fuente.render("Herramientas", True, (245, 246, 249)), (14, 65))

    for numero, (nombre, codigo) in enumerate(elementos):

        y = 98 + numero * 42

        # Dibujar botón
        pygame.draw.rect(
            ventana,
            (80, 102, 135) if seleccionado == codigo else (48, 57, 72),
            (12, y, anchoPanel - 24, 34),
            border_radius=5
        )

        # Dibujar icono de color
        pygame.draw.rect(ventana, colores[codigo], (21, y + 8, 18, 18))

        # Dibujar nombre del material separado del icono
        imagen = fuentePequena.render(nombre, True, (245, 246, 249))
        ventana.blit(
            imagen,
            (50, y + (34 - imagen.get_height()) // 2)
        )

    dibujar_boton(ventana, fuentePequena, "Reducir matriz (-10)",
                  (12, 290, anchoPanel - 24, 36))
    dibujar_boton(ventana, fuentePequena, "Aumentar matriz (+10)",
                  (12, 334, anchoPanel - 24, 36))
    dibujar_boton(ventana, fuentePequena, "Limpiar matriz",
                  (12, 378, anchoPanel - 24, 36))

    textoTamaño = "Tamaño: " + str(tamaño) + " x " + str(tamaño)
    ventana.blit(fuentePequena.render(textoTamaño, True, (224, 229, 238)), (15, 440))
    ventana.blit(fuentePequena.render("Clic izquierdo: dibujar", True, (177, 188, 204)), (15, 472))
    ventana.blit(fuentePequena.render("Clic derecho: borrar", True, (177, 188, 204)), (15, 494))

    for y in range(tamaño):

        for x in range(tamaño):

            codigo = matriz[y][x]
            rectangulo = (anchoPanel + x * tamañoCelda,
                          altoBarra + y * tamañoCelda,
                          tamañoCelda, tamañoCelda)
            pygame.draw.rect(ventana, colores[codigo], rectangulo)
            pygame.draw.rect(ventana, (205, 210, 218), rectangulo, 1)

    if mensaje != "":

        imagenMensaje = fuentePequena.render(mensaje, True, (31, 35, 42))
        ventana.blit(imagenMensaje, (anchoPanel + 8, altoBarra + tamaño * tamañoCelda + 8))


def ejecutar():

    pygame.init()
    pygame.display.set_caption("Proyecto II")

    tamaño = 20
    matriz = crear_matriz(tamaño)
    ventana = pygame.display.set_mode((anchoPanel + tamaño * tamañoCelda,
                                       altoBarra + tamaño * tamañoCelda + 40))
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 18)
    fuentePequena = pygame.font.SysFont("Arial", 15)

    seleccionado = 1
    dibujando = False
    mensaje = "El mundo comienza lleno de aire."
    abierto = True

    while abierto:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                abierto = False

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:

                abierto = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1 and evento.pos[0] < anchoPanel:

                    y = evento.pos[1]

                    if 98 <= y < 98 + len(elementos) * 42:

                        seleccionado = elementos[(y - 98) // 42][1]

                    elif 290 <= y < 326 and tamaño > 20:

                        tamaño -= 10
                        matriz = crear_matriz(tamaño)
                        ventana = pygame.display.set_mode((anchoPanel + tamaño * tamañoCelda,
                                                           altoBarra + tamaño * tamañoCelda + 40))
                        mensaje = "Matriz nueva creada."

                    elif 334 <= y < 370 and tamaño < 100:

                        tamaño += 10
                        matriz = crear_matriz(tamaño)
                        ventana = pygame.display.set_mode((anchoPanel + tamaño * tamañoCelda,
                                                           altoBarra + tamaño * tamañoCelda + 40))
                        mensaje = "Matriz nueva creada."

                    elif 378 <= y < 414:

                        matriz = crear_matriz(tamaño)
                        mensaje = "Matriz limpiada."

                elif evento.button == 1:

                    celda = obtener_celda(evento.pos, tamaño)

                    if celda is not None:

                        matriz[celda[1]][celda[0]] = seleccionado
                        dibujando = True

                elif evento.button == 3:

                    celda = obtener_celda(evento.pos, tamaño)

                    if celda is not None:

                        matriz[celda[1]][celda[0]] = 0

            elif evento.type == pygame.MOUSEMOTION and dibujando:

                celda = obtener_celda(evento.pos, tamaño)

                if celda is not None:

                    matriz[celda[1]][celda[0]] = seleccionado

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:

                dibujando = False

        dibujar(ventana, fuente, fuentePequena, matriz, tamaño, seleccionado, mensaje)
        pygame.display.flip()
        reloj.tick(fps)

    pygame.quit()


if __name__ == "__main__":

    ejecutar()
