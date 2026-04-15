import pygame
import pygame.freetype
import sys
import random

# 1. Inicialização
pygame.init()
pygame.freetype.init()

# 2. Configurações da Janela
LARGURA = 800
ALTURA = 600
ecra = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Forca Cyber - Terminal de Acesso")

# 3. Cores Cyber
COR_FUNDO = (15, 15, 20)
VERDE_NEON = (57, 255, 20)
CIANO = (0, 255, 255)
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)
AMARELO = (255, 255, 0)

# 4. Fontes
fonte_titulo = pygame.freetype.SysFont('couriernew', 48, bold=True)
fonte_texto = pygame.freetype.SysFont('couriernew', 24, bold=True)
fonte_dica = pygame.freetype.SysFont('couriernew', 20, italic=True)

# 5. Banco de Dados Integrado
banco_empresarios = {
    "ELON MUSK": ["Magnata sul-africano.", "CEO da Tesla.", "Fundador da SpaceX."],
    "STEVE JOBS": ["Usava gola rolê preta.", "Revolucionou os smartphones.", "Cofundador da Apple."],
    "BILL GATES": ["Pioneiro do software para PCs.", "Ex-homem mais rico do mundo.", "Cofundador da Microsoft."],
    "SILVIO SANTOS": ["Começou como camelô.", "Dono do bordão 'Ma-oee!'.", "Fundador do SBT."]
}

relogio = pygame.time.Clock()

def sortear_palavra():
    palavra = random.choice(list(banco_empresarios.keys()))
    return palavra, banco_empresarios[palavra]

def executar_jogo():
    # Prepara a rodada
    palavra, dicas = sortear_palavra()
    letras_descobertas = [' ' if letra == ' ' else '_' for letra in palavra]
    tentativas = 6
    chutadas = []
    estado_jogo = "JOGANDO" # Controla se o jogador está jogando, ganhou ou perdeu

    a_correr = True
    while a_correr:
        ecra.fill(COR_FUNDO)

        # --- CAPTURA DE EVENTOS (Onde o teclado ganha vida!) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                a_correr = False
            
            # Deteta se uma tecla foi pressionada e o jogo não acabou
            if evento.type == pygame.KEYDOWN and estado_jogo == "JOGANDO":
                # Captura a letra digitada e converte para maiúscula
                letra = evento.unicode.upper()
                
                # Valida se é uma letra real e se ainda não foi testada
                if letra.isalpha() and letra not in chutadas:
                    chutadas.append(letra)
                    
                    if letra in palavra:
                        # Acertou! Revela a letra na tela
                        for i, l in enumerate(palavra):
                            if l == letra:
                                letras_descobertas[i] = letra
                        
                        # Verifica se descriptografou tudo
                        if '_' not in letras_descobertas:
                            estado_jogo = "VITORIA"
                    else:
                        # Errou! Reduz as tentativas
                        tentativas -= 1
                        if tentativas == 0:
                            estado_jogo = "DERROTA"

        # --- RENDERIZAÇÃO VISUAL ---
        
        # 1. Título
        texto_titulo = fonte_titulo.render("FORCA CYBER", CIANO)[0]
        ecra.blit(texto_titulo, (LARGURA//2 - texto_titulo.get_width()//2, 30))

        # 2. Palavra Oculta Dinâmica
        palavra_exibicao = " ".join(letras_descobertas)
        texto_alvo = fonte_titulo.render(palavra_exibicao, BRANCO)[0]
        ecra.blit(texto_alvo, (LARGURA//2 - texto_alvo.get_width()//2, 380))

        # 3. Letras já testadas
        texto_chutes = fonte_texto.render(f"Testadas: {', '.join(chutadas)}", CIANO)[0]
        ecra.blit(texto_chutes, (50, 480))

        # 4. Sistema de Dicas Progressivas
        dica_atual = f"> Dica 1: {dicas[0]}"
        if tentativas <= 4: dica_atual = f"> Dica 2: {dicas[1]}"
        if tentativas <= 2: dica_atual = f"> Dica CRÍTICA: {dicas[2]}"
        
        texto_dica = fonte_dica.render(dica_atual, VERDE_NEON)[0]
        ecra.blit(texto_dica, (50, 540))

        # 5. Contador de Falhas
        texto_erros = fonte_texto.render(f"Falhas Restantes: {tentativas}/6", VERMELHO)[0]
        ecra.blit(texto_erros, (50, 100))

        # 6. Telas Finais
        if estado_jogo == "VITORIA":
            msg = fonte_titulo.render("ACESSO CONCEDIDO!", VERDE_NEON)[0]
            ecra.blit(msg, (LARGURA//2 - msg.get_width()//2, 200))
        elif estado_jogo == "DERROTA":
            msg = fonte_titulo.render("SISTEMA BLOQUEADO!", VERMELHO)[0]
            ecra.blit(msg, (LARGURA//2 - msg.get_width()//2, 180))
            # Mostra qual era a palavra
            msg_alvo = fonte_texto.render(f"O alvo era: {palavra}", AMARELO)[0]
            ecra.blit(msg_alvo, (LARGURA//2 - msg_alvo.get_width()//2, 250))

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    executar_jogo()