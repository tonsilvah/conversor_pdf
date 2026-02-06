import pdfplumber
import pandas as pd
import io

def processar_pdf_para_excel(uploaded_file):
    # Buffer para o arquivo Excel final
    output = io.BytesIO()
    
    all_data = []
    
    # Abre o PDF direto da memória (sem salvar no disco)
    with pdfplumber.open(uploaded_file) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extrai tabelas. A config 'vertical_strategy' ajuda a detectar colunas por linhas
            tables = page.extract_tables({
                "vertical_strategy": "text", 
                "horizontal_strategy": "text"
            })
            
            for table in tables:
                # Limpeza básica: remove linhas vazias ou muito curtas
                clean_table = [row for row in table if row and any(row)]
                if clean_table:
                    df_temp = pd.DataFrame(clean_table)
                    all_data.append(df_temp)

    if not all_data:
        return None

    # Consolida tudo num único DataFrame
    # Stress Test: E se as tabelas tiverem colunas diferentes?
    # Solução MVP: Concatena tudo. O usuário ajusta no Excel depois.
    df_final = pd.concat(all_data, ignore_index=True)
    
    # Exporta para Excel em memória
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Dados Extraídos')
    
    output.seek(0)
    return output