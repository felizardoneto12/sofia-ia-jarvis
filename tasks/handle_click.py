"""
Tarefa: Automação e Clique em Coordenadas (Etapas 1 e 2)
Move o cursor e executa clique na coordenada informada.
"""
import json
import pyautogui

description = "Move o cursor do mouse e clica com precisão nas coordenadas (x, y) da tela."
trigger = "click"
example = '{"type": "click", "content": {"x": 500, "y": 300, "button": "left"}}'

def execute(content) -> str:
    try:
        if isinstance(content, str):
            content = json.loads(content)
            
        x = int(content.get("x", 0))
        y = int(content.get("y", 0))
        button = content.get("button", "left")
        
        # Mover com segurança
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click(button=button)
        return f"Clique com botão {button} realizado na posição ({x}, {y})."
    except Exception as e:
        return f"Erro ao executar clique: {e}"
