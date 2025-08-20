from flask import Flask, request, jsonify, send_file
import weasyprint
from weasyprint import HTML, CSS
import os
import tempfile
from datetime import datetime

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# O formulário HTML será servido como um arquivo estático pelo Vercel
# A rota abaixo é a que a função JavaScript do formulário irá chamar.
@app.route('/gerar-pdf', methods=['POST'])
def gerar_pdf():
    """
    Endpoint para gerar um relatório em PDF a partir de dados JSON.
    O PDF é criado usando a biblioteca WeasyPrint.
    """
    try:
        data = request.get_json()
        
        # Gerar HTML do relatório
        html_content = generate_report_html(data)
        
        # Criar arquivo temporário para o PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            # Converter HTML para PDF
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(tmp_file.name)
            
            # Retornar o arquivo PDF para o navegador
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=f"relatorio_passagem_turno_{data.get('data', 'sem_data')}.pdf",
                mimetype='application/pdf'
            )
            
    except Exception as e:
        # Em caso de erro, retorna uma resposta JSON com a mensagem de erro.
        return jsonify({'error': str(e)}), 500

# Funções de geração de HTML (MANTENHA O SEU CÓDIGO AQUI)
def generate_report_html(data):
    # ... O seu código original para gerar o HTML ...
    data_formatada = data.get('data', '')
    if data_formatada:
        try:
            data_obj = datetime.strptime(data_formatada, '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
        except:
            pass
    # ... etc ...
    # (Mantenha todas as funções de geração de HTML aqui)
    return html_template
    
def generate_equipamentos_html(data):
    # ... seu código ...
    pass
    
def generate_atividades_html(data):
    # ... seu código ...
    pass

def generate_observacoes_html(observacoes):
    # ... seu código ...
    pass