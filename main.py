from enum import Enum
import psutil
import time
from datetime import datetime
from tkinter import Tk, Label, Toplevel
import os
import subprocess

class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

root = Tk()
root.withdraw()

JOGOS = { 
    "robloxplayerbeta.exe", 
    "hydra.exe",
    "minecraft.exe",
    "tlauncher.exe",
    "steam.exe"
}

ARQUIVO_LOG = os.path.join(os.path.expanduser("~"), "historico_de_foco.txt")
SCRIPT_GUARDIAO = "guardiao.py"

def garantir_guardiao_rodando():
    """Verifica se o guardiao.py está vivo, se não estiver, ressuscita ele"""
    guardiao_rodando = False
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info.get('cmdline')
            if cmd and any(SCRIPT_GUARDIAO in arg for arg in cmd):
                guardiao_rodando = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
    if not guardiao_rodando:
        caminho_guardiao = os.path.join(r"C:\Bloqueador", SCRIPT_GUARDIAO)
        subprocess.Popen(["pythonw", caminho_guardiao], cwd=r"C:\Bloqueador")

def registrar_tentativa(nome_jogo):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{agora}] Tentativa bloqueada: {nome_jogo}\n")
    except Exception as e:
        print(f"Erro ao salvar log: {e}")

def eh_horario_de_estudo():
    agora = datetime.now()
    
    if agora.weekday() >= Weekday.SATURDAY.value:
        return False
    
    minuto_limite = 0 if agora.weekday() == Weekday.FRIDAY.value else 30
    
    inicio = (6, 0)
    fim = (19, minuto_limite)
    atual = (agora.hour, agora.minute)
    
    return inicio <= atual <= fim

janela_aviso_atual = None

def mostrar_aviso(mensagem):
    global janela_aviso_atual
    
    if janela_aviso_atual is not None:
        try:
            if janela_aviso_atual.winfo_exists():
                janela_aviso_atual.attributes('-topmost', True)
                janela_aviso_atual.lift()
                janela_aviso_atual.focus_force()
                return
        except Exception:
            pass

    janela_aviso_atual = Toplevel(root)
    janela_aviso_atual.title("ACESSO NEGADO")
    
    largura, altura = 450, 180
    largura_tela = janela_aviso_atual.winfo_screenwidth()
    altura_tela = janela_aviso_atual.winfo_screenheight()
    pos_x = int((largura_tela / 2) - (largura / 2))
    pos_y = int((altura_tela / 2) - (altura / 2))
    
    janela_aviso_atual.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    janela_aviso_atual.attributes('-topmost', True)
    janela_aviso_atual.resizable(False, False)
    janela_aviso_atual.focus_force()

    lbl = Label(
        janela_aviso_atual, 
        text=mensagem, 
        font=("Arial", 11, "bold"), 
        fg="red", 
        justify="center",
        pady=20
    )
    lbl.pack(expand=True)

def varredura_implacavel():
    for processo in psutil.process_iter(['name']):
        try:
            nome = str(processo.info['name']).lower()
            
            if nome in JOGOS:
                processo.kill()
                registrar_tentativa(nome)
                
                agora = datetime.now()
                limite = "19:00" if agora.weekday() == Weekday.FRIDAY.value else "19:30"
                mensagem = f"⛔ FOCO TOTAL!\n\nO jogo '{nome}' foi encerrado.\nBloqueio ativo até às {limite}.\n\nVolte para os livros!"
                
                mostrar_aviso(mensagem)
                time.sleep(1)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# Loop principal
while True:
    garantir_guardiao_rodando()
    
    if eh_horario_de_estudo():
        varredura_implacavel()

    root.update()
    time.sleep(3)