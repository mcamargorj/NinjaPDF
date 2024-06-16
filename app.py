from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import pikepdf

app = Flask(__name__)
app.secret_key = os.urandom(24)

DIRETORIO_UPLOADS = 'uploads'


app.config['DIRETORIO_UPLOADS'] = DIRETORIO_UPLOADS
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16 MB para uploads

# Certifique-se de que o diretório de uploads exista
os.makedirs(DIRETORIO_UPLOADS, exist_ok=True)

# Definindo a variável global
arquivo_gerado = None

def extensao_permitida(arquivo):
    return '.' in arquivo and arquivo.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/', methods=['POST'])
def upload_arquivo():
 
    if 'arquivo' not in request.files:
        mensagem_erro = 'Nenhum arquivo enviado.'
        return redirect(url_for('formulario_upload', erro=mensagem_erro))

    arquivo = request.files['arquivo'] 
      
    if arquivo.filename == '':
        mensagem_erro = 'Nenhum arquivo selecionado.'
        return redirect(url_for('formulario_upload', erro=mensagem_erro))
    
    if not extensao_permitida(arquivo.filename):
        mensagem_erro = 'Extensão inválida!'
        limpar()
        return redirect(url_for('formulario_upload', erro=mensagem_erro))
    
    nome_arquivo = arquivo.filename
    caminho_arquivo = os.path.join(app.config['DIRETORIO_UPLOADS'], nome_arquivo)
    arquivo.save(caminho_arquivo)

    session['arquivo_enviado'] = nome_arquivo
    session['sucesso'] = "Enviado com sucesso!"
    arquivo_enviado = session.get('arquivo_enviado')


 
    return render_template('upload.html', arquivo_enviado=arquivo_enviado, sucesso=session['sucesso'])


@app.route('/processar', methods=['POST'])
def processar_arquivos():
    global arquivo_gerado
    
    """Rota para processar os arquivos enviados."""
    try:
        senha = request.form.get('senha')
        print(f'Senha recebida: {senha}')  # Adiciona mensagem de depuração
        
        arquivo_enviado = session.get('arquivo_enviado')

        if arquivo_enviado:
            dir_uploads = app.config['DIRETORIO_UPLOADS']
            nome_arquivo_saida = 'pdf_desbloqueado.pdf'
            caminho_arquivo_saida = os.path.join(dir_uploads, nome_arquivo_saida)

            if arquivo_enviado.endswith('.pdf'):
                caminho_arquivo = os.path.join(dir_uploads, arquivo_enviado)
                
                try:
                    # Tentar abrir o PDF sem senha
                    with pikepdf.open(caminho_arquivo) as pdf:
                        # Salvar o PDF sem restrições
                        pdf.save(caminho_arquivo_saida)
                        print(f'PDF salvo em: {caminho_arquivo_saida}')  # Adicionar mensagem de depuração
                except pikepdf.PasswordError:
                    # Se a exceção PasswordError for levantada, o arquivo está protegido por senha
                    if not senha or senha == "":
                        # Redirecionar de volta para a página de upload com mensagem de erro
                        mensagem_erro = 'Este arquivo requer <br> uma senha para desbloqueio.'
                        return redirect(url_for('formulario_upload', erro=mensagem_erro))
                    else:
                        try:
                            # Tentar abrir o PDF com a senha fornecida
                            with pikepdf.open(caminho_arquivo, password=senha) as pdf:
                                # Salvar o PDF sem restrições
                                pdf.save(caminho_arquivo_saida)
                                print(f'PDF salvo em: {caminho_arquivo_saida}')  # Adicionar mensagem de depuração
                        except pikepdf.PasswordError:
                            # Senha incorreta
                            mensagem_erro = 'Senha incorreta!'
                            return redirect(url_for('formulario_upload', erro=mensagem_erro))
                        except Exception as e:
                            print(f'Ocorreu um erro ao tentar abrir o PDF: {e}')
                            mensagem_erro = 'Erro ao processar o arquivo.'
                            return redirect(url_for('formulario_upload', erro=mensagem_erro))
                except Exception as e:
                    print(f'Ocorreu um erro ao tentar abrir o PDF: {e}')
                    mensagem_erro = 'Erro ao processar o arquivo.'
                    return redirect(url_for('formulario_upload', erro=mensagem_erro))

            arquivo_gerado = caminho_arquivo_saida  # Definindo o arquivo gerado
            return redirect(url_for('formulario_upload', download_file=arquivo_gerado))
        else:
            mensagem_erro = 'Selecione o arquivo!'
            limpar()
            return redirect(url_for('formulario_upload', erro=mensagem_erro))
    except Exception as e:
        print(f'Ocorreu um erro: {e}')
        mensagem_erro = 'Erro ao processar o arquivo.'
        limpar()
        return redirect(url_for('formulario_upload', erro=mensagem_erro))



@app.route('/', methods=['GET'])
def formulario_upload():
    global arquivo_gerado
    arquivo_enviado = session.get('arquivo_enviado')
    download_file = request.args.get('download_file')

    if download_file:
        return render_template('upload.html', sucesso="Arquivo Gerado!", arquivo_gerado=arquivo_gerado, arquivo_enviado=arquivo_enviado)
    if not arquivo_enviado: 
        erro = request.args.get('erro')
        return render_template('upload.html', erro=erro)
    else:
        erro = request.args.get('erro')
        return render_template('senha.html', erro=erro, arquivo_enviado=arquivo_enviado)

@app.route('/download')
def download_base():
    global arquivo_gerado
    if arquivo_gerado is not None:
        enviar = send_file(arquivo_gerado, as_attachment=True)
        limpar()
        return enviar
    else:
        erro = "Selecione o arquivo!"
        return render_template('upload.html', erro=erro)
    
@app.route('/restaurar')
def restaurar():
    global arquivo_gerado
    if arquivo_gerado is not None:
        limpar()
        return redirect(url_for('upload_arquivo'))
    else:
        limpar()
        return redirect(url_for('upload_arquivo'))

def limpar():
    """Limpa a pasta de uploads e a lista de arquivos enviados."""
    for arquivo in os.listdir(app.config['DIRETORIO_UPLOADS']):
        os.remove(os.path.join(app.config['DIRETORIO_UPLOADS'], arquivo))
    session['arquivo_enviado'] = []  # Define a lista de arquivos enviados como vazia
    global arquivo_gerado
    arquivo_gerado = None

if __name__ == '__main__':
    app.run(debug=True)
