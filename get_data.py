import requests
import csv
import json

import json
import matplotlib.pyplot as plt
import numpy as np

#from geopy.geocoders import Nominatim
#geolocator = Nominatim(user_agent="andrei.garbo@gmail.com")


datafile = open("./pv_part_cnty_prsd_cj.csv", 'r', encoding='utf-8')

candidati = {
    "ELENA-VALERICA LASCONI-voturi" : 0,
    "GEORGE-NICOLAE SIMION-voturi" : 0,
    "ION-MARCEL CIOLACU-voturi" : 0,
    "NICOLAE-IONEL CIUCĂ-voturi" : 0,
    "HUNOR KELEMEN-voturi" : 0,
    "MIRCEA-DAN GEOANĂ-voturi" : 0,
    "ANA BIRCHALL-voturi" : 0,
    "ALEXANDRA-BEATRICE BERTALAN-PĂCURARU-voturi" : 0,
    "SEBASTIAN-CONSTANTIN POPESCU-voturi" : 0,
    "LUDOVIC ORBAN-voturi" : 0,
    "CĂLIN GEORGESCU-voturi" : 0,
    "CRISTIAN DIACONESCU-voturi" : 0,
    "CRISTIAN-VASILE TERHEȘ-voturi" : 0,
    "SILVIU PREDOIU-voturi" : 0
}

cartiere = {
    "Gheorgheni" : dict(candidati),
    "Mărăști" : dict(candidati),
    "Mănăștur" : dict(candidati),
    "Zorilor" : dict(candidati),
    "Centru" : dict(candidati),
    "Bulgaria" : dict(candidati),
    "Andrei Mureșanu" : dict(candidati),
    "Becaș" : dict(candidati),
    "Borhanci" : dict(candidati),
    "Dâmbul Rotund" : dict(candidati),
    "Bună Ziua" : dict(candidati),
    "Europa" : dict(candidati),
    "Făget" : dict(candidati),
    "Grădini Manastur" : dict(candidati),
    "Plopilor" : dict(candidati),
    "Zorilor" : dict(candidati),
    "Gruia" : dict(candidati),
    "Grigorescu" : dict(candidati),
    "Iris" : dict(candidati),
    "Între Lacuri" : dict(candidati),
    "Măgura" : dict(candidati),
    "Someșeni" : dict(candidati),
    "Sopor" : dict(candidati)
}

csv_reader = csv.DictReader(datafile, delimiter=',')
cartiere_file = open("cartiere_sectii.txt", 'r', encoding='utf-8')

for row in csv_reader:
    if row["uat_name"] == "MUNICIPIUL CLUJ-NAPOCA":
        found = False
        for cartier_line in cartiere_file:
            if row["precinct_name"] in cartier_line:
                for cartier in cartiere:
                    if cartier in cartier_line:
                        found = True
                        for candidat in candidati:
                            cartiere[cartier][candidat] = cartiere[cartier][candidat] + int(row[candidat])
        cartiere_file.seek(0)
        if not found:
            print(row["precinct_name"])

with open("rezultate.json", 'w') as fisier_final:
    print(json.dumps(cartiere), file=fisier_final)

with open("rezultate.json", 'r', encoding='utf-8') as fisier_final:
    json_cartiere = json.load(fisier_final)
    with open("visualize.txt", 'w', encoding='utf-8') as fisier_out: 
        print(json.dumps(json_cartiere, indent=4), file=fisier_out)

candidati = list(json_cartiere[list(json_cartiere.keys())[0]].keys())
cartiere = list(json_cartiere.keys())


#plot the data
for cartier in cartiere:
    fig, ax = plt.subplots(figsize=(10, 6))

    votes = [json_cartiere[cartier][candidat] for candidat in candidati]
    
    x = np.arange(len(candidati))
    
    bars = ax.bar(x, votes, tick_label=candidati, color='skyblue')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=9)

    candidati_nume_scurtat = [label[:-7] for label in candidati]

    ax.set_title(f'Voturi în {cartier}')
    ax.set_ylabel('Voturi')
    ax.set_xlabel('Candidați')
    ax.set_xticklabels(candidati_nume_scurtat, rotation=45, ha='right')

    plt.tight_layout() 
    plt.show()






#manual_file = open("cartiere_manual.txt", "w", encoding='utf-8')
#automatic_file = open("cartiere_automat.txt", "w", encoding='utf-8')
#for row in csv_reader:
#    if row["uat_name"] == "MUNICIPIUL CLUJ-NAPOCA":
#        #print(row["precinct_name"],row["uat_name"])
#        location = geolocator.geocode(row["precinct_name"])
#        if location:
#            with_data = with_data + 1
#            found = False
#            for key in location:
#                for cartier in cartiere:
#                    if cartier in key and ("CLUJ" in key or "Cluj" in key) and not found: 
#                        found = True
#                        cartiere[cartier] = cartiere[cartier] + 1
#                        print(row["precinct_name"], ",", cartier, file=automatic_file)
#        else:
#            manual_list.append(row["precinct_name"])
#            without_data = without_data + 1

