from flask import Flask, request, jsonify, send_file
import weasyprint
from weasyprint import HTML, CSS
import os
import tempfile
from datetime import datetime

# Cria a instância principal do aplicativo Flask
app = Flask(__name__)

# A rota abaixo é a que a função JavaScript do formulário irá chamar.
@app.route('/api/gerar-pdf', methods=['POST'])
def gerar_pdf():
    """
    Endpoint para gerar um relatório em PDF a partir de dados JSON.
    O PDF é criado usando a biblioteca WeasyPrint.
    """
    try:
        data = request.get_json()
        
        html_content = generate_report_html(data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(tmp_file.name)
            
            return send_file(
                tmp_file.name,
                as_attachment=True,
                download_name=f"relatorio_passagem_turno_{data.get('data', 'sem_data')}.pdf",
                mimetype='application/pdf'
            )
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# (Seu código original para as funções de geração de HTML deve ser mantido aqui,
# com a imagem da logo ajustada para ser referenciada pelo Vercel, se necessário)
def generate_report_html(data):
    # Seu código original para esta função
    data_formatada = data.get('data', '')
    if data_formatada:
        try:
            data_obj = datetime.strptime(data_formatada, '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
        except:
            pass
            
    # As suas funções que geram as tabelas...
    equipamentos_html = generate_equipamentos_html(data)
    atividades_html = generate_atividades_html(data)
    observacoes_html = generate_observacoes_html(data.get('observacoes', []))
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Passagem de Turno - Energy Center</title>
        <style>
            @page {{
                margin: 2cm;
                size: A4;
            }}
            
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #000;
                background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 50%, #e6f2ff 100%);
                margin: 0;
                padding: 20px;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #2c5aa0 0%, #4a7bc8 100%);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(44, 90, 160, 0.2);
            }}
            
            .logo {{
                max-width: 300px;
                height: auto;
                margin-bottom: 20px;
            }}
            
            h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 28px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            
            .info-section {{
                background: #ffffff;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                border-left: 5px solid #2c5aa0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .info-section strong {{
                color: #2c5aa0;
            }}
            
            h2 {{
                color: #2c5aa0;
                border-bottom: 2px solid #4a7bc8;
                padding-bottom: 10px;
                margin-top: 30px;
                font-size: 22px;
            }}
            
            h3 {{
                color: #2c5aa0;
                margin-top: 25px;
                font-size: 18px;
            }}
            
            h4 {{
                color: #4a7bc8;
                margin-top: 20px;
                font-size: 16px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                background: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            th {{
                background: linear-gradient(135deg, #2c5aa0 0%, #4a7bc8 100%);
                color: #ffffff;
                padding: 12px;
                text-align: left;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}
            
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #e6f2ff;
                color: #000;
            }}
            
            tr:nth-child(even) {{
                background: #f8fbff;
            }}
            
            tr:hover {{
                background: #e6f2ff;
            }}
            
            .status-realizada {{
                color: #2c5aa0;
                font-weight: bold;
            }}
            
            .status-pendente {{
                color: #ff8c00;
                font-weight: bold;
            }}
            
            .status-nao-realizada {{
                color: #dc3545;
                font-weight: bold;
            }}
            
            .observacoes {{
                background: #f8fbff;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                border: 1px solid #e6f2ff;
            }}
            
            .observacoes ul {{
                margin: 0;
                padding-left: 20px;
            }}
            
            .observacoes li {{
                margin: 10px 0;
                color: #000;
            }}
            
            hr {{
                border: none;
                height: 2px;
                background: linear-gradient(135deg, #2c5aa0 0%, #4a7bc8 100%);
                margin: 30px 0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="https://i.ibb.co/6P01vQj/Stellantis-Logo2.jpg" alt="Stellantis Logo" class="logo">
            <h1>RELATÓRIO DE PASSAGEM DE TURNO - ENERGY CENTER</h1>
        </div>
        
        <div class="info-section">
            <strong>Data:</strong> {data_formatada}<br>
            <strong>Turno:</strong> {data.get('turno', '')}<br>
            <strong>Líder presente:</strong> {data.get('liderPresente', '')}<br>
            <strong>Absenteísmo:</strong> {data.get('absenteismo', '')}<br>
            <strong>Líder próximo turno:</strong> {data.get('liderProximoTurno', '')}
        </div>
        
        {equipamentos_html}
        
        {atividades_html}
        
        {observacoes_html}
    </body>
    </html>
    """
    
    return html_template

def generate_equipamentos_html(data):
    # ... seu código aqui
    html = """
    <h2>1. STATUS DOS EQUIPAMENTOS</h2>
    <h3>1.1 Energy Center</h3>
    <h4>Compressores</h4>
    <table>
        <thead>
            <tr>
                <th>Equipamentos</th>
                <th>Status</th>
                <th>Observações</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Compressores
    if data.get('compressoresOperacao'):
        html += f"""
            <tr>
                <td>{data.get('compressoresOperacao', '')}</td>
                <td>Em operação</td>
                <td>{data.get('compressoresObs', '-')}</td>
            </tr>
        """
    if data.get('compressoresBackup'):
        html += f"""
            <tr>
                <td>{data.get('compressoresBackup', '')}</td>
                <td>Backup</td>
                <td>{data.get('compressoresObs', '-')}</td>
            </tr>
        """
    if data.get('compressoresManutencao'):
        html += f"""
            <tr>
                <td>{data.get('compressoresManutencao', '')}</td>
                <td>Em manutenção</td>
                <td>{data.get('compressoresObs', '-')}</td>
            </tr>
        """
    if data.get('compressoresSP'):
        html += f"""
            <tr>
                <td><strong>{data.get('compressoresSP', '')} Bar</strong></td>
                <td><strong>SP</strong></td>
                <td>-</td>
            </tr>
        """
    html += """
        </tbody>
    </table>
    """
    
    # Torres
    html += """
    <h4>Torres</h4>
    <table>
        <thead>
            <tr>
                <th>Equipamentos</th>
                <th>Status</th>
                <th>Observações</th>
            </tr>
        </thead>
        <tbody>
    """
    
    if data.get('torresOperacao'):
        html += f"""
            <tr>
                <td>{data.get('torresOperacao', '')}</td>
                <td>Em operação</td>
                <td>{data.get('torresObs', '-')}</td>
            </tr>
        """
    if data.get('torresBackup'):
        html += f"""
            <tr>
                <td>{data.get('torresBackup', '')}</td>
                <td>Backup</td>
                <td>{data.get('torresObs', '-')}</td>
            </tr>
        """
    if data.get('torresManutencao'):
        html += f"""
            <tr>
                <td>{data.get('torresManutencao', '')}</td>
                <td>Em manutenção</td>
                <td>{data.get('torresObs', '-')}</td>
            </tr>
        """
    html += """
        </tbody>
    </table>
    """
    
    # Continuar com outros equipamentos...
    # (Secadores, Chillers, Bombas CW, Bombas CHW, Central de Ar)
    
    return html

def generate_atividades_html(data):
    # ... seu código aqui
    html = """
    <hr>
    <h2>2. ATIVIDADES PROGRAMADAS</h2>
    """
    
    # Mecânica
    if data.get('mecanicaOrdem'):
        html += """
        <h3>2.1 Mecânica</h3>
        <table>
            <thead>
                <tr>
                    <th>Ordem</th>
                    <th>Descrição</th>
                    <th>Status</th>
                    <th>Observações</th>
                </tr>
            </thead>
            <tbody>
        """
        
        ordens = data.get('mecanicaOrdem', [])
        descricoes = data.get('mecanicaDescricao', [])
        status = data.get('mecanicaStatus', [])
        observacoes = data.get('mecanicaObservacoes', [])
        
        for i in range(len(ordens)):
            if ordens[i]:  # Só adiciona se tiver ordem
                status_class = ""
                if i < len(status):
                    if "Realizada" in status[i]:
                        status_class = "status-realizada"
                    elif "Pendente" in status[i]:
                        status_class = "status-pendente"
                    elif "Não realizada" in status[i]:
                        status_class = "status-nao-realizada"
                        
                html += f"""
                <tr>
                    <td>{ordens[i]}</td>
                    <td>{descricoes[i] if i < len(descricoes) else ''}</td>
                    <td class="{status_class}">{status[i] if i < len(status) else ''}</td>
                    <td>{observacoes[i] if i < len(observacoes) else '-'}</td>
                </tr>
                """
        
        html += """
            </tbody>
        </table>
        """
        
    # Elétrica
    if data.get('eletricaOrdem'):
        html += """
        <h3>2.2 Elétrica</h3>
        <table>
            <thead>
                <tr>
                    <th>Ordem</th>
                    <th>Descrição</th>
                    <th>Status</th>
                    <th>Observações</th>
                </tr>
            </thead>
            <tbody>
        """
        
        ordens = data.get('eletricaOrdem', [])
        descricoes = data.get('eletricaDescricao', [])
        status = data.get('eletricaStatus', [])
        observacoes = data.get('eletricaObservacoes', [])
        
        for i in range(len(ordens)):
            if ordens[i]:  # Só adiciona se tiver ordem
                status_class = ""
                if i < len(status):
                    if "Realizada" in status[i]:
                        status_class = "status-realizada"
                    elif "Pendente" in status[i]:
                        status_class = "status-pendente"
                    elif "Não realizada" in status[i]:
                        status_class = "status-nao-realizada"
                        
                html += f"""
                <tr>
                    <td>{ordens[i]}</td>
                    <td>{descricoes[i] if i < len(descricoes) else ''}</td>
                    <td class="{status_class}">{status[i] if i < len(status) else ''}</td>
                    <td>{observacoes[i] if i < len(observacoes) else '-'}</td>
                </tr>
                """
        
        html += """
            </tbody>
        </table>
        """
        
    # Atividades Extras
    if data.get('extraOrdem'):
        html += """
        <hr>
        <h2>3. ATIVIDADES EXTRAS</h2>
        <table>
            <thead>
                <tr>
                    <th>Ordem</th>
                    <th>Descrição</th>
                    <th>Status</th>
                    <th>Observações</th>
                </tr>
            </thead>
            <tbody>
        """
        
        ordens = data.get('extraOrdem', [])
        descricoes = data.get('extraDescricao', [])
        status = data.get('extraStatus', [])
        observacoes = data.get('extraObservacoes', [])
        
        for i in range(len(ordens)):
            if ordens[i]:  # Só adiciona se tiver ordem
                status_class = ""
                if i < len(status):
                    if "Realizada" in status[i]:
                        status_class = "status-realizada"
                    elif "Pendente" in status[i]:
                        status_class = "status-pendente"
                    elif "Não realizada" in status[i]:
                        status_class = "status-nao-realizada"
                        
                html += f"""
                <tr>
                    <td>{ordens[i]}</td>
                    <td>{descricoes[i] if i < len(descricoes) else ''}</td>
                    <td class="{status_class}">{status[i] if i < len(status) else ''}</td>
                    <td>{observacoes[i] if i < len(observacoes) else '-'}</td>
                </tr>
                """
        
        html += """
            </tbody>
        </table>
        """
        
    return html

def generate_observacoes_html(observacoes):
    # ... seu código aqui
    if not observacoes:
        return ""
        
    html = """
    <hr>
    <h2>4. OBSERVAÇÕES IMPORTANTES</h2>
    <div class="observacoes">
        <ul>
    """
    
    for obs in observacoes:
        html += f"<li>{obs}</li>"
        
    html += """
        </ul>
    </div>
    """
    
    return html