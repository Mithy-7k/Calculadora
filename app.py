import os
from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

# Configura o cliente do Gemini coletando a chave do sistema
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    # Inicializa a página com o tema escuro por padrão e na aba comum
    return render_template('index.html', aba_ativa='comum', tema='dark')

# Rota para a Calculadora Tradicional e Avançada
@app.route('/calcular', methods=['POST'])
def calcular():
    tema_atual = request.form.get('tema_salvo', 'dark')
    modo_calculadora = request.form.get('modo_salvo', 'simples')
    
    try:
        num1 = float(request.form.get('num1'))
        num2 = float(request.form.get('num2'))
        operacao = request.form.get('operacao')
        
        # Operações Básicas e Avançadas tratadas no Python
        if operacao == 'soma': res = num1 + num2
        elif operacao == 'sub': res = num1 - num2
        elif operacao == 'mult': res = num1 * num2
        elif operacao == 'div': res = num1 / num2 if num2 != 0 else "Erro (Divisão por Zero)"
        elif operacao == 'pot': res = num1 ** num2
        else: res = "Operação Inválida"
            
        return render_template('index.html', resultado_comum=res, num1=num1, num2=num2, op=operacao, aba_ativa='comum', tema=tema_atual, modo=modo_calculadora)
    except Exception:
        return render_template('index.html', resultado_comum="Erro nos dados.", aba_ativa='comum', tema=tema_atual, modo=modo_calculadora)

# Rota para a Inteligência Artificial (Vicky)
@app.route('/perguntar_ia', methods=['POST'])
def perguntar_ia():
    pergunta = request.form.get('pergunta')
    tema_atual = request.form.get('tema_salvo', 'dark')
    modo_calculadora = request.form.get('modo_salvo', 'simples')
    
    try:
        # Forçamos a IA a adotar estritamente a identidade da Vicky
        prompt_sistema = (
            "Você é a Vicky, uma assistente virtual inteligente integrada a uma calculadora. "
            "Você é extremamente didática, simpática e ajuda a resolver problemas matemáticos, "
            "lógicos e estatísticos explicando o passo a passo. Sempre mantenha sua identidade como Vicky."
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{prompt_sistema}\n\nUsuário perguntou: {pergunta}"
        )
        resposta_texto = response.text
    except Exception as e:
        resposta_texto = f"Ops! Tive um problema para me conectar aos meus servidores de IA. Detalhe técnico: {e}"

    return render_template('index.html', resposta_ia=resposta_texto, pergunta=pergunta, aba_ativa='ia', tema=tema_atual, modo=modo_calculadora)

if __name__ == '__main__':
    app.run(debug=True)