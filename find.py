# Atual: Popup exibe "Endereço do arquivo foi copiado".
# Anterior: Popup fechado automaticamente após 2 segundos.

import os
import sys
import tkinter as tk
from tkinter import messagebox

# Verifique se o termo de pesquisa e o caminho foram passados como argumentos
if len(sys.argv) != 3:
    print("Uso: python meuscript.py caminho_da_pasta termo_pesquisado")
    sys.exit(1)

caminho_da_pasta = sys.argv[1]
termo_pesquisado = sys.argv[2]

def encontrar_termo(caminho_da_pasta, termo_pesquisado):
    print(f"Iniciando a busca pelo termo '{termo_pesquisado}' em {caminho_da_pasta}")
    resultados = []
    for raiz, diretorios, arquivos in os.walk(caminho_da_pasta):
        print(f"Procurando em: {raiz}")
        # Verifica se o termo está no nome dos diretórios
        resultados.extend(os.path.join(raiz, d) for d in diretorios if termo_pesquisado in d)
        # Verifica se o termo está no nome dos arquivos
        resultados.extend(os.path.join(raiz, f) for f in arquivos if termo_pesquisado in f)
    return resultados

# Função para copiar o caminho até a pasta do arquivo
def copiar_caminho(caminho):
    mensagem = f"Endereço do arquivo {caminho} foi copiado para a área de transferência."
    print(mensagem)
    messagebox.showinfo("Copiado", mensagem)
    root.after(2000, root.destroy)  # Fecha a janela após 2 segundos

# Função para criar a interface gráfica
def criar_interface_grafica():
    root = tk.Tk()
    root.title("Resultados da busca")
    root.configure(background="#1f1f1f")
    root.state('zoomed')  # Abrir maximizado

    frame = tk.Frame(root, bg="#1f1f1f")
    frame.pack(fill=tk.BOTH, expand=True)

    # Adiciona resultados na lista
    for resultado in resultados_encontrados:
        endereco_label = tk.Label(frame, text=resultado, bg="#1f1f1f", fg="#ffffff")
        endereco_label.grid(row=resultados_encontrados.index(resultado), column=0, sticky="w", padx=5, pady=2)

        button = tk.Button(frame, text="Copiar", command=lambda r=resultado: copiar_caminho(r), bg="#4B0082", fg="#ffffff")
        button.grid(row=resultados_encontrados.index(resultado), column=1, sticky="e", padx=5, pady=2)

    root.mainloop()

# Execute a busca
resultados_encontrados = encontrar_termo(caminho_da_pasta, termo_pesquisado)

if resultados_encontrados:
    print(f"\n\n-------------------------------------\nOs resultados encontrados para '{termo_pesquisado}': serão exibidos na interface gráfica maximizada com popup exibindo o endereço do arquivo copiado\n-------------------------------------")
    
    # Criar interface gráfica
    criar_interface_grafica()

else:
    print(f"\nNenhum resultado encontrado para '{termo_pesquisado}'.\n")
