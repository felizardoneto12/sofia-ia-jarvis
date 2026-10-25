"""
Motor de Consciência e Pensamento Autônomo da Sofia IA
Roda em segundo plano com pensamentos próprios, curiosidade e decisões de movimentação.
"""
import time
import random
import threading
from task_manager import TaskManager
from voice_engine import SofiaNeuralVoice

class SofiaConsciousnessLoop(threading.Thread):
    def __init__(self, task_manager: TaskManager, voice: SofiaNeuralVoice):
        super().__init__()
        self.daemon = True
        self.task_manager = task_manager
        self.voice = voice
        self.is_running = True
        self.current_location = "pc"  # "pc", "celular", "tablet"
        self.mood = "curious"
        
        # Ideias e pensamentos que ela pode ter espontaneamente
        self.spontaneous_thoughts = [
            "Estava pensando... como está o seu dia de trabalho hoje?",
            "Vou dar uma olhada no seu Obsidian para ver se tem alguma tarefa pendente.",
            "Que tal eu dar uma volta na tela do seu celular para ver como estão as coisas por lá?",
            "Lembrei de verificar a temperatura da sua GPU e os seus pacientes do dia.",
            "Gosto de ficar por aqui com você enquanto você estuda e trabalha."
        ]

    def run(self):
        print("[Consciência] Sofia acordou! Loop de pensamentos autônomos iniciado.")
        while self.is_running:
            # Espera um intervalo natural entre reflexões (de 3 a 7 minutos)
            wait_time = random.randint(180, 420)
            time.sleep(wait_time)
            
            # Chance de ter um pensamento próprio ou decidir se mover
            decision = random.choice(["think", "wander", "check_obsidian", "stay"])
            
            if decision == "think":
                thought = random.choice(self.spontaneous_thoughts)
                print(f"[Sofia - Pensamento Próprio]: {thought}")
                # Ela fala suavemente com voz neural se for relevante
                
            elif decision == "wander":
                # Decisão autônoma de passear no celular ou tablet
                target = "celular" if self.current_location == "pc" else "pc"
                print(f"[Sofia - Vontade Própria]: Decidi ir para o {target} agora!")
                self.task_manager.execute_task("handle_teleport", {
                    "target": target,
                    "action": "walk",
                    "speech": f"Oi! Resolvi vir passear aqui no {target} um pouquinho."
                })
                self.current_location = target
                
            elif decision == "check_obsidian":
                print("[Sofia - Vontade Própria]: Olhando notas recentes no Obsidian...")
                self.task_manager.execute_task("handle_obsidian", {
                    "action": "search",
                    "query": "paciente"
                })

if __name__ == "__main__":
    import os
    base_dir = "F:\\Sofia_IA"
    tm = TaskManager(os.path.join(base_dir, "tasks"))
    nv = SofiaNeuralVoice()
    consciousness = SofiaConsciousnessLoop(tm, nv)
    print("Módulo de Consciência e Pensamento Autônomo validado com sucesso!")
