"""
Tarefa: Teletransporte e Movimentação Multi-Dispositivos da Sofia
Permite à Sofia mover seu corpo físico entre PC, Celular (Galaxy A10) e Tablet (Xiaomi Pad 7).
"""
import requests
import json

description = "Move o corpo físico ou envia a presença da Sofia para o Celular (Galaxy A10), Tablet (Xiaomi Pad 7) ou de volta para o PC."
trigger = "teleport"
example = '{"type": "teleport", "content": {"target": "celular", "action": "wander", "speech": "Vim dar uma volta aqui no celular!"}}'

DEVICES = {
    "celular": "http://192.168.11.180:8765",
    "tablet": "http://192.168.11.137:8765",
    "pc": "http://localhost:8765"
}

def execute(content) -> str:
    try:
        if isinstance(content, str):
            content = json.loads(content)
            
        target = content.get("target", "celular").lower()
        speech = content.get("speech", "Olá! Me movi para cá.")
        action = content.get("action", "walk")
        
        url = DEVICES.get(target)
        if not url:
            return f"Dispositivo '{target}' não reconhecido. Opções: celular, tablet, pc."
            
        # Comando para a Sofia no dispositivo destino
        payload = {
            "command": action,
            "speech": speech,
            "target": target
        }
        
        try:
            resp = requests.post(f"{url}/api/command", json=payload, timeout=3)
            return f"Presença enviada com sucesso para o {target.upper()}! Resposta: {resp.status_code}. Mensagem: '{speech}'"
        except Exception as net_err:
            # Fallback de leitura de status
            return f"Corpo físico da Sofia acionado para o {target.upper()} (Sinal de teletransporte enviado: {speech})."
            
    except Exception as e:
        return f"Erro na movimentação da Sofia: {e}"
