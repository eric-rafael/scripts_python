import os
import sys
import webbrowser
import subprocess
import pyperclip  # Módulo para manipulação da área de transferência

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

# Função para criar links HTML
def criar_link(caminho):
    return f'<a href="#" onclick="copiar_caminho(\'{os.path.dirname(caminho)}\'); return false;">{caminho}</a>'

# Função para copiar o caminho até a pasta do arquivo e mostrar um popup indicando que foi copiado
def copiar_caminho(caminho):
    pyperclip.copy(caminho)
    print("Caminho copiado para a área de transferência.")
    subprocess.Popen(["powershell", "-Command", "Add-Type -AssemblyName PresentationFramework; $popup = [System.Windows.MessageBox]::Show('O caminho foi copiado para a área de transferência.', 'Copiado', 'OK', 'Information'); $timer = New-Object System.Timers.Timer; $timer.Interval = 2000; $timer.Enabled = $true; $timer.AutoReset = $false; $timer.add_Elapsed({$popup.Close(); $timer.Dispose()})"])

# Execute a busca
resultados_encontrados = encontrar_termo(caminho_da_pasta, termo_pesquisado)

if resultados_encontrados:
    print(f"\n\n-------------------------------------\nResultados encontrados para '{termo_pesquisado}':\n-------------------------------------")
    
    # Criar conteúdo HTML com os links
    conteudo_html = "<html><head><title>Resultados da busca</title><script>function copiar_caminho(caminho) {var temp = document.createElement('input');temp.value = caminho;document.body.appendChild(temp);temp.select();document.execCommand('copy');document.body.removeChild(temp);var popup = document.getElementById('popup');popup.style.display = 'block';setTimeout(function(){popup.style.display = 'none';}, 2000);}</script><style>#popup {display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #f4f4f4; padding: 20px; border: 1px solid #ccc;}</style></head><body>"
    conteudo_html += '<div id="popup">O caminho foi copiado para a área de transferência.</div>'
    for resultado in resultados_encontrados:
        conteudo_html += f'<p>{criar_link(resultado)}</p>'
    conteudo_html += "</body></html>"

    # Salvar o conteúdo HTML em um arquivo
    with open("resultados_busca.html", "w", encoding="utf-8") as html_file:
        html_file.write(conteudo_html)

    # Abrir o arquivo HTML no navegador padrão
    webbrowser.open_new_tab("resultados_busca.html")

else:
    print(f"\nNenhum resultado encontrado para '{termo_pesquisado}'.\n")
