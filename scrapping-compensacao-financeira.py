import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

dir_path = os.getcwd()
chrome = dir_path+'\chromedriver.exe'

driver = webdriver.Chrome(chrome)
driver.get(url)

dfEmpresas = pd.read_excel('tabela_concessionarias.xlsx')
lista_ano = range(2016,2020)
dados_cf = []

for regiao in set(dfEmpresas['Região']):
    url = f'https://www2.aneel.gov.br/aplicacoes_liferay/Compensacao_de_Continuidade_Conformidade_v2/pesquisa.cfm?regiao={regiao}'
    driver.get(url)
    driver.implicitly_wait(30)
    
    for e in dfEmpresas[ dfEmpresas['Região'] == regiao]['Código']:
              
        for ano in lista_ano:
            
            tipo = Select(driver.find_element_by_name('tipo'))
            tipo.select_by_value('c')
            time.sleep(1)
            distribuidora = Select(driver.find_element_by_name('distribuidora'))
            distribuidora.select_by_value(str(e))
            time.sleep(1)
            periodo = Select(driver.find_element_by_name('periodo'))
            periodo.select_by_value(str(ano))
            
            driver.find_element_by_xpath('/html/body/div/table/tbody/tr[3]/td/input').click()
            time.sleep(2)
            
            registro = []
            
            registro.append(e)
            registro.append(ano)
            
            linha_1 = driver.find_element_by_xpath('/html/body/div/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/table/tbody/tr[6]')
            linha_2 = driver.find_element_by_xpath('/html/body/div/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/table/tbody/tr[7]')

            for i, x in enumerate(linha_1.find_elements_by_tag_name('td')):
                if i != 0:
                    registro.append(x.text.strip())

            for i, x in enumerate(linha_2.find_elements_by_tag_name('td')):
                if i != 0:
                    registro.append(x.text.strip())
            
            dados_cf.append(registro)

nome_colunas = ['distribuidora', 'ano', 'qtd_DFM_mes', 'qtd_DFM_tri', 'qtd_DFM_ano', 'qtd_DICRI_mes', 'qtd_total', 'valor_DFM_mes', 'valor_DFM_tri', 'valor_DFM_ano', 'valor_DICRI_mes', 'valor_total']
df = pd.DataFrame(dados_cf, columns = nome_colunas)
df.to_csv('base_compensacao_distribuidoras.csv', sep=';')