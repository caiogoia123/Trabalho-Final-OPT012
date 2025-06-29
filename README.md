Pré-requisitos

Antes de começar, garanta que você tenha os seguintes pré-requisitos de hardware e software instalados.

Hardware

    Uma webcam conectada ao computador.

Software

    Python 3.7 ou superior.

    pip (gerenciador de pacotes do Python), que geralmente já vem instalado com o Python.

Configuração do Ambiente

Siga estes passos para preparar sua máquina para executar o projeto. É altamente recomendável usar um ambiente virtual (venv) para isolar as dependências deste projeto.

1. Clone ou Baixe o Projeto

Se o seu projeto estiver em um repositório Git, clone-o:
Bash

    git clone <URL_DO_SEU_REPOSITORIO>
    cd <NOME_DO_DIRETORIO_DO_PROJETO>

Caso contrário, apenas crie uma pasta, coloque seu arquivo .py dentro dela e navegue até essa pasta pelo terminal.

2. Crie e Ative um Ambiente Virtual (Recomendado)

No Windows:

    Bash

# Criar o ambiente virtual

    python -m venv venv

# Ativar o ambiente virtual

    .\venv\Scripts\activate

No macOS ou Linux:

    Bash

    # Criar o ambiente virtual
    python3 -m venv venv

    # Ativar o ambiente virtual
    source venv/bin/activate

Seu terminal deverá agora mostrar (venv) no início da linha, indicando que o ambiente virtual está ativo.

3. Instale as Dependências

Com o ambiente virtual ativo, instale as bibliotecas Python necessárias com um único comando:
Bash

pip install opencv-python mediapipe pyautogui

Detalhes das bibliotecas:

    opencv-python: Para captura e processamento de imagem da webcam.

    mediapipe: Para a detecção e rastreamento das mãos e seus pontos de referência.

    pyautogui: Para simular o pressionamento das teclas do teclado.

Como Executar o Script

    Certifique-se de que sua webcam está conectada e funcionando.

    Verifique se o seu ambiente virtual está ativo.

    Execute o seguinte comando no terminal (substitua seu_script.py pelo nome real do seu arquivo):
    Bash

    python seu_script.py

    Uma janela de vídeo será aberta, mostrando a imagem da sua webcam. Posicione suas mãos em frente à câmera para começar a controlar o computador.

Como Parar o Script

Para encerrar a execução do programa de forma segura, clique na janela de vídeo e pressione a tecla q.