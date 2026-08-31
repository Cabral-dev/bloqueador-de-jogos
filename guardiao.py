import psutil
import subprocess
import time
import os

SCRIPT_PRINCIPAL = "main.py"
CAMINHO_PROJETO = r"C:\Bloqueador"

def main_esta_rodando():
    """Verifica se o main.py está em execução no sistema"""
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info.get('cmdline')
            if cmd and any(SCRIPT_PRINCIPAL in arg for arg in cmd):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def iniciar_main():
    """Ressuscita o main.py em segundo plano"""
    caminho_script = os.path.join(CAMINHO_PROJETO, SCRIPT_PRINCIPAL)
    subprocess.Popen(["pythonw", caminho_script], cwd=CAMINHO_PROJETO)

# Loop de vigilância
while True:
    if not main_esta_rodando():
        iniciar_main()
    time.sleep(1) # Checa a cada 1 segundo