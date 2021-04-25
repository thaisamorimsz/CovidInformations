query_lista_localidades = 'select distinct(location) as "Localidade" from owid order by location'

query_linha_mundo = '''
  select
    location as "Localidade",
    date as "Data",
    total_cases as "Total de casos",
    new_cases as "Novos casos",
    new_cases_smoothed as "Novos casos - média móvel",
    new_cases_smoothed_per_million as "Novos casos - média móvel por milhão",
    total_deaths as "Total de mortes",
    new_deaths as "Novas mortes",
    new_deaths_smoothed as "Novas mortes - média móvel",
    new_deaths_smoothed_per_million as "Novas mortes - média móvel por milhão",
    reproduction_rate as "R",
    hosp_patients as "Pacientes hospitalizados",
    hosp_patients_per_million as "Pacientes hospitalizados por milhão",
    icu_patients as "Pacientes na UTI",
    icu_patients_per_million as "Pacientes na UTI por milhão",
    total_tests as "Total de testes",
    new_tests as "Novos testes",
    tests_per_case as "Testes por caso",
    people_vaccinated as "Pessoas vacinadas",
    people_fully_vaccinated as "Pessoas imunizadas",
    new_vaccinations as "Novas vacinações"
  from owid
  where location in {}
'''

query_mapa_mundo = '''
  select
    iso_code,
    location as "Localidade",
    sum(new_cases) as "Casos",
    sum(new_deaths) as "Mortes",
    sum(new_tests) as "Testes",
    sum(new_vaccinations) as "Vacinações"
  from owid
  where
    date >= '{}'
    and date <= '{}'
  group by
    iso_code,
    location
'''

query_estados = '''select state_name from states_ids'''

query_linha_brasil = '''
    select
      state_name as "Estado",
      scf.last_updated as "Data",
      active_cases as "Casos atuais",
      confirmed_cases as "Casos confirmados",
      daily_cases as "Casos diários",
      daily_cases_mavg_100k as "Média móvel de casos diários por 100k",
      deaths as "Mortes",
      new_deaths as "Novas Mortes",
      new_deaths_mavg_100k as "Média móvel de novas mortes por 100k",
      sr."Rt_most_likely" as "R"
    from states_cases_full scf
    inner join states_ids si on si.state_num_id = scf.state_num_id
    full outer join states_rt sr on sr.state_num_id = scf.state_num_id and sr.last_updated = scf.last_updated
    where
      state_name in {}
    group by active_cases,confirmed_cases,daily_cases,daily_cases_mavg_100k,deaths,scf.last_updated,new_deaths,state_name,new_deaths_mavg_100k,sr."Rt_most_likely"
    order by scf.last_updated
'''

query_contorno = '''select geojson_file from geojson where place_num_id = {}'''

query_estado_id_nome = '''select state_num_id,state_name from states_ids'''


query_mapa_brasil = '''
    select 
      sv.state_num_id,
      state_name as "Estado",
      imunizados as "Imunizados",
      nao_vacinados as "Pessoas não vacinadas",
      perc_imunizados as "Percentual de pessoas imunizadas",
      perc_vacinados as "Percentual de pessoas vacinadas",
      vacinados as "Vacinados",
      sum(number_beds) as "Número de leitos",
      sum(number_covid_icu_beds) as "Número de leitos de UTI para Covid",
      sum(number_icu_beds) as "Número de leitos de UTI",
      sum(number_ventilators) as "Número de respiradores"
    from states_vacina sv
    inner join cities_cnes cc on cc.state_num_id = sv.state_num_id
    inner join states_ids si on si.state_num_id = sv.state_num_id 
    group by imunizados,nao_vacinados, perc_imunizados, perc_vacinados, vacinados,sv.state_num_id, state_name
'''

query_linha_estados = '''
    select
      ci.city_name as "Cidade",
      ccf.last_updated as "Data",
      active_cases as "Casos atuais",
      daily_cases as "Casos diários",
      daily_cases_mavg_100k as "Média móvel de casos diários por 100k",
      deaths as "Mortes",
      new_deaths as "Novas Mortes",
      new_deaths_mavg_100k as "Média móvel de novas mortes por 100k",
      cr."Rt_most_likely" as "R"
    from cities_cases_full ccf
    inner join states_ids si on si.state_num_id = ccf.state_num_id
    inner join cities_ids ci on ci.city_id = ccf.city_id
    full outer join cities_rt cr on cr.city_id = ccf.city_id and cr.last_updated = ccf.last_updated
    where
      state_name in {}
    group by active_cases,daily_cases,daily_cases_mavg_100k,deaths,ccf.last_updated,new_deaths,state_name,new_deaths_mavg_100k,cr."Rt_most_likely",ci.city_name
    order by ccf.last_updated
'''


query_mapa_estados = '''
    select
      cv.city_id,
      ci.city_name as "Cidade",
      si.state_name as "Estado",
      imunizados as "Imunizados",
      nao_vacinados as "Pessoas não vacinadas",
      perc_imunizados as "Percentual de pessoas imunizadas",
      perc_vacinados as "Percentual de pessoas vacinadas",
      vacinados as "Vacinados",
      sum(number_beds) as "Número de leitos",
      sum(number_covid_icu_beds) as "Número de leitos de UTI para Covid",
      sum(number_icu_beds) as "Número de leitos de UTI",
      sum(number_ventilators) as "Número de respiradores"
    from cities_vacina cv
    inner join cities_cnes cc on cc.city_id = cv.city_id
    inner join cities_ids ci on ci.city_id = cv.city_id
    inner join states_ids si on si.state_num_id = cv.state_num_id
    group by imunizados,nao_vacinados, perc_imunizados, perc_vacinados, vacinados,cv.city_id, ci.city_name,si.state_name
'''

query_atualizacao_tabelas = '''select distinct on (tabela) tabela,data_atualizacao from atualizacao_tabelas order by tabela,data_atualizacao desc'''