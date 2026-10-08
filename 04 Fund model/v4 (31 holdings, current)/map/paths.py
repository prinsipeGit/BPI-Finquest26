import json, sys
sys.path.insert(0,'.')
from universe3 import L
SUF = {'.MC':'bme','.MI':'bit','.PA':'epa','.DE':'etr','.L':'lon','.NS':'nse','.CO':'cph','.TO':'tsx','.HK':'hkg','.T':'tyo','.KS':'krx',
       '.KL':'klse','.SR':'tadawul','.BK':'bkk','.SW':'swx','.AX':'asx','.SI':'sgx','.AS':'ams','.JK':'idx','.TW':'tpe','.SA':'bvmf','.JO':'jse','.AD':'adx'}
KLSE = {'5347.KL':'TENAGA','5246.KL':'WPRTS','5225.KL':'IHH'}
HC = [('HCA','US','HCA Healthcare','HCA'),('IHH','MY','IHH Healthcare','5225.KL'),('APOLLO','IN','Apollo Hospitals','APOLLOHOSP.NS'),
 ('MAXH','IN','Max Healthcare','MAXHEALTH.NS'),('UHS','US','Universal Health Services','UHS'),('THC','US','Tenet Healthcare','THC'),
 ('SULAIMAN','SA','Dr. Sulaiman Al Habib Medical','4013.SR'),('EHC','US','Encompass Health','EHC'),('ENSG','US','Ensign Group','ENSG'),
 ('BDMS','TH','Bangkok Dusit Medical Services','BDMS.BK'),('RDOR','BR',"Rede D'Or Sao Luiz",'RDOR3.SA'),('FORTISH','IN','Fortis Healthcare','FORTIS.NS'),
 ('BH','TH','Bumrungrad Hospital','BH.BK'),('RHC','AU','Ramsay Health Care','RHC.AX'),('MEDANTA','IN','Global Health (Medanta)','MEDANTA.NS'),
 ('NH','IN','Narayana Hrudayalaya','NH.NS'),('MOUWASAT','SA','Mouwasat Medical Services','4002.SR'),('ACHC','US','Acadia Healthcare','ACHC'),
 ('SEM','US','Select Medical','SEM'),('SILO','ID','Siloam International Hospitals','SILO.JK'),('MIKA','ID','Mitra Keluarga','MIKA.JK'),
 ('ASTERDM','IN','Aster DM Healthcare','ASTERDM.NS'),('KIMS','IN','Krishna Institute of Medical Sciences','KIMS.NS'),('RAINBOW','IN',"Rainbow Children's Medicare",'RAINBOW.NS'),
 ('BSL','SG','Raffles Medical Group','BSL.SI'),('SGRY','US','Surgery Partners','SGRY'),('NMC4005','SA','National Medical Care','4005.SR'),
 ('DALLAH','SA','Dallah Healthcare','4004.SR'),('MEH','SA','Middle East Healthcare','4009.SR'),('NTC','ZA','Netcare','NTC.JO'),('LHC','ZA','Life Healthcare','LHC.JO')]
def path(key, yh):
    if yh is None: return f'quote/pse/{key}'
    if yh in KLSE: return f'quote/klse/{KLSE[yh]}'
    for s, ex in SUF.items():
        if yh.endswith(s):
            t = yh[:-len(s)]
            if s == '.HK': t = t.zfill(4)
            return f'quote/{ex}/{t}'
    return f'stocks/{yh.lower()}'
P = {k: path(k, yh) for k, *_ , yh in L}
P['FORTIS'] = 'stocks/fts'
for k, c, n, yh in HC: P[k] = path(k, yh)
json.dump(P, open('paths.json','w'))
json.dump(HC, open('hc.json','w'))
print(len(P)); print(json.dumps(P)[:3000])
