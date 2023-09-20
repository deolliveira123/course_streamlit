import streamlit as st
import requests
import pandas as pd
import plotly.express as px


st.set_page_config(layout='wide')

def num_format(valor, prefixo = ''):
    for un in ['', 'mil']:
        if valor <1000:
            return f'{prefixo} {valor:.2f} {un}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões '


st.title(' DASHBOARD DE VENDAS :shopping_trolley: ')

url = 'https://labdados.com/produtos'
response = requests.request('GET', url)
dados = pd.DataFrame.from_dict(response.json())

dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mês'] = receita_mensal['Data da Compra'].dt.month_name()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)


## Tabelas

dados_grop = dados.groupby('Local da compra')[['Preço']].sum()
dados_grop_2 = dados.drop_duplicates(subset= 'Local da compra')[['Local da compra', 'lat', 'lon']].\
    merge(dados_grop, left_on= 'Local da compra', right_index= True).sort_values('Preço', ascending= False)




## visualizações do gráfico

fig_mapa_receita = px.scatter_geo(
    dados_grop_2,
    lat = 'lat',
    lon = 'lon',
    scope = 'south america',
    size = 'Preço',
    template = 'seaborn',
    hover_name = 'Local da compra',
    hover_data = {'lat': False, 'lon': False},
    title = 'Receita por Estado'
)

fig_receita_mensal = px.line(receita_mensal,
                             x = 'Mês',
                             y = 'Preço',
                             markers=True,
                             range_y=(0, receita_mensal.max()),
                             color='Ano',
                             line_dash='Ano',
                             title="Receita Mensal"
                             )

fig_receita_mensal.update_layout(yaxis_title = 'Receita')

fig_receitas_estados = px.bar(dados_grop_2.head(5),
                              x = 'Local da compra',
                              y = 'Preço',
                              text_auto=True,
                              title='Top Estados (receitas)'
                              )
fig_receitas_estados.update_layout(yaxis_title = 'Receita')

fig_receitas_categorias = px.bar(receita_categorias,
                                 text_auto=True,
                                 title = 'Receita por Categorias')

fig_receitas_categorias.update_layout(yaxis_title = 'Receita')


aba1, aba2, aba3 = st.tabs(['Receita', 'Quantidade de Vwndas', 'Vendedores'])


with aba1:


    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita", num_format(dados['Preço'].sum(), 'R$'))
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receitas_estados, use_container_width=True)
    with col2:
        st.metric('Quantidade de Vendas ', num_format(dados.shape[0]))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receitas_categorias, use_container_width=True)

with aba2:

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita", num_format(dados['Preço'].sum(), 'R$'))
  
    with col2:
        st.metric('Quantidade de Vendas ', num_format(dados.shape[0]))


with aba3:
         
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita", num_format(dados['Preço'].sum(), 'R$'))

    with col2:
        st.metric('Quantidade de Vendas ', num_format(dados.shape[0]))
 







