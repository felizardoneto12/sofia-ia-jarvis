"""
Tarefa Mestre: Criação Dinâmica de Novas Tarefas em Tempo Real (Etapa 7)
Permite à Sofia gerar código Python para aprender novas habilidades instantaneamente.
"""
import os
import json
import re

description = "Cria uma nova tarefa/habilidade dinamicamente em tempo real gerando código Python seguro na pasta tasks/."
trigger = "nova_tarefa"
example = '{"type": "nova_tarefa", "content": {"function_name": "somar", "description": "Soma dois numeros", "trigger": "somar", "code": "def execute(content): ..."}}'

TASKS_DIR = os.path.dirname(os.path.abspath(__file__))

def execute(content) -> str:
    try:
        if isinstance(content, str):
            content = json.loads(content)
            
        function_name = content.get("function_name", "").strip()
        desc = content.get("description", "Nova tarefa gerada dinamicamente.")
        trigger = content.get("trigger", function_name)
        code = content.get("code", "")
        
        # Limpar nome da função para segurança
        function_name = re.sub(r"[^a-zA-Z0-9_]", "", function_name)
        if not function_name:
            return "Erro: Nome da função inválido."
            
        if not function_name.startswith("handle_"):
            filename = f"handle_{function_name}.py"
        else:
            filename = f"{function_name}.py"
            
        file_path = os.path.join(TASKS_DIR, filename)
        
        # Template padrão garantindo que contenha description, trigger, example e execute
        if "def execute" not in code:
            return "Erro: O código precisa conter a função obrigatória 'def execute(content):'."
            
        task_file_content = f'''"""
Tarefa Dinâmica Gerada: {function_name}
"""
description = """{desc}"""
trigger = "{trigger}"
example = '{{"type": "{trigger}", "content": "..."}}'

{code}
'''
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(task_file_content)
            
        return f"Sucesso! Nova habilidade '{function_name}' foi aprendida e salva em tasks/{filename}. Já está disponível para uso imediato!"
    except Exception as e:
        return f"Erro ao criar nova tarefa: {e}"
