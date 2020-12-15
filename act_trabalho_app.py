# Importando as bibliotecas
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

## Carregando os dados (load datasets) ##

@st.cache(persist=True)
def load_complete_data():
    df0 = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_mes_clean.csv")
    df1 = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_idade_clean.csv")
    df2 = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_parte_corpo_clean.csv")
    df3 = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_cnae20_clean.csv")
    return [df0, df1, df2, df3]

@st.cache(persist=True)
def load_mm():
    # url_mes = PEGAR LINK NO GITHUB
    df_mes = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_mes_clean.csv")
    df_mm = pd.DataFrame(df_mes.groupby(by='mes')['qte_acidentes'].mean())
    return df_mm

@st.cache(persist=True)
def load_ea():
    df_mes = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_mes_clean.csv")
    df_ea = pd.DataFrame(df_mes.groupby(by='ano')['qte_acidentes'].sum())
    return df_ea

@st.cache(persist=True)
def load_fe():
    # url_idade = PEGAR LINK NO GITHUB
    df_idade = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_idade_clean.csv")
    df_fe = df_idade.groupby(by=['idade', 'sexo'])['qte_acidentes'].sum().reset_index()
    df_fe = df_fe.set_index('idade')
    return df_fe

@st.cache(persist=True)
def load_pa():
    # url_partecorpo = PEGAR LINK NO GITHUB
    df_partecorpo = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_parte_corpo_clean.csv")
    df_pa = pd.DataFrame(df_partecorpo.groupby(by='parte_atingida')['qte_acidentes'].sum()).sort_values(by=['qte_acidentes'])
    df_pa = df_pa[df_pa.index != 'Ignorada']
    df_pa = df_pa.tail(10)
    return df_pa

@st.cache(persist=True)
def load_c2():
    # url_cnae = PEGAR LINK NO GITHUB
    df_cnae = pd.read_csv("https://raw.githubusercontent.com/dinopolo/streamlit_work_accident/main/Datasets/df_cnae20_clean.csv")
    df_c2 = pd.DataFrame(df_cnae.groupby(by='cnae')['qte_acidentes'].sum()).sort_values(by=['qte_acidentes'], ascending=False)
    df_c2 = df_c2[df_c2.index != '9999:Ignorado']
    df_c2 = df_c2.head(10)
    return df_c2

dfs = load_complete_data()
df_mm = load_mm()
df_ea = load_ea()
df_fe = load_fe()
df_pa = load_pa()
df_c2 = load_c2()

## Conteúdo da barra lateral esquerda (left sidebar) ##

# Descrição
st.sidebar.markdown("**Sobre o *web app*:**")
st.sidebar.markdown("Com esse *web app* você pode analisar os acidentes de trabalho no Brasil até 2015 por diferentes categorias. Além disso, pode verificar tendências e quantidades dos acidentes de trabalho, e, com isso, tirar *insights* para prevenção em seu trabalho ou empresa.")

st.sidebar.markdown("**Como funciona o *web app*:**")
st.sidebar.markdown("Para utilizar o *web app*, basta selecionar a categoria que deseja visualizar e então o visualização será exibida. Além disso, todos os gráficos são interativos, assim, é possível baixar a imagem dos gráficos, aumentar o zoom em determinadas áreas e  basta passar o ponteiro do mouse no canto superior direito do gráfico que a barra com as opções de controle aparece. Ainda, ao marcar a caixa 'Mostrar dataset completo' é possível visualizar a partir de qual dataset as visualizações foram geradas.")

## Página principal (Main page) ##

# Título
st.title('Acidentes de Trabalho no Brasil até 2015')

# Fazer gráfico da média mensal e da soma anual
selbox = st.selectbox("Selecione a categoria dos acidentes de trabalho para visualizar o gráfico:", ("Média mensal dos acidentes de trabalho", "Evolução anual dos acidentes de trabalho", "Acidentes de trabalho por faixa etária", "Top 10 partes do corpo atingidas", "Top 10 CNAEs com mais acidentes"))

if selbox == "Média mensal dos acidentes de trabalho":
    fig = px.scatter(df_mm, x = df_mm.index, y = 'qte_acidentes', template='simple_white')
    fig.update_traces(mode='lines+markers', line_color="blue", marker_color="blue")
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array', tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
            ticktext = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
            ), 
        title_text = "Quantidade média de acidentes de trabalho por mês, de 1997 a 2015"
        )
    fig.update_xaxes(title_text = 'Mês')
    fig.update_yaxes(title_text = 'Quantidade média de acidentes')

    st.plotly_chart(fig)

    if st.checkbox('Mostrar dataset completo'):
        st.markdown('Pode demorar um poquinho...')
        st.dataframe(dfs[0])
        st.markdown('**Pronto!**')

elif selbox == "Evolução anual dos acidentes de trabalho":
    fig = px.scatter(df_ea, x = df_ea.index, y = 'qte_acidentes', template='simple_white')
    fig.update_traces(mode='lines+markers', line_color="blue", marker_color="blue")
    fig.update_layout(xaxis = dict(tickmode = 'linear', tick0 = 1996, dtick = 1), title_text = 'Evolução anual dos acidentes de trabalho, de 1997 a 2015')
    fig.update_layout(yaxis = dict(tickmode = 'auto', nticks = 12))
    fig.update_xaxes(title_text = 'Ano', tickangle = 315)
    fig.update_yaxes(title_text = 'Quantidade de acidentes')
    
    st.plotly_chart(fig)

    if st.checkbox('Mostrar dataset completo'):
        st.markdown('Pode demorar um poquinho...')
        st.dataframe(dfs[0])
        st.markdown('**Pronto!**')


elif selbox == "Acidentes de trabalho por faixa etária":
    fig = px.bar(df_fe, x = df_fe.index, y = 'qte_acidentes', template='simple_white', color='sexo', labels = {'sexo': 'Gênero'})
    fig.update_layout(title_text = 'Quantidade de acidentes de trabalho por faixa etária, de 1997 a 2015')
    fig.update_layout(yaxis = dict(tickmode = 'auto', nticks = 12))
    fig.update_xaxes(title_text = 'Faixa etária')
    fig.update_yaxes(title_text = 'Quantidade de acidentes')

    st.plotly_chart(fig)

    if st.checkbox('Mostrar dataset completo'):
        st.markdown('Pode demorar um poquinho...')
        st.dataframe(dfs[1])
        st.markdown('**Pronto!**')

elif selbox == "Top 10 partes do corpo atingidas":
    fig = px.bar(df_pa, x = 'qte_acidentes', y = df_pa.index, template = 'simple_white', orientation = 'h')
    fig.update_traces(marker_color='blue', marker_line_color='blue')
    fig.update_layout(title_text = '10 partes do corpo mais atingidas em acidentes do trabalho, de 2002 a 2015')
    fig.update_layout(xaxis = dict(tickmode = 'auto', nticks = 12))
    fig.update_xaxes(title_text = 'Quantidade de acidentes', tickangle = 315)
    fig.update_yaxes(title_text = 'Parte do corpo atingida')

    st.plotly_chart(fig)

    if st.checkbox('Mostrar dataset completo'):
        st.markdown('Pode demorar um poquinho...')
        st.dataframe(dfs[2])
        st.markdown('**Pronto!**')

else:
    df_show = df_c2.rename(columns={'qte_acidentes': "Quantidade de acidentes"})
    
    st.markdown("**Top 10 CNAEs 2.0 com mais acidentes de trabalho, de 2006 a 2015**")
    st.dataframe(df_show)

    if st.checkbox('Mostrar dataset completo'):
        st.markdown('Pode demorar um poquinho...')
        st.dataframe(dfs[3])
        st.markdown('**Pronto!**')