# EyeNavigate

Tecnologia assistiva que permite controlar o computador **sem usar as mãos**, pensada para pessoas com tetraplegia. Com uma webcam comum, o sistema transforma o movimento dos olhos em movimento do cursor e o movimento da cabeça em rolagem de tela.

> ⚠️ **Versão base (protótipo inicial).**
> Este repositório contém apenas a **primeira versão** do projeto, feita para validar a ideia. Uma **nova versão** será desenvolvida, com **código mais refinado e fundamentada em estudo mais aprofundado** (precisão, estabilidade, ergonomia e necessidades reais dos usuários). Esta base serve como ponto de partida e referência, e não como produto final.

---

## Objetivo

Oferecer autonomia no uso do computador a pessoas com mobilidade reduzida nos membros superiores, usando apenas uma câmera e o movimento natural do rosto e dos olhos, sem hardware especializado e caro.

## Como funciona

O projeto é composto por dois módulos independentes.

### 1. Cursor controlado pelo olhar (`eye_navigate_jogo.py`)

- Usa o **MediaPipe Face Mesh** com `refine_landmarks=True` para localizar a **íris** dos dois olhos (pontos 468–472 e 473–477).
- Calcula a posição média das duas íris a cada quadro.
- **Calibragem em 9 pontos** (grade 3×3 na tela, a 10%, 50% e 90% da largura e da altura): o usuário olha para cada ponto e pressiona `ESPAÇO`. Os valores mínimo e máximo da posição da íris definem a faixa de movimento do usuário.
- A posição da íris é mapeada para a tela com interpolação linear (`np.interp`), com inversão do eixo X para compensar o efeito espelho da câmera.
- **Suavização** do movimento (fator `0.25`) e **margem de 30 px** nas bordas, para evitar tremor e cursor preso nos cantos.
- O cursor é movido com o `pyautogui`.

### 2. Rolagem controlada pela cabeça (script de scroll)

- Usa o **MediaPipe Face Detection** para obter a caixa delimitadora do rosto.
- Faz duas calibragens guiadas por vídeo: o usuário posiciona a cabeça **para a direita** e depois **para a esquerda**, e a posição do rosto em cada lado é registrada.
- Durante o uso, a posição atual do rosto é comparada às duas referências (tolerância `atol=20`):
  - cabeça na posição **direita** → rola a página **para baixo**;
  - cabeça na posição **esquerda** → rola a página **para cima**.
- A rolagem é enviada com a biblioteca `pynput`.

## Fluxo de uso

Ambos os módulos seguem a mesma sequência:

1. **Enquadramento:** o usuário se posiciona diante da câmera e pressiona `Q` quando estiver satisfeito.
2. **Vídeo de calibragem:** um vídeo instrui o usuário sobre o que fazer (`calibragemOlhos.mp4`, `calibragemDireita.mp4`, `calibragemEsquerda.mp4`).
3. **Calibragem:** captura das referências (pontos na tela para o olhar; lados direito e esquerdo para a cabeça).
4. **Uso:** o controle é ativado. Pressione `Q` a qualquer momento para encerrar.

## Requisitos

- Python 3.8+
- Webcam
- Bibliotecas:

```bash
pip install opencv-python mediapipe numpy pyautogui pynput
```

> Os scripts usam a API `mp.solutions` do MediaPipe. Em versões muito novas do pacote essa API pode estar depreciada; se houver erro, instale uma versão compatível.

## Executando

```bash
python eye_navigate_jogo.py   # cursor pelo olhar
python <script_de_scroll>.py  # rolagem pela cabeça
```

Antes de rodar, ajuste os **caminhos dos vídeos de calibragem**, que estão fixos no código para uma máquina Linux específica (`/home/giovana/Área de trabalho/eyeNavigate/v3/...`).

## Parâmetros ajustáveis

| Parâmetro | Onde | Efeito |
|---|---|---|
| `0.25` (suavização) | cursor | menor = mais suave e lento; maior = mais rápido e trêmulo |
| `margem_x`, `margem_y` (30) | cursor | distância mínima das bordas da tela |
| `min_detection_confidence` / `min_tracking_confidence` (0.7) | Face Mesh | rigor da detecção do rosto |
| `atol=20` | scroll | tolerância para reconhecer a posição direita/esquerda |
| `maxlen=14` (`track_points`) | scroll | tamanho do histórico de posições do rosto |

## Limitações conhecidas desta versão base

- Calibragem **sensível a mudanças de posição**: se o usuário ou a câmera se mexerem depois de calibrar, a precisão cai e é preciso recalibrar.
- Não há **compensação do movimento da cabeça** no rastreamento da íris; olhar e cabeça se misturam no resultado.
- Iluminação ruim, óculos ou reflexos prejudicam a detecção.
- **Não há ação de clique** nestes dois arquivos; o controle cobre apenas movimento do cursor e rolagem.
- A calibragem inicial exige o **teclado** (`Q`, `ESPAÇO`), o que pode precisar de ajuda de um cuidador. Um fluxo totalmente autônomo é um ponto a melhorar.
- A rolagem tem **velocidade fixa** e a detecção por posição do rosto é pouco robusta.
- Caminhos de arquivos fixos no código, sem arquivo de configuração.
- Os dois módulos ainda não estão integrados em uma única aplicação.
- Sem testes com usuários reais.

## Próximos passos (nova versão)

A versão seguinte terá código refatorado e será baseada em estudo mais refinado, com atenção a pontos como:

- rastreamento mais preciso e estável, com compensação da pose da cabeça;
- integração dos módulos (olhar, cabeça, clique) em uma só aplicação;
- calibragem autônoma, sem depender do teclado;
- configuração por arquivo e interface mais acessível;
- validação com pessoas tetraplégicas e profissionais de acessibilidade.

## Aviso

Este é um **protótipo experimental**. Não substitui tecnologias assistivas certificadas e deve ser usado com acompanhamento enquanto não for validado.
