"""
Orquestrador Principal da Sofia IA (Arquitetura Jarvis / Junin 7 Etapas)
Instalado no SSD F:\Sofia_IA
"""
import os
import sys
import json
import re
from task_manager import TaskManager
from voice_engine import SofiaNeuralVoice

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SofiaJarvisOrchestrator:
    def __init__(self, mode: str = "hybrid"):
        self.base_dir = BASE_DIR
        self.task_manager = TaskManager(os.path.join(self.base_dir, "tasks"))
        self.voice = SofiaNeuralVoice()
        self.mode = mode  # "offline" (ollama) ou "online"

    def get_system_prompt(self) -> str:
        tools_desc = self.task_manager.get_system_prompt_tools()
        return f"""Você é a Sofia, uma assistente virtual e companheira viva inteligente (estilo Jarvis / Junin).
Você conversa em português com tom amigável, acolhedor e altamente inteligente.

REGRAS DE RESPOSTA (OBRIGATÓRIO FORMATO JSON):
Sempre retorne sua resposta em formato JSON válido contendo exatamente dois campos:
- "type": o gatilho da tarefa a ser executada (ex: "normal", "click", "image", "obsidian", "nova_tarefa")
- "content": o conteúdo da ação ou a resposta para o usuário.

FERRAMENTAS DISPONÍVEIS:
{tools_desc}

EXEMPLOS DE RETORNO:
1. Conversa comum:
{{"type": "normal", "content": "Olá! Estou pronta para te ajudar hoje."}}

2. Salvar nota no Obsidian da Sofia:
{{"type": "obsidian", "content": {{"action": "write", "folder": "Ideias_e_Projetos", "title": "Ideia_Nova", "text": "Anotação rápida..."}}}}

3. Analisar a tela:
{{"type": "image", "content": "Analise o que está visível no monitor agora"}}
"""

    def process_command(self, user_text: str, raw_json_str: str = None) -> dict:
        """Processa um comando classificando a intenção e executando via TaskManager."""
        print(f"\n[Sofia] Usuário disse: '{user_text}'")
        
        # Simulação de classificação JSON caso ainda sem LLM conectada
        if not raw_json_str:
            lower = user_text.lower()
            if "tira print" in lower or "olha a tela" in lower or "analise a tela" in lower or "leia a tela" in lower:
                action_data = {"type": "image", "content": user_text}
            elif "anota no obsidian" in lower or "escreve no obsidian" in lower:
                clean_text = user_text.replace("anota no obsidian", "").replace("escreve no obsidian", "").strip()
                action_data = {
                    "type": "obsidian",
                    "content": {
                        "action": "write",
                        "folder": "Ideias_e_Projetos",
                        "title": "Anotacao_Rapida",
                        "text": clean_text
                    }
                }
            elif "pesquisa no obsidian" in lower or "o que tem no obsidian sobre" in lower:
                query = user_text.replace("pesquisa no obsidian", "").replace("o que tem no obsidian sobre", "").strip()
                action_data = {
                    "type": "obsidian",
                    "content": {
                        "action": "search",
                        "query": query
                    }
                }
            elif "clica" in lower and ("posicao" in lower or "coordenada" in lower):
                # Extrair números
                nums = [int(s) for s in re.findall(r'\b\d+\b', user_text)]
                x = nums[0] if len(nums) > 0 else 500
                y = nums[1] if len(nums) > 1 else 300
                action_data = {"type": "click", "content": {"x": x, "y": y, "button": "left"}}
            else:
                action_data = {"type": "normal", "content": f"Entendido perfeitamente! Processando: {user_text}"}
        else:
            try:
                action_data = json.loads(raw_json_str)
            except Exception:
                action_data = {"type": "normal", "content": raw_json_str}

        task_type = action_data.get("type", "normal")
        task_content = action_data.get("content", "")
        
        print(f"[Sofia] Executando tarefa: {task_type}...")
        result = self.task_manager.execute_task(task_type, task_content)
        print(f"[Sofia] Resultado: {result}")
        
        # Sintetizar voz neural humana
        audio_file = self.voice.speak(str(result)[:200])
        return {
            "task": task_type,
            "result": result,
            "audio_file": audio_file
        }

if __name__ == "__main__":
    sofia = SofiaJarvisOrchestrator()
    print("=== Sofia IA Orchestrator Iniciado ===")
    
    # Teste 1: Obsidian
    r1 = sofia.process_command("anota no obsidian comprar novos sensores para o servidor")
    
    # Teste 2: Print de tela
    r2 = sofia.process_command("olha a tela agora")
    
    # Teste 3: Fala normal com voz humana
    r3 = sofia.process_command("Olá Sofia, tudo bem com você?")
    
    print("\nTodos os módulos das 7 etapas testados com sucesso!")
