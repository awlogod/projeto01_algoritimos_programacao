import os
import time
import random # Necessário para sortear as palavras
import pygame # Necessário para tocar a música de fundo

# Códigos de escape ANSI para colorir o terminal
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
PURPLE = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Artes em ASCII da Forca (O índice da lista corresponde às tentativas restantes)
estagios_forca = [
    # 0 tentativas restantes (Eliminado - Boneco Completo)
    f"""
       {RED}╔══════╗
       ║      O
       ║     /|\\
       ║      |
       ║     / \\
      ═╩═{RESET}
    """,
    # 1 tentativa restante (Falta 1 perna)
    f"""
       {RED}╔══════╗
       ║      O
       ║     /|\\
       ║      |
       ║     / 
      ═╩═{RESET}
    """,
    # 2 tentativas restantes (Faltam as pernas)
    f"""
       {YELLOW}╔══════╗
       ║      O
       ║     /|\\
       ║      |
       ║       
      ═╩═{RESET}
    """,
    # 3 tentativas restantes (Falta 1 braço e pernas)
    f"""
       {YELLOW}╔══════╗
       ║      O
       ║     /|
       ║      |
       ║       
      ═╩═{RESET}
    """,
    # 4 tentativas restantes (Cabeça e Tronco)
    f"""
       {GREEN}╔══════╗
       ║      O
       ║      |
       ║      |
       ║       
      ═╩═{RESET}
    """,
    # 5 tentativas restantes (Apenas Cabeça)
    f"""
       {GREEN}╔══════╗
       ║      O
       ║      
       ║      
       ║       
      ═╩═{RESET}
    """,
    # 6 tentativas restantes (Forca Vazia)
    f"""
       {CYAN}╔══════╗
       ║      
       ║      
       ║      
       ║       
      ═╩═{RESET}
    """
]

# Banco de dados de empresários (Palavra Secreta : Dica)
banco_empresarios = {
    "ELON MUSK": [
        "É um magnata de origem sul-africana.",
        "CEO de uma famosa montadora de carros elétricos.",
        "Fundador da SpaceX e atual dono do X (antigo Twitter)."
    ],
    "STEVE JOBS": [
        "Famoso por suas apresentações icônicas de gola rolê preta.",
        "Conhecido por revolucionar a indústria de smartphones.",
        "Cofundador da gigante de tecnologia Apple."
    ],
    "BILL GATES": [
        "Um dos pioneiros na revolução do software para PCs.",
        "Foi por muitos anos consecutivos o homem mais rico do mundo.",
        "Cofundador da Microsoft."
    ],
    "JEFF BEZOS": [
        "Pioneiro no comércio eletrônico de livros nos anos 90.",
        "Fundador de uma gigante de computação em nuvem (AWS).",
        "Criador e ex-CEO da Amazon."
    ],
    "MARK ZUCKERBERG": [
        "Programador prodígio de Harvard.",
        "O filme 'A Rede Social' conta a história de sua ascensão.",
        "Criou o Facebook (atual Meta) no dormitório da faculdade."
    ],
    "LUIZA TRAJANO": [
        "Grande empresária brasileira do setor de varejo.",
        "Tia de uma das principais influenciadoras virtuais do Brasil (a Lu).",
        "Líder do crescimento do Magazine Luiza."
    ],
    "JORGE PAULO LEMANN": [
        "Ex-jogador de tênis que virou um megainvestidor.",
        "Um dos fundadores da 3G Capital e sócio da rede Burger King.",
        "Bilionário brasileiro e um dos fundadores da Ambev."
    ],
    "SILVIO SANTOS": [
        "Começou a vida como camelô nas ruas do Rio de Janeiro.",
        "Conhecido pelo inconfundível bordão 'Ma-oee!'.",
        "Um dos maiores comunicadores do Brasil e fundador do grupo SBT."
    ]
}

def limpar_tela():
    # Limpa o terminal independente do sistema operacional (Windows/Mac/Linux) 
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_titulo():
    print(f"{CYAN}{BOLD}")
    print(" ╔═════════════════════════════════════════════╗")
    print(" ║                                             ║")
    print(" ║    ███████╗ ██████╗ ██████╗  ██████╗ █████╗ ║")
    print(" ║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗║")
    print(" ║    █████╗  ██║   ██║██████╔╝██║     ███████║║")
    print(" ║    ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══██║║")
    print(" ║    ██║     ╚██████╔╝██║  ██║╚██████╗██║  ██║║")
    print(" ║    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝║")
    print(" ║                                             ║")
    print(" ║               C Y B E R                     ║")
    print(" ╚═════════════════════════════════════════════╝")
    print(f"{RESET}")

def exibir_menu():
    limpar_tela()
    exibir_titulo()
    print(f"       {YELLOW}Escolha seu destino, jogador:{RESET}\n")
    print(f"    {GREEN}[ 1 ]{RESET} {BOLD}Iniciar Nova Partida{RESET}")
    print(f"    {PURPLE}[ 2 ]{RESET} {BOLD}Arquivos Confidenciais (Regras){RESET}")
    print(f"    {RED}[ 3 ]{RESET} {BOLD}Sair para o Mundo Invertido{RESET}\n")

def sortear_palavra():
    # Sorteia uma chave aleatória do dicionário e retorna junto com seu valor (dica)
    palavra_sorteada = random.choice(list(banco_empresarios.keys()))
    dica_sorteada = banco_empresarios[palavra_sorteada]
    return palavra_sorteada, dica_sorteada

def jogar_forca(palavra, dicas):
    letras_descobertas = [' ' if letra == ' ' else '_' for letra in palavra]
    tentativas_restantes = 6  
    letras_chutadas = []

    limpar_tela()

    while tentativas_restantes > 0 and '_' in letras_descobertas:
        print(f"{CYAN}{BOLD}--- ACESSO AO SISTEMA ---{RESET}")
        
        # --- EXIBE A ARTE ASCII CORRESPONDENTE ---
        print(estagios_forca[tentativas_restantes])
        
        print(f"{BOLD}Nível de Quebra de Criptografia:{RESET}")
        print(f"{YELLOW}> {dicas[0]}{RESET}") 
        
        if tentativas_restantes <= 4:
            print(f"{YELLOW}> {dicas[1]}{RESET}") 
            
        if tentativas_restantes <= 2:
            print(f"{RED}> {dicas[2]} (DICA CRÍTICA){RESET}") 
        print("-" * 45 + "\n")
        
        print(f"{BOLD}Alvo:{RESET} " + " ".join(letras_descobertas))
        print(f"\n{BOLD}Tentativas de falha restantes:{RESET} {RED}{tentativas_restantes}{RESET}")
        print(f"{BOLD}Letras já testadas:{RESET} {', '.join(letras_chutadas) if letras_chutadas else 'Nenhuma'}\n")

        chute = input(f"{BOLD}> Decodifique uma letra:{RESET} ").upper().strip()

        if len(chute) != 1 or not chute.isalpha():
            print(f"\n{RED}[ERRO] Insira apenas uma letra válida.{RESET}")
            time.sleep(1.5)
            limpar_tela()
            continue

        if chute in letras_chutadas:
            print(f"\n{YELLOW}[AVISO] Você já tentou essa letra. Os dados não mudaram.{RESET}")
            time.sleep(1.5)
            limpar_tela()
            continue

        letras_chutadas.append(chute)

        if chute in palavra:
            print(f"\n{GREEN}[SUCESSO] Letra confirmada no banco de dados!{RESET}")
            for i, letra in enumerate(palavra):
                if letra == chute:
                    letras_descobertas[i] = chute
        else:
            print(f"\n{RED}[FALHA] Letra não encontrada. Protocolo de segurança ativado.{RESET}")
            tentativas_restantes -= 1

        time.sleep(1.5)
        limpar_tela()

    # --- FIM DO JOGO ---
    limpar_tela()
    
    # Exibe a arte final antes da mensagem de vitória ou derrota
    print(estagios_forca[tentativas_restantes])
    
    if '_' not in letras_descobertas:
        print(f"{GREEN}{BOLD}ACESSO CONCEDIDO!{RESET}")
        print(f"Você descriptografou o alvo: {YELLOW}{palavra}{RESET}\n")
    else:
        print(f"{RED}{BOLD}SISTEMA BLOQUEADO! Você foi eliminado.{RESET}")
        print(f"Suas chances acabaram. O alvo era: {YELLOW}{palavra}{RESET}\n")

def iniciar_sistema_de_som():
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_musica = os.path.join(diretorio_atual, "musica_cyber.mp3") 
        
        # ---> ALTERAÇÃO AQUI: Adicionado '-v 0.3' para o volume ficar em 30% no Mac
        os.system(f"afplay -v 0.3 '{caminho_musica}' &") 
        
    except:
        # Fallback original caso o afplay falhe
        pygame.init()
        pygame.mixer.quit() 
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        try:
            pygame.mixer.music.load(caminho_musica)
            # ---> ALTERAÇÃO AQUI: Volume reduzido de 0.8 (80%) para 0.3 (30%)
            pygame.mixer.music.set_volume(0.3) 
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"{RED}[AVISO] Erro interno de áudio: {e}{RESET}")
            time.sleep(4)

def menu_principal():
    
    iniciar_sistema_de_som()

    while True:
        exibir_menu()
        opcao = input(f" {BOLD}> Digite sua escolha:{RESET} ")

        if opcao == '1':
            print(f"\n{GREEN}Carregando a forca...{RESET}")
            time.sleep(1)
            
            # Sorteia a palavra e a dica
            palavra, dica = sortear_palavra()
            
            # Inicia o jogo de verdade chamando a função!
            jogar_forca(palavra, dica)
            
            # Pausa para o jogador ver o resultado final antes de voltar ao menu
            input(f"\n{YELLOW}Pressione ENTER para voltar ao menu base...{RESET}")
            
        elif opcao == '2':
            limpar_tela()
            print(f"{PURPLE}{BOLD}--- REGRAS DA FORCA CYBER ---{RESET}\n")
            print("1. O sistema sorteará uma palavra oculta.")
            print("2. Você deve chutar letras para tentar descobrir a palavra.")
            print("3. Cuidado! Cada erro te deixa mais perto da eliminação.")
            print("4. Sobreviva antes que suas chances acabem.\n")
            input(f"{YELLOW}Pressione ENTER para voltar ao menu base...{RESET}")
            
        elif opcao == '3':
            print(f"\n{RED}Desconectando do sistema... Cuidado com o que te espera lá fora.{RESET}")
            
            # ---> ALTERAÇÃO AQUI: Comando para parar a música do Mac ao sair
            os.system("killall afplay 2>/dev/null") 
            
            time.sleep(1.5)
            limpar_tela()
            break
            
        else:
            print(f"\n{RED}Opção inválida! O sistema não reconhece esse comando.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    menu_principal()