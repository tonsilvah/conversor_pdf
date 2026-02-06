import streamlit as st
from core import processar_pdf_para_excel

st.set_page_config(page_title="PDF Financer", page_icon="📊")

st.title("📊 Extrator de Tabelas Financeiras")

# ... (seu texto de intro) ...

uploaded_file = st.file_uploader("Arraste seu PDF aqui", type="pdf")

if uploaded_file is not None:
    
    # NOVO: Campo de senha
    st.markdown("### 🔒 O arquivo possui senha?")
    pdf_password = st.text_input("Se o PDF tiver senha (ex: CPF/CNPJ), digite abaixo:", type="password")
    
    # Botão para iniciar o processamento (opcional, mas bom UX quando tem senha)
    if st.button("Processar Arquivo"):
        st.info("Processando...")
        
        # Chama a função passando a senha
        resultado = processar_pdf_para_excel(uploaded_file, senha=pdf_password)
        
        # Checagem de erros
        if resultado == "SENHA_INCORRETA":
            st.error("⛔ A senha está incorreta ou o arquivo exige uma senha que não foi informada.")
        elif isinstance(resultado, str) and resultado.startswith("ERRO"):
            st.error(f"Ocorreu um problema: {resultado}")
        elif resultado is None:
            st.warning("Não encontramos tabelas legíveis neste PDF.")
        else:
            st.success("Conversão concluída!")
            st.download_button(
                label="📥 Baixar Planilha Excel",
                data=resultado,
                file_name="relatorio_extraido.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )