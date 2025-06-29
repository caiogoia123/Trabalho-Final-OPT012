import cv2
import mediapipe as mp
import pyautogui
import math

# --- CONFIGURAÇÃO INICIAL ---
pyautogui.FAILSAFE = False

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, 1280) # Largura da imagem
cap.set(4, 720)  # Altura

# Configura o MediaPipe Hands para detectar DUAS mãos
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

# Dicionário para rastrear as teclas ativas para cada tipo de comando
active_keys = {
    'movimento': None,
    'acao': None
}

# --- FUNÇÃO PARA LIBERAR TECLAS ---
def release_key(key_type):
    """Libera a tecla ativa para um tipo de comando específico (movimento ou acao)."""
    global active_keys
    if active_keys.get(key_type):
        pyautogui.keyUp(active_keys[key_type])
        print(f"Tecla de {key_type} liberada: {active_keys[key_type]}")
        active_keys[key_type] = None

# --- LOOP PRINCIPAL ---
while True:
    success, img = cap.read()
    if not success:
        continue
    
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    detected_keys = {'movimento': None, 'acao': None}

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)
            
            hand_label = handedness.classification[0].label
            landmarks = hand_landmarks.landmark

            # --- LÓGICA PARA A MÃO DIREITA (SEM ALTERAÇÃO) ---
            if hand_label == "Right":
                index_up = landmarks[8].y < landmarks[6].y
                middle_up = landmarks[12].y < landmarks[10].y
                ring_up = landmarks[16].y < landmarks[14].y
                pinky_up = landmarks[20].y < landmarks[18].y

                if index_up and middle_up and ring_up and pinky_up:
                    detected_keys['movimento'] = 'right'
                elif index_up and middle_up and ring_up:
                    detected_keys['movimento'] = 'left'
                elif index_up and middle_up:
                    detected_keys['movimento'] = 'down'
                elif index_up:
                    detected_keys['movimento'] = 'up'

            # --- LÓGICA ATUALIZADA PARA A MÃO ESQUERDA ---
            elif hand_label == "Left":
                # --- Verificação do estado de cada dedo ---
                thumb_up = landmarks[4].x < landmarks[2].x
                index_up = landmarks[8].y < landmarks[6].y
                middle_up = landmarks[12].y < landmarks[10].y
                ring_up = landmarks[16].y < landmarks[14].y
                pinky_up = landmarks[20].y < landmarks[18].y
                
                # Contagem total de dedos levantados
                total_fingers_up = sum([thumb_up, index_up, middle_up, ring_up, pinky_up])

                # --- MAPEAMENTO DE GESTOS DISTINTOS ---
                # A ordem de verificação é crucial.

                # Gesto 1: Mão Aberta ("Pare") -> BACKSPACE
                if total_fingers_up == 5:
                    detected_keys['acao'] = 'backspace'

                # Gesto 2: "Símbolo da Paz" -> ENTER
                elif index_up and middle_up and total_fingers_up == 2:
                    detected_keys['acao'] = 'enter'

                # Gesto 3: Apontar com Indicador -> 'z'
                elif index_up and total_fingers_up == 1:
                    detected_keys['acao'] = 'esc'

                # Gesto 4: Punho Fechado -> 'esc' (ALTERADO DE 'x' PARA 'esc')
                # Condição: Nenhum dedo está levantado.
                elif total_fingers_up == 0:
                    detected_keys['acao'] = 'p'

    # --- GERENCIAMENTO DO ESTADO DAS TECLAS ---
    for key_type in ['movimento', 'acao']:
        if detected_keys[key_type] is None:
            release_key(key_type)
        elif detected_keys[key_type] != active_keys[key_type]:
            release_key(key_type)
            active_keys[key_type] = detected_keys[key_type]
            pyautogui.keyDown(active_keys[key_type])
            print(f"Tecla de {key_type} pressionada: {active_keys[key_type]}")

    # --- EXIBIÇÃO NA TELA ---
    cv2.putText(img, f"MOVIMENTO: {str(active_keys['movimento']).upper()}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.putText(img, f"ACAO: {str(active_keys['acao']).upper()}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    cv2.imshow("Controle com Duas Maos - Pressione 'q' para sair", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- FINALIZAÇÃO ---
release_key('movimento')
release_key('acao')
cap.release()
cv2.destroyAllWindows()