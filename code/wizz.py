#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:27:45 2020

@author: simplon
"""

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

donnees = pd.read_excel("/home/simplon/STAGE WIZZ/Reporting_mensuel_WIIIZ_-_Aout_2020_-_Simplon.xlsx")
engine=create_engine('mysql+pymysql://simplon:simplon@localhost:3306/wizz')
donnees = donnees.drop(columns = {'Site','Roaming','Année de fin'})
donnees = donnees.rename(columns = {'Année de début':'Annee'})
donnees.columns

#Preparation et insertion de la table Borne dans la base de données
borne_columns = ['Parc','Station','Borne','Type de prise','Prise','Fabricant']
borne_id = donnees.Borne
print(borne_id)
borne_id = borne_id.drop_duplicates()
print(borne_id)
borne_id = borne_id.reset_index(drop = True).reset_index().rename(columns={"index":"BO_ID"})
print(borne_id)

borne = donnees[borne_columns].drop_duplicates(subset=['Borne'])
borne = borne.merge(borne_id,on = 'Borne')
print(borne)
borne = borne.drop_duplicates()
borne.to_sql('Borne',con = engine,if_exists='append',index=False)
#Preparation et insertion de la table Utilisation dans la base de données

util_columns = ['Date de début', 'Jour de début', 'Mois de début', 'Annee',
        'Heure de début ', 'Minute de Début', 'Date de fin', 'Jour de fin',
        'Mois de fin', 'Heure de fin', 'Minute de fin', 'Durée (sec)',
        "L'énergie (Wh)", 'Puissance max (W)']

util = donnees[util_columns].reset_index().rename(columns={"index":"UT_ID","Heure de début ":"UT_heure_début"})
print(util.columns)
util.to_sql('Utilisation',con = engine,if_exists='append',index=False)
#Preparation et insertion de la table Client dans la base de données
util_id = util.UT_ID.reset_index()

client_columns =['Nom du client','Nom du badge','Référence MobeePass','UUID Badge']
client = donnees[client_columns].drop_duplicates(subset='UUID Badge').fillna(value='Unknown').reset_index()
client = client.merge(util_id,on='index')
client = client.rename(columns={"UT_ID":"CL_UT_id"}).drop(columns={'index'})
client.to_sql('Client',con=engine,if_exists='append',index=False)
#Preparation et insertion de la table Enregistrement dans la base de données

util_id_enr = donnees['Borne'].reset_index().rename(columns={"index":"UT_ID"})
enr = util_id_enr.merge(borne_id,on='Borne')
enr = enr.drop(columns={'Borne'})
enr.to_sql("Enregistrement",con=engine,if_exists="append",index=False)

