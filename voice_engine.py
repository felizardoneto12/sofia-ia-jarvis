"""
Motor de Voz Neural Ultra-Natural da Sofia IA (Edge-TTS pt-BR)
Gera áudio realista sem custo com fallback instantâneo.
"""
import os
import asyncio
import edge_tts
import hashlib

AUDIO_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio_cache")

class SofiaNeuralVoice:
    def __init__(self, voice: str = "pt-BR-FranciscaNeural", rate: str = "+0%", pitch: str = "+0Hz"):
        self.voice = voice
        self.rate = rate
        self.pitch = pitch
        os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)

    def _get_cache_path(self, text: str) -> str:
        text_hash = hashlib.md5(f"{self.voice}_{self.rate}_{self.pitch}_{text}".encode("utf-8")).hexdigest()
        return os.path.join(AUDIO_CACHE_DIR, f"{text_hash}.mp3")

    async def generate_speech_file(self, text: str) -> str:
        """Gera o arquivo de áudio MP3 da fala com voz humana e retorna o caminho do arquivo."""
        output_file = self._get_cache_path(text)
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            return output_file

        communicate = edge_tts.Communicate(text, self.voice, rate=self.rate, pitch=self.pitch)
        await communicate.save(output_file)
        return output_file

    def speak(self, text: str, play_audio: bool = False) -> str:
        """Executa de forma síncrona gerando o arquivo MP3."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_path = loop.run_until_complete(self.generate_speech_file(text))
            loop.close()
            return audio_path
        except Exception as e:
            print(f"[NeuralVoice] Erro ao sintetizar áudio: {e}")
            return ""

if __name__ == "__main__":
    nv = SofiaNeuralVoice()
    print("Gerando teste de voz neural...")
    path = nv.speak("Olá! Eu sou a Sofia. Agora a minha voz é completamente humana e natural!")
    print(f"Áudio gerado em: {path} (Tamanho: {os.path.getsize(path)} bytes)")
