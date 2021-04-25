import streamlit as st
import pandas as pd
import sqlalchemy
import plotly.express as px

import sql_queries
from engine import engine


def mundo_linha(opcoes_selectbox):
    
    lista_localidades = pd.read_sql_query(sql_queries.query_lista_localidades,engine)

    localidades_selecionadas = st.multiselect('Selecione as localidades', lista_localidades['Localidade'].to_list(),
        ["Brazil","United States"])

    if len(localidades_selecionadas) == 1:
        localidades_selecionadas.append('')

    if localidades_selecionadas:
    
        query_linha_mundo = sql_queries.query_linha_mundo.format(tuple(localidades_selecionadas))
        mundo = pd.read_sql_query(query_linha_mundo,engine)
        fig_mundo = px.line(mundo,
            x="Data", y="{}".format(opcoes_selectbox),
            color="Localidade",
            width=1200, height=600
            )

        fig_mundo.update_traces(connectgaps=True)
        st.plotly_chart(fig_mundo)

        st.dataframe(data=mundo.sort_values(by='Data'),width=1200, height=300)


def mundo_mapa(opcoes_radio):

    col1,col2,col3,col4 = st.beta_columns(4)
    data_inicial = pd.to_datetime(col2.date_input('Data inicial',pd.to_datetime('2021-01-01').date(), key="1")).date()
    data_final = pd.to_datetime(col3.date_input('Data final', key="2")).date()
    
    query_mapa_mundo = sql_queries.query_mapa_mundo.format(data_inicial,data_final)
    casos_mundo = pd.read_sql_query(query_mapa_mundo,engine)
    casos_mundo = casos_mundo[~casos_mundo['iso_code'].isin(['OWID_AFR','OWID_ASI','OWID_CYN','OWID_EUN','OWID_EUR','OWID_INT','OWID_KOS','OWID_NAM','OWID_OCE','OWID_SAM','OWID_WRL'])]

    fig_casos_mundo = px.choropleth(casos_mundo, locations="iso_code",
                    color="{}".format(opcoes_radio),
                    hover_name="Localidade",
                    range_color=[casos_mundo["{}".format(opcoes_radio)].min(),casos_mundo["{}".format(opcoes_radio)].max()],
                    color_continuous_scale=px.colors.sequential.YlOrRd,
                    width=1200, height=600)
    st.plotly_chart(fig_casos_mundo)

    st.dataframe(data=casos_mundo.sort_values(by='Localidade'),width=1200, height=300)