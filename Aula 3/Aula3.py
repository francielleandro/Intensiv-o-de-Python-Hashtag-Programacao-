# importando o selenium: import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
path = "/home/francielleandro/Projetos/chromedriver_linux64/chromedriver" #diretorio onde o webdriver esta
navegador = webdriver.Chrome(executable_path=r"/home/francielleandro/Projetos/chromedriver_linux64/chromedriver") #instanciando o webdriver
#acessando o google e pesquisar a cotação do dolar
#para acessar uma pagina web -> navegador.get("www.google.com") - neste caso abrimos o google
#PEGAR COTAÇÕES DO GOOGLE
def pegar_cotacao_by_google(moeda):
    #BLOCO 1 - Fazendo a pesquisa
    navegador.get("http://www.google.com")
    XPATH = "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input"#xpath obtido atraves da inspeção do console F12
    campo_de_busca = navegador.find_element(By.XPATH,XPATH)#acessar o elemento atraves do XPATH
    campo_de_busca.send_keys(f'Cotação {moeda}') #enviando input para o navegador
    campo_de_busca.send_keys(Keys.ENTER) #enviando o comando enter
    #FIM BLOCO 1
    #navegador.get("https://www.google.com/search?q=cota%C3%A7%C3%A3o+dolar") #O BLOCO 1 pode ser substituido por essa linha
    #BLOCO 2 - Pegando os valores
    XPATH = '//*[@id="knowledge-currency__updatable-data-column"]/div[3]/table/tbody/tr[3]/td[1]/input'
    campo_valor = navegador.find_element(By.XPATH,XPATH)
    valor = campo_valor.get_attribute('value')
    valor_formatado = valor.replace(",",".")
    print(valor_formatado)
    #FIM BLOCO 2
    return valor_formatado


def pegar_cotacao_ouro():
    navegador.get('https://www.melhorcambio.com/ouro-hoje')
    XPATH = '//*[@id="comercial"]'
    campo_valor = navegador.find_element(By.XPATH,XPATH)#acessar o elemento atraves do XPATH
    valor = campo_valor.get_attribute('value')
    valor_formatado = valor.replace(",",".")
    print(valor_formatado)
    return valor_formatado

cotacao_euro = pegar_cotacao_by_google('euro')
cotacao_dolar = pegar_cotacao_by_google('dolar')
cotacao_ouro = pegar_cotacao_ouro()

navegador.quit()

#importando o pandas para tratar dados
import pandas as pd
PATH = '/home/francielleandro/Projetos/Python/Intensivão python/Aula 3/Produtos.xlsx'
tabela = pd.read_excel(PATH)#importando arquivos

# display(tabela)#exibindo a tabela

tabela.loc[tabela['Moeda'] == 'Dólar','Cotação'] = float(cotacao_dolar)#tabela.loc[0,'Cotação'] = float(cotacao_dolar) ->pode-se utilizar o indice
tabela.loc[tabela['Moeda'] == 'Euro','Cotação'] = float(cotacao_euro)
tabela.loc[tabela['Moeda'] == 'Ouro','Cotação'] = float(cotacao_ouro)

# display(tabela)

tabela['Preço de Compra'] = tabela['Preço Original']*tabela['Cotação']
# display(tabela)

tabela['Preço de Venda'] = tabela['Preço de Compra']*tabela['Margem']
# display(tabela)

from datetime import date

data_atual = date.today()
print(data_atual)
tabela.to_excel(f'Produtos {data_atual}.xlsx',index= False)

#para criar um executavel, instale o pyinstaller com pip install pyinstaller
#para criar é: pyinstaller --onefile Aula3.py 