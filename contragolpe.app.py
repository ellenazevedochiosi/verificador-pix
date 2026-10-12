import streamlit as st
import re

st.set_page_config(
    page_title="Verificador de Segurança PIX",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 18px; }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 20px !important;
        font-weight: bold;
        background-color: #0d6efd;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Verificador de Segurança PIX e Contatos")
st.subheader("Ferramenta de Proteção contra Golpes Virtuais")
st.write("Digite abaixo o **Nome**, **Número de Telefone** ou **Chave PIX** que você recebeu para verificar se há indícios de fraude.")

st.divider()

BASE_GOLPES_CONHECIDOS = {
    "chaves_pix": ["11999999999", "11988887777", "suporte@falsobanco.com", "12345678900"],
    "nomes_suspeitos": ["central de atendimento pix", "suporte whatsapp", "atendimento banco bradesco", "central de seguranca caixa"],
    "termos_alerta": ["urgente", "bloqueio", "sua conta sera cancelada", "mudei de numero"]
}

entrada_usuario = st.text_input(
    "Digite a chave PIX, Número ou Nome para consulta:",
    placeholder="Ex: 11999999999 ou nome do contato"
)

if st.button("🔎 VERIFICAR SEGURANÇA"):
    termo = entrada_usuario.strip().lower()
    if not termo:
        st.warning("⚠️ Por favor, digite algum valor para realizar a verificação.")
    else:
        termo_limpo = re.sub(r'[^a-zA-Z0-9@.]', '', termo)
        eh_chave_suspeita = any(chave in termo_limpo for chave in BASE_GOLPES_CONHECIDOS["chaves_pix"])
        eh_nome_suspeito = any(nome in termo for nome in BASE_GOLPES_CONHECIDOS["nomes_suspeitos"])
        possui_termo_alerta = any(alerta in termo for alerta in BASE_GOLPES_CONHECIDOS["termos_alerta"])
        
        if eh_chave_suspeita or eh_nome_suspeito:
            st.error("🚨 **ALERTA DE ALTO RISCO: POSSÍVEL GOLPE DETECTADO!**")
            st.markdown("""
            **Por que este contato foi sinalizado?**
            * 🔴 Esta chave PIX ou nome está cadastrado em nossa base de alertas de fraudes recentes.
            * 🔴 Instituições financeiras **NUNCA** usam nomes genéricos como "Suporte WhatsApp" ou "Central Pix".
            
            **O que fazer agora?**
            1. **NÃO faça nenhuma transferência de dinheiro.**
            2. Bloqueie o número imediatamente no seu celular.
            """)
        elif possui_termo_alerta:
            st.warning("⚠️ **ATENÇÃO: MENSAGEM COM PADRÃO DE SUSPEITA!**")
            st.markdown("🟡 **Alerta:** Palavras de urgência identificadas. Confirme sempre por outro canal oficial.")
        else:
            st.success("✅ **NENHUM ALERTA DE GOLPE ENCONTRADO PARA ESTE DADO**")
            st.markdown("ℹ️ Mesmo sem alertas na base, confirme sempre o nome do favorecido no aplicativo do banco.")

st.divider()

with st.expander("💡 O que fazer se cair em um golpe?"):
    st.write("1. Contate o banco imediatamente. 2. Peça o acionamento do MED (Mecanismo Especial de Devolução). 3. Registre um B.O.")
    