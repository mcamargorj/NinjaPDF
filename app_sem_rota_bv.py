from flask import Flask, render_template, request

#Inicializa o uso do Flask
app = Flask(__name__)

#Cria um dicionário com usuario e senha para login
login_data = {
    'marcelo':'davi',
    'hugo':'pedro',
    'caio':'maria'

}

# Criar a rota para login.html
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Verificar se o usuario e senha estão no dicionário login_data
        if usuario in login_data and login_data[usuario] == senha :
            return render_template('bem_vindo.html', usuario=usuario)
        else:
            return render_template('login.html', mensagem='Usuário ou senha inválidos!')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)


