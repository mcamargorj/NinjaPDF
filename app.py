from flask import Flask, render_template, request, redirect, url_for
import os

# Cria uma instância de aplicativo Flask pronta para ser usada e definir as rotas
# Inicializa o uso do Flask
app = Flask(__name__)

# Para autenticação direto no APP sem banco de dados
login_data = {
    'marcelo': 'davi'
}

# Primeira rota do site, página de login. Chama o template: login.html
@app.route('/', methods=['GET','POST'])
def login():
    # Se o método for POST, pegar as informações do formulário e armazenas nas variáveis usuario e senha
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Condição para verificar o usuário e senha em login_data
        if usuario in login_data and login_data[usuario] == senha :
            return redirect(url_for('bem_vindo', usuario=usuario))
        else:
            return render_template('login.html', mensagem='Usuário ou senha incorretos!')
    return render_template('login.html', mensagem='')

# Agora iremos criar a rota para o template bem_vindo.html
@app.route('/bem_vindo/<usuario>')
def bem_vindo(usuario):
    # Chama o template agora bem_vindo.html
    return render_template('bem_vindo.html', usuario=usuario)

# Agora chamar a função main() para execução do código

if __name__ == '__main__' :
    # Pode-e utilizar com debug app.run(debug)
    app.run()

    


