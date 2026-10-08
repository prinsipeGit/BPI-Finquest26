"""Global capacity universe (Map v3): no regions. Each name: capacity type, country, GICS sub-industry (team-assigned),
display name, Yahoo symbol. Conglomerates carry a segment share (qualifying revenue / total)."""
FX = dict(USD=1.0, HKD=7.8482, JPY=158.114, KRW=1339.1, EUR=0.8932, GBP=0.7567, CHF=0.832, AUD=1.436, SGD=1.2796,
          INR=96.765, MYR=4.087, THB=33.7, TWD=31.851, PHP=62.763, DKK=6.6806, CAD=1.4255, IDR=17878, SAR=3.7541, AED=3.673)
TYPES = {1: 'Power generation & grids', 2: 'Water', 3: 'Digital networks', 4: 'Ports', 5: 'Airports & toll roads',
         6: 'Grid & power equipment', 7: 'Semiconductors'}
ROLE = {1: 'Owner', 2: 'Owner', 3: 'Owner', 4: 'Owner', 5: 'Owner', 6: 'Supplier', 7: 'Supplier'}
QUALIFYING = {'Electric Utilities', 'Multi-Utilities', 'Water Utilities', 'Independent Power Producers', 'Renewable Electricity',
              'Integrated Telecommunication Services', 'Wireless Telecommunication Services', 'Alternative Carriers',
              'Telecom Tower REITs', 'Data Center REITs', 'Marine Ports & Services', 'Airport Services', 'Highways & Railtracks',
              'Heavy Electrical Equipment', 'Electrical Components & Equipment', 'Semiconductors', 'Semiconductor Materials & Equipment'}
SEGMENT = {  # conglomerates: qualifying segment revenue share, latest fiscal year (annual reports)
 'HITACHI': (0.304, 'Energy ¥3,220bn of ¥10,587bn, FY2025', 'https://www2.infomart.co.jp/web/jp/images/upload/3677/140120260427511921_22801870.pdf'),
 'SIE': (0.291, 'Smart Infrastructure €23.0bn of €78.9bn, FY2025', 'https://assets.new.siemens.com/siemens/assets/api/uuid:3948cdd4-35e0-4c1d-8412-9aed4097b3d0/HQCOPR202511117277EN.pdf'),
 'MELCO': (0.248, 'Infrastructure ¥1,463bn of ¥5,895bn, FY2025', 'https://www.mitsubishielectric.com/en/pr/2026/pdf/0428_co1.pdf'),
 'SAMSUNG': (0.390, 'Device Solutions KRW 130tn of KRW 334tn, 2025', 'https://news.samsungsemiconductor.com/global/samsung-electronics-announces-fourth-quarter-and-fy-2025-results/'),
 'DG': (0.164, 'Concessions €12.2bn of €74.6bn, 2025', 'https://www.vinci.com/sites/default/files/medias/communiques/file/2026-02/press-release-vinci-full-year-2025.pdf'),
 'FER': (0.154, 'Highways and airports €1.5bn of €9.6bn, 2025', 'https://static-iai.ferrovial.com/wp-content/uploads/sites/14/2026/02/25214727/ferrovial-integrated-annual-report-2025-business-performance.pdf'),
}
EU, MU_, WU, IPP, RE = 'Electric Utilities', 'Multi-Utilities', 'Water Utilities', 'Independent Power Producers', 'Renewable Electricity'
IT_, WT, AC, TR, DC = 'Integrated Telecommunication Services', 'Wireless Telecommunication Services', 'Alternative Carriers', 'Telecom Tower REITs', 'Data Center REITs'
MP, AS, HR, HE, EC = 'Marine Ports & Services', 'Airport Services', 'Highways & Railtracks', 'Heavy Electrical Equipment', 'Electrical Components & Equipment'
SC, SE, IC, CE, TH = 'Semiconductors', 'Semiconductor Materials & Equipment', 'Industrial Conglomerates', 'Construction & Engineering', 'Technology Hardware'
L = [
 # power
 ('NEE',1,'US',EU,'NextEra Energy','NEE'),('IBE',1,'ES',EU,'Iberdrola','IBE.MC'),('CEG',1,'US',EU,'Constellation Energy','CEG'),
 ('SO',1,'US',EU,'Southern Company','SO'),('ENEL',1,'IT',EU,'Enel','ENEL.MI'),('DUK',1,'US',EU,'Duke Energy','DUK'),
 ('NG',1,'GB',MU_,'National Grid','NG.L'),('AEP',1,'US',EU,'American Electric Power','AEP'),('ENGI',1,'FR',MU_,'Engie','ENGI.PA'),
 ('VST',1,'US',IPP,'Vistra','VST'),('D',1,'US',MU_,'Dominion Energy','D'),('SRE',1,'US',MU_,'Sempra','SRE'),('EOAN',1,'DE',MU_,'E.ON','EOAN.DE'),
 ('ETR',1,'US',EU,'Entergy','ETR'),('ELE',1,'ES',EU,'Endesa','ELE.MC'),('RWE',1,'DE',IPP,'RWE','RWE.DE'),('XEL',1,'US',EU,'Xcel Energy','XEL'),
 ('EXC',1,'US',EU,'Exelon','EXC'),('SSE',1,'GB',EU,'SSE','SSE.L'),('ADANIPOWER',1,'IN',IPP,'Adani Power','ADANIPOWER.NS'),('ED',1,'US',MU_,'Consolidated Edison','ED'),
 ('PEG',1,'US',MU_,'Public Service Enterprise Group','PEG'),('WEC',1,'US',MU_,'WEC Energy','WEC'),('NTPC',1,'IN',IPP,'NTPC','NTPC.NS'),
 ('ORSTED',1,'DK',RE,'Orsted','ORSTED.CO'),('PCG',1,'US',EU,'PG&E','PCG'),('FORTIS',1,'CA',EU,'Fortis','FTS'),('PGRID',1,'IN',EU,'Power Grid Corp of India','POWERGRID.NS'),
 ('CLP',1,'HK',EU,'CLP Holdings','0002.HK'),('ADANIGREEN',1,'IN',RE,'Adani Green Energy','ADANIGREEN.NS'),('HYDRO1',1,'CA',EU,'Hydro One','H.TO'),
 ('NRG',1,'US',IPP,'NRG Energy','NRG'),('KANSAI',1,'JP',EU,'Kansai Electric Power','9503.T'),('TENAGA',1,'MY',EU,'Tenaga Nasional','5347.KL'),
 ('SEC',1,'SA',EU,'Saudi Electricity','5110.SR'),('KEPCO',1,'KR',EU,'Korea Electric Power','015760.KS'),('CRPOWER',1,'HK',IPP,'China Resources Power','0836.HK'),
 ('CHUBU',1,'JP',EU,'Chubu Electric Power','9502.T'),('TATAPOWER',1,'IN',EU,'Tata Power','TATAPOWER.NS'),('MER',1,'PH',EU,'Meralco',None),
 ('AP',1,'PH',IPP,'Aboitiz Power',None),('TEPCO',1,'JP',EU,'Tokyo Electric Power','9501.T'),
 # water
 ('AWK',2,'US',WU,'American Water Works','AWK'),('VIE',2,'FR',MU_,'Veolia','VIE.PA'),('SBS',2,'BR',WU,'Sabesp','SBS'),('UU',2,'GB',WU,'United Utilities','UU.L'),
 ('SVT',2,'GB',WU,'Severn Trent','SVT.L'),('WTRG',2,'US',WU,'Essential Utilities','WTRG'),('GDI',2,'HK',WU,'Guangdong Investment','0270.HK'),
 ('AWR',2,'US',WU,'American States Water','AWR'),('CWT',2,'US',WU,'California Water Service','CWT'),('BEW',2,'HK',WU,'Beijing Enterprises Water','0371.HK'),
 ('PNN',2,'GB',WU,'Pennon','PNN.L'),('MWC',2,'PH',WU,'Manila Water',None),
 # digital networks
 ('CHMOB',3,'HK',WT,'China Mobile','0941.HK'),('VZ',3,'US',IT_,'Verizon','VZ'),('TMUS',3,'US',WT,'T-Mobile US','TMUS'),('T',3,'US',IT_,'AT&T','T'),
 ('DTE',3,'DE',IT_,'Deutsche Telekom','DTE.DE'),('AIRTEL',3,'IN',WT,'Bharti Airtel','BHARTIARTL.NS'),('EQIX',3,'US',DC,'Equinix','EQIX'),
 ('NTT',3,'JP',IT_,'NTT','9432.T'),('CHTEL',3,'HK',IT_,'China Telecom','0728.HK'),('AMT',3,'US',TR,'American Tower','AMT'),
 ('SBCORP',3,'JP',WT,'SoftBank Corp','9434.T'),('KDDI',3,'JP',WT,'KDDI','9433.T'),('DLR',3,'US',DC,'Digital Realty','DLR'),('AMX',3,'MX',WT,'America Movil','AMX'),
 ('STC',3,'SA',IT_,'Saudi Telecom','7010.SR'),('SINGTEL',3,'SG',IT_,'Singtel','Z74.SI'),('EAND',3,'AE',IT_,'e& (Emirates Telecom)','EAND.AD'),
 ('ORA',3,'FR',IT_,'Orange','ORA.PA'),('SCMN',3,'CH',IT_,'Swisscom','SCMN.SW'),('VOD',3,'GB',WT,'Vodafone','VOD.L'),('TLS',3,'AU',IT_,'Telstra','TLS.AX'),
 ('CHT',3,'TW',IT_,'Chunghwa Telecom','2412.TW'),('ADVANC',3,'TH',WT,'Advanced Info Service','ADVANC.BK'),('CCI',3,'US',TR,'Crown Castle','CCI'),
 ('CHUNI',3,'HK',IT_,'China Unicom','0762.HK'),('CHTOWER',3,'HK',AC,'China Tower','0788.HK'),('TEF',3,'ES',IT_,'Telefonica','TEF.MC'),
 ('BCE',3,'CA',IT_,'BCE','BCE'),('SBAC',3,'US',TR,'SBA Communications','SBAC'),('CLNX',3,'ES',AC,'Cellnex','CLNX.MC'),('KPN',3,'NL',IT_,'KPN','KPN.AS'),
 ('TLKM',3,'ID',IT_,'Telkom Indonesia','TLKM.JK'),('TU',3,'CA',IT_,'Telus','TU'),('INDUS',3,'IN',AC,'Indus Towers','INDUSTOWER.NS'),
 ('TEL',3,'PH',WT,'PLDT',None),('GLO',3,'PH',WT,'Globe Telecom',None),('CNVRG',3,'PH',AC,'Converge ICT',None),
 # ports
 ('ADPORTS',4,'IN',MP,'Adani Ports & SEZ','ADANIPORTS.NS'),('ICT',4,'PH',MP,'ICTSI',None),('CMPORT',4,'HK',MP,'China Merchants Port','0144.HK'),
 ('JSWINFRA',4,'IN',MP,'JSW Infrastructure','JSWINFRA.NS'),('QUB',4,'AU',MP,'Qube Holdings','QUB.AX'),('WPRTS',4,'MY',MP,'Westports','5246.KL'),
 ('COSCOP',4,'HK',MP,'COSCO Shipping Ports','1199.HK'),('KAMIGUMI',4,'JP',MP,'Kamigumi','9364.T'),('HHFA',4,'DE',MP,'Hamburger Hafen (HHLA)','HHFA.DE'),
 # airports & toll roads
 ('DG',5,'FR',CE,'Vinci','DG.PA'),('AENA',5,'ES',AS,'Aena','AENA.MC'),('FER',5,'ES',CE,'Ferrovial','FER.MC'),('TCL',5,'AU',HR,'Transurban','TCL.AX'),
 ('AOT',5,'TH',AS,'Airports of Thailand','AOT.BK'),('PAC',5,'MX',AS,'Grupo Aeroportuario del Pacifico','PAC'),('ADP',5,'FR',AS,'Aeroports de Paris','ADP.PA'),
 ('GMR',5,'IN',AS,'GMR Airports','GMRAIRPORT.NS'),('GET',5,'FR',HR,'Getlink','GET.PA'),('JSEXP',5,'HK',HR,'Jiangsu Expressway','0177.HK'),
 ('ASR',5,'MX',AS,'Grupo Aeroportuario del Sureste','ASR'),('FHZN',5,'CH',AS,'Flughafen Zurich','FHZN.SW'),('FRA',5,'DE',AS,'Fraport','FRA.DE'),
 ('ZJEXP',5,'HK',HR,'Zhejiang Expressway','0576.HK'),('OMAB',5,'MX',AS,'OMA (Centro Norte airports)','OMAB'),('ALX',5,'AU',HR,'Atlas Arteria','ALX.AX'),
 ('JAT',5,'JP',AS,'Japan Airport Terminal','9706.T'),('SZEXP',5,'HK',HR,'Shenzhen Expressway','0548.HK'),('IRB',5,'IN',HR,'IRB Infrastructure','IRB.NS'),
 ('BCIA',5,'HK',AS,'Beijing Capital Intl Airport','0694.HK'),
 # grid & power equipment
 ('GEV',6,'US',HE,'GE Vernova','GEV'),('SIE',6,'DE',IC,'Siemens','SIE.DE'),('ABB',6,'CH',EC,'ABB','ABBN.SW'),('ETN',6,'US',EC,'Eaton','ETN'),
 ('HITACHI',6,'JP',IC,'Hitachi','6501.T'),('SU',6,'FR',EC,'Schneider Electric','SU.PA'),('ENR',6,'DE',HE,'Siemens Energy','ENR.DE'),('PWR',6,'US',CE,'Quanta Services','PWR'),
 ('VRT',6,'US',EC,'Vertiv','VRT'),('MELCO',6,'JP',IC,'Mitsubishi Electric','6503.T'),('LR',6,'FR',EC,'Legrand','LR.PA'),('PRY',6,'IT',EC,'Prysmian','PRY.MI'),
 ('HUBB',6,'US',EC,'Hubbell','HUBB'),('LSELEC',6,'KR',EC,'LS Electric','010120.KS'),('HYOSUNG',6,'KR',HE,'Hyosung Heavy Industries','298040.KS'),
 ('HDHE',6,'KR',HE,'HD Hyundai Electric','267260.KS'),('ABBIND',6,'IN',HE,'ABB India','ABB.NS'),('CGPOWER',6,'IN',HE,'CG Power','CGPOWER.NS'),
 ('FUJIELEC',6,'JP',HE,'Fuji Electric','6504.T'),('NEX',6,'FR',EC,'Nexans','NEX.PA'),
 # semiconductors
 ('NVDA',7,'US',SC,'NVIDIA','NVDA'),('TSMC',7,'TW',SC,'TSMC','2330.TW'),('AVGO',7,'US',SC,'Broadcom','AVGO'),('SAMSUNG',7,'KR',TH,'Samsung Electronics','005930.KS'),
 ('MU',7,'US',SC,'Micron','MU'),('SKHYNIX',7,'KR',SC,'SK hynix','000660.KS'),('AMD',7,'US',SC,'AMD','AMD'),('ASML',7,'NL',SE,'ASML','ASML.AS'),
 ('INTC',7,'US',SC,'Intel','INTC'),('AMAT',7,'US',SE,'Applied Materials','AMAT'),('LRCX',7,'US',SE,'Lam Research','LRCX'),('ARM',7,'GB',SC,'Arm Holdings','ARM'),
 ('TXN',7,'US',SC,'Texas Instruments','TXN'),('KLAC',7,'US',SE,'KLA','KLAC'),('MEDIATEK',7,'TW',SC,'MediaTek','2454.TW'),('ADI',7,'US',SC,'Analog Devices','ADI'),
 ('QCOM',7,'US',SC,'Qualcomm','QCOM'),('ADVANTEST',7,'JP',SE,'Advantest','6857.T'),('TEL8035',7,'JP',SE,'Tokyo Electron','8035.T'),('IFX',7,'DE',SC,'Infineon','IFX.DE'),
 ('NXPI',7,'NL',SC,'NXP Semiconductors','NXPI'),('STM',7,'FR',SC,'STMicroelectronics','STMPA.PA'),('MCHP',7,'US',SC,'Microchip Technology','MCHP'),
 ('RENESAS',7,'JP',SC,'Renesas Electronics','6723.T'),('ON',7,'US',SC,'onsemi','ON'),
]
