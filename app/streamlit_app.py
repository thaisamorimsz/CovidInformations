import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import sqlalchemy
import plotly.express as px

import sql_queries
import mundo
import brasil
import atualizar_dados
from engine import engine

pd.options.plotting.backend = "plotly"

# Organiza o selecionador radio para horizontal
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)


# Ajusta o tamanho da barra lateral esquerda
def _max_width_():
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 220px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )


def main():
    _max_width_()
    st.sidebar.title("Covid")
    app_mode = st.sidebar.selectbox("Escolha uma opção",
        ["Mundo", "Brasil", "Atualizar dados"])
        #["Atualizar dados"])
    if app_mode == "Mundo":

        opcoes_selectbox_mundo_linha = st.selectbox('Opções', [
                    'Total de casos',
                    'Novos casos',
                    'Novos casos - média móvel',
                    'Novos casos - média móvel por milhão',
                    'Total de mortes',
                    'Novas mortes',
                    'Novas mortes - média móvel',
                    'Novas mortes - média móvel por milhão',
                    'R',
                    'Pacientes hospitalizados',
                    'Pacientes hospitalizados por milhão',
                    'Pacientes na UTI',
                    'Pacientes na UTI por milhão',
                    'Total de testes',
                    'Novos testes',
                    'Testes por caso',
                    'Pessoas vacinadas',
                    'Pessoas imunizadas',
                    'Novas vacinações'
                    ])


        mundo_tabela = mundo.mundo_linha(opcoes_selectbox_mundo_linha)

        opcoes_radio_mapa_mundo = st.radio('Opções', ['Casos','Mortes','Testes','Vacinações'])
        mundo.mundo_mapa(opcoes_radio_mapa_mundo)
    

    elif app_mode == "Brasil":
        lista_estados = pd.read_sql_query(sql_queries.query_estados,engine)
        estado = st.sidebar.selectbox("Estado",['Todos'] + lista_estados['state_name'].to_list())
        
        if estado == 'Todos':

            opcoes_selectbox_linha_brasil = st.selectbox('Opções', [
            'Casos atuais',
            'Casos confirmados',
            'Casos diários',
            'Média móvel de casos diários por 100k',
            'Mortes',
            'Novas Mortes',
            'Média móvel de novas mortes por 100k',
            'R',
            ])
            brasil.brasil_linha(lista_estados,estado,opcoes_selectbox_linha_brasil)

            opcoes_selectbox_mapa_brasil = st.selectbox('Opções', [
            'Imunizados',
            'Pessoas não vacinadas',
            'Percentual de pessoas imunizadas',
            'Percentual de pessoas vacinadas',
            'Vacinados',
            'Número de leitos',
            'Número de leitos de UTI para Covid',
            'Número de leitos de UTI',
            'Número de respiradores'
            ])
            brasil.brasil_mapa(lista_estados,estado,opcoes_selectbox_mapa_brasil)
        else:

            opcoes_selectbox_mapa_estado = st.selectbox('Opções', [
            'Imunizados',
            'Pessoas não vacinadas',
            'Percentual de pessoas imunizadas',
            'Percentual de pessoas vacinadas',
            'Vacinados',
            'Número de leitos',
            'Número de leitos de UTI para Covid',
            'Número de leitos de UTI',
            'Número de respiradores'
            ])
            brasil.brasil_estados(lista_estados,estado,opcoes_selectbox_mapa_estado)

    elif app_mode == "Atualizar dados":
        atualizar_dados.atualizar()

if __name__ == '__main__':
    main()