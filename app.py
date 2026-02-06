import streamlit as st
from core import processar_pdf_para_excel

st.set_page_config(page_title="PDF Financer", page_icon="📊")

st.title("📊 Extrator de Tabelas Financeiras")
st.markdown("""
Converta faturas e relatórios PDF para Excel em segundos.
**Focado em documentos nativos (não escaneados).**
""")

# Área de Upload
uploaded_file = st.file_uploader("Arraste seu PDF aqui", type="pdf")

if uploaded_file is not None:
    st.info("Processando arquivo... O tempo depende do número de páginas.")
    
    try:
        excel_data = processar_pdf_para_excel(uploaded_file)
        
        if excel_data:
            st.success("Conversão concluída com sucesso!")
            
            # Botão de Download
            st.download_button(
                label="📥 Baixar Planilha Excel",
                data=excel_data,
                file_name="relatorio_extraido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Não encontramos tabelas legíveis neste PDF. Verifique se é um PDF nativo.")
            
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        # Dica de Senior: Logue esse erro internamente para você corrigir depois

st.divider()
st.caption("Desenvolvido para Financeiro e Contabilidade. Versão Beta.")