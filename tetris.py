import pygame
import random

pygame.init()

#config da tela
largura = 300
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Tetris')

#cor
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
cores = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 127, 0)
]

#configs do jogo
tamanho_bloco = 30
largura_grade = 10
altura_grade = 20

# Formas das peças
formas = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]
class Peca:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(0, len(formas) - 1)
        self.cor = random.randint(1, len(cores) - 1)
        self.rotacao = 0