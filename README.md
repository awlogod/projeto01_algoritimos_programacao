### JOGO DA FORCA - FEITO POR ANDRÉ WILCKAY LAGE OLIVEIRA

## Faculdade: Pontifícia Universidade Católica de Campinas
## Nome: André Wilckay Lage Oliveira
## Ra: 25017047
## Turma: 103

---

### [Contexto do Jogo]

Jogo da forca com interface gráfica desenvolvida em **Python + Pygame**, com estética inspirada no jogo *Termo* (dark mode minimalista). O objetivo é adivinhar o nome de **empresários e empreendedores famosos** a partir de dicas progressivas, antes que o boneco da forca seja completado.

O tema foi escolhido para unir entretenimento e conhecimento sobre figuras que marcaram o mundo dos negócios e da tecnologia.

### [Como Jogar]

1. No menu principal, pressione `1` para iniciar uma nova partida.
2. Digite seu nome (codinome) e pressione `ENTER`.
3. O computador sorteia uma palavra secreta (nome de um empresário) e exibe os espaços em branco.
4. Dependendo do nível de dificuldade, algumas letras já são reveladas no início.
5. Pressione as teclas do teclado para propor **uma letra por vez**.
6. Se a letra estiver na palavra, ela é revelada em **verde** e você ganha **+10 pontos**.
7. Se a letra **não** estiver na palavra, você perde **-5 pontos** e uma parte do boneco é desenhada.
8. As dicas vão ficando mais específicas conforme você erra.
9. Se completar a palavra antes de esgotar as tentativas, você **vence** e recebe bônus (+50 pontos + 10 por tentativa restante).
10. Se as tentativas acabarem, a partida é encerrada como **derrota**.
11. Pressione `ENTER` ao final para voltar ao menu.

### [Níveis de Dificuldade]

| Nível   | Tentativas | Letras Reveladas |
|---------|------------|------------------|
| Fácil   | 8          | 2                |
| Médio   | 6          | 1                |
| Difícil | 4          | 0                |

### [Sistema de Pontuação]

| Evento                    | Pontos |
|---------------------------|--------|
| Letra correta             | +10    |
| Letra errada              | -5     |
| Vitória (bônus)           | +50    |
| Por tentativa restante    | +10    |

### [Funcionalidades]

- **Interface gráfica** com Pygame (dark mode, teclado QWERTY visual, forca animada).
- **Música ambiente** com controle de volume (`-` e `=` para ajustar).
- **3 dicas progressivas** por palavra, reveladas conforme os erros aumentam.
- **Histórico de partidas** salvo em `resultados.txt` com data, nome, pontuação, acertos, erros, tentativas e resultado.
- **Tela de regras** acessível pelo menu.
- **Tela de histórico** com resumo de vitórias, derrotas e melhor pontuação.
- **Palavras e dicas** carregadas de arquivo externo (`palavras.txt`), facilitando a expansão do banco de palavras.

### [Arquivos do Projeto]

| Arquivo           | Descrição                                              |
|-------------------|--------------------------------------------------------|
| `projeto01.py`    | Código principal do jogo                               |
| `palavras.txt`    | Banco de palavras, dicas e níveis de dificuldade       |
| `resultados.txt`  | Histórico de partidas (gerado automaticamente)         |
| `musica_cyber.mp3`| Música de fundo (opcional)                             |

---

## Visão Empreendedora

### Quais são os clientes para o seu jogo?

- **Estudantes do ensino fundamental e médio**: jovens em fase de formação que podem aprender sobre grandes empreendedores de forma lúdica e interativa.
- **Professores e educadores**: que buscam ferramentas pedagógicas para aulas de empreendedorismo, história, tecnologia ou língua portuguesa (vocabulário e ortografia).
- **Instituições de ensino**: escolas e universidades que desejam incluir atividades interativas em seus programas.
- **Empresas e startups**: para treinamentos corporativos gamificados sobre cultura empreendedora e liderança.
- **Público geral**: qualquer pessoa interessada em jogos de palavras e cultura geral sobre o mundo dos negócios.

### Quais problemas o jogo pode solucionar?

- **Educação de forma lúdica**: transforma o aprendizado sobre empreendedorismo em uma experiência divertida, fugindo do modelo tradicional de aula expositiva.
- **Ampliação de vocabulário e cultura geral**: o jogador aprende nomes, trajetórias e curiosidades sobre grandes figuras do mundo dos negócios.
- **Estímulo ao raciocínio lógico e dedução**: o jogador precisa pensar estrategicamente sobre quais letras propor com base nas dicas.
- **Inclusão digital**: o jogo pode ser utilizado em projetos sociais e comunitários para introduzir jovens ao uso de computadores e tecnologia.
- **Diversos contextos temáticos**: o banco de palavras pode ser adaptado para temas como ciência, história, geografia, saúde, meio ambiente, esportes, entre outros — ampliando os escopos de aplicação e o mercado consumidor.

### O jogo está relacionado a alguma demanda institucional?

Sim. O jogo se alinha com diversas demandas:

- **BNCC (Base Nacional Comum Curricular)**: a BNCC incentiva o desenvolvimento de competências ligadas ao pensamento crítico, cultura digital e empreendedorismo desde o ensino fundamental.
- **Educação empreendedora**: programas como o SEBRAE nas Escolas e Junior Achievement promovem o empreendedorismo na educação básica — o jogo pode ser utilizado como ferramenta complementar.
- **Gamificação no ensino**: há uma crescente demanda por ferramentas que utilizem jogos como recurso pedagógico em sala de aula e em plataformas EAD.

### O jogo pode incorporar alguma tendência do mercado consumidor?

- **Gamificação educacional**: uma das maiores tendências em EdTech, utilizando mecânicas de jogos (pontuação, ranking, níveis) para engajar alunos.
- **Jogos casuais e mobile**: o formato simples e rápido se encaixa na tendência de jogos casuais que podem ser jogados em sessões curtas — o jogo pode ser portado para dispositivos móveis.
- **Personalização de conteúdo**: a estrutura baseada em arquivos de texto permite que qualquer pessoa crie seus próprios bancos de palavras temáticos, tornando o jogo uma plataforma customizável.
- **Rankings e competição social**: a funcionalidade de histórico pode evoluir para um sistema de rankings online, incentivando competição saudável entre jogadores.

### O jogo incorpora alguma novidade/inovação?

- **Tema diferenciado**: ao contrário de jogos de forca tradicionais com palavras genéricas, o foco em **empreendedores e empresários** agrega valor educacional e inspira o jogador com histórias de sucesso.
- **Dicas progressivas**: o sistema de 3 dicas que se revelam conforme o número de erros é uma mecânica que diferencia o jogo da forca convencional, tornando a experiência mais estratégica.
- **Plataforma expansível**: a arquitetura com banco de palavras em arquivo externo permite transformar o jogo em uma **plataforma temática** — qualquer professor ou empresa pode criar seus próprios pacotes de palavras (ex: "Cientistas Brasileiros", "Inventores", "Mulheres na Tecnologia").
- **Potencial para modelo freemium**: pacotes temáticos básicos gratuitos, com pacotes especializados pagos — criando uma oportunidade de **renda passiva** com baixo custo de manutenção.
- **Estética moderna**: a interface inspirada no Termo/Wordle atrai um público habituado a jogos de palavras modernos, diferenciando-se dos jogos de forca com visual ultrapassado.

---

## Referências e Fontes

### Linguagem e Documentação

- [Documentação oficial do Python](https://docs.python.org/pt-br/3/) — referência para sintaxe, manipulação de arquivos, strings e módulos padrão.
- [Python - Leitura e escrita de arquivos](https://docs.python.org/pt-br/3/tutorial/inputoutput.html#reading-and-writing-files) — base para a lógica de carregar `palavras.txt` e salvar `resultados.txt`.
- [Módulo random - Python](https://docs.python.org/pt-br/3/library/random.html) — utilizado para sortear palavras e letras iniciais reveladas.
- [Módulo time - Python](https://docs.python.org/pt-br/3/library/time.html) — utilizado para registrar data/hora nos resultados.

### Pygame

- [Documentação oficial do Pygame](https://www.pygame.org/docs/) — referência principal para criação da interface gráfica.
- [Pygame - Módulo freetype](https://www.pygame.org/docs/ref/freetype.html) — utilizado para renderização de texto com fontes do sistema.
- [Pygame - Módulo draw](https://www.pygame.org/docs/ref/draw.html) — utilizado para desenhar a forca, o boneco e os elementos visuais.
- [Pygame - Módulo mixer](https://www.pygame.org/docs/ref/music.html) — utilizado para reprodução da música de fundo.
- [Pygame - Tratamento de eventos](https://www.pygame.org/docs/ref/event.html) — base para captura de teclas e interação com o jogador.

### Tutoriais e Inspiração

- [Real Python - Making a Hangman Game](https://realpython.com/python-hangman/) — tutorial sobre lógica de jogo da forca em Python.
- [GeeksforGeeks - Hangman Game in Python](https://www.geeksforgeeks.org/hangman-game-python/) — referência para estrutura de controle do jogo.
- [Termo (term.ooo)](https://term.ooo/) — inspiração para a estética dark mode e o layout de tiles.
- [Wordle - The New York Times](https://www.nytimes.com/games/wordle/index.html) — inspiração para o conceito de feedback visual por cores nas letras.

### Empreendedorismo e Educação

- [BNCC - Base Nacional Comum Curricular](http://basenacionalcomum.mec.gov.br/) — referência sobre competências de cultura digital e empreendedorismo na educação.
- [SEBRAE - Educação Empreendedora](https://sebrae.com.br/sites/PortalSebrae/educacaoempreendedora) — contexto sobre programas de empreendedorismo nas escolas.
- [Forbes - Bilionários do Mundo](https://forbes.com.br/listas/bilionarios-do-mundo/) — fonte para pesquisa sobre os empresários utilizados no banco de palavras.
