from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
from datetime import datetime

atual = datetime.now()
hoje = datetime.today()

data = f'{hoje.day}/{hoje.month}/{hoje.year}'
horario = atual.strftime("%H:%M:%S")


option = Options()
option.add_argument('--headless')

navegador = webdriver.Chrome(options=option)
navegador.get('https://www.linkedin.com/jobs/search?keywords=Marketing%20E%20Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F&f_E=1&position=1&pageNum=0')

sleep(2)

site = bs(navegador.page_source, 'html.parser')

links = site.find('ul', attrs={'class': 'jobs-search__results-list'})
li = links.findAll('li')

lista_dados_scraping = []


for lista in li:
    link = lista.find('a', attrs={'class', 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})
    link1 = lista.find('a', attrs={'class', 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'})
    if link:
        print(link['href'])
        vaga = webdriver.Chrome(options=option)
        vaga.get(link['href'])
        sleep(1)

        urlEmpresa = link['href'] 

        siteVaga = bs(vaga.page_source, 'html.parser')

        topo_do_bloco = siteVaga.find('div', attrs={'class': 'top-card-layout__card relative p-2 papabear:p-details-container-padding'})

        #
        linkEmpresa = topo_do_bloco.find('a')
        if linkEmpresa:
            linkEmpresa = linkEmpresa['href']
        else:
            linkEmpresa = 'URL da empresa não encontrada'
        #
        nomeEmpresa = topo_do_bloco.find('a', attrs={'class': 'topcard__org-name-link topcard__flavor--black-link'})
        cidadeEmpresa = topo_do_bloco.find('span', attrs={'class': 'topcard__flavor topcard__flavor--bullet'})
        quantidadeAplicacoes = topo_do_bloco.find('span', attrs={'class': 'num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet'})
        
        if nomeEmpresa != None:
            print(nomeEmpresa.text)
            nomeEmpresa = nomeEmpresa.text
        else:
            nomeEmpresa = 'nome não encontrado'
            print(nomeEmpresa)
        #
        if cidadeEmpresa:
            print(cidadeEmpresa.text)
            cidadeEmpresa = cidadeEmpresa.text
        else:
            cidadeEmpresa = 'Cidade não encontrada'
            print(cidadeEmpresa)
        #
        if quantidadeAplicacoes != None:
            print(quantidadeAplicacoes.text)
            quantidadeAplicacoes = quantidadeAplicacoes.text
        else:
            quantidadeAplicacoes = 'Quantidade de aplicações não encontrada'
            print(quantidadeAplicacoes)
        #
        inferior_do_bloco = site.find('div', attrs={'class': 'core-section-container__content break-words'})

        li = inferior_do_bloco.findAll('li')

        lista = []

        for itens in li:
            span = itens.find('span', attrs={'class': 'description__job-criteria-text description__job-criteria-text--criteria'})
            if span:
                span = span.text
                lista.append(span)

        nivelExperiencia = lista[0]
        tempoEstagio = lista[1]
        funcaoEstagio = lista[2]

        print(nivelExperiencia, tempoEstagio, funcaoEstagio)

    elif link1:
        print(link1['href'])
        vaga1 = webdriver.Chrome(options=option)
        vaga1.get(link1['href'])
        sleep(1)

        urlEmpresa = link1['href']

        siteVaga = bs(vaga1.page_source, 'html.parser')

        topo_do_bloco = siteVaga.find('div', attrs={'class': 'top-card-layout__card relative p-2 papabear:p-details-container-padding'})

        linkEmpresa = topo_do_bloco.find('a', attrs={'class': 'topcard__org-name-link topcard__flavor--black-link'})
        if linkEmpresa:
            linkEmpresa = linkEmpresa['href']
        else:
            linkEmpresa = 'URL da empresa não encontrada'

        nomeEmpresa = topo_do_bloco.find('a', attrs={'class': 'topcard__org-name-link topcard__flavor--black-link'})
        cidadeEmpresa = topo_do_bloco.find('span', attrs={'class': 'topcard__flavor topcard__flavor--bullet'})
        quantidadeAplicacoes = topo_do_bloco.find('span', attrs={'class': 'num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet'})

        ''' if linkEmpresa:
            print('Link da empresa: ', linkEmpresa['href'])
            linkEmpresa = linkEmpresa['href']
        else:
            linkEmpresa = 'URL da dempresa não encontrada'
            print(linkEmpresa)'''
        #

        if nomeEmpresa != None:
            print(nomeEmpresa.text)
            nomeEmpresa = nomeEmpresa.text
        else:
            nomeEmpresa = 'nome não encontrado'
        #    
        if cidadeEmpresa:
            print(cidadeEmpresa.text)
            cidadeEmpresa = cidadeEmpresa.text
        else:
            cidadeEmpresa = 'Cidade não encontrada'
            print(cidadeEmpresa)
        #
        if quantidadeAplicacoes != None:
            print(quantidadeAplicacoes.text)
            quantidadeAplicacoes = quantidadeAplicacoes.text
        else:
            quantidadeAplicacoes = 'Quantidade de aplicações não encontrada'
            print(quantidadeAplicacoes)

        inferior_do_bloco = site.find('div', attrs={'class': 'core-section-container__content break-words'})

        li = inferior_do_bloco.findAll('li')

        lista = []

        for itens in li:
            span = itens.find('span', attrs={'class': 'description__job-criteria-text description__job-criteria-text--criteria'})
            if span:
                span = span.text
                lista.append(span)

        nivelExperiencia = lista[0]
        tempoEstagio = lista[1]
        funcaoEstagio = lista[2]

        print('\n', nivelExperiencia,'\n',tempoEstagio, '\n',funcaoEstagio)

    else:
        print('Link não encontrando através da classe')
    
    lista_dados_scraping.append([nomeEmpresa, linkEmpresa, urlEmpresa,cidadeEmpresa, nivelExperiencia, tempoEstagio, funcaoEstagio, quantidadeAplicacoes, horario, data])

    sleep(0.5)

lista_vagas_organizada = pd.DataFrame(lista_dados_scraping, columns=['Nome da Empresa', 'URL da Empresa','URL da vaga' , 'Cidade da Empresa', 'Nivel de experiência', 'Tempo de estágio', 'Função do estágio', 'Quantidade de aplicações', 'Horário do Scraping', 'Data do Scraping'])
lista_vagas_organizada.to_excel('webScrapingLinkedin.xlsx', index=False)

sleep(2)