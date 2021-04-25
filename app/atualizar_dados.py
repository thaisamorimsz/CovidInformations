import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy.sql import text as sa_text

import sql_queries
from engine import engine


def atualizar():

    st.header('Última atualização')

    atualizacao_tabelas = pd.read_sql_query(sql_queries.query_atualizacao_tabelas,engine)
    st.dataframe(atualizacao_tabelas)

    st.header('Tabelas a serem atualizadas')

    col1,col2 = st.beta_columns([0.25,0.75])

    cities_cases_full = col1.checkbox('cities_cases_full')
    cities_cnes = col1.checkbox('cities_cnes')
    cities_parameters = col1.checkbox('cities_parameters')
    cities_rt = col1.checkbox('cities_rt')
    cities_vacina = col1.checkbox('cities_vacina')
    owid = col1.checkbox('owid')
    states_cases_full = col1.checkbox('states_cases_full')
    states_parameters = col1.checkbox('states_parameters')
    states_rt = col1.checkbox('states_rt')
    states_vacina = col1.checkbox('states_vacina')
    
    botao_atualizar = col1.button('Atualizar')


    if botao_atualizar and cities_cases_full:
        alerta_atualizacao('cities_cases_full',atualizacao_tabelas,col2)

    if botao_atualizar and cities_cnes:
        alerta_atualizacao('cities_cnes',atualizacao_tabelas,col2)

    if botao_atualizar and cities_parameters:
        alerta_atualizacao('cities_parameters',atualizacao_tabelas,col2)

    if botao_atualizar and cities_rt:
        alerta_atualizacao('cities_rt',atualizacao_tabelas,col2)

    if botao_atualizar and cities_vacina:
        alerta_atualizacao('cities_vacina',atualizacao_tabelas,col2)

    if botao_atualizar and owid:
        alerta_atualizacao('owid',atualizacao_tabelas,col2)

    if botao_atualizar and states_cases_full:
        alerta_atualizacao('states_cases_full',atualizacao_tabelas,col2)

    if botao_atualizar and states_parameters:
        alerta_atualizacao('states_parameters',atualizacao_tabelas,col2)

    if botao_atualizar and states_rt:
        alerta_atualizacao('states_rt',atualizacao_tabelas,col2)

    if botao_atualizar and states_vacina:
        alerta_atualizacao('states_vacina',atualizacao_tabelas,col2)


def alerta_atualizacao(tabela,atualizacao_tabelas,col2):
    sucesso = 'Tabela {tabela} atualizada com sucesso!'
    aviso = 'Tabela {tabela} já foi atualizada hoje.'
    erro = 'Erro ao atualizar tabela {tabela}.'

    if atualizacao_tabelas[atualizacao_tabelas['tabela'] == tabela]['data_atualizacao'].max().normalize()==pd.to_datetime('today').normalize():
        col2.warning(aviso.format(tabela=tabela))
    else:
        resultado = eval('atualizar_{tabela}()'.format(tabela=tabela))
        if resultado:
            col2.success(sucesso.format(tabela=tabela))
        else:
            col2.error(erro.format(tabela=tabela))


def atualizar_cities_cases_full():
    try:
        cities_cases_full = pd.read_csv('http://datasource.coronacidades.org/br/cities/cases/full')
        cities_cases_full_filtro = ['active_cases', 'city_id', 'daily_cases', 'daily_cases_mavg',
                                'daily_cases_mavg_100k', 'deaths','estimated_cases',
                                'last_updated', 'new_deaths', 'new_deaths_mavg',
                                'new_deaths_mavg_100k', 'state_num_id', 'total_estimated_cases']
        cities_cases_full_filtrado = cities_cases_full[cities_cases_full_filtro]
        engine.execute(sa_text('''truncate table cities_cases_full''').execution_options(autocommit=True))
        cities_cases_full_filtrado.to_sql('cities_cases_full',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['cities_cases_full'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_cities_cnes():
    try:
        cities_cnes = pd.read_csv('http://datasource.coronacidades.org/br/cities/cnes')
        cities_cnes_filtro = ['city_id', 'last_updated_number_beds',
                          'last_updated_number_covid_icu_beds', 'last_updated_number_icu_beds',
                          'last_updated_number_ventilators', 'number_beds',
                          'number_covid_icu_beds', 'number_icu_beds', 'number_ventilators', 'state_num_id']
        cities_cnes_filtrado = cities_cnes[cities_cnes_filtro]
        engine.execute(sa_text('''truncate table cities_cnes''').execution_options(autocommit=True))
        cities_cnes_filtrado.to_sql('cities_cnes',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['cities_cnes'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_cities_parameters():
    try:
        cities_parameters = pd.read_csv('http://datasource.coronacidades.org/br/cities/parameters')
        cities_parameters_filtro = ['city_id', 'fatality_ratio', 'hospitalized_by_age_perc',
                                'i1_percentage', 'i2_percentage', 'i3_percentage', 'data_last_refreshed']
        cities_parameters_filtrado = cities_parameters[cities_parameters_filtro]
        engine.execute(sa_text('''truncate table cities_parameters''').execution_options(autocommit=True))
        cities_parameters_filtrado.to_sql('cities_parameters',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['cities_parameters'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_cities_rt():
    try:
        cities_rt = pd.read_csv('http://datasource.coronacidades.org/br/cities/rt')
        cities_rt_filtro = ['Rt_most_likely', 'Rt_most_likely_mavg', 'Rt_most_likely_mavg_100k', 'city_id', 'last_updated']
        cities_rt_filtrado = cities_rt[cities_rt_filtro]
        engine.execute(sa_text('''truncate table cities_rt''').execution_options(autocommit=True))
        cities_rt_filtrado.to_sql('cities_rt',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['cities_rt'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_states_cases_full():
    try:
        states_cases_full = pd.read_csv('http://datasource.coronacidades.org/br/states/cases/full')
        states_cases_full_filtro = ['active_cases', 'confirmed_cases', 'daily_cases',
                                'daily_cases_mavg', 'daily_cases_mavg_100k', 'deaths',
                                'last_updated', 'new_deaths','new_deaths_mavg',
                                'new_deaths_mavg_100k', 'state_num_id', 'total_estimated_cases']
        states_cases_full_filtrado = states_cases_full[states_cases_full_filtro]
        engine.execute(sa_text('''truncate table states_cases_full''').execution_options(autocommit=True))
        states_cases_full_filtrado.to_sql('states_cases_full',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['states_cases_full'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_states_parameters():   
    try:
        states_parameters = pd.read_csv('http://datasource.coronacidades.org/br/states/parameters')
        states_parameters_filtro = ['fatality_ratio', 'hospitalized_by_age_perc', 'i1_percentage',
                                    'i2_percentage', 'i3_percentage', 'state_num_id']
        states_parameters_filtrado = states_parameters[states_parameters_filtro]
        engine.execute(sa_text('''truncate table states_parameters''').execution_options(autocommit=True))
        states_parameters_filtrado.to_sql('states_parameters',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['states_parameters'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_states_rt():
    try:
        states_rt = pd.read_csv('http://datasource.coronacidades.org/br/states/rt')
        states_rt_filtro = ['Rt_most_likely', 'Rt_most_likely_mavg', 'Rt_most_likely_mavg_100k', 'last_updated', 'state_num_id']
        states_rt_filtrado = states_rt[states_rt_filtro]
        engine.execute(sa_text('''truncate table states_rt''').execution_options(autocommit=True))
        states_rt_filtrado.to_sql('states_rt',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['states_rt'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_states_vacina():
    try:
        states_vacina = pd.read_csv('http://datasource.coronacidades.org/br/states/vacina')
        states_vacina_filtro = ['imunizados', 'last_updated', 'nao_vacinados', 'perc_imunizados',
                                'perc_vacinados', 'state_num_id', 'vacinados']
        states_vacina_filtrado = states_vacina[states_vacina_filtro]
        engine.execute(sa_text('''truncate table states_vacina''').execution_options(autocommit=True))
        states_vacina_filtrado.to_sql('states_vacina',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['states_vacina'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_cities_vacina():  
    try:
        cities_vacina = pd.read_csv('http://datasource.coronacidades.org/br/cities/vacina')
        cities_vacina_filtro = ['city_id', 'imunizados', 'last_updated', 'nao_vacinados', 'perc_imunizados',
                                'perc_vacinados', 'state_num_id', 'vacinados']
        cities_vacina_filtrado = cities_vacina[cities_vacina_filtro]
        engine.execute(sa_text('''truncate table cities_vacina''').execution_options(autocommit=True))
        cities_vacina_filtrado.to_sql('cities_vacina',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['cities_vacina'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado


def atualizar_owid(): 
    try:
        owid = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
        owid_filtro = ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases',
                       'new_cases_smoothed', 'total_deaths', 'new_deaths',
                       'new_deaths_smoothed', 'new_cases_smoothed_per_million',
                       'new_deaths_per_million', 'new_deaths_smoothed_per_million', 'reproduction_rate',
                       'icu_patients', 'icu_patients_per_million', 'hosp_patients',
                       'hosp_patients_per_million', 'weekly_icu_admissions',
                       'weekly_hosp_admissions',
                       'new_tests', 'total_tests',
                       'total_tests_per_thousand', 'new_tests_per_thousand',
                       'positive_rate', 'tests_per_case', 'total_vaccinations',
                       'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
                       'population', 'population_density', 'median_age', 'gdp_per_capita', 'extreme_poverty',
                       'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
                       'male_smokers', 'hospital_beds_per_thousand',
                       'life_expectancy', 'human_development_index']
        owid_filtrado = owid[owid_filtro]
        engine.execute(sa_text('''truncate table owid''').execution_options(autocommit=True))
        owid_filtrado.to_sql('owid',engine,if_exists='append',index=False)
        pd.DataFrame({'tabela':['owid'],'data_atualizacao':[pd.Timestamp.now()]}).to_sql('atualizacao_tabelas',engine,if_exists='append',index=False)
        resultado = True
    except:
        resultado = False
    finally:
        return resultado
