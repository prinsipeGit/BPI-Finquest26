# Map v2 long-list: capacity type, region, country, GICS sector, display name, Yahoo symbol
FX = dict(USD=1.0,HKD=7.8482,JPY=158.114,KRW=1339.1,EUR=0.8932,GBP=0.7567,CHF=0.832,AUD=1.436,SGD=1.2796,
          INR=96.765,MYR=4.087,THB=33.7,TWD=31.851,PHP=62.763)  # units per USD, Yahoo, 7 Oct 2026
TYPES = {1:'Power generation & grid',2:'Water',3:'Telecom & digital infrastructure',4:'Ports',
         5:'Airports & toll roads',6:'Power & grid equipment',7:'Semiconductors'}
ROLE = {1:'Owner',2:'Owner',3:'Owner',4:'Owner',5:'Owner',6:'Supplier',7:'Supplier'}
U = 'Utilities'; C='Communication Services'; I='Industrials'; T='Information Technology'; R='Real Estate'
L = [
# key, type, country, gics, name, yahoo
('ADANIPOWER',1,'IN',U,'Adani Power','ADANIPOWER.NS'),('ADANIGREEN',1,'IN',U,'Adani Green Energy','ADANIGREEN.NS'),
('TATAPOWER',1,'IN',U,'Tata Power','TATAPOWER.NS'),('NTPC',1,'IN',U,'NTPC','NTPC.NS'),('CLP',1,'HK',U,'CLP Holdings','0002.HK'),
('PGRID',1,'IN',U,'Power Grid Corp of India','POWERGRID.NS'),('KANSAI',1,'JP',U,'Kansai Electric Power','9503.T'),
('MER',1,'PH',U,'Meralco',None),('TENAGA',1,'MY',U,'Tenaga Nasional','5347.KL'),('TEPCO',1,'JP',U,'Tokyo Electric Power','9501.T'),
('CRPOWER',1,'HK',U,'China Resources Power','0836.HK'),('CHUBU',1,'JP',U,'Chubu Electric Power','9502.T'),('AP',1,'PH',U,'Aboitiz Power',None),
('ENEL',1,'IT',U,'Enel','ENEL.MI'),('ENGI',1,'FR',U,'Engie','ENGI.PA'),('NG',1,'GB',U,'National Grid','NG.L'),('EOAN',1,'DE',U,'E.ON','EOAN.DE'),
('IBE',1,'ES',U,'Iberdrola','IBE.MC'),('RWE',1,'DE',U,'RWE','RWE.DE'),('NEE',1,'US',U,'NextEra Energy','NEE'),('VST',1,'US',U,'Vistra','VST'),
('CEG',1,'US',U,'Constellation Energy','CEG'),('DUK',1,'US',U,'Duke Energy','DUK'),('SO',1,'US',U,'Southern Company','SO'),
('BEW',2,'HK',U,'Beijing Enterprises Water','0371.HK'),('MWC',2,'PH',U,'Manila Water',None),('GDI',2,'HK',U,'Guangdong Investment','0270.HK'),
('SVT',2,'GB',U,'Severn Trent','SVT.L'),('UU',2,'GB',U,'United Utilities','UU.L'),('VIE',2,'FR',U,'Veolia','VIE.PA'),
('WTRG',2,'US',U,'Essential Utilities','WTRG'),('AWK',2,'US',U,'American Water Works','AWK'),('SBS',2,'BR',U,'Sabesp','SBS'),
('AIRTEL',3,'IN',C,'Bharti Airtel','BHARTIARTL.NS'),('CHMOB',3,'HK',C,'China Mobile','0941.HK'),('SINGTEL',3,'SG',C,'Singtel','Z74.SI'),
('NTT',3,'JP',C,'NTT','9432.T'),('TEL',3,'PH',C,'PLDT',None),('SBCORP',3,'JP',C,'SoftBank Corp','9434.T'),('GLO',3,'PH',C,'Globe Telecom',None),
('TLS',3,'AU',C,'Telstra','TLS.AX'),('KDDI',3,'JP',C,'KDDI','9433.T'),('VOD',3,'GB',C,'Vodafone','VOD.L'),('INDUS',3,'IN',C,'Indus Towers','INDUSTOWER.NS'),
('CNVRG',3,'PH',C,'Converge ICT',None),('DTE',3,'DE',C,'Deutsche Telekom','DTE.DE'),('ORA',3,'FR',C,'Orange','ORA.PA'),
('CLNX',3,'ES',C,'Cellnex','CLNX.MC'),('TEF',3,'ES',C,'Telefonica','TEF.MC'),('VZ',3,'US',C,'Verizon','VZ'),('TMUS',3,'US',C,'T-Mobile US','TMUS'),
('SCMN',3,'CH',C,'Swisscom','SCMN.SW'),('AMT',3,'US',R,'American Tower','AMT'),('T',3,'US',C,'AT&T','T'),('EQIX',3,'US',R,'Equinix','EQIX'),
('AMX',3,'MX',C,'America Movil','AMX'),
('COSCOP',4,'HK',I,'COSCO Shipping Ports','1199.HK'),('ICT',4,'PH',I,'ICTSI',None),('CMPORT',4,'HK',I,'China Merchants Port','0144.HK'),
('ADPORTS',4,'IN',I,'Adani Ports & SEZ','ADANIPORTS.NS'),('HHFA',4,'DE',I,'Hamburger Hafen (HHLA)','HHFA.DE'),('WPRTS',4,'MY',I,'Westports','5246.KL'),
('QUB',4,'AU',I,'Qube Holdings','QUB.AX'),
('AOT',5,'TH',I,'Airports of Thailand','AOT.BK'),('TCL',5,'AU',I,'Transurban','TCL.AX'),('JAT',5,'JP',I,'Japan Airport Terminal','9706.T'),
('PAC',5,'MX',I,'Grupo Aeroportuario del Pacifico','PAC'),('ADP',5,'FR',I,'Aeroports de Paris','ADP.PA'),('FER',5,'ES',I,'Ferrovial','FER.MC'),
('DG',5,'FR',I,'Vinci','DG.PA'),('AENA',5,'ES',I,'Aena','AENA.MC'),('ASR',5,'MX',I,'Grupo Aeroportuario del Sureste','ASR'),
('OMAB',5,'MX',I,'OMA (Centro Norte airports)','OMAB'),
('JSEXP',5,'HK',I,'Jiangsu Expressway','0177.HK'),('ZJEXP',5,'HK',I,'Zhejiang Expressway','0576.HK'),
('ALX',5,'AU',I,'Atlas Arteria','ALX.AX'),('BCIA',5,'HK',I,'Beijing Capital Intl Airport','0694.HK'),
('GMR',5,'IN',I,'GMR Airports','GMRAIRPORT.NS'),('IRB',5,'IN',I,'IRB Infrastructure','IRB.NS'),
('MELCO',6,'JP',I,'Mitsubishi Electric','6503.T'),('HDHE',6,'KR',I,'HD Hyundai Electric','267260.KS'),('LSELEC',6,'KR',I,'LS Electric','010120.KS'),
('HITACHI',6,'JP',I,'Hitachi','6501.T'),('SIE',6,'DE',I,'Siemens','SIE.DE'),('ABBIND',6,'IN',I,'ABB India','ABB.NS'),('SU',6,'FR',I,'Schneider Electric','SU.PA'),
('ABB',6,'CH',I,'ABB','ABBN.SW'),('LR',6,'FR',I,'Legrand','LR.PA'),('ENR',6,'DE',I,'Siemens Energy','ENR.DE'),('VRT',6,'US',I,'Vertiv','VRT'),
('GEV',6,'US',I,'GE Vernova','GEV'),('PRY',6,'IT',I,'Prysmian','PRY.MI'),('ETN',6,'US',I,'Eaton','ETN'),('PWR',6,'US',I,'Quanta Services','PWR'),
('TSMC',7,'TW',T,'TSMC','2330.TW'),('ASML',7,'NL',T,'ASML','ASML.AS'),('SKHYNIX',7,'KR',T,'SK hynix','000660.KS'),('TEL8035',7,'JP',T,'Tokyo Electron','8035.T'),
('SAMSUNG',7,'KR',T,'Samsung Electronics','005930.KS'),('STM',7,'FR',T,'STMicroelectronics','STMPA.PA'),('IFX',7,'DE',T,'Infineon','IFX.DE'),
('NVDA',7,'US',T,'NVIDIA','NVDA'),('AMD',7,'US',T,'AMD','AMD'),('AVGO',7,'US',T,'Broadcom','AVGO'),('MU',7,'US',T,'Micron','MU'),
]
APAC = {'IN','HK','JP','PH','MY','SG','AU','KR','TW','TH','NZ'}
EUROPE = {'IT','FR','GB','DE','ES','CH','NL'}
AMERICAS = {'US','MX','BR'}
def region(c): return 'Asia-Pacific' if c in APAC else 'Europe' if c in EUROPE else 'Americas'
