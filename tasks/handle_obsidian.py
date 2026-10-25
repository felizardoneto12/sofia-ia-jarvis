"""
Tarefa: Integração e Gestão do Obsidian Vault da Sofia
Lê, pesquisa e cria notas organizadas no cofre exclusivo da Sofia.
"""
import os
import json
from datetime import datetime

description = "Lê, busca e cria notas no cofre exclusivo do Obsidian da Sofia em F:\\Sofia_IA\\Obsidian_Sofia_Vault."
trigger = "obsidian"
example = '{"type": "obsidian", "content": {"action": "write", "folder": "Ideias_e_Projetos", "title": "Plano_IA", "text": "Ideia do Jarvis..."}}'

VAULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Obsidian_Sofia_Vault")

def execute(content) -> str:
    try:
        if isinstance(content, str):
            content = json.loads(content)
            
        action = content.get("action", "read")  # "read", "write", "search"
        folder = content.get("folder", "Ideias_e_Projetos")
        title = content.get("title", f"Nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        text = content.get("text", "")
        
        target_dir = os.path.join(VAULT_DIR, folder)
        os.makedirs(target_dir, exist_ok=True)
        
        if not title.endswith(".md"):
            title += ".md"
            
        target_file = os.path.join(target_dir, title)
        
        if action == "write":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            note_content = f"# {title[:-3]}\n\n*Criado pela Sofia IA em {timestamp}*\n\n{text}\n"
            with open(target_file, "a", encoding="utf-8") as f:
                f.write(note_content)
            return f"Nota salva com sucesso no Obsidian: {folder}/{title}"
            
        elif action == "read":
            if os.path.exists(target_file):
                with open(target_file, "r", encoding="utf-8") as f:
                    return f.read()
            return f"Arquivo {title} não encontrado no cofre."
            
        elif action == "search":
            query = content.get("query", "").lower()
            results = []
            for root, _, files in os.walk(VAULT_DIR):
                for f in files:
                    if f.endswith(".md"):
                        path = os.path.join(root, f)
                        try:
                            with open(path, "r", encoding="utf-8") as rf:
                                c = rf.read()
                                if query in c.lower():
                                    rel = os.path.relpath(path, VAULT_DIR)
                                    results.append(f"- **{rel}**: {c[:200]}...")
                        except Exception:
                            continue
            if results:
                return "Resultados encontrados no Obsidian:\n" + "\n".join(results[:5])
            return f"Nenhuma nota encontrada com o termo '{query}'."
            
        return "Ação do Obsidian não reconhecida."
    except Exception as e:
        return f"Erro na operação com Obsidian: {e}"
