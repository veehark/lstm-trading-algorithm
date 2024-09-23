import yfinance as yf
import pandas as pd


omxh = [ #Nasdaq Helsinki
    "NOKIA.HE", #Nokia Oyj
    "KNEBV.HE", #KONE Oyj
    "STERV.HE", #Stora Enso Oyj
    "FORTUM.HE", #Fortum Oyj
    "TIETO.HE", #TietoEVRY Oyj
    "TYRES.HE", #Nokian Renkaat Oyj
    "METSB.HE", #Metsä Board Oyj
    "KESKOB.HE", #Kesko Oyj
    "HUH1V.HE", #Huhtamäki Oyj
    "ELISA.HE", #Elisa Oyj
    "TELIA1.HE", #Telia Company AB (publ)
    "ORNBV.HE", #Orion Oyj
    "NESTE.HE", #Neste Oyj  
    "UPM.HE", #UPM-Kymmene Oyj
    "NDA-FI.HE", #Nordea Bank Abp
    "WRT1V.HE", #Wärtsilä Oyj Abp
    "METSO.HE", #Metso Oyj
    "SAMPO.HE", #Sampo Oyj
    "KCR.HE", #Konecranes Plc
    "OUT1V.HE", #Outokumpu Oyj
    "CGCBV.HE" #Cargotec Corporation
    ]

nse = [ #National Stock Exchange of India
    "TATASTEEL.NS",
    "TATACONSUM.NS",
    "RELIANCE.NS",
    "HDFCLIFE.NS",
    "LT.NS",
    "TCS.NS",
    "KOTAKBANK.NS",
    "HINDALCO.NS",
    "LTIM.NS",
    "MARUTI.NS",
    "ULTRACEMCO.NS",
    "BAJFINANCE.NS",
    "WIPRO.NS",
    "BRITANNIA.NS",
    "BAJAJ-AUTO.NS",
    "SHRIRAMFIN.NS",
    "BAJAJFINSV.NS",
    "ITC.NS",
    "HEROMOTOCO.NS",
    "CIPLA.NS",
    "NTPC.NS",
    "ADANIENT.NS",
    "ONGC.NS",
    "COALINDIA.NS",
    "NESTLEIND.NS",
    "TITAN.NS",
    "APOLLOHOSP.NS",
    "BHARTIARTL.NS"
    ]

nyse = [ #New York Stock Exchange
    'SCX', #Starrett Company
    'ACCO', #ACCO Brands Corporation
    'WMB', #The Williams Companies, Inc.
    'CMSD', #CMSD	
    'BCO', #The Brink's Company
    'BCE', #BCE Inc.	
    'CMSC', #CMSC	
    'ATEN', #A10 Networks, Inc.	
    'WLK', #Westlake Corporation	
    'WLY', #John Wiley & Sons, Inc.	
    'BCC', #Boise Cascade Company	
    'BBY', #Best Buy Co., Inc.
    'SCS', #Steelcase Inc.
    'GMED', #Globus Medical, Inc.	
    'SEE', #Sealed Air Corporation	
    'BBW', #Build-A-Bear Workshop, Inc.
    'BBU', #Brookfield Business Partners L.P.	
    'BCH', #Banco de Chile	
    'BSAC', #Banco Santander-Chile	
    'CMRE', #Costamare Inc.	
    'SPHR', #Sphere Entertainment Co.	
    ]

lists = [
    [omxh,'omxh'],
    [nse,'nse'],
    [nyse,'nyse']
    ]

def get_data(symbols,exchange):
    print(f'Getting data from {exchange}')
    for symbol in symbols:
        data = yf.download(symbol, start="2010-01-01", end="2024-01-01")
        name = symbol.split(".")[0]
        data.to_csv(f"data/{exchange}/{name}.csv", sep = ";")
    print('done')

print('Start')
for list in lists:
    get_data(list[0],list[1])
print('Done')