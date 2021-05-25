from bs4 import BeautifulSoup
import codecs
import csv
import json
from pathlib import Path

"""
IDEES A RAJOUTER
- ordonner les métadonnées dans le json
- séparer temps total et temps longueur
- attention retour à la ligne si distance>250m
"""

#functions
def save_csv(path,name,table):
    with open(path+name+"/"+name+".csv", mode='w+' ,newline='') as csv_file:
        csv_file_writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in table:
            csv_file_writer.writerow(i)


def save_json(path,name,sex,nage,epreuve,dist,lignes):
    data = {'name':name,'sexe':sex,'nage':nage,'epreuve':epreuve,'distance':dist,'lignes':lignes}

    with open(path+name+"/"+name+".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4,sort_keys=True)


def formating_metadata(type,serie,sex,dist,k):
    if sex == 'WOMEN':
        sex = 'dames'
    elif sex == 'MEN':
        sex = 'hommes'
    elif sex == 'MIXED':
        sex = 'mixte'
    else:
        Print("Error: metadata[sex] unknown")

    if type == 'FREESTYLE':
        nage = 'freestyle'
    elif type == 'BACKSTROKE':
        nage = 'dos'
    elif type == 'BUTTERFLY':
        nage = 'papillon'
    elif type == 'BREASTSTROKE':
        nage = 'brasse'
    else:
        print("Error: metadata[type] unknown")

    if serie == 'PRELIMINARY':
        epreuve = 'serie'+str(k)
    elif serie == 'FINAL':
        epreuve = 'finale'+str(k)
    elif serie == 'SEMIFINAL':
        epreuve = 'demi'+str(k)
    else:
        print("Error: metadata[serie] unknown")

    name = "2021_Budapest_"+nage+"_"+sex+"_"+dist+"_"+epreuve
    return name,nage,epreuve,sex,dist

def new_columns(table):
# Ajout des colonnes Nom de famille, Prénoms et Date de naissance
    for i in range(len(table)):
        if i == 0:
            table[i].insert(4, 'SURNAME')
            table[i].insert(5, 'NAME')
            table[i].insert(6, 'BIRTH')
        else :
            [surname,name_date] = table[i][3].split('\xa0')[0:2]
            [name,date] = name_date.split('(')
            date = date.replace(')','')
            table[i].insert(4, surname)
            table[i].insert(5,name)
            table[i].insert(6,date)
        table[i].pop(3)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def str_to_numbers(table):
# Remplacement des strings en nombres
    for i in range (len(table)):
        for j in range(len(table[i])):
            if table[i][j].isdigit():
                table[i][j] = int(table[i][j])
            elif isfloat(table[i][j]):
                table[i][j] = float(table[i][j])

def delete_xa0(table):
# Suppression des \xa0
    for i in range(len(table)):
        for j in range (len(table[i])):
            if isinstance(table[i][j],str):
                table[i][j] = table[i][j].replace('\xa0','')

def formating_data(table):
    str_to_numbers(table)
    new_columns(table)
    delete_xa0(table)

def collecting_run(data2,nombre_nageur, index):
    delete_list = ['\xa0','','q','R1','R2','R','WR-ER-CR']
    for j in range(index,index+nombre_nageur+1):
        base_data = list(list(data2.children)[j].children)
        for i in range(len(base_data)):
            if (base_data[i].get_text() not in delete_list):
                table[j-index].append(base_data[i].get_text())




path = "C:/Users/Simon/Desktop/Stage d'Application/Scraping internet/"

# Ouverture du fichier en local (On a enregistré le fichier html de la page au préalable)
page = codecs.open('C:/Users/Simon/Desktop/European Championships 2020 _ Budapest5.html','r','utf-8')
soup = BeautifulSoup(page.read())

# Collecte des métadonnées
metadata_raw = soup.find("td", {"id": "tdGaraRound"})
metadata_raw = list(metadata_raw.children)[-1].get_text()
metadata_raw = metadata_raw.replace('-','')
metadata = metadata_raw.split(" ")

if metadata[4]=='X':
    type_raw = metadata[-3]
    serie_raw = metadata[-1]
    sex_dist = metadata[3].split('\xa0')
    sex_raw = sex_dist[0]
    dist_raw='4x100'

else:
    type_raw = metadata[-3]
    serie_raw = metadata[-1]
    sex_dist = metadata[3].split('\xa0')
    sex_raw = sex_dist[0]
    dist_raw = sex_dist[-1].replace('M','')

# On identifie la partie de la page où l'on cherche les données à scraper
data = soup.find("table", {"id": "tblContenuti "})
data2 = data.find("tbody")
listed_data = list(data2.children)


l=3 # indice
k=1 #nombre de run

while l<len(listed_data):
    nombre_nageur = 0
    while len(listed_data[l+nombre_nageur])!=1:
        nombre_nageur+=1

    # Collecting data in a table
    table=[[] for i in range(nombre_nageur)]
    collecting_run(data2,nombre_nageur,l)

    # Print
    for i in table:
        print(i)
    print('')

    # Formating the data for csv
    formating_data(table)

    # formatting metadata for json file
    data_json = {}
    name,nage,epreuve,sex,dist = formating_metadata(type_raw,serie_raw,sex_raw,dist_raw,k)
    lignes = {}
    for i in range(1,nombre_nageur):
        lignes["ligne"+str(i)]=table[i][3]+" "+table[i][4]

    # Create folder
    try:
        os.makedirs(path+name)
    except FileExistsError:
        pass

    # Write json file with metadata
    save_json(path,name,sex,nage,epreuve, dist,lignes)

    # Write csv file with data
    save_csv(path,name,table)

    l+= nombre_nageur+5
    k+=1

