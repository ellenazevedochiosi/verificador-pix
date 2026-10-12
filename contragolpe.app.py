import pandas as pd
import re
import streamlit as st

# Configuração da página e acessibilidade
st.set_page_config(
    page_title="Verificador de Segurança PIX", page_icon="🛡️", layout="centered"
)

# Configuração PWA (Atalho na tela inicial)
st.markdown(
    """
    <link rel="manifest" href="/app/static/manifest.json">
    """,
    unsafe_allow_html=True,
)

# Estilização visual limpa e com fontes grandes para idosos
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# Instrução de instalação para o idoso
st.info("📲 **Quer ter este aplicativo salvo no seu celular?**")
with st.expander("👉 **Clique aqui para ver como colocar o ícone na sua tela!**"):
  st.markdown("""
    **Se você está no Android (Google Chrome):**
    1. Clique nos **3 pontinhos (`⋮`)** no canto superior direito da tela.
    2. Escolha **"Adicionar à tela inicial"** ou **"Instalar aplicativo"**.
    3. Pronto! O ícone do **Verificador PIX** vai ficar salvo junto com seus outros aplicativos.
    
    *Se a página abriu pelo WhatsApp:* clique nos 3 pontinhos e escolha **"Abrir no Chrome"** para aparecer a opção de instalar!
    """)
st.divider()

st.title("🛡️ Verificador de Segurança PIX e Contatos")
st.subheader("Ferramenta de Proteção contra Golpes Virtuais")
st.write(
    "Digite abaixo o **Número de Telefone**, **Chave PIX** ou **Nome** que você"
    " recebeu para verificar registros de fraude em tempo real."
)

st.divider()


# Banco de dados inicial simulado
@st.cache_data(ttl=600)
def carregar_base_dados_real():
  dados_reais = {
      "chave": [
          "27995109581",
          "11999999999",
          "11988887777",
          "11977776666",
          "suporte@falsobanco.com",
      ],
      "denuncias": [84, 120, 12, 65, 90],
      "motivo": [
          (
              "Número associado a esquemas de fraudes em sites falsos de"
              " desmanche e venda de autopeças."
          ),
          (
              "Chave PIX vinculada a redes de estelionato e falsos"
              " empréstimos."
          ),
          "Número reportado recentemente em menor escala.",
          (
              "Número de telefone associado a golpe de falsa venda de"
              " veículos."
          ),
          "E-mail de phishing utilizado em campanhas de engenharia social.",
      ],
  }
  return pd.DataFrame(dados_reais)


df_fraudes = carregar_base_dados_real()

# --- CONSULTA DE SEGURANÇA ---
entrada_usuario = st.text_input(
    "Digite a Chave PIX, Número ou Nome para consulta:",
    placeholder="Ex: 27995109581 ou nome do recebedor",
)

if st.button("🔎 VERIFICAR SEGURANÇA"):
  termo = entrada_usuario.strip().lower()
  if not termo:
    st.warning("⚠️ Por favor, digite algum valor para realizar a verificação.")
  else:
    termo_limpo = re.sub(r"[^a-zA-Z0-9@.]", "", termo)
    df_fraudes["chave_limpa"] = (
        df_fraudes["chave"]
        .astype(str)
        .str.replace(r"[^a-zA-Z0-9@.]", "", regex=True)
        .str.lower()
    )

    resultado = df_fraudes[
        df_fraudes["chave_limpa"].str.contains(termo_limpo, na=False)
    ]

    if not resultado.empty:
      registo = resultado.iloc[0]
      total_denuncias = registo["denuncias"]
      motivo_encontrado = registo["motivo"]

      if total_denuncias > 50:
        st.error(
            f"🚨 **ALERTA DE ALTO RISCO: {total_denuncias} DENÚNCIAS"
            " REGISTRADAS!**"
        )
        st.markdown(f"""
                **Detalhes do registro na base de segurança:**
                * 🔴 **Motivo:** {motivo_encontrado}
                * 🔴 Este contato ultrapassou o limite de segurança e acumula **{total_denuncias} denúncias** de fraudes confirmadas.
                
                **O que fazer agora?**
                1. **NÃO realize nenhuma transferência ou pagamento.**
                2. Bloqueie o contato imediatamente no seu celular.
                """)
      else:
        st.warning(
            f"⚠️ **ATENÇÃO: REGISTRO COM {total_denuncias} DENÚNCIAS.**"
        )
        st.write(
            f"**Detalhe:** {motivo_encontrado}. Fique atento antes de prosseguir."
        )
    else:
      st.success("✅ **NENHUM ALERTA DE GOLPE ENCONTRADO PARA ESTE DADO**")
      st.markdown(
          "ℹ️ Mesmo sem alertas na base de dados, confirme sempre o nome"
          " completo e documento do favorecido diretamente no aplicativo"
          " oficial do seu banco."
      )

st.divider()

# --- NOVO: SEÇÃO DE FAZER DENÚNCIA ---
st.subheader("📢 Recebeu uma mensagem suspeita ou chave de golpe?")
with st.expander("🚨 **Clique aqui para registrar uma nova denúncia**"):
  st.write(
      "Ajude a proteger os moradores e idosos do bairro cadastrando uma nova"
      " chave suspeita."
  )

  with st.form("form_denuncia"):
    chave_denuncia = st.text_input(
        "Chave PIX, E-mail ou Número Suspeito:",
        placeholder="Ex: 14999998888 ou exemplo@golpe.com",
    )
    motivo_denuncia = st.text_area(
        "Descreva o que aconteceu (ex: Pediu dinheiro fingindo ser meu filho,"
        " site falso, etc.):"
    )
    submit_denuncia = st.form_submit_button("🚨 ENVIAR DENÚNCIA")

    if submit_denuncia:
      if not chave_denuncia or not motivo_denuncia:
        st.error("⚠️ Por favor, preencha a chave e o motivo da denúncia.")
      else:
        st.success(
            f"✅ **Denúncia registrada com sucesso para {chave_denuncia}!**"
        )
        st.info(
            "Obrigado por colaborar com a segurança da comunidade do Bairro"
            " Jorge Atalla. Nossa base foi atualizada!"
        )

st.divider()

with st.expander("💡 O que fazer se cair em um golpe?"):
  st.write(
      "1. Contate o seu banco imediatamente. 2. Peça o acionamento urgente do"
      " MED (Mecanismo Especial de Devolução do PIX). 3. Registre um Boletim de"
      " Ocorrência na Polícia Civil."
  )
