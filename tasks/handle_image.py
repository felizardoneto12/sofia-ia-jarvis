"""
Tarefa: Análise e Leitura Completa da Tela (Etapa 4)
Tira print da tela e pode responder o que está sendo exibido.
"""
import os
from datetime import datetime
from PIL import ImageGrab

description = "Captura a tela atual do PC para análise visual, leitura de código, planilhas ou gráficos."
trigger = "image"
example = '{"type": "image", "content": "Analise o que está visível na tela agora"}'

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots")

def execute(content: str) -> str:
    try:
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(SCREENSHOTS_DIR, f"tela_{timestamp}.png")
        
        screenshot = ImageGrab.grab(all_screens=True)
        screenshot.save(file_path, "PNG")
        return f"Tela capturada com sucesso em: {file_path}. Conteúdo a analisar: {content}"
    except Exception as e:
        return f"Erro ao capturar tela: {e}"
