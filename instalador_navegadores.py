import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from PIL import Image, ImageTk

def instalar_via_web(navegador):
    try:
        if navegador == "Chrome":
            url = "https://dl.google.com/chrome/install/latest/chrome_installer.exe"
            silent_args = "/silent /install"
        elif navegador == "Firefox":
            url = "https://download.mozilla.org/?product=firefox-latest&os=win&lang=pt-BR"
            silent_args = "-ms"
        elif navegador == "Brave":
            url = "https://laptop-updates.brave.com/latest/winx64"
            silent_args = "/silent /install"
        elif navegador == "Opera":
            url = "https://net.geo.opera.com/opera/stable/windows"
            silent_args = "/silent /install"
        elif navegador == "Edge":
            url = "https://go.microsoft.com/fwlink/?linkid=2108834"
            silent_args = "/silent /install"

        # Atualizar barra de progresso e status para download
        barra_progresso["value"] = 10
        status_label.config(text=f"Baixando instalador do {navegador}...")
        janela.update_idletasks()

        # Baixar o instalador
        subprocess.run(["powershell", "-Command", f"(New-Object System.Net.WebClient).DownloadFile('{url}', '{navegador}.exe')"], check=True)

        # Atualizar barra de progresso e status para instalação
        barra_progresso["value"] = 50
        status_label.config(text=f"Instalando {navegador}...")
        janela.update_idletasks()

        # Executar o instalador no modo silencioso
        subprocess.run([f"{navegador}.exe", silent_args], check=True)

        # Atualizar barra de progresso e status para finalização
        barra_progresso["value"] = 100
        status_label.config(text=f"{navegador} instalado com sucesso!")
        janela.update_idletasks()

        messagebox.showinfo("Sucesso", f"{navegador} foi instalado com sucesso!")
    except Exception as e:
        barra_progresso["value"] = 0
        status_label.config(text=f"Erro ao instalar {navegador}.")
        janela.update_idletasks()
        messagebox.showerror("Erro", f"Erro ao instalar {navegador}: {e}")

def instalar_offline(navegador):
    try:
        # Caminho relativo do instalador offline
        instalador = os.path.join("offline_installers", f"{navegador}.exe")
        if os.path.exists(instalador):
            # Atualizar barra de progresso e status para instalação offline
            barra_progresso["value"] = 50
            status_label.config(text=f"Instalando {navegador} offline...")
            janela.update_idletasks()

            # Executar o instalador
            subprocess.run([instalador, "/silent", "/install"], check=True)

            # Atualizar barra de progresso e status para finalização
            barra_progresso["value"] = 100
            status_label.config(text=f"{navegador} instalado com sucesso!")
            janela.update_idletasks()

            messagebox.showinfo("Sucesso", f"{navegador} foi instalado com sucesso!")
        else:
            barra_progresso["value"] = 0
            status_label.config(text=f"Instalador offline para {navegador} não encontrado.")
            janela.update_idletasks()
            messagebox.showerror("Erro", f"Instalador offline para {navegador} não encontrado.")
    except Exception as e:
        barra_progresso["value"] = 0
        status_label.config(text=f"Erro ao instalar {navegador} offline.")
        janela.update_idletasks()
        messagebox.showerror("Erro", f"Erro ao instalar {navegador}: {e}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Instalador de Navegadores")
janela.geometry("500x400")

# Título
titulo = tk.Label(janela, text="Instalador de Navegadores", font=("Arial", 16))
titulo.pack(pady=10)

# Lista de navegadores
navegadores = ["Chrome", "Firefox", "Brave", "Opera", "Edge"]

# Dicionário para armazenar as logos
logos = {}

# Carregar e redimensionar a logo do Firefox
logo_path = os.path.join("logos", "firefox.png")
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path).resize((32, 32), Image.ANTIALIAS)
    logos["Firefox"] = ImageTk.PhotoImage(logo_image)

for navegador in navegadores:
    frame = tk.Frame(janela)
    frame.pack(pady=5)

    # Adicionar logo se disponível
    if navegador in logos:
        logo_label = tk.Label(frame, image=logos[navegador])
        logo_label.pack(side=tk.LEFT, padx=5)

    label = tk.Label(frame, text=navegador, font=("Arial", 12))
    label.pack(side=tk.LEFT, padx=10)

    btn_web = tk.Button(frame, text="Instalar via Web", command=lambda n=navegador: instalar_via_web(n))
    btn_web.pack(side=tk.LEFT, padx=5)

    btn_offline = tk.Button(frame, text="Instalar Offline", command=lambda n=navegador: instalar_offline(n))
    btn_offline.pack(side=tk.LEFT, padx=5)

# Barra de progresso
barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=400, mode="determinate")
barra_progresso.pack(pady=10)

# Status da instalação
status_label = tk.Label(janela, text="", font=("Arial", 10))
status_label.pack(pady=5)

# Rodapé
rodape = tk.Label(janela, text="Adicione os instaladores offline na pasta 'offline_installers'.", font=("Arial", 10))
rodape.pack(pady=10)

janela.mainloop()