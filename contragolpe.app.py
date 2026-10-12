import re
import pandas as pd
import streamlit as st

# Configuração da página e acessibilidade
st.set_page_config(
    page_title="Verificador de Segurança PIX, Contatos e Sites",
    page_icon="🛡️",
    layout="centered",
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

st.title("🛡️ Verificador de Segurança PIX, Contatos e Sites")
st.subheader("Ferramenta de Proteção contra Golpes Virtuais")
st.write(
    "Digite abaixo a **Chave PIX**, **Telefone**, **Nome**, **CNPJ/CPF** ou"
    " **Endereço do Site** para verificar se há registros de fraude."
)

st.divider()

# Lista Completa do Procon-SP + Chaves de Testes Locais
PROCON_E_FRAUDES_COMPLETO = [
    # Chaves PIX e Telefones de Testes
    (
        "27995109581",
        84,
        "Número associado a esquemas de fraudes em sites falsos de desmanche e"
        " venda de autopeças.",
    ),
    (
        "11999999999",
        120,
        "Chave PIX vinculada a redes de estelionato e falsos empréstimos.",
    ),
    ("11988887777", 12, "Número reportado recentemente em menor escala."),
    # Registros do Procon-SP
    (
        "123importados.com",
        150,
        "Site na lista 'Evite estes Sites' do PROCON-SP (Online Intermediações e"
        " Comércio Ltda).",
    ),
    (
        "35912902000189",
        150,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (Online Intermediações e"
        " Comércio Ltda / 123importados.com).",
    ),
    (
        "123multiofertas.com.br",
        95,
        "Site na lista 'Evite estes Sites' do PROCON-SP (WE HUB NEGÓCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "123multiofertas.net",
        90,
        "Site na lista 'Evite estes Sites' do PROCON-SP (WE HUB NEGÓCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "47876836000118",
        95,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (WE HUB NEGÓCIOS"
        " DIGITAIS LTDA / 123multiofertas).",
    ),
    (
        "acessivelmodasbras.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (J.W.G.DOS SANTOS COM E"
        " CONF).",
    ),
    (
        "41670743000156",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (J.W.G.DOS SANTOS COM E"
        " CONF).",
    ),
    (
        "agachecomercial.net",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (Eline Ferraz Cruz"
        " Franco).",
    ),
    (
        "40037869000125",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (Eline Ferraz Cruz"
        " Franco).",
    ),
    (
        "allprinter.com.br",
        60,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ALL PRINTER LTDA).",
    ),
    (
        "46189271000138",
        60,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ALL PRINTER LTDA).",
    ),
    (
        "ascarishop.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (DROP AGENCY LTDA).",
    ),
    (
        "42154916000146",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (DROP AGENCY LTDA).",
    ),
    (
        "bmjbaby.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (BMJ COM E SERV DE"
        " ARTIGOS INFANTIS LTDA).",
    ),
    (
        "34657443000171",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (BMJ COM E SERV DE"
        " ARTIGOS INFANTIS LTDA).",
    ),
    (
        "boavistaacabamentos.com",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (SAULO DE OLIVEIRA"
        " FERREIRA).",
    ),
    (
        "46189241000121",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (SAULO DE OLIVEIRA"
        " FERREIRA).",
    ),
    (
        "boticamaviris.com.br",
        25,
        "Site na lista 'Evite estes Sites' do PROCON-SP (JA FERREIRA SELANI"
        " ASSESSORIA ADM LTDA).",
    ),
    (
        "33519131000139",
        25,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (JA FERREIRA SELANI"
        " ASSESSORIA ADM LTDA).",
    ),
    (
        "brasilmagazine.com",
        55,
        "Site na lista 'Evite estes Sites' do PROCON-SP (MATEUS REIS VENUTO).",
    ),
    (
        "38275330000162",
        55,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (MATEUS REIS VENUTO).",
    ),
    (
        "brezzy.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (SIMOA FERREIRA DE"
        " SOUZA).",
    ),
    (
        "35838744000164",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (SIMOA FERREIRA DE"
        " SOUZA).",
    ),
    (
        "caixamisteriosa.com",
        70,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GRUPO ECOM BRASIL"
        " LTDA).",
    ),
    (
        "36716138000139",
        70,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GRUPO ECOM BRASIL"
        " LTDA).",
    ),
    (
        "casadonatebrasil.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (YURI DA SILVA"
        " MACHADO).",
    ),
    (
        "47231669000158",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (YURI DA SILVA"
        " MACHADO).",
    ),
    (
        "casakith.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GABRIEL OLIVEIRA DO"
        " CARMO).",
    ),
    (
        "48852510000113",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GABRIEL OLIVEIRA DO"
        " CARMO).",
    ),
    (
        "casamagazinebrasil.com",
        65,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ANTONIO ALEXANDRE DE"
        " CARVALHO E SOUSA JR).",
    ),
    (
        "48855323000193",
        65,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ANTONIO ALEXANDRE DE"
        " CARVALHO E SOUSA JR).",
    ),
    (
        "centroofertas.com.br",
        80,
        "Site na lista 'Evite estes Sites' do PROCON-SP (N TECH NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "40502690000100",
        80,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (N TECH NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "cintosbyhi.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (BYHI CONFECÇÕES LTDA).",
    ),
    (
        "42535486000102",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (BYHI CONFECÇÕES LTDA).",
    ),
    (
        "cogumeloshop.com",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (CS PRODUTOS ELETRONICOS"
        " LTDA).",
    ),
    (
        "36146120000149",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (CS PRODUTOS ELETRONICOS"
        " LTDA).",
    ),
    (
        "comandantedasofertas.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP"
        " (comandantedasofertas.com).",
    ),
    (
        "compufree.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (COMPUFREE INFORMÁTICA"
        " LTDA).",
    ),
    (
        "07124694000118",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (COMPUFREE INFORMÁTICA"
        " LTDA).",
    ),
    (
        "dbellestore.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ENVIA TENIS LTDA).",
    ),
    (
        "48161625000161",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ENVIA TENIS LTDA).",
    ),
    (
        "descontosbrasileiro.com",
        60,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LIND PROMOÇÃO DE"
        " VENDAS LTDA).",
    ),
    (
        "41740062000117",
        60,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (LIND PROMOÇÃO DE"
        " VENDAS LTDA).",
    ),
    (
        "drogariamc.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (TH COMERCIO DA CIDADE"
        " ALEGRIA LTDA).",
    ),
    (
        "43628110000105",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (TH COMERCIO DA CIDADE"
        " ALEGRIA LTDA).",
    ),
    (
        "dutrametais.com",
        75,
        "Site na lista 'Evite estes Sites' do PROCON-SP (THALIA OLIVEIRA /"
        " FRANCIELLE CONSTANCIO).",
    ),
    (
        "44481477000101",
        75,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (THALIA OLIVEIRA DE"
        " ALMEIDA).",
    ),
    (
        "50553453000113",
        75,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (FRANCIELLE CONSTANCIO"
        " DA SILVA).",
    ),
    (
        "equipamentosrodrigues.com",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (PEDRO AUGUSTO"
        " FERREIRA).",
    ),
    (
        "45326521000171",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (PEDRO AUGUSTO"
        " FERREIRA).",
    ),
    (
        "everestgroup.com.br",
        55,
        "Site na lista 'Evite estes Sites' do PROCON-SP (EVEREST GROUP"
        " PARTICIPACOES LTDA).",
    ),
    (
        "40921411000134",
        55,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (EVEREST GROUP"
        " PARTICIPACOES LTDA).",
    ),
    (
        "fabricaauthenticite.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (CELIO ASSIS CORREA"
        " TEIXEIRA FILHO).",
    ),
    (
        "49464245000169",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (CELIO ASSIS CORREA"
        " TEIXEIRA FILHO).",
    ),
    (
        "fabricashoes.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ENVIA TENIS LTDA).",
    ),
    (
        "feme.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (FEME BR LTDA).",
    ),
    (
        "45986109000188",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (FEME BR LTDA).",
    ),
    (
        "ferrutini.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (VITOR FERNANS ALVES"
        " ARTIGOS DO VEST).",
    ),
    (
        "53177029000100",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (VITOR FERNANS ALVES"
        " ARTIGOS DO VEST).",
    ),
    (
        "flystorebrasil.com.br",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (DEL NEGOCIOS DIGITAIS"
        " LTDA).",
    ),
    (
        "48066558000104",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (DEL NEGOCIOS DIGITAIS"
        " LTDA).",
    ),
    (
        "fully.com.br",
        85,
        "Site na lista 'Evite estes Sites' do PROCON-SP (FULLY VIAGENS LTDA).",
    ),
    (
        "13647645000162",
        85,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (FULLY VIAGENS LTDA).",
    ),
    (
        "futcertobrasil.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (JEFERSON DE LIMA).",
    ),
    (
        "44349816000109",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (JEFERSON DE LIMA).",
    ),
    (
        "gelniche.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (PERFUMARIA E"
        " COSMÉTICOS KA LTDA).",
    ),
    (
        "20808977000147",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (PERFUMARIA E"
        " COSMÉTICOS KA LTDA).",
    ),
    (
        "gigavarejo.com.br",
        60,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GIGAVAREJO COMERCIO E"
        " ARTIGOS PARA O LAR LTDA).",
    ),
    (
        "37551442000136",
        60,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GIGAVAREJO COMERCIO E"
        " ARTIGOS PARA O LAR LTDA).",
    ),
    (
        "gomic.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GOMIC BEAUTY LTDA).",
    ),
    (
        "40701445000113",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GOMIC BEAUTY LTDA).",
    ),
    ("hofferta.com", 25, "Site na lista 'Evite estes Sites' do PROCON-SP."),
    (
        "hotelurbano.com.br",
        220,
        "Site na lista 'Evite estes Sites' do PROCON-SP (HURB TECHNOLOGIES"
        " S/A).",
    ),
    (
        "hurb.com",
        220,
        "Site na lista 'Evite estes Sites' do PROCON-SP (HURB TECHNOLOGIES"
        " S/A).",
    ),
    (
        "12954744000124",
        220,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (HURB TECHNOLOGIES"
        " S/A).",
    ),
    (
        "iluminim.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (COMERCIAL ILUMINIM"
        " LTDA).",
    ),
    (
        "23429903000198",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (COMERCIAL ILUMINIM"
        " LTDA).",
    ),
    (
        "iwoseries.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (V M C DOS SANTOS).",
    ),
    (
        "19510938000180",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (V M C DOS SANTOS).",
    ),
    (
        "laserfast.com",
        110,
        "Empresa na lista de reclamações do PROCON-SP (AVDV ESTÉTICA LTDA).",
    ),
    (
        "31237773000100",
        110,
        "CNPJ na lista de reclamações do PROCON-SP (AVDV ESTÉTICA LTDA).",
    ),
    (
        "lbashop.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ISABELA MARCONDES"
        " KHZOUZ EIRELI).",
    ),
    (
        "24117433000190",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ISABELA MARCONDES"
        " KHZOUZ EIRELI).",
    ),
    (
        "leggingbrasil.com",
        70,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LEEGING BRASIL LTDA /"
        " BRASIL TEXTIL).",
    ),
    (
        "leggingbrasil.com.br",
        70,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LEGGING BRASIL LTDA).",
    ),
    (
        "37563308000155",
        70,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (LEGGING BRASIL LTDA).",
    ),
    (
        "34269853000145",
        70,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (BRASIL TEXTIL LTDA).",
    ),
    (
        "lewadoimports.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LTCM CALCADOS LTDA).",
    ),
    (
        "40746343000114",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (LTCM CALCADOS LTDA).",
    ),
    (
        "liquidashoes.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (BMCT EMPRESARIAL"
        " LTDA).",
    ),
    (
        "48945336000153",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (BMCT EMPRESARIAL"
        " LTDA).",
    ),
    (
        "lojaatlantis.com",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GV ECOMMERCE GROUP"
        " BRASIL LTDA).",
    ),
    (
        "42868039000175",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GV ECOMMERCE GROUP"
        " BRASIL LTDA).",
    ),
    (
        "lojabestvarejos.com",
        60,
        "Site na lista 'Evite estes Sites' do PROCON-SP (WE HUB NEGÓCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "lojacondi.com",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (AGOGE INTERMEDIACAO DE"
        " NEGOCIOS LTDA).",
    ),
    (
        "36277320000130",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (AGOGE INTERMEDIACAO DE"
        " NEGOCIOS LTDA).",
    ),
    (
        "lojadigivarejista.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (DIGI HUB NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "48286627000187",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (DIGI HUB NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "lojadubaiimports.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (DROP AGENCY LTDA).",
    ),
    (
        "lojamiofarma.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (MIOFARMA LTDA).",
    ),
    (
        "45809838000169",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (MIOFARMA LTDA).",
    ),
    (
        "lojaslondrina.com.br",
        60,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LOJAS LONDRINA LTDA).",
    ),
    (
        "36623723000194",
        60,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (LOJAS LONDRINA LTDA).",
    ),
    (
        "lojavitesse.com",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (FAST NET NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "49205851000160",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (FAST NET NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "lovelybox.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (LOVELYBOX EMBALAGENS"
        " PERSON).",
    ),
    (
        "40473193000112",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (LOVELYBOX EMBALAGENS"
        " PERSON).",
    ),
    (
        "magazineal.com",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (VH SERVICOS"
        " ADMINISTRATIVOS LTDA).",
    ),
    (
        "41512423000178",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (VH SERVICOS"
        " ADMINISTRATIVOS LTDA).",
    ),
    (
        "magazinedosatacados.com",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (DROP AGENCY LTDA).",
    ),
    (
        "magazinestore.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (EMANUEL ANTA CARVALHO).",
    ),
    (
        "32109554000118",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (EMANUEL ANTA CARVALHO).",
    ),
    (
        "magazinmulher.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (EMANUEL ANTAS"
        " CARVALHO).",
    ),
    (
        "marabraz.com.br",
        180,
        "Site na lista 'Evite estes Sites' do PROCON-SP (COMERCIAL DE MÓVEIS"
        " JORDANÉSIA SOC LTDA).",
    ),
    (
        "21660838000262",
        180,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (COMERCIAL DE MÓVEIS"
        " JORDANÉSIA SOC LTDA).",
    ),
    (
        "mundialeletro.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (MUNDIAL ELETRO E"
        " TECNOLOGIA LTDA).",
    ),
    (
        "51375455000122",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (MUNDIAL ELETRO E"
        " TECNOLOGIA LTDA).",
    ),
    (
        "nuvemdedescontos.com",
        55,
        "Site na lista 'Evite estes Sites' do PROCON-SP (WE HUB NEGÓCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "ofertastore.com",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (JOAO BATISTA MONTEIRO"
        " BRAGA).",
    ),
    (
        "24068929000110",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (JOAO BATISTA MONTEIRO"
        " BRAGA).",
    ),
    (
        "outletdasfraldas.com.br",
        25,
        "Site na lista 'Evite estes Sites' do PROCON-SP (BRENDO GONÇALVES DA"
        " SILVA).",
    ),
    (
        "30177993000132",
        25,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (BRENDO GONÇALVES DA"
        " SILVA).",
    ),
    (
        "peixeurbano.com.br",
        150,
        "Site na lista 'Evite estes Sites' do PROCON-SP (PEIXE URBANO WEB"
        " SITE).",
    ),
    (
        "11701558000110",
        150,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (PEIXE URBANO WEB"
        " SITE).",
    ),
    (
        "premierexclusive.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (EZFIX IMPORTACAO E"
        " COMERCIO LTDA).",
    ),
    (
        "15272816000141",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (EZFIX IMPORTACAO E"
        " COMERCIO LTDA).",
    ),
    (
        "rocklin.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ROCKLIN STORE LTDA).",
    ),
    (
        "23809815000111",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ROCKLIN STORE LTDA).",
    ),
    (
        "rosafashion.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ROSA JOAQUIM DOS S."
        " NOGUEIRA).",
    ),
    (
        "40210751000157",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ROSA JOAQUIM DOS S."
        " NOGUEIRA).",
    ),
    (
        "safiravillage.com.br",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (YURI NEGROMONTE"
        " NASCIMENTO ROCHA).",
    ),
    (
        "47189721000155",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (YURI NEGROMONTE"
        " NASCIMENTO ROCHA).",
    ),
    (
        "saldaocarioca.com.br",
        50,
        "Site na lista 'Evite estes Sites' do PROCON-SP (MWM DO BRASIL"
        " MARKETPLACE LTDA).",
    ),
    (
        "21905681000107",
        50,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (MWM DO BRASIL"
        " MARKETPLACE LTDA).",
    ),
    (
        "santolarmoveis.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (SANTO LAR MÓVEIS E"
        " ELETRO LTDA).",
    ),
    (
        "31447793000115",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (SANTO LAR MÓVEIS E"
        " ELETRO LTDA).",
    ),
    (
        "shopmaxx.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (SHOPMAXX DIGITAL"
        " GESTAO DE NEGOCIOS).",
    ),
    (
        "sigaofertas.com.br",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (SIGA OFERTAS COM."
        " ELETRÔNICO).",
    ),
    (
        "34294667000166",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (SIGA OFERTAS COM."
        " ELETRÔNICO).",
    ),
    (
        "tecnotec.com.br",
        45,
        "Site na lista 'Evite estes Sites' do PROCON-SP (TECNOTEC LTDA).",
    ),
    (
        "05904663000154",
        45,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (TECNOTEC LTDA).",
    ),
    (
        "tiggoshop.com.br",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (F.BRAZ MENDES NEGOCIOS"
        " DIGITAIS).",
    ),
    (
        "42929632000184",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (F.BRAZ MENDES NEGOCIOS"
        " DIGITAIS).",
    ),
    (
        "usenox.com",
        30,
        "Site na lista 'Evite estes Sites' do PROCON-SP (GABRIEL LUCAS ALVES"
        " ALVARENGO).",
    ),
    (
        "40961139000116",
        30,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (GABRIEL LUCAS ALVES"
        " ALVARENGO).",
    ),
    (
        "vivadecor.com.br",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (VIVA DECORACOES TEXTIL"
        " LTDA).",
    ),
    (
        "34375662000168",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (VIVA DECORACOES TEXTIL"
        " LTDA).",
    ),
    (
        "vivonestore.com",
        35,
        "Site na lista 'Evite estes Sites' do PROCON-SP (VIVONE NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "33765910000114",
        35,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (VIVONE NEGOCIOS"
        " DIGITAIS LTDA).",
    ),
    (
        "zinnimodas.com",
        40,
        "Site na lista 'Evite estes Sites' do PROCON-SP (ZINNI PROMOCAO EM"
        " VENDAS ONLINE LTDA).",
    ),
    (
        "42078169000104",
        40,
        "CNPJ na lista 'Evite estes Sites' do PROCON-SP (ZINNI PROMOCAO EM"
        " VENDAS ONLINE LTDA).",
    ),
]

# Inicializa no estado da sessão
if "df_fraudes" not in st.session_state:
  chaves, denuncias, motivos = zip(*PROCON_E_FRAUDES_COMPLETO)
  st.session_state.df_fraudes = pd.DataFrame({
      "chave": list(chaves),
      "denuncias": list(denuncias),
      "motivo": list(motivos),
  })

df_fraudes = st.session_state.df_fraudes

# --- CONSULTA DE SEGURANÇA ---
entrada_usuario = st.text_input(
    "Digite a Chave PIX, Número, CNPJ ou Endereço do Site:",
    placeholder="Ex: 27995109581, 123importados.com ou 35912902000189",
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

      if total_denuncias > 15:
        st.error("🚨 **ALERTA DE ALTO RISCO: REGISTRO ENCONTRADO!**")
        st.markdown(f"""
                **Detalhes do registro na base de segurança:**
                * 🔴 **Motivo / Fonte:** {motivo_encontrado}
                * 🔴 Este item acumula **{total_denuncias} registros/denúncias** de irregularidades no PROCON-SP ou na comunidade.
                
                **O que fazer agora?**
                1. **NÃO faça compras, transferências ou pagamentos.**
                2. Verifique se o site possui canais oficiais de atendimento antes de qualquer ação.
                """)
      else:
        st.warning(
            f"⚠️ **ATENÇÃO: REGISTRO ENCONTRADO COM {total_denuncias} DENÚNCIAS.**"
        )
        st.write(f"**Detalhe:** {motivo_encontrado}.")
    else:
      st.success("✅ **NENHUM ALERTA ENCONTRADO PARA ESTE DADO**")
      st.markdown(
          "ℹ️ Mesmo sem alertas na base, confirme sempre o nome completo, CNPJ"
          " e endereço do site oficial antes de concluir qualquer transação."
      )

st.divider()

# --- SEÇÃO DE DENÚNCIA ---
st.subheader("📢 Viu um site, CNPJ ou chave suspeita?")
with st.expander("🚨 **Clique aqui para registrar uma nova denúncia**"):
  st.write(
      "Ajude a proteger os moradores do bairro cadastrando um site, CNPJ ou"
      " chave suspeita."
  )

  with st.form("form_denuncia"):
    chave_denuncia = st.text_input(
        "Chave PIX, Site, CNPJ ou Número Suspeito:",
        placeholder="Ex: sitefalso.com.br ou 00.000.000/0001-00",
    )
    motivo_denuncia = st.text_area(
        "Descreva o problema (ex: Comprei no site e não recebi, pediram PIX"
        " adiantado, etc.):"
    )
    submit_denuncia = st.form_submit_button("🚨 ENVIAR DENÚNCIA")

    if submit_denuncia:
      if not chave_denuncia or not motivo_denuncia:
        st.error("⚠️ Por favor, preencha o dado e o motivo da denúncia.")
      else:
        chave_limpa_nova = re.sub(
            r"[^a-zA-Z0-9@.]", "", chave_denuncia.strip().lower()
        )

        filtro_existente = st.session_state.df_fraudes["chave"].str.replace(
            r"[^a-zA-Z0-9@.]", "", regex=True
        ).str.lower() == chave_limpa_nova

        if filtro_existente.any():
          st.session_state.df_fraudes.loc[filtro_existente, "denuncias"] += 1
          denuncias_atuais = st.session_state.df_fraudes.loc[
              filtro_existente, "denuncias"
          ].values[0]
          st.success(
              f"✅ **Nova denúncia registrada para {chave_denuncia}!** Total:"
              f" {denuncias_atuais} denúncias."
          )
        else:
          nova_linha = pd.DataFrame({
              "chave": [chave_denuncia.strip()],
              "denuncias": [16],
              "motivo": [f"Denúncia Comunitária: {motivo_denuncia.strip()}"],
          })
          st.session_state.df_fraudes = pd.concat(
              [st.session_state.df_fraudes, nova_linha], ignore_index=True
          )
          st.success(
              f"✅ **Item {chave_denuncia} cadastrado e ativo no banco de"
              " dados!**"
          )

        st.info("Obrigado por colaborar com a segurança da comunidade!")

st.divider()

with st.expander("💡 O que fazer se cair em um golpe?"):
  st.write(
      "1. Registre reclamação no PROCON (procon.sp.gov.br). 2. Contate o seu"
      " banco imediatamente. 3. Registre Boletim de Ocorrência na Polícia"
      " Civil."
  )
