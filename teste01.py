import pygame
import pygame.freetype
import sys
import random
import os
import time

# ═══════════════════════════════════════════════════════════════════
#  JANELA
# ═══════════════════════════════════════════════════════════════════
LARGURA = 820
ALTURA  = 650

# ═══════════════════════════════════════════════════════════════════
#  PALETA — dark mode minimalista (inspirado em term.ooo)
# ═══════════════════════════════════════════════════════════════════
COR_FUNDO   = (18,  18,  19)
COR_SEP     = (58,  58,  60)
COR_TILE_BD = (86,  87,  88)    # borda tile vazio
COR_CERTO   = (83,  141, 78)    # verde — letra correta
COR_ERRADO  = (58,  58,  60)    # cinza escuro — letra errada
COR_KEY     = (129, 131, 132)   # tecla padrão
COR_TEXTO   = (255, 255, 255)
COR_SUTIL   = (129, 131, 132)
COR_FORCA_S = (68,  68,  78)    # estrutura da forca
COR_BONECO  = (185, 185, 200)   # boneco padrão
COR_PERIGO  = (214, 62,  62)    # vermelho — perigo/erro
COR_AVISO   = (200, 170, 50)    # amarelo — intermediário

# ═══════════════════════════════════════════════════════════════════
#  LAYOUT
# ═══════════════════════════════════════════════════════════════════
HDR_H  = 52
FORCA_Y = 62
WORD_Y  = 282
KBD_Y   = 432
KEY_W   = 52
KEY_H   = 48
KEY_GAP = 6
TECLADO = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

# ═══════════════════════════════════════════════════════════════════
#  REGRAS DE JOGO
# ═══════════════════════════════════════════════════════════════════
PONTOS_ACERTO   = 10
PONTOS_ERRO     = -5
BONUS_VITORIA   = 50
BONUS_TENTATIVA = 10
TENTATIVAS_POR_NIVEL = {"FACIL": 8, "MEDIO": 6, "DIFICIL": 4}
LETRAS_INICIAIS      = {"FACIL": 2, "MEDIO": 1, "DIFICIL": 0}

# ═══════════════════════════════════════════════════════════════════
#  EFEITOS VISUAIS
# ═══════════════════════════════════════════════════════════════════
FLASH_MS       = 200
BONECO_ANIM_MS = 450
DIGITACAO_MS   = 28

# ═══════════════════════════════════════════════════════════════════
#  ARQUIVOS
# ═══════════════════════════════════════════════════════════════════
ARQUIVO_PALAVRAS   = "palavras.txt"
ARQUIVO_RESULTADOS = "resultados.txt"


def _caminho(nome):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, nome)


def carregar_palavras():
    banco = {}
    try:
        with open(_caminho(ARQUIVO_PALAVRAS), 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith('#'):
                    continue
                partes = linha.split('|')
                if len(partes) < 5:
                    continue
                palavra = partes[0].strip().upper()
                dicas   = [partes[1].strip(), partes[2].strip(), partes[3].strip()]
                nivel   = partes[4].strip().upper()
                if nivel not in TENTATIVAS_POR_NIVEL:
                    nivel = "MEDIO"
                banco[palavra] = {"dicas": dicas, "nivel": nivel}
    except FileNotFoundError:
        banco = {
            "ELON MUSK":       {"dicas": ["Magnata sul-africano.", "CEO da Tesla.", "Fundador da SpaceX."],             "nivel": "MEDIO"},
            "BILL GATES":      {"dicas": ["Pioneiro do software.", "Ex-homem mais rico.", "Cofundador da Microsoft."],  "nivel": "FACIL"},
            "MARK ZUCKERBERG": {"dicas": ["Prodigio de Harvard.", "A Rede Social.", "Criou o Facebook."],              "nivel": "DIFICIL"},
            "SILVIO SANTOS":   {"dicas": ["Comecou como camelo.", "Bordao: Ma-oee!", "Fundador do SBT."],              "nivel": "FACIL"},
        }
    return banco


def salvar_resultado(nome, pontuacao, acertos, erros, tentativas, max_tent, palavra, venceu):
    t    = time.localtime()
    data = f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d} {t.tm_hour:02d}:{t.tm_min:02d}"
    res  = "VITORIA" if venceu else "DERROTA"
    linha = f"{data}|{nome}|{pontuacao}|{acertos}|{erros}|{tentativas}/{max_tent}|{palavra}|{res}\n"
    with open(_caminho(ARQUIVO_RESULTADOS), 'a', encoding='utf-8') as f:
        f.write(linha)


def carregar_historico():
    try:
        with open(_caminho(ARQUIVO_RESULTADOS), 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def sortear_palavra(banco):
    chave = random.choice(list(banco.keys()))
    return chave, banco[chave]["dicas"], banco[chave]["nivel"]


def revelar_iniciais(palavra, nivel):
    posicoes = [i for i, c in enumerate(palavra) if c.isalpha()]
    n = LETRAS_INICIAIS.get(nivel, 0)
    if n == 0 or not posicoes:
        return []
    return random.sample(posicoes, min(n, len(posicoes)))


def thresh(max_t, k):
    return (max_t * k + 5) // 6


def iniciar_som(vol=0.3):
    try:
        caminho = _caminho('musica_cyber.mp3')
        if os.path.exists(caminho):
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(vol)
            pygame.mixer.music.play(-1)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
def executar_jogo():
    pygame.init()
    pygame.freetype.init()

    ecra    = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Forca")
    relogio = pygame.time.Clock()

    # Fontes sans-serif limpas
    def _f(size, bold=False):
        for nome in ['helveticaneue', 'helvetica', 'arial', 'dejavusans']:
            try:
                return pygame.freetype.SysFont(nome, size, bold=bold)
            except Exception:
                pass
        return pygame.freetype.SysFont(None, size, bold=bold)

    F_TITULO = _f(28, bold=True)
    F_GRANDE = _f(24, bold=True)
    F_TEXTO  = _f(17, bold=True)
    F_DICA   = _f(14)
    F_PEQNA  = _f(12)
    F_KEY    = _f(14, bold=True)
    F_STATS  = _f(13)

    # ── helpers ────────────────────────────────────────────────────
    def blit(fonte, texto, cor, x, y):
        s = fonte.render(texto, cor)[0]
        ecra.blit(s, (x, y))
        return s.get_width()

    def blit_c(fonte, texto, cor, y):
        s = fonte.render(texto, cor)[0]
        ecra.blit(s, (LARGURA // 2 - s.get_width() // 2, y))

    def pulso_cor(cor, periodo_ms, min_v=50):
        t    = ticks % periodo_ms
        meio = periodo_ms // 2
        frac = (t / meio) if t < meio else ((periodo_ms - t) / meio)
        b    = int(min_v + (255 - min_v) * frac)
        return (b * cor[0] // 255, b * cor[1] // 255, b * cor[2] // 255)

    def linha_h(y, x0=0, x1=LARGURA, cor=COR_SEP):
        pygame.draw.line(ecra, cor, (x0, y), (x1, y), 1)

    # ── estado global ───────────────────────────────────────────────
    tela         = "MENU"
    nome_jogador = ""
    nome_input   = ""

    # ── estado de partida ───────────────────────────────────────────
    palavra          = ""
    dicas            = []
    nivel            = ""
    letras_desc      = []
    max_tent         = 6
    erros            = 0
    acertos_letras   = 0
    tentativas_total = 0
    chutadas         = []
    pontuacao        = 0
    estado           = "JOGANDO"

    # ── efeitos visuais ─────────────────────────────────────────────
    flash_timer       = 0
    flash_cor         = COR_CERTO
    boneco_anim_timer = 0
    boneco_nova_parte = -1
    dica_texto_alvo   = ""
    dica_chars_visto  = 0
    dica_ultimo_tick  = 0
    dica_idx_atual    = -1
    ticks  = 0
    volume = 0.3

    def mudar_volume(delta):
        nonlocal volume
        volume = max(0.0, min(1.0, round(volume + delta, 1)))
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass

    def parte_cor(idx, cor_base):
        if erros < thresh(max_tent, idx + 1):
            return None
        if boneco_nova_parte == idx and ticks - boneco_anim_timer < BONECO_ANIM_MS:
            prog = min(1.0, (ticks - boneco_anim_timer) / BONECO_ANIM_MS)
            r = int(255 + (cor_base[0] - 255) * prog)
            g = int(255 + (cor_base[1] - 255) * prog)
            b = int(255 + (cor_base[2] - 255) * prog)
            return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
        return cor_base

    def nova_partida():
        nonlocal palavra, dicas, nivel, letras_desc, max_tent
        nonlocal erros, acertos_letras, tentativas_total, chutadas, pontuacao, estado
        nonlocal flash_timer, boneco_anim_timer, boneco_nova_parte
        nonlocal dica_texto_alvo, dica_chars_visto, dica_ultimo_tick, dica_idx_atual

        palavra, dicas, nivel = sortear_palavra(banco)
        letras_desc      = [' ' if c == ' ' else '_' for c in palavra]
        max_tent         = TENTATIVAS_POR_NIVEL[nivel]
        erros            = 0
        acertos_letras   = 0
        tentativas_total = 0
        chutadas         = []
        pontuacao        = 0
        estado           = "JOGANDO"
        flash_timer       = 0
        boneco_anim_timer = 0
        boneco_nova_parte = -1
        dica_idx_atual    = 0
        dica_texto_alvo   = dicas[0]
        dica_chars_visto  = 0
        dica_ultimo_tick  = pygame.time.get_ticks()

        for i in revelar_iniciais(palavra, nivel):
            letras_desc[i] = palavra[i]

    # ── desenhadores de componentes ─────────────────────────────────
    def desenhar_forca():
        tent_rest = max_tent - erros
        pct_perigo = 1 - tent_rest / max_tent

        if pct_perigo >= 0.67:
            COR_B = COR_PERIGO
        elif pct_perigo >= 0.34:
            r = int(COR_BONECO[0] + (COR_PERIGO[0] - COR_BONECO[0]) * (pct_perigo - 0.34) / 0.33)
            g = int(COR_BONECO[1] + (COR_PERIGO[1] - COR_BONECO[1]) * (pct_perigo - 0.34) / 0.33)
            b = int(COR_BONECO[2] + (COR_PERIGO[2] - COR_BONECO[2]) * (pct_perigo - 0.34) / 0.33)
            COR_B = (max(0,min(255,r)), max(0,min(255,g)), max(0,min(255,b)))
        else:
            COR_B = COR_BONECO

        # Forca centralizada, proporções compactas
        cx = LARGURA // 2
        cy = FORCA_Y + 10

        # Estrutura (linhas finas 3px, cor sutil)
        pygame.draw.line(ecra, COR_FORCA_S, (cx - 65, cy + 205), (cx + 65, cy + 205), 3)  # base
        pygame.draw.line(ecra, COR_FORCA_S, (cx - 28, cy + 205), (cx - 28, cy + 28),  3)  # poste
        pygame.draw.line(ecra, COR_FORCA_S, (cx - 28, cy + 28),  (cx + 35, cy + 28),  3)  # topo
        pygame.draw.line(ecra, COR_FORCA_S, (cx + 35, cy + 28),  (cx + 35, cy + 48),  3)  # corda

        bx, by = cx + 35, cy + 48

        c0 = parte_cor(0, COR_B)
        if c0: pygame.draw.circle(ecra, c0, (bx, by + 18), 18, 3)
        c1 = parte_cor(1, COR_B)
        if c1: pygame.draw.line(ecra, c1, (bx, by + 36), (bx, by + 96), 3)
        c2 = parte_cor(2, COR_B)
        if c2: pygame.draw.line(ecra, c2, (bx, by + 52), (bx - 28, by + 72), 3)
        c3 = parte_cor(3, COR_B)
        if c3: pygame.draw.line(ecra, c3, (bx, by + 52), (bx + 28, by + 72), 3)
        c4 = parte_cor(4, COR_B)
        if c4: pygame.draw.line(ecra, c4, (bx, by + 96), (bx - 24, by + 138), 3)
        c5 = parte_cor(5, COR_B)
        if c5: pygame.draw.line(ecra, c5, (bx, by + 96), (bx + 24, by + 138), 3)

    def desenhar_tiles():
        n_letras = sum(1 for c in palavra if c != ' ')
        n_esp    = palavra.count(' ')
        T   = 52
        GAP = 5
        ESP = 14

        total_w = n_letras * (T + GAP) - GAP + n_esp * ESP
        if total_w > LARGURA - 40:
            fac = (LARGURA - 40) / total_w
            T   = max(28, int(T * fac))
            GAP = max(3,  int(GAP * fac))
            ESP = max(8,  int(ESP * fac))
            total_w = n_letras * (T + GAP) - GAP + n_esp * ESP

        x = LARGURA // 2 - total_w // 2
        y = WORD_Y
        fs = max(12, int(T * 0.54))
        FT = pygame.freetype.SysFont('arial', fs, bold=True)

        for ch, desc in zip(palavra, letras_desc):
            if ch == ' ':
                x += ESP
                continue
            if desc != '_':
                pygame.draw.rect(ecra, COR_CERTO, (x, y, T, T), border_radius=5)
                s = FT.render(desc, COR_TEXTO)[0]
                ecra.blit(s, (x + T//2 - s.get_width()//2, y + T//2 - s.get_height()//2))
            else:
                pygame.draw.rect(ecra, COR_FUNDO,   (x, y, T, T), border_radius=5)
                pygame.draw.rect(ecra, COR_TILE_BD, (x, y, T, T), 2, border_radius=5)
            x += T + GAP

    def desenhar_teclado():
        for row_idx, row in enumerate(TECLADO):
            row_w = len(row) * (KEY_W + KEY_GAP) - KEY_GAP
            rx    = LARGURA // 2 - row_w // 2
            ry    = KBD_Y + row_idx * (KEY_H + KEY_GAP)

            for col_idx, letra in enumerate(row):
                kx = rx + col_idx * (KEY_W + KEY_GAP)
                ky = ry
                if letra in chutadas:
                    cor_k = COR_CERTO if letra in palavra else COR_ERRADO
                else:
                    cor_k = COR_KEY
                pygame.draw.rect(ecra, cor_k, (kx, ky, KEY_W, KEY_H), border_radius=4)
                s = F_KEY.render(letra, COR_TEXTO)[0]
                ecra.blit(s, (kx + KEY_W//2 - s.get_width()//2,
                               ky + KEY_H//2 - s.get_height()//2))

    banco = carregar_palavras()
    iniciar_som(volume)

    # ═══════════════════════════════════════════════════════════════
    a_correr = True
    while a_correr:
        ticks = pygame.time.get_ticks()
        ecra.fill(COR_FUNDO)

        # ── EVENTOS ────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                a_correr = False

            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    mudar_volume(0.1)
                elif ev.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    mudar_volume(-0.1)

                if tela == "MENU":
                    if ev.key == pygame.K_1:
                        tela = "NOME"; nome_input = ""
                    elif ev.key == pygame.K_2:
                        tela = "REGRAS"
                    elif ev.key == pygame.K_3:
                        tela = "HISTORICO"
                    elif ev.key == pygame.K_4:
                        a_correr = False

                elif tela == "NOME":
                    if ev.key == pygame.K_RETURN and nome_input.strip():
                        nome_jogador = nome_input.strip().upper()
                        nova_partida()
                        tela = "JOGO"
                    elif ev.key == pygame.K_ESCAPE:
                        tela = "MENU"
                    elif ev.key == pygame.K_BACKSPACE:
                        nome_input = nome_input[:-1]
                    elif ev.unicode.isprintable() and len(nome_input) < 18:
                        nome_input += ev.unicode

                elif tela in ("REGRAS", "HISTORICO"):
                    if ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        tela = "MENU"

                elif tela == "JOGO":
                    if estado == "JOGANDO":
                        letra = ev.unicode.upper()
                        if letra.isalpha() and letra not in chutadas:
                            chutadas.append(letra)
                            tentativas_total += 1
                            if letra in palavra:
                                acertos_letras += 1
                                pontuacao      += PONTOS_ACERTO
                                flash_timer     = ticks
                                flash_cor       = COR_CERTO
                                for i, c in enumerate(palavra):
                                    if c == letra:
                                        letras_desc[i] = letra
                                if '_' not in letras_desc:
                                    sobraram  = max_tent - erros
                                    pontuacao += BONUS_VITORIA + sobraram * BONUS_TENTATIVA
                                    estado     = "VITORIA"
                                    salvar_resultado(
                                        nome_jogador, pontuacao, acertos_letras,
                                        erros, tentativas_total, max_tent, palavra, True
                                    )
                            else:
                                erros            += 1
                                pontuacao        += PONTOS_ERRO
                                flash_timer       = ticks
                                flash_cor         = COR_PERIGO
                                boneco_nova_parte = erros - 1
                                boneco_anim_timer = ticks
                                if erros >= max_tent:
                                    estado = "DERROTA"
                                    salvar_resultado(
                                        nome_jogador, pontuacao, acertos_letras,
                                        erros, tentativas_total, max_tent, palavra, False
                                    )
                    else:
                        if ev.key == pygame.K_RETURN:
                            tela = "MENU"

        # ── ATUALIZAÇÕES POR FRAME ──────────────────────────────────
        if tela == "JOGO" and estado == "JOGANDO":
            novo_idx = 0
            if erros >= max_tent * 2 // 3: novo_idx = 1
            if erros >= max_tent - 1:      novo_idx = 2

            if novo_idx != dica_idx_atual:
                dica_idx_atual   = novo_idx
                prefixo          = "[!] " if dica_idx_atual == 2 else ""
                dica_texto_alvo  = prefixo + dicas[dica_idx_atual]
                dica_chars_visto = 0
                dica_ultimo_tick = ticks

            if dica_chars_visto < len(dica_texto_alvo):
                if ticks - dica_ultimo_tick >= DIGITACAO_MS:
                    dica_chars_visto += 1
                    dica_ultimo_tick  = ticks

        # ═══════════════════════════════════════════════════════════
        # ── RENDERIZAÇÃO ───────────────────────────────────────────
        # ═══════════════════════════════════════════════════════════

        # ───────────────────────────────────────────── MENU ────────
        if tela == "MENU":
            blit_c(F_TITULO, "FORCA", COR_TEXTO, ALTURA // 2 - 138)
            blit_c(F_DICA,   "Descubra a palavra secreta",  COR_SUTIL, ALTURA // 2 - 100)

            if nome_jogador:
                blit_c(F_PEQNA, f"agente: {nome_jogador}", COR_SUTIL, ALTURA // 2 - 70)

            linha_h(ALTURA // 2 - 52, LARGURA // 2 - 90, LARGURA // 2 + 90)

            itens = [
                ("1", "Nova Partida",  COR_TEXTO),
                ("2", "Regras",        COR_SUTIL),
                ("3", "Histórico",     COR_SUTIL),
                ("4", "Sair",          COR_SUTIL),
            ]
            y = ALTURA // 2 - 38
            for num, desc, cor in itens:
                s = F_TEXTO.render(f"[ {num} ]  {desc}", cor)[0]
                ecra.blit(s, (LARGURA // 2 - s.get_width() // 2, y))
                y += 38

            linha_h(ALTURA // 2 + 118, LARGURA // 2 - 90, LARGURA // 2 + 90)

            blocos_v = round(volume * 10)
            blit_c(F_PEQNA,
                   f"[ - ]  {'█' * blocos_v}{'░' * (10 - blocos_v)}  {int(volume*100)}%  [ = ]",
                   COR_SUTIL, ALTURA // 2 + 130)

        # ───────────────────────────────────────────── NOME ────────
        elif tela == "NOME":
            blit_c(F_GRANDE, "Identificação", COR_TEXTO, ALTURA // 2 - 100)
            blit_c(F_DICA,   "Digite seu codinome:", COR_SUTIL, ALTURA // 2 - 58)

            bw, bh = 340, 48
            bx = LARGURA // 2 - bw // 2
            by = ALTURA // 2 - 22
            pygame.draw.rect(ecra, COR_FUNDO, (bx, by, bw, bh), border_radius=6)
            pygame.draw.rect(ecra, COR_TILE_BD, (bx, by, bw, bh), 2, border_radius=6)
            cursor = "_" if (ticks // 500) % 2 == 0 else " "
            blit(F_TEXTO, nome_input + cursor, COR_TEXTO, bx + 14, by + 13)

            blit_c(F_PEQNA, "ENTER confirma  ·  ESC cancela", COR_SUTIL, ALTURA // 2 + 45)

        # ───────────────────────────────────────────── REGRAS ──────
        elif tela == "REGRAS":
            blit_c(F_GRANDE, "Regras", COR_TEXTO, 30)
            linha_h(62, 40, LARGURA - 40)

            linhas = [
                ("O jogo sorteia uma palavra secreta.", COR_SUTIL),
                ("Adivinhe as letras uma por uma.", COR_SUTIL),
                ("", COR_SUTIL),
                ("PONTUAÇÃO", COR_TEXTO),
                ("  +10  por letra correta", COR_CERTO),
                ("   -5  por letra errada",  COR_PERIGO),
                ("  +50  ao vencer a partida",       COR_CERTO),
                ("  +10  por tentativa poupada",     COR_CERTO),
                ("", COR_SUTIL),
                ("DIFICULDADE", COR_TEXTO),
                ("  FÁCIL    8 tentativas  (2 letras reveladas)", COR_CERTO),
                ("  MÉDIO    6 tentativas  (1 letra revelada)",   COR_AVISO),
                ("  DIFÍCIL  4 tentativas  (nenhuma revelada)",   COR_PERIGO),
                ("", COR_SUTIL),
                ("As dicas aparecem conforme os erros aumentam.", COR_SUTIL),
                ("O histórico é salvo em resultados.txt.",        COR_SUTIL),
            ]
            y = 78
            for txt, cor in linhas:
                if txt:
                    blit(F_PEQNA, txt, cor, 55, y)
                y += 27

            linha_h(y + 2, 40, LARGURA - 40)
            blit_c(F_DICA, "ENTER  ·  Voltar", COR_SUTIL, y + 14)

        # ───────────────────────────────────────────── HISTORICO ───
        elif tela == "HISTORICO":
            blit_c(F_GRANDE, "Histórico", COR_TEXTO, 22)

            registros = carregar_historico()
            vitorias  = sum(1 for r in registros if r.strip().endswith("VITORIA"))
            derrotas  = sum(1 for r in registros if r.strip().endswith("DERROTA"))
            melhor    = 0
            for r in registros:
                p = r.strip().split('|')
                if len(p) >= 3:
                    try: melhor = max(melhor, int(p[2]))
                    except ValueError: pass

            blit_c(F_PEQNA,
                   f"{vitorias} vitórias  ·  {derrotas} derrotas  ·  melhor: {melhor} pts",
                   COR_SUTIL, 56)
            linha_h(76, 18, LARGURA - 18)

            cabec = "DATA/HORA            NOME           PTS   CRT ERR  TENT     RESULTADO"
            blit(F_PEQNA, cabec, COR_SUTIL, 18, 84)
            linha_h(100, 18, LARGURA - 18)

            if not registros:
                blit_c(F_TEXTO, "Nenhuma partida ainda.", COR_SUTIL, 310)
            else:
                y = 106
                for idx, reg in enumerate(registros[-14:]):
                    p = reg.strip().split('|')
                    if len(p) >= 8:
                        data, nome, pts, ac, er, tent, pal, res = p[:8]
                        cor = COR_CERTO if res == "VITORIA" else COR_PERIGO
                        if idx % 2 == 0:
                            pygame.draw.rect(ecra, (28, 28, 35),
                                             (16, y - 1, LARGURA - 32, 20))
                        txt_l = (f"{data[:16]}  {nome[:12]:<12} {pts:>5}"
                                 f"  {ac:>3} {er:>3}  {tent:>6}   {res}")
                        blit(F_PEQNA, txt_l, cor, 18, y)
                        y += 24

            blit_c(F_DICA, "ENTER  ·  Voltar", COR_SUTIL, ALTURA - 30)

        # ───────────────────────────────────────────── JOGO ────────
        elif tela == "JOGO":
            # Header
            blit(F_TITULO, "FORCA", COR_TEXTO, 18, 12)
            stats = (f"Nível: {nivel}  ·  Pontos: {pontuacao}"
                     f"  ·  Erros: {erros}/{max_tent}"
                     f"  ·  Vol: {int(volume*100)}%  [ - / = ]")
            s_st = F_STATS.render(stats, COR_SUTIL)[0]
            ecra.blit(s_st, (LARGURA - s_st.get_width() - 16, 18))
            linha_h(HDR_H)

            # Forca
            desenhar_forca()

            # Separador
            linha_h(WORD_Y - 12, LARGURA // 2 - 180, LARGURA // 2 + 180)

            # Tiles da palavra
            desenhar_tiles()

            # Contagem de letras
            total_letras = sum(1 for c in palavra if c.isalpha())
            blit_c(F_PEQNA, f"{total_letras} letras", COR_SUTIL, WORD_Y + 58)

            # Dica — break por pixels dentro de max_w
            dica_cor     = COR_PERIGO if dica_idx_atual == 2 else COR_SUTIL
            dica_exibida = dica_texto_alvo[:dica_chars_visto]
            max_w_dica   = LARGURA - 80

            if F_DICA.render(dica_exibida, COR_TEXTO)[0].get_width() <= max_w_dica:
                blit_c(F_DICA, dica_exibida, dica_cor, WORD_Y + 76)
            else:
                tokens = dica_exibida.split(' ')
                linha1, corte = "", 0
                for i, tok in enumerate(tokens):
                    cand = (linha1 + " " + tok).strip()
                    if F_DICA.render(cand, COR_TEXTO)[0].get_width() <= max_w_dica:
                        linha1, corte = cand, i
                    else:
                        break
                linha2 = " ".join(tokens[corte + 1:])
                blit_c(F_DICA, linha1, dica_cor, WORD_Y + 76)
                if linha2:
                    blit_c(F_DICA, linha2, dica_cor, WORD_Y + 94)

            if estado == "JOGANDO":
                blit_c(F_PEQNA, "pressione uma tecla para digitar",
                       pulso_cor(COR_SUTIL, 2200, 35), WORD_Y + 114)

            # Teclado QWERTY
            desenhar_teclado()

            # Flash de feedback
            if flash_timer > 0 and ticks - flash_timer < FLASH_MS:
                prog  = (ticks - flash_timer) / FLASH_MS
                alpha = int(75 * (1 - prog ** 1.8))
                ov    = pygame.Surface((LARGURA, ALTURA))
                ov.set_alpha(alpha)
                ov.fill(flash_cor)
                ecra.blit(ov, (0, 0))

            # Overlay fim de jogo
            if estado != "JOGANDO":
                ov = pygame.Surface((LARGURA, ALTURA))
                ov.set_alpha(230)
                ov.fill(COR_FUNDO)
                ecra.blit(ov, (0, 0))

                if estado == "VITORIA":
                    blit_c(F_TITULO, "Você venceu!", COR_CERTO, ALTURA // 2 - 72)
                else:
                    blit_c(F_TITULO, "Fim de jogo", COR_PERIGO, ALTURA // 2 - 72)
                    blit_c(F_TEXTO,  f"A palavra era:  {palavra}",
                           COR_TEXTO, ALTURA // 2 - 26)

                blit_c(F_PEQNA,
                       f"Pontuação: {pontuacao}  ·  Acertos: {acertos_letras}"
                       f"  ·  Erros: {erros}  ·  Tentativas: {tentativas_total}",
                       COR_SUTIL, ALTURA // 2 + 16)

                linha_h(ALTURA // 2 + 44, LARGURA // 2 - 120, LARGURA // 2 + 120)
                blit_c(F_TEXTO, "ENTER  ·  Voltar ao Menu", COR_TEXTO, ALTURA // 2 + 58)

        pygame.display.flip()
        relogio.tick(60)

    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    executar_jogo()
