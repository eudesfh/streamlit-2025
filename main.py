import streamlit as st

import pandas as pd

# Inserindo o título da página e o ícone do navegador
st.set_page_config(page_title='Finanças', page_icon='💰')


# Inserindo o título na página
st.markdown("""
# Boas vindas!

## Nosso APP Finanaceiro!

Espero que você curta a experiência da nossa solução para organização financeira.
            
""")

# Widget de upload de dados
file_upload = st.file_uploader(label="Faça upload dos dados aqui", type=['csv'])

# Verificar se algum arquivo foi feito upload
if file_upload:

    # Leitura dos dados
    df = pd.read_csv(file_upload)

    # Transformando coluna Data em formato de Data
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date

    # Criando um sistema de Expandir a tabela
    exp1 = st.expander("Dados Brutos")
    # Formatar a coluna de valor
    columns_format = {"Valor": st.column_config.NumberColumn("Valor", format="R$ %f")}
    # Exibição dos dados no App
    exp1.dataframe(df, hide_index=True, column_config=columns_format)

    # Pivotando tabela / Visão das Instituições

    exp2 = st.expander("Insituições")
    df_instituicao = df.pivot_table(index="Data", columns="Instituição", values="Valor")
    
    # Criando abas de navegação
    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])
    
    # Exibe Dataframe
    with tab_data:
       st.dataframe(df_instituicao)

        # Plotando gráfico da Visão das instituições e exibe Histórico
    with tab_history:
        st.line_chart(df_instituicao)

    # Exibe Distribuição
    with tab_share:

        # -------------- MODELO FILTRO 1 COM CALENDÁRIO --------------
        # Incluindo campo de filtro de data
        # date = st.date_input("Data para Distrituição", 
                    # limitando o calendário
        #            min_value=df_instituicao.index.min(),
        #            max_value=df_instituicao.index.max())
        
        # if date not in df_instituicao.index:
        #    st.warning("Insira uma data válida")
        # -------------- MODELO FILTRO 2 LISTA SUSPENSA --------------

        date = st.selectbox("Filtro Data", options=df_instituicao.index)

        # Obtém a última data de dados
        # last_date = df_instituicao.sort_index().iloc[-1]

        # Gráfico de Distruição
        # else:
        st.bar_chart(df_instituicao.loc[date])