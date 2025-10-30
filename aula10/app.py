from flask import Flask, render_template, request

# Inicializa a aplicação Flask
app = Flask(__name__)


# Rota para a página inicial (métodos GET e POST)
# O método GET exibe o formulário.
# O método POST processa os dados do formulário.
@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # Inicializa a variável do resultado como nula

    if request.method == "POST":
        try:
            # Obtém os dados do formulário
            num1 = float(request.form.get("num1"))
            num2 = float(request.form.get("num2"))
            operation = request.form.get("operation")

            # Realiza a operação com base na seleção do usuário
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    result = "Erro: Divisão por zero!"
                else:
                    result = num1 / num2
            else:
                result = "Operação inválida!"
        except (ValueError, TypeError):
            result = "Erro: Por favor, insira números válidos."

    # Renderiza o template, passando o resultado (se existir)
    return render_template("index.html", result=result)


# Inicia o servidor web
if __name__ == "__main__":
    app.run(debug=True)
