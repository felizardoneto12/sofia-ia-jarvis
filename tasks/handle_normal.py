"""
Tarefa: Conversa Normal e Resposta Falada
"""
description = "Responde a perguntas e conversa amigável com o usuário em linguagem natural."
trigger = "normal"
example = '{"type": "normal", "content": "Olá! Como posso ajudar você hoje?"}'

def execute(content: str) -> str:
    # A resposta direta em texto para ser falada pela Sofia
    return str(content)
