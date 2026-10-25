"""
Task Manager Modular da Sofia IA (Arquitetura Jarvis / Junin - Etapa 6 e 7)
Carrega dinamicamente todas as habilidades da pasta tasks/
"""
import os
import sys
import importlib.util
import json
from typing import Dict, Any

TASKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")

class TaskManager:
    def __init__(self, tasks_dir: str = TASKS_DIR):
        self.tasks_dir = tasks_dir
        os.makedirs(self.tasks_dir, exist_ok=True)
        self.tasks: Dict[str, Any] = {}
        self.reload_tasks()

    def reload_tasks(self):
        """Carrega ou recarrega dinamicamente todos os scripts da pasta tasks/."""
        self.tasks.clear()
        for filename in os.listdir(self.tasks_dir):
            if filename.startswith("handle_") and filename.endswith(".py"):
                task_name = filename[:-3]  # ex: handle_normal
                file_path = os.path.join(self.tasks_dir, filename)
                try:
                    spec = importlib.util.spec_from_file_location(task_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[task_name] = module
                        spec.loader.exec_module(module)
                        
                        # Validar se segue o contrato obrigatório
                        if hasattr(module, "execute") and hasattr(module, "description"):
                            self.tasks[task_name] = module
                            print(f"[TaskManager] Tarefa carregada: {task_name}")
                        else:
                            print(f"[TaskManager] Aviso: {filename} não implementa 'execute' ou 'description'")
                except Exception as e:
                    print(f"[TaskManager] Erro ao carregar {filename}: {e}")

    def get_system_prompt_tools(self) -> str:
        """Gera a lista formatada de ferramentas para a LLM entender o que pode executar."""
        lines = []
        for name, mod in self.tasks.items():
            desc = getattr(mod, "description", "")
            trigger = getattr(mod, "trigger", name)
            example = getattr(mod, "example", "")
            lines.append(f"- Tarefa: `{name}` | Gatilho: `{trigger}`\n  Descrição: {desc}\n  Exemplo: {example}")
        return "\n".join(lines)

    def execute_task(self, task_name: str, content: Any) -> str:
        """Executa a tarefa correspondente de forma segura."""
        if not task_name.startswith("handle_"):
            task_name = f"handle_{task_name}"
            
        if task_name not in self.tasks:
            # Tentar recarregar caso seja uma nova tarefa recém-gerada (Etapa 7)
            self.reload_tasks()
            
        if task_name in self.tasks:
            try:
                mod = self.tasks[task_name]
                return str(mod.execute(content))
            except Exception as e:
                return f"Erro ao executar tarefa {task_name}: {e}"
        else:
            return f"Tarefa '{task_name}' não encontrada no catálogo da Sofia."

if __name__ == "__main__":
    tm = TaskManager()
    print("\n--- Ferramentas Disponíveis ---")
    print(tm.get_system_prompt_tools())
