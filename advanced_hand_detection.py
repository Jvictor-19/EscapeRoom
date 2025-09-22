import cv2
import serial
import time
import numpy as np
from collections import deque
import math

class LibrasDetector:
    def __init__(self, serial_port='COM6', baudrate=115200):
        # Conexão serial
        try:
            self.serial_conn = serial.Serial(serial_port, baudrate, timeout=1)
            time.sleep(2)
            print("✓ Conexão serial estabelecida!")
        except Exception as e:
            print(f"✗ Erro na conexão serial: {e}")
            self.serial_conn = None
        
        # Parâmetros de detecção
        self.min_area = 8000
        self.max_area = 50000
        
        # Sistema de reconhecimento de sequências
        self.detected_letters = deque(maxlen=10)  # Últimas 10 letras
        self.target_word = "UAU"  # Palavra que ativa o motor
        self.last_gesture = ""
        self.gesture_count = 0
        self.stability_threshold = 15  # Frames para confirmar gesto
        
        # Buffer para estabilização
        self.gesture_buffer = deque(maxlen=20)
        
        # Histórico de gestos
        self.gesture_history = []
        self.max_history = 50
        
        # Estado do sistema
        self.motor_activated = False
        self.last_activation_time = 0
        self.activation_cooldown = 5  # 5 segundos entre ativações
        
        print("=== DETECTOR LIBRAS INICIALIZADO ===")
        print(f"✓ Palavra alvo: '{self.target_word}'")
        print("✓ Detecção por análise de contornos e geometria da mão")
        
    def create_skin_mask(self, frame):
        """Cria máscara de pele usando múltiplos espaços de cor"""
        # Converte para HSV e YCrCb
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        
        # Máscaras HSV
        lower_hsv = np.array([0, 20, 70], dtype=np.uint8)
        upper_hsv = np.array([25, 255, 255], dtype=np.uint8)
        mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)
        
        # Máscaras YCrCb
        lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
        upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
        mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)
        
        # Combina máscaras
        mask = cv2.bitwise_or(mask_hsv, mask_ycrcb)
        
        # Morfologia
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.GaussianBlur(mask, (3, 3), 0)
        
        return mask
    
    def analyze_hand_geometry(self, contour):
        """Analisa geometria da mão para classificação LIBRAS"""
        try:
            # Momentos e centro
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return {}
            
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Características geométricas
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            
            if perimeter == 0:
                return {}
            
            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h if h > 0 else 0
            
            # Hull convexo
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = area / hull_area if hull_area > 0 else 0
            
            # Compacidade
            compactness = (perimeter * perimeter) / (4 * np.pi * area)
            
            # Defeitos de convexidade
            hull_indices = cv2.convexHull(contour, returnPoints=False)
            if len(hull_indices) > 3:
                defects = cv2.convexityDefects(contour, hull_indices)
                defect_count = len(defects) if defects is not None else 0
            else:
                defect_count = 0
            
            # Extent (proporção da área em relação ao bounding rectangle)
            extent = area / (w * h) if (w * h) > 0 else 0
            
            return {
                'center': (cx, cy),
                'area': area,
                'perimeter': perimeter,
                'aspect_ratio': aspect_ratio,
                'solidity': solidity,
                'compactness': compactness,
                'defect_count': defect_count,
                'extent': extent,
                'width': w,
                'height': h
            }
            
        except Exception as e:
            print(f"Erro na análise geométrica: {e}")
            return {}
    
    def count_extended_fingers(self, contour, frame):
        """Conta dedos estendidos usando análise de convexidade"""
        try:
            # Hull e defeitos
            hull_indices = cv2.convexHull(contour, returnPoints=False)
            if len(hull_indices) < 4:
                return 0
                
            defects = cv2.convexityDefects(contour, hull_indices)
            if defects is None:
                return 0
            
            # Centro da mão
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return 0
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            valid_fingers = 0
            
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                
                # Distância mínima para ser considerado dedo
                if d > 6000:
                    # Calcula ângulo entre os pontos
                    a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    
                    if a > 0 and b > 0 and c > 0:
                        angle = np.arccos((b**2 + c**2 - a**2) / (2*b*c))
                        angle_deg = np.degrees(angle)
                        
                        # Ângulo típico entre dedos
                        if 30 < angle_deg < 120:
                            valid_fingers += 1
                            # Desenha ponto de defeito
                            cv2.circle(frame, far, 4, (255, 255, 0), -1)
            
            # Retorna número de dedos (defeitos + 1)
            return min(valid_fingers + 1, 5)
            
        except Exception as e:
            return 0
    
    def classify_libras_letter(self, geometry, finger_count, frame):
        """Classifica letra LIBRAS baseada na geometria e dedos"""
        if not geometry:
            return "INDEFINIDO"
        
        area = geometry.get('area', 0)
        aspect_ratio = geometry.get('aspect_ratio', 0)
        solidity = geometry.get('solidity', 0)
        compactness = geometry.get('compactness', 0)
        extent = geometry.get('extent', 0)
        defect_count = geometry.get('defect_count', 0)
        
        # Classificação baseada em características específicas de LIBRAS
        
        # Letra A - Punho fechado com polegar para cima
        if finger_count <= 1 and solidity > 0.85 and compactness < 8:
            return "A"
        
        # Letra B - Mão aberta, dedos juntos
        if finger_count >= 4 and solidity > 0.9 and aspect_ratio < 1.3:
            return "B"
        
        # Letra C - Mão em formato de C
        if 1 <= finger_count <= 2 and 0.6 < solidity < 0.8 and compactness > 12:
            return "C"
        
        # Letra D - Indicador apontando
        if finger_count == 1 and aspect_ratio > 1.5 and extent < 0.6:
            return "D"
        
        # Letra E - Punho fechado
        if finger_count == 0 and solidity > 0.9 and compactness < 6:
            return "E"
        
        # Letra F - Três dedos (indicador, médio, anelar)
        if finger_count == 3 and solidity > 0.75:
            return "F"
        
        # Letra G - Indicador e polegar estendidos
        if finger_count == 2 and aspect_ratio > 1.2:
            return "G"
        
        # Letra I - Mindinho estendido
        if finger_count == 1 and aspect_ratio < 1.2 and extent > 0.6:
            return "I"
        
        # Letra L - L com indicador e polegar
        if finger_count == 2 and aspect_ratio > 1.4 and compactness > 15:
            return "L"
        
        # Letra O - Formato circular
        if finger_count <= 2 and 0.7 < solidity < 0.85 and 8 < compactness < 15:
            return "O"
        
        # Letra U - Dois dedos juntos
        if finger_count == 2 and aspect_ratio < 1.3 and solidity > 0.8:
            return "U"
        
        # Letra V - Dois dedos separados (vitória)
        if finger_count == 2 and defect_count >= 1 and solidity < 0.8:
            return "V"
        
        # Padrão padrão baseado no número de dedos
        finger_letters = {0: "E", 1: "D", 2: "V", 3: "F", 4: "B", 5: "ABERTA"}
        return finger_letters.get(finger_count, "INDEFINIDO")
    
    def update_letter_sequence(self, letter):
        """Atualiza sequência de letras detectadas"""
        if letter != "INDEFINIDO" and letter != self.detected_letters[-1] if self.detected_letters else True:
            self.detected_letters.append(letter)
            print(f"Letra detectada: {letter}")
            print(f"Sequência atual: {' '.join(list(self.detected_letters))}")
            
            # Verifica se formou a palavra alvo
            self.check_target_word()
    
    def check_target_word(self):
        """Verifica se a sequência forma a palavra alvo"""
        if len(self.detected_letters) >= len(self.target_word):
            # Pega as últimas N letras
            recent_letters = ''.join(list(self.detected_letters)[-len(self.target_word):])
            
            if recent_letters == self.target_word:
                current_time = time.time()
                if current_time - self.last_activation_time > self.activation_cooldown:
                    self.activate_motor()
                    self.last_activation_time = current_time
                    self.detected_letters.clear()  # Limpa para nova detecção
    
    def activate_motor(self):
        """Envia sinal para ativar o motor"""
        if self.serial_conn:
            try:
                # Envia comando para ativar motor
                self.serial_conn.write("ACTIVATE_MOTOR\n".encode())
                print(f" PALAVRA '{self.target_word}' DETECTADA! MOTOR ATIVADO!")
                self.motor_activated = True
                
                # Opcional: enviar sequência de ativação específica
                time.sleep(0.1)
                self.serial_conn.write("START_SEQUENCE\n".encode())
                
            except Exception as e:
                print(f"Erro ao ativar motor: {e}")
        else:
            print(f" PALAVRA '{self.target_word}' DETECTADA! (Sem conexão serial)")
    
    def run(self):
        """Loop principal do detector"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("=== DETECTOR DE LIBRAS ATIVO ===")
        print(f" Palavra alvo: '{self.target_word}'")
        print("📝 Letras suportadas: A, B, C, D, E, F, G, I, L, O, U, V")
        print("🔄 Forme a palavra para ativar o motor")
        print("-" * 50)
        print("Controles: 'q'=sair, 'r'=reset, 'w'=mudar palavra")
        print("-" * 50)
        
        # ROI para detecção
        roi_x, roi_y, roi_w, roi_h = 350, 80, 450, 450
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # ROI
            roi = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
            
            # Detecção de mão
            mask = self.create_skin_mask(roi)
            
            # Encontra contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            current_gesture = "INDEFINIDO"
            
            if contours:
                # Maior contorno
                hand_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(hand_contour)
                
                if self.min_area < area < self.max_area:
                    # Ajusta coordenadas
                    hand_contour[:, 0, 0] += roi_x
                    hand_contour[:, 0, 1] += roi_y
                    
                    # Desenha contorno
                    cv2.drawContours(frame, [hand_contour], -1, (0, 255, 0), 2)
                    
                    # Análise
                    geometry = self.analyze_hand_geometry(hand_contour)
                    finger_count = self.count_extended_fingers(hand_contour, frame)
                    
                    # Classifica letra
                    current_gesture = self.classify_libras_letter(geometry, finger_count, frame)
                    
                    # Adiciona ao buffer para estabilização
                    self.gesture_buffer.append(current_gesture)
                    
                    # Mostra informações
                    if geometry:
                        cv2.putText(frame, f"Dedos: {finger_count}", (10, 80), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                        cv2.putText(frame, f"Solidity: {geometry.get('solidity', 0):.2f}", 
                                   (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
                        cv2.putText(frame, f"Aspect: {geometry.get('aspect_ratio', 0):.2f}", 
                                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Sistema de estabilização
            if len(self.gesture_buffer) >= 10:
                # Gesto mais comum nos últimos frames
                gesture_counts = {}
                for g in list(self.gesture_buffer)[-10:]:
                    gesture_counts[g] = gesture_counts.get(g, 0) + 1
                
                most_common = max(gesture_counts, key=gesture_counts.get)
                confidence = gesture_counts[most_common] / 10
                
                # Confirma gesto se confiança alta
                if confidence >= 0.7 and most_common != "INDEFINIDO":
                    if most_common != self.last_gesture:
                        self.update_letter_sequence(most_common)
                        self.last_gesture = most_common
            
            # Interface
            color = (0, 255, 0) if current_gesture != "INDEFINIDO" else (0, 0, 255)
            cv2.putText(frame, f"LETRA: {current_gesture}", (10, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
            
            # Palavra alvo e progresso
            cv2.putText(frame, f"Palavra alvo: {self.target_word}", (10, frame.shape[0] - 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Sequência atual
            sequence_text = ' '.join(list(self.detected_letters)) if self.detected_letters else "Nenhuma"
            cv2.putText(frame, f"Sequencia: {sequence_text}", (10, frame.shape[0] - 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Status do motor
            motor_status = "ATIVO" if self.motor_activated else "INATIVO"
            motor_color = (0, 255, 0) if self.motor_activated else (0, 0, 255)
            cv2.putText(frame, f"Motor: {motor_status}", (10, frame.shape[0] - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, motor_color, 2)
            
            # ROI
            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2)
            cv2.putText(frame, "ROI - Coloque a mao aqui", (roi_x, roi_y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Mostra resultado
            cv2.imshow('Detector LIBRAS', frame)
            cv2.imshow('Mascara', cv2.resize(mask, (300, 300)))
            
            # Controles
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.detected_letters.clear()
                self.gesture_buffer.clear()
                self.last_gesture = ""
                self.motor_activated = False
                print("Sistema resetado")
            elif key == ord('w'):
                new_word = input("Digite a nova palavra alvo: ").upper().strip()
                if new_word:
                    self.target_word = new_word
                    self.detected_letters.clear()
                    print(f"Nova palavra alvo: {self.target_word}")
        
        cap.release()
        cv2.destroyAllWindows()
        if self.serial_conn:
            self.serial_conn.close()

if __name__ == "__main__":
    # Inicia o detector
    detector = LibrasDetector(serial_port='COM6')
    detector.run()