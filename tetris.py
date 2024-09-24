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

#formato das pecas
formas = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]
#criar classe das pecas
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
#colisao
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

#desenhos da grade
    for i in range(altura_grade):
        for j in range(largura_grade):
            pygame.draw.rect(tela, branco, (j*tamanho_bloco, i*tamanho_bloco, tamanho_bloco, tamanho_bloco), 1)
            if grade[i][j] != 0:
                pygame.draw.rect(tela, cores[grade[i][j]], (j*tamanho_bloco+1, i*tamanho_bloco+1, tamanho_bloco-2, tamanho_bloco-2))
    
    #pontuacao
    font = pygame.font.SysFont('comicsans', 30)
    texto_pontuacao = font.render(f'Pontuação: {pontuacao}', 1, branco)
    tela.blit(texto_pontuacao, (10, 10))
    
    pygame.display.update()

def desenhar_fim_jogo(tela, pontuacao):
    tela.fill(preto)
    font_grande = pygame.font.SysFont('comicsans', 50)
    font_pequena = pygame.font.SysFont('comicsans', 30)
    
    texto_fim = font_grande.render('Fim de Jogo', 1, vermelho)
    texto_pontuacao = font_pequena.render(f'Pontuação Final: {pontuacao}', 1, branco)
    texto_recomecar = font_pequena.render('Pressione R para Recomeçar', 1, verde)
    texto_sair = font_pequena.render('Pressione Q para Sair', 1, vermelho)
    
    tela.blit(texto_fim, (largura/2 - texto_fim.get_width()/2, 200))
    tela.blit(texto_pontuacao, (largura/2 - texto_pontuacao.get_width()/2, 300))
    tela.blit(texto_recomecar, (largura/2 - texto_recomecar.get_width()/2, 400))
    tela.blit(texto_sair, (largura/2 - texto_sair.get_width()/2, 450))
    
    pygame.display.update()

def jogo():
    peca_travada = {}
    grade = criar_grade(peca_travada)
    mudar_peca = False
    rodando = True
    peca_atual = Peca(5, 0)
    clock = pygame.time.Clock()
    tempo_queda = 0
    velocidade_queda = 0.30
    pontuacao = 0

    while rodando:
        grade = criar_grade(peca_travada)
        tempo_queda += clock.get_rawtime()
        clock.tick()

        if tempo_queda/1000 > velocidade_queda:
            tempo_queda = 0
            peca_atual.y += 1
            if colide(grade, peca_atual):
                peca_atual.y -= 1
                mudar_peca = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    peca_atual.x -= 1
                    if colide(grade, peca_atual):
                        peca_atual.x += 1
                if evento.key == pygame.K_RIGHT:
                    peca_atual.x += 1
                    if colide(grade, peca_atual):
                        peca_atual.x -= 1
                if evento.key == pygame.K_DOWN:
                    peca_atual.y += 1
                    if colide(grade, peca_atual):
                        peca_atual.y -= 1
                if evento.key == pygame.K_UP:
                    peca_atual.rodar()
                    if colide(grade, peca_atual):
                        peca_atual.rodar()  

        forma_pos = formas[peca_atual.tipo][peca_atual.rotacao]
        for i, pos in enumerate(forma_pos):
            x, y = peca_atual.x + pos % 4, peca_atual.y + pos // 4
            if y > -1:
                grade[y][x] = peca_atual.cor

        if mudar_peca:
            for pos in forma_pos:
                p = (peca_atual.x + pos % 4, peca_atual.y + pos // 4)
                peca_travada[p] = peca_atual.cor
            peca_atual = Peca(5, 0)
            mudar_peca = False
            
            linhas_removidas = limpar_linhas(grade, peca_travada)
            pontuacao += linhas_removidas * 100

            if colide(grade, peca_atual):
                rodando = False

        desenhar_janela(tela, grade, pontuacao)

    return pontuacao

def main():
    rodando = True
    while rodando:
        pontuacao_final = jogo()
        fim_jogo = True
        
        while fim_jogo:
            desenhar_fim_jogo(tela, pontuacao_final)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    fim_jogo = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        fim_jogo = False
                    if evento.key == pygame.K_q:
                        rodando = False
                        fim_jogo = False

    pygame.quit()

if __name__ == "__main__":
    main()
