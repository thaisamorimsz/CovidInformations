import streamlit as st
import pandas as pd
import sqlalchemy
import plotly.express as px

import sql_queries
from engine import engine

def brasil_linha(lista_estados,estado,opcoes_selectbox_linha_brasil):
        
    query_linha_brasil = sql_queries.query_linha_brasil.format(tuple(lista_estados['state_name']))
    brasil_linha = pd.read_sql_query(query_linha_brasil,engine)

    fig_brasil_linha = px.line(brasil_linha,
        x="Data", y=opcoes_selectbox_linha_brasil,
        color="Estado",
        width=1200, height=600
        )

    st.plotly_chart(fig_brasil_linha)

    st.dataframe(brasil_linha.sort_values(by=['Data']))

def brasil_mapa(lista_estados,estado,opcoes_selectbox_mapa_brasil):
    contorno_brasil = pd.read_sql_query(sql_queries.query_contorno.format('1000'),engine)

    dados_brasil = pd.read_sql_query(sql_queries.query_mapa_brasil,engine)

    fig_casos_brasil = px.choropleth(dados_brasil, locations="state_num_id",
                geojson=eval(contorno_brasil['geojson_file'][0]),
                featureidkey='properties.codigo_ibg',
                color="{}".format(opcoes_selectbox_mapa_brasil),
                hover_name="Estado",
                range_color=[dados_brasil[opcoes_selectbox_mapa_brasil].min(),dados_brasil[opcoes_selectbox_mapa_brasil].max()],
                color_continuous_scale=px.colors.sequential.YlOrRd,
                width=1200, height=600)
    fig_casos_brasil.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig_casos_brasil)

    dados_brasil_tabela = dados_brasil.drop(columns=['state_num_id'])
    st.dataframe(dados_brasil_tabela)

def brasil_estados(lista_estados,estado,opcoes_selectbox_mapa_estado):
    '''   
    opcoes_selectbox_linha_estado = st.selectbox('Opções', [
        'Casos atuais',
        'Casos diários',
        'Média móvel de casos diários por 100k',
        'Mortes',
        'Novas Mortes',
        'Média móvel de novas mortes por 100k',
        'R',
        ])

    query_linha_estados = sql_queries.query_linha_estados.format(tuple(lista_estados['state_name']))
    estados_linha = pd.read_sql_query(query_linha_estados,engine)

    fig_estados_linha = px.line(estados_linha,
        x="Data", y="{}".format(opcoes_selectbox_linha_estado),
        color="Cidade",
        width=1200, height=600
        )

    st.plotly_chart(fig_estado_linha)
    '''
    id_estado = pd.read_sql_query(sql_queries.query_estado_id_nome,engine)
    id_estado = id_estado[id_estado['state_name']==estado]['state_num_id'].values[0]

    contorno_estados = pd.read_sql_query(sql_queries.query_contorno.format(id_estado),engine)

    dados_cidades = pd.read_sql_query(sql_queries.query_mapa_estados,engine)

    color_min = dados_cidades[dados_cidades['Estado']==estado][opcoes_selectbox_mapa_estado].min()
    color_max = dados_cidades[dados_cidades['Estado']==estado][opcoes_selectbox_mapa_estado].max()

    fig_casos_cidade = px.choropleth(dados_cidades,
                locations="city_id",
                geojson=eval(contorno_estados['geojson_file'][0]),
                featureidkey='properties.id',
                color="{}".format(opcoes_selectbox_mapa_estado),
                hover_name="Cidade",
                range_color=[color_min,color_max],
                color_continuous_scale=px.colors.sequential.YlOrRd,
                width=1200, height=600)
    fig_casos_cidade.update_geos(fitbounds='locations', visible=False)
    st.plotly_chart(fig_casos_cidade)

    dados_cidade_tabela = dados_cidades[dados_cidades['Estado']==estado]
    dados_cidade_tabela = dados_cidade_tabela.drop(columns=['Estado','city_id'])

    st.dataframe(dados_cidade_tabela)