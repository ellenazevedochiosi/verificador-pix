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


# Inicializa a base de dados na memória do app (session_state) para acumular denúncias reais
if "df_fraudes" not in st.session_state:
  dados_iniciais = {
      "chave": [
          "27995109581",
          "11999999999",
          "11988887777",
          "11977776666",
          "suporte@falsobanco.com",
      ],
      "denuncias": [
          84,
          120,
          12,
          65,
          90,
      ],  # Acima de 15 já gera alerta de alto risco
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
  st.session_state.df_fraudes = pd.DataFrame(dados_iniciais)

df_fraudes = st.session_state.df_fraudes

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

    # Prepara coluna limpa para busca
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

      # Regra atualizada: Mais de 15 denúncias já dispara o alerta vermelho de alto risco!
      if total_denuncias > 15:
        st.error(
            f"🚨 **ALERTA DE ALTO RISCO: {total_denuncias} DENÚNCIAS"
            " REGISTRADAS!**"
        )
        st.markdown(f"""
                **Detalhes do registro na base de segurança:**
                * 🔴 **Motivo:** {motivo_encontrado}
                * 🔴 Este contato ultrapassou o limite de segurança e acumula **{total_denuncias} denúncias** confirmadas pela comunidade.
                
                **O que fazer agora?**
                1. **NÃO realize nenhuma transferência ou pagamento.**
                2. Bloqueie o contato imediatamente no seu celular.
                """)
      else:
        st.warning(
            f"⚠️ **ATENÇÃO: REGISTRO COM {total_denuncias} DENÚNCIAS.**"
        )
        st.write(
            f"**Detalhe:** {motivo_encontrado}. O número ainda tem poucas"
            " denúncias, mas fique atento."
        )
    else:
      st.success("✅ **NENHUM ALERTA DE GOLPE ENCONTRADO PARA ESTE DADO**")
      st.markdown(
          "ℹ️ Mesmo sem alertas na base de dados, confirme sempre o nome"
          " completo e documento do favorecido diretamente no aplicativo"
          " oficial do seu banco."
      )

st.divider()

# --- SEÇÃO DE FAZER DENÚNCIA INTEGRADA AO BANCO DE DADOS ---
st.subheader("📢 Recebeu uma mensagem suspeita ou chave de golpe?")
with st.expander("🚨 **Clique aqui para registrar uma nova denúncia**"):
  st.write(
      "Ajude a proteger os moradores e idosos do bairro cadastrando uma nova"
      " chave suspeita. Se uma chave receber **mais de 15 denúncias**, ela"
      " passa a ser bloqueada automaticamente no app!"
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
        chave_limpa_nova = re.sub(
            r"[^a-zA-Z0-9@.]", "", chave_denuncia.strip().lower()
        )

        # Verifica se a chave já existe na base da sessão
        filtro_existente = st.session_state.df_fraudes["chave"].str.replace(
            r"[^a-zA-Z0-9@.]", "", regex=True
        ).str.lower() == chave_limpa_nova

        if filtro_existente.any():
          # Se já existe, incrementa +1 denúncia
          st.session_state.df_fraudes.loc[filtro_existente, "denuncias"] += 1
          denuncias_atuais = st.session_state.df_fraudes.loc[
              filtro_existente, "denuncias"
          ].values[0]
          st.success(
              f"✅ **Nova denúncia somada para {chave_denuncia}!** Total atual:"
              f" {denuncias_atuais} denúncias."
          )
        else:
          # Se é nova, adiciona com 16 denúncias iniciais (ou o valor que preferir) para ir direto pro banco com alerta
          nova_linha = pd.DataFrame({
              "chave": [chave_denuncia.strip()],
              "denuncias": [
                  16
              ],  # Entra direto com 16 (>15) para já ativar o alerta na hora
              "motivo": [motivo_denuncia.strip()],
          })
          st.session_state.df_fraudes = pd.concat(
              [st.session_state.df_fraudes, nova_linha], ignore_index=True
          )
          st.success(
              f"✅ **Chave {chave_denuncia} cadastrada e enviada para o banco de"
              " dados com alerta ativo (>15 denúncias)!**"
          )

        st.info("Obrigado por colaborar com a segurança do Bairro Jorge Atalla!")

st.divider()

with st.expander("💡 O que fazer se cair em um golpe?"):
  st.write(
      "1. Contacte o seu banco imediatamente. 2. Peça o acionamento urgente do"
      " MED (Mecanismo Especial de Devolução do PIX). 3. Registre um Boletim de"
      " Ocorrência na Polícia Civil."
  )
