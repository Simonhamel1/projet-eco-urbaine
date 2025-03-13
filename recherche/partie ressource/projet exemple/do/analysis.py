#############################
################################
####### IMPORTATION PACKAGES##########
#############################
################################
import geopandas as gpd
import requests 
import zipfile 
import pandas as pd
import os
from io import BytesIO
import py7zr
import shapefile
import numpy as np
import matplotlib.pyplot as plt 
from stargazer.stargazer import Stargazer
import statsmodels.api as sm

#############################
################################
####### DOSSIER ##########
#############################
################################
directory=r'C:\Dropbox\cours\urban CY tech 2\exemple'
#Dowlnoad shapefile from COMMUNES


#############################
################################
####### TELECHARGEMENT DONNEES ##########
#############################
################################


#############################
################################
####### CARTES COMMUNES ET AIRES URBAINES ##########
#############################
################################
#Ancienne URL
url='https://wxs.ign.fr/oikr5jryiph0iwhw36053ptm/telechargement/inspire/GEOFLA_THEME-COMMUNE_2010-01$GEOFLA_1-1_COMMUNES_SHP_LAMB93_FXX_2010-01-01/file/GEOFLA_1-1_COMMUNES_SHP_LAMB93_FXX_2010-01-01.7z'
#URL MAJ
url='https://data.geopf.fr/telechargement/download/GEOFLA/GEOFLA_1-1_COMMUNES_SHP_LAMB93_FXX_2010-01-01/GEOFLA_1-1_COMMUNES_SHP_LAMB93_FXX_2010-01-01.7z'
file=requests.get(url)

os.chdir(directory+r'\inputs')
#Sauvegarde 
with open("commune.7z", "wb") as f:
    f.write(file.content)
#Open and extract zip
file=py7zr.SevenZipFile('commune.7z', mode='r')    
file.reset()
file.extractall('C:\\')
filenames = [y for y in sorted(file.getnames()) for ending in [ 'SHP'] if y.endswith(ending)] 
file='C:\\'+filenames[0]

#On ouvre la carte 
gdf=gpd.read_file(file)
gdf['CODGEO']=gdf['INSEE_COM']
gdf.loc[gdf['CODE_DEPT']=='75','CODGEO']='75056'
gdf.loc[gdf['CODGEO'].isin(map(str,list(range(69381,69390)))),'INSEE_COM']='69123'
gdf.loc[gdf['CODGEO'].isin(map(str,list(range(13201,13217)))),'INSEE_COM']='13055'


#download composition communales 2010
#Former URL
url='https://www.insee.fr/fr/statistiques/fichier/2028028/table-appartenance-geo-communes-12.zip'
#New URL
url='https://www.insee.fr/fr/statistiques/fichier/7671844/table-appartenance-geo-communes-12.zip'
au2010=requests.get(url)
#Save file
with open(au2010.url.split('/')[-1:][0], "wb") as f:
    f.write(au2010.content)
au2010zip=zipfile.ZipFile(BytesIO(au2010.content))
#Extract information
au2010df=pd.read_excel(BytesIO(au2010zip.read(au2010zip.namelist()[0])),sheet_name='Emboîtements communaux',skiprows=5)
au2010df.to_csv(directory+r'\inputs\au2010df.csv',index=False)

gdf2=gdf.merge(au2010df,on='CODGEO')

#AJUSTEMENT DES DONNEES POUR LES ARRONDISSEMENTS pour eviter le double compte de la population communale + arrondissements
for v in ['POP2010','POP1999']:
    
    gdf2.loc[gdf2['INSEE_COM'].isin( list(map(str,list(range(75102,75121))))),v]=0
    gdf2.loc[gdf2['INSEE_COM'].isin(list(map(str,list(range(69382,69390))))),v]=0
    gdf2.loc[gdf2['INSEE_COM'].isin(list(map(str,list(range(13202,13217))))),v]=0

#CREATION DE LA CARTE DES AIRES URBAINES
gdf2=gdf2[['AU2010','POP1999','POP2010','geometry']].dissolve(by='AU2010', aggfunc='sum').reset_index()

gdfau2010=gdf2.loc[~gdf2['AU2010'].isin(['999','000','997','998'])]


#############################
################################
####### SALAIRES ISSUS DE DADS ##########
#############################
################################

url='https://www.insee.fr/fr/statistiques/fichier/2021266/base-cc-dads-2012.zip'

dads=requests.get(url)
#Save Zip File
with open(dads.url.split('/')[-1:][0], "wb") as f:
    f.write(dads.content)
#Extract Data
dadszip=zipfile.ZipFile(BytesIO(dads.content))
dadsdf=pd.read_excel(BytesIO(dadszip.read(dadszip.namelist()[0])),sheet_name='AU2010',skiprows=5).rename(columns={'CODGEO': 'AU2010'})
dadsdf.to_csv(directory+r'\inputs\dadsdf.csv',index=False)

#merge With AU
gdfau2010=gdfau2010.merge(dadsdf,on='AU2010')
#Compute area
gdfau2010['area']=gdfau2010.geometry.area
#Compute Density
gdfau2010['density']=gdfau2010['POP2010']/gdfau2010['area']


#############################
################################
#######GRAPHIQUES  ##########
#############################
################################


#############################################
###########################################
############ENSEMBLE : DENSITEN############
#############################################
###########################################


#Fit OLS (polyno)
x=np.log(gdfau2010['density'])
y=np.log(gdfau2010['SNHM12'])
#First way to display regression line
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 

#Second way to export to a table
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()



#First Chart
plt.figure()
plt.scatter(np.log(gdfau2010['density']),np.log(gdfau2010['SNHM12']))
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Densite)')
plt.ylabel('log(salaire horaire)')
plt.grid(True)
plt.savefig(directory+r'\outputs\densitesalaire.eps')


#############################################
###########################################
############ENSEMBLE : POPULATION############
#############################################
###########################################

#Second Fit
x=np.log(gdfau2010['POP2010'])
y=np.log(gdfau2010['SNHM12'])
coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 
X = sm.add_constant(x)
model2 = sm.OLS(y, X).fit()


#Second Chart
plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('log(salaire horaire)')
plt.ylim(2, 3.5)
plt.grid(True)
plt.savefig(directory+r'\outputs\populationsalaire.eps')



#############################################
###########################################
############CADRES : POPULATION############
#############################################
###########################################

x=np.log(gdfau2010['POP2010'])
y=np.log(gdfau2010['SNHMC12'])
coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 
X = sm.add_constant(x)
model3 = sm.OLS(y, X).fit()

plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('log(salaire horaire)')
plt.ylim(2, 3.5)
plt.grid(True)
plt.savefig(directory+r'\outputs\populationsalairecadre.eps')



#############################################
###########################################
############PROF INTERMEDIAIRE : POPULATION############
#############################################
###########################################
x=np.log(gdfau2010['POP2010'])
y=np.log(gdfau2010['SNHMP12'])
coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 
X = sm.add_constant(x)
model4 = sm.OLS(y, X).fit()

plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('log(salaire horaire)')
plt.ylim(2, 3.5)
plt.grid(True)
plt.savefig(directory+r'\outputs\populationsalaireprofinter.eps')



#############################################
###########################################
############EMPLOYES : POPULATION############
#############################################
###########################################

x=np.log(gdfau2010['POP2010'])
y=np.log(gdfau2010['SNHME12'])
coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 
X = sm.add_constant(x)
model5 = sm.OLS(y, X).fit()

plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('log(salaire horaire)')
plt.ylim(2, 3.5)
plt.grid(True)
plt.savefig(directory+r'\outputs\populationsalaireprofemp.eps')



#############################################
###########################################
############OUVRIERS : POPULATION############
#############################################
###########################################

x=np.log(gdfau2010['POP2010'])
y=np.log(gdfau2010['SNHMO12'])
coef = np.polyfit(x,y,2)
poly1d_fn = np.poly1d(coef) 
X = sm.add_constant(x)
model6 = sm.OLS(y, X).fit()


plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('log(salaire horaire)')
plt.ylim(2, 3.5)
plt.grid(True)
plt.savefig(directory+r'\outputs\populationsalaireprofouv.eps')



# Generate table using Stargazer
stargazer = Stargazer([model2,model3,model4,model5,model6])
table_latex = stargazer.render_latex()  # Export as LaTeX
table_html = stargazer.render_html()  # Export as HTML
# Export to a .tex file
with open(directory+r'\outputs\OLS_results.tex', "w") as f:
    f.write(table_latex)


#############################################
###########################################
############DENSITE ############
#############################################
###########################################
#regression sur la Densité
models=[]
for v in ['SNHM12','SNHMC12','SNHMP12','SNHMO12','SNHMO12']:
    x=np.log(gdfau2010['density'])
    y=np.log(gdfau2010[v])
    X = sm.add_constant(x)
    models.append( sm.OLS(y, X).fit())
stargazer = Stargazer(models)
table_latex = stargazer.render_latex()  # Export as LaTeX
table_html = stargazer.render_html()  # Export as HTML
# Export to a .tex file
with open(directory+r'\outputs\OLS_results2.tex', "w") as f:
    f.write(table_latex)
    
    
    
#############################################
###########################################
############ILLUSTRATION SORTING ############
#############################################
###########################################    
    
#Download CSP composition of AU
url='https://www.insee.fr/fr/statistiques/fichier/4171334/base-cc-evol-struct-pop-2016-xls.zip'
csp=requests.get(url)

#Save ZIP
with open(csp.url.split('/')[-1:][0], "wb") as f:
    f.write(csp.content)
cspzip=zipfile.ZipFile(BytesIO(csp.content))

#Nettoyage 
cspdf=pd.read_excel(BytesIO(cspzip.read(cspzip.namelist()[0])),sheet_name='COM_2016',skiprows=5)
cspdf2=cspdf.merge(au2010df,on='CODGEO')
col=['C16_POP15P', 'C16_POP15P_CS1',	'C16_POP15P_CS2','C16_POP15P_CS3','C16_POP15P_CS4', 'C16_POP15P_CS5','C16_POP15P_CS6','C16_POP15P_CS7',	'C16_POP15P_CS8']
cspau=cspdf2.groupby('AU2010')[col].sum().reset_index()
cspau['share_csp+']=cspau['C16_POP15P_CS2']/cspau[['C16_POP15P_CS1',	'C16_POP15P_CS2','C16_POP15P_CS3','C16_POP15P_CS4', 'C16_POP15P_CS5','C16_POP15P_CS6']].sum(axis=1)
cspau['share_ouvrier']=cspau['C16_POP15P_CS6']/cspau[['C16_POP15P_CS1',	'C16_POP15P_CS2','C16_POP15P_CS3','C16_POP15P_CS4', 'C16_POP15P_CS5','C16_POP15P_CS6']].sum(axis=1)
cspau['share_employe']=cspau['C16_POP15P_CS5']/cspau[['C16_POP15P_CS1',	'C16_POP15P_CS2','C16_POP15P_CS3','C16_POP15P_CS4', 'C16_POP15P_CS5','C16_POP15P_CS6']].sum(axis=1)
gdfau2010=gdfau2010.merge(cspau[['AU2010','share_csp+','share_ouvrier','share_employe']],on='AU2010')


#Graphique Sorting
x=np.log(gdfau2010['POP2010'])
y=gdfau2010['share_ouvrier']
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 

plt.figure()
plt.scatter(x,y)
plt.plot( x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker

plt.xlabel('log(Population)')
plt.ylabel('part ouvrier')
plt.grid(True)
plt.savefig(directory+r'\outputs\populationcsp.eps')