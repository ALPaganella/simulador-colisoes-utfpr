#Arthur Leonel Paganella
#simulador de colisões fisica 1 (estilo mesa de sinuca)
#estou usando a biblioteca pygame (recomendaação do PETECO)
import pygame
import math

#Classe Bola
class Bola:
    def __init__(self, x, y, vx, vy, r, massa, cor):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.raio = r
        self.massa = massa
        self.cor = cor

#métodos:

    #atualiza posição da bola (na verdade a bola não se movimenta
    # e sim uma imagem é sobreposta a outra num intervalo de dt em dt
    # com as posçiões atualizadas)
    def atualizar_posicao(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    #colisão com a parede
    def colisao_parede(self, largura_janela, altura_janela):

        #se x - raio < 0 então inverte componente x da velocidade
        if self.x - self.raio < 0:
            self.x = self.raio
            self.vx *= -1

        #se x + raio > largura da janela então inverte componente x da velocidade
        elif self.x + self.raio > largura_janela:
            self.x = largura_janela - self.raio
            self.vx *= -1

        #analogo para y
        if self.y - self.raio < 0:
            self.y = self.raio
            self.vy *= -1
        elif self.y + self.raio > altura_janela:
            self.y = altura_janela - self.raio
            self.vy *= -1

    #colisão bola bola 2D
    def colisao_particula(self, outra_particula):

        #calculando módulo do vetor definido pela posição das bolas (distancia entre as bolas)
        dx = outra_particula.x - self.x
        dy = outra_particula.y - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        #se distancia <= soma dos raios então colisão
        if distancia <= (self.raio + outra_particula.raio):

            #separando a velocidade em componentes para calcular vx e vy separadamente

            # Vetor normal
            nx = dx / distancia
            ny = dy / distancia

            # Vetor tangencial
            tx = -ny
            ty = nx

            # Projeção das velocidades nos vetores normal e tangencial
            dp_n1 = self.vx * nx + self.vy * ny
            dp_t1 = self.vx * tx + self.vy * ty

            dp_n2 = outra_particula.vx * nx + outra_particula.vy * ny
            dp_t2 = outra_particula.vx * tx + outra_particula.vy * ty

            # Cálculo das novas velocidades normais após a colisão
            m1 = self.massa
            m2 = outra_particula.massa

            vn1_final = (dp_n1 * (m1 - m2) + 2 * m2 * dp_n2) / (m1 + m2)
            vn2_final = (dp_n2 * (m2 - m1) + 2 * m1 * dp_n1) / (m1 + m2)

            # Recombina as componentes de velocidade
            self.vx = vn1_final * nx + dp_t1 * tx
            self.vy = vn1_final * ny + dp_t1 * ty

            outra_particula.vx = vn2_final * nx + dp_t2 * tx
            outra_particula.vy = vn2_final * ny + dp_t2 * ty

            # Correção da sobreposição
            overlap = (self.raio + outra_particula.raio) - distancia
            self.x -= overlap * nx * 0.5
            self.y -= overlap * ny * 0.5
            outra_particula.x += overlap * nx * 0.5
            outra_particula.y += overlap * ny * 0.5

#referencias: manual de colisões do PETECO
# Inicialização do Pygame
pygame.init()

# Definição das dimensões da janela (mesa de sinuca)
largura, altura = 800, 500
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulador de Sinuca Elástica")

# Definindo o FPS e criando o Clock
FPS = 60
clock = pygame.time.Clock()

# Cores
VERDE_SINUCA = (0, 140, 70)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
AZUL = (0, 0, 255)
VERDE_ESQUISITO = (0, 255, 255)

# Variáveis para as bolas (bolas iguais)
raio_bola = 15 
massa_bola = 1

lista_bolas = []

#pedi para ia posicionar as bolas numa posição legal
# Posição inicial da primeira bola do triângulo
inicio_x_triangulo = largura * 0.7
inicio_y_triangulo = altura / 2

# Criando as bolas do triângulo (15 bolas para uma mesa completa)
# Posição aproximada do triângulo:
# Linha 1: 1 bola
# Linha 2: 2 bolas
# Linha 3: 3 bolas
# Linha 4: 4 bolas
# Linha 5: 5 bolas

offset_y = raio_bola * math.sqrt(3) # Distância vertical entre as linhas do triângulo
offset_x = raio_bola * 2 # Distância horizontal entre as bolas na mesma linha

# Linha 1
lista_bolas.append(Bola(inicio_x_triangulo, inicio_y_triangulo, 0, 0, raio_bola, massa_bola, VERMELHO)) # Bola principal do triângulo

# Linha 2
lista_bolas.append(Bola(inicio_x_triangulo + raio_bola, inicio_y_triangulo - raio_bola, 0, 0, raio_bola, massa_bola, AMARELO))
lista_bolas.append(Bola(inicio_x_triangulo + raio_bola, inicio_y_triangulo + raio_bola, 0, 0, raio_bola, massa_bola, AZUL))

# Linha 3
lista_bolas.append(Bola(inicio_x_triangulo + offset_x, inicio_y_triangulo - offset_y, 0, 0, raio_bola, massa_bola, VERDE_ESQUISITO))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x, inicio_y_triangulo, 0, 0, raio_bola, massa_bola, PRETO)) # Bola 8
lista_bolas.append(Bola(inicio_x_triangulo + offset_x, inicio_y_triangulo + offset_y, 0, 0, raio_bola, massa_bola, VERMELHO))

# Linha 4
lista_bolas.append(Bola(inicio_x_triangulo + offset_x + raio_bola, inicio_y_triangulo - offset_y - raio_bola, 0, 0, raio_bola, massa_bola, AMARELO))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x + raio_bola, inicio_y_triangulo - raio_bola, 0, 0, raio_bola, massa_bola, AZUL))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x + raio_bola, inicio_y_triangulo + raio_bola, 0, 0, raio_bola, massa_bola, VERMELHO))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x + raio_bola, inicio_y_triangulo + offset_y + raio_bola, 0, 0, raio_bola, massa_bola, AMARELO))

# Linha 5
lista_bolas.append(Bola(inicio_x_triangulo + offset_x * 2, inicio_y_triangulo - offset_y * 2, 0, 0, raio_bola, massa_bola, AZUL))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x * 2, inicio_y_triangulo - offset_y, 0, 0, raio_bola, massa_bola, VERMELHO))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x * 2, inicio_y_triangulo, 0, 0, raio_bola, massa_bola, AMARELO))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x * 2, inicio_y_triangulo + offset_y, 0, 0, raio_bola, massa_bola, AZUL))
lista_bolas.append(Bola(inicio_x_triangulo + offset_x * 2, inicio_y_triangulo + offset_y * 2, 0, 0, raio_bola, massa_bola, VERMELHO))
#fim do posicionamento

# Criando a bola "branca"
# Ela terá uma velocidade inicial alta                        massa_bola
bola_branca = Bola(largura * 0.25, altura / 2, 600, 0, raio_bola, 1, BRANCO) # Velocidade alta em X
lista_bolas.append(bola_branca)

#referencias: manual de colisões do PETECO
# Variável de controle do loop principal
run = True

# Loop principal (conforme manual do PETECO)
while run:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    janela.fill(VERDE_SINUCA)

    for i, particula1 in enumerate(lista_bolas):
        particula1.atualizar_posicao(dt)
        particula1.colisao_parede(largura, altura)

        for j, particula2 in enumerate(lista_bolas):
            if i < j:
                particula1.colisao_particula(particula2)

        pygame.draw.circle(janela, particula1.cor, (int(particula1.x), int(particula1.y)), particula1.raio)

    pygame.display.update()

pygame.quit()
