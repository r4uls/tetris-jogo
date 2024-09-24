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
    def imagem(self):
        return formas[self.tipo][self.rotacao]

    def rodar(self):
        self.rotacao = (self.rotacao + 1) % len(formas[self.tipo])
def criar_grade(peca_travada):
    grade = [[0 for _ in range(largura_grade)] for _ in range(altura_grade)]

    for i in range(altura_grade):
        for j in range(largura_grade):
            if (j, i) in peca_travada:
                c = peca_travada[(j, i)]
                grade[i][j] = c
    return grade

def colide(grade, peca):
    forma = formas[peca.tipo][peca.rotacao]
    for i, pos in enumerate(forma):
        linha = peca.y + pos // 4
        coluna = peca.x + pos % 4
        if linha >= altura_grade or coluna < 0 or coluna >= largura_grade or (linha > -1 and grade[linha][coluna] != 0):
            return True
    return False

def limpar_linhas(grade, peca_travada):
    linhas_removidas = 0
    for i in range(len(grade)-1, -1, -1):
        if 0 not in grade[i]:
            linhas_removidas += 1
            for j in range(len(grade[i])):
                try:
                    del peca_travada[(j, i)]
                except:
                    continue

    if linhas_removidas > 0:
        for key in sorted(list(peca_travada), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < i:
                novo_key = (x, y + linhas_removidas)
                peca_travada[novo_key] = peca_travada.pop(key)

    return linhas_removidas

def desenhar_janela(tela, grade, pontuacao):
    tela.fill(preto)