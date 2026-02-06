import pdfplumber
import pandas as pd
import io
from pdfminer.pdfdocument import PDFPasswordIncorrect

# Adicionamos o parametro 'senha' com valor padrão None
def processar_pdf_para_excel(uploaded_file, senha=None):
    output = io.BytesIO()
    all_data = []
    
    try:
        # Passamos a senha aqui. Se for None, passamos string vazia ou None.
        # O pdfplumber lida bem com password="" para arquivos sem senha, 
        # mas para garantir, usamos lógica ternária.
        password_to_use = senha if senha else ""
        
        with pdfplumber.open(uploaded_file, password=password_to_use) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables({
                    "vertical_strategy": "text", 
                    "horizontal_strategy": "text"
                })
                
                for table in tables:
                    clean_table = [row for row in table if row and any(row)]
                    if clean_table:
                        df_temp = pd.DataFrame(clean_table)
                        all_data.append(df_temp)

    except PDFPasswordIncorrect:
        # Se a senha estiver errada ou faltando, retornamos um erro específico
        return "SENHA_INCORRETA"
        
    except Exception as e:
        # Qualquer outro erro
        return f"ERRO: {str(e)}"

    if not all_data:
        return None

    df_final = pd.concat(all_data, ignore_index=True)
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Dados Extraídos')
    
    output.seek(0)
    return output