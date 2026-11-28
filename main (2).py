import pygame

anchoPanel = 190
altoBarra = 50
tamañoCelda = 20
fps = 60

#Variables para colores
porGrupo = 4 #botones visibles en el panel
yElementos = 98 #donde empiezan los botones de elementos
yMenu = yElementos + porGrupo * 42 #botón que abre el menú emergente

colores = {
    0: (238, 240, 243),  # Aire
    1: (211, 177, 111),  # Arena
    2: (55, 133, 220),   # Agua
    3: (112, 119, 130),  # Piedra
    4: (90, 70, 50),  # Tierra
    5: (200, 120, 40),  # Fuego
    6: (220, 200, 170),  # Semilla
    7: (170, 210, 40),  # Pasto
    8: (70, 170, 70),  # Planta1
    9: (40, 140, 40),  # Planta2
    10: (10, 110, 10), # Planta3
    11: (120, 60, 120), # Animal
}

elementos = [("Aire", 0), ("Arena", 1), ("Agua", 2), ("Piedra", 3),
             ("Tierra", 4), ("Fuego", 5), ("Semilla", 6), ("Pasto", 7),
             ("Planta1", 8), ("Planta2", 9), ("Planta3", 10), ("Animal", 11)]

anchoBoton = 130
rectsMenu = []
for n in range(len(elementos)):
    columna, fila = divmod(n, porGrupo)
    rectsMenu.append(pygame.Rect(anchoPanel + 14 + columna * (anchoBoton + 8),
                                 yElementos + fila * 42,
                                 anchoBoton, 34))
rectFondoMenu = rectsMenu[0].unionall(rectsMenu).inflate(16, 16)
rectBotonMenu = pygame.Rect(12, yMenu, anchoPanel - 24, 34)

def crear_matriz(tamaño):
    matriz = []
    for y in range(tamaño):
        fila = []
        for x in range(tamaño):
            fila.append(0)
        matriz.append(fila)
    return matriz

def tamaño_ventana(tamaño):
    ancho = max(anchoPanel + tamaño * tamañoCelda, anchoPanel + 3 * (anchoBoton + 8) + 20)
    alto = max(altoBarra + tamaño * tamañoCelda + 40, 570)
    return ancho, alto

def dibujar_boton(ventana, fuente, texto, rectangulo, activo=False):
    if activo:
        colorFondo = (80, 102, 135)
    else:
        colorFondo = (48, 57, 72)
    pygame.draw.rect(ventana, colorFondo, rectangulo, border_radius=5)
    imagen = fuente.render(texto, True, (245, 246, 249))
    x, y, ancho, alto = rectangulo
    ventana.blit(imagen, (x + 10, y + (alto - imagen.get_height()) // 2))

def dibujar_elemento(ventana, fuentePequena, nombre, codigo, rect, activo):
    #Botón con icono de color + nombre (se usa en el panel y en el menú).
    pygame.draw.rect(ventana, (80, 102, 135) if activo else (48, 57, 72),
                     rect, border_radius=5)
    pygame.draw.rect(ventana, colores[codigo], (rect.x + 9, rect.y + 8, 18, 18))
    imagen = fuentePequena.render(nombre, True, (245, 246, 249))
    ventana.blit(imagen, (rect.x + 38, rect.y + (rect.height - imagen.get_height()) // 2))
    
def obtener_celda(posicion, tamaño):
    x = (posicion[0] - anchoPanel) // tamañoCelda
    y = (posicion[1] - altoBarra) // tamañoCelda
    if posicion[0] < anchoPanel or posicion[1] < altoBarra:
        return None
    if x < 0 or y < 0 or x >= tamaño or y >= tamaño:
        return None
    return x, y

def dibujar(ventana, fuente, fuentePequena, matriz, tamaño, seleccionado, mensaje, grupo, menuAbierto):
    ventana.fill((24, 28, 37))
    pygame.draw.rect(ventana, (37, 44, 57), (0, 0, ventana.get_width(), altoBarra))
    ventana.blit(fuente.render("SANDBOX", True, (245, 246, 249)), (14, 14))
    pygame.draw.rect(ventana, (31, 37, 48), (0, altoBarra, anchoPanel, ventana.get_height()))
    ventana.blit(fuente.render("Herramientas", True, (245, 246, 249)), (14, 65))
    # Los 4 elementos del grupo actual
    for i in range(porGrupo):
        nombre, codigo = elementos[grupo * porGrupo + i]
        rect = pygame.Rect(12, yElementos + i * 42, anchoPanel - 24, 34)
        dibujar_elemento(ventana, fuentePequena, nombre, codigo, rect, seleccionado == codigo)

    # Botón que abre el menú
    dibujar_boton(ventana, fuentePequena, "Menú  (" + str(grupo + 1) + "/3)",
                  rectBotonMenu, menuAbierto)
    yBase = yMenu + 56
    dibujar_boton(ventana, fuentePequena, "Reducir matriz (-10)",
                  (12, yBase, anchoPanel - 24, 36))
    dibujar_boton(ventana, fuentePequena, "Aumentar matriz (+10)",
                  (12, yBase + 42, anchoPanel - 24, 36))
    dibujar_boton(ventana, fuentePequena, "Limpiar matriz",
                  (12, yBase +84, anchoPanel - 24, 36))

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
    
    # Menú emergente: se dibuja de último para quedar encima de todo
    if menuAbierto:
        pygame.draw.rect(ventana, (31, 37, 48), rectFondoMenu, border_radius=8)
        pygame.draw.rect(ventana, (80, 102, 135), rectFondoMenu, 2, border_radius=8)
        for n, rect in enumerate(rectsMenu):
            nombre, codigo = elementos[n]
            dibujar_elemento(ventana, fuentePequena, nombre, codigo, rect, seleccionado == codigo)


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
    grupo = 0 #0 = 0-3, 1 = 4-7, 2 = 8-11
    menuAbierto = False
    dibujando = False
    mensaje = "El mundo comienza lleno de aire."
    abierto = True

    while abierto:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                abierto = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                abierto = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and menuAbierto:
                if evento.button == 1:
                    for n, rect in enumerate(rectsMenu):
                        if rect.collidepoint(evento.pos):
                            grupo = n // porGrupo
                            seleccionado = elementos[n][1]
                            break
                menuAbierto = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:

                if evento.button == 1 and evento.pos[0] < anchoPanel:

                    y = evento.pos[1]
                    yBase = yMenu + 56

                    if yElementos <= y < yElementos + porGrupo * 42:
                        seleccionado = elementos[grupo * porGrupo + (y - yElementos) // 42][1]

                    elif rectBotonMenu.collidepoint(evento.pos):
                        menuAbierto = True
                    elif yBase <= y < yBase + 36 and tamaño > 20:
                        tamaño -= 10
                        matriz = crear_matriz(tamaño)
                        ventana = pygame.display.set_mode(tamaño_ventana(tamaño))
                        mensaje = "Matriz nueva creada."

                    elif yBase + 44 <= y < yBase + 80 and tamaño < 100:
                        tamaño += 10
                        matriz = crear_matriz(tamaño)
                        ventana = pygame.display.set_mode(tamaño_ventana(tamaño))
                        mensaje = "Matriz nueva creada."

                    elif yBase + 88 <= y < yBase + 124:
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
                
        dibujar(ventana, fuente, fuentePequena, matriz, tamaño, seleccionado, mensaje, grupo, menuAbierto)
        
        pygame.display.flip()
        
        reloj.tick(fps)
        
    pygame.quit()

if __name__ == "__main__":
    ejecutar()
