import string
import os
import urllib.request
import MySQLdb
from bs4 import BeautifulSoup
import sys
import locale
#variaveis globais

if os.path.exists('errorLog.txt'):
    os.remove('errorLog.txt')

errorLog = open('errorLog.txt','w')

link_base       = "https://empresasdobrasil.com.br"
link_estado     = "/empresas/amapa/"
link_atividades = "/atividades-de-organizacoes-religiosas"

#link_pag = link_base + "/empresas/goias/goiania/atividades-de-organizacoes-religiosas/page/"

headers = {}
headers['User-Agent'] = 'GoogleBot'

def ler_cidade(link):
    if link is None:
        return
    
    soup = get_html(link)
    lista_cidades = soup.find(attrs={"class":"large-12 columns margin-top-2 regiones"})

    tamanho_link_estado = len(link_estado)
    print(tamanho_link_estado)
    
    for lista in lista_cidades.findAll(attrs={"class": "link-directorio"}):
        if lista is None:
            continue
        
    
        valor = lista.a    
        cidade = valor.get("href")
        cidade = cidade[tamanho_link_estado:]
        print(cidade)    
        
        link_completo = link_base + link_estado + cidade + link_atividades + "/page/"
        
        print(link_completo)
        print("################################################################################################")
        print("                                           Mudando de Cidade                                    ")
        print("################################################################################################")
        run(link_completo)

def run(link_completo):
    if link_completo is None:
        return

    soup = get_html(link_completo + str(1))

    pagina_atual = soup.find(attrs={"id":"page"})

    print (pagina_atual)

    ultima_pagina = pagina_atual.find(attrs={"class":"large-12 columns pagination-centered margin-top-1"})
    tamanho_endereco_pag = len(link_completo)
    print("Tamanho endereco Pag: ")
    print(tamanho_endereco_pag)
    print(ultima_pagina)
    
    valor_string = str(pagina_atual)
    resultado = valor_string.count("»")
    print("tetetetet" ,resultado)

    if resultado > 0:
        for lista in ultima_pagina.findAll(attrs={"class": "arrow"}):
            if lista is None:
                continue

            valor = lista.a    
        
        link_ultimo_completo = link_base + valor.get("href")
        print(valor.get("href"))    

        endereco_pag_total = len(link_ultimo_completo)
        print("Pagina Total")
        print(endereco_pag_total)
        
        print("------------------------")
        page_end = link_ultimo_completo[tamanho_endereco_pag:endereco_pag_total]
        print(page_end)

        total_pag = page_end + str(1)        
    
        for i in range(1,int(total_pag)):

            soup = get_html(link_completo + str(i))

            if soup is None:
                return

            people_list = soup.find(attrs={"id":"page"})
                    
            for people in people_list.findAll(attrs={"class": "row padding-left-right-1"}):
                if people is None:
                    continue
                
                people_data = (people.find(attrs={"class": "large-12 columns small-centered medium-centered colegio-list"}))

                if people_data is None:
                    continue

    #           name = people_data.a.text
                link = people.a.get("href")

                get_data_child(link_base + link)
         
#        print(name)
#        print(link)

def get_data_child(link):
    soup = get_html(link)

    if soup is None:
        return
    
    data = soup.find(attrs={"id": "content"})

    people_conteudo = (data.find(attrs={"class": "large-12 columns margin-top-1"}))

    lista_objeto = []
    name = people_conteudo.h1.text
    name = name.replace('"','')    
    telefone =""
    email    =""
    atividade_economica = ""
    classificacao_cnae = ""
    fonte_dados = ""
    natureza_juridica = ""
    tamanho_estabelecimento = ""
    codigo_cnae = ""
    endereco =""
    cep=""
    bairro=""
    cidade=""
    estado=""
    endereco2 = ""
    bairro2 = ""
    cidade2 = ""
    estado2 = ""
    outros = ""
    
    print ('-------------------------------------------------------------------------------------------------------')
    print (name)

    people_detail_list = soup.find(attrs={"id":"page"})

    lista_objeto.append(name)
    count = 1 
    insert = 'INSERT INTO pessoas (nome,telefone,email,estado,cidade,cep,bairro,endereco,atividade_economica,tamanho_estabelecimento,cnae,fonte_dados) VALUES ("%s", "%s", "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
    for people_detail in people_detail_list.findAll(attrs={"class": "row padding-left-right-1 info-establ"}):
        if people_detail is None:
            continue
        
        conn = connectDB()
        conn.autocommit(False)
        cursor = conn.cursor()

        p_detail =""        
        p_detail_title =""
        
        for p in people_detail.findAll('p'):
            p_detail = p.find(attrs={"class": "info"})
            p_detail_title = p.find(attrs={"class": "title-field"})
            print( str(count) + " ---" + p_detail_title.text)
            print( str(count) + " ---" + p_detail.text)
            
            if (p_detail_title.text == "Atividad Econômica:" ):
                atividade_economica = p_detail.text          
            
            if (p_detail_title.text == "Telefone:" ):
                telefone = p_detail.text          

            if (p_detail_title.text == "Código de endereçamento postal:" ):
                cep = p_detail.text            

            if (p_detail_title.text == "Endereço:" ):
                endereco = p_detail.text            
            
            if (p_detail_title.text == "Bairro:" ):
                bairro = p_detail.text            

            if (p_detail_title.text == "Email:" ):
                email = p_detail.text         

            if (p_detail_title.text == "Município:" ):
                cidade = p_detail.text         
            
            if (p_detail_title.text == "Uf:" ):
                estado = p_detail.text         
            
            if (p_detail_title.text == "Tamanho do estabelecimento:" ):
                tamanho_estabelecimento = p_detail.text         
            
            if (p_detail_title.text == "Código cnae:" ):
                codigo_cnae = p_detail.text         
            
            if (p_detail_title.text == "Fonte de dados:" ):
                fonte_dados = p_detail.text         
         

            count += 1        
        
    insert %= (name,telefone,email.lower(),estado,cidade,cep,bairro,endereco,atividade_economica,tamanho_estabelecimento,codigo_cnae,fonte_dados)
    cursor.execute(insert)
    conn.commit()
            
        

def connectDB():
    return MySQLdb.connect(host="localhost", user="root", passwd="root", db="webcrawler")        


def get_html(link):
    request = urllib.request.Request(link,headers=headers)
    return BeautifulSoup(urllib.request.urlopen(request),"html.parser")

if __name__ == "__main__":
    ler_cidade(link_base + link_estado)
