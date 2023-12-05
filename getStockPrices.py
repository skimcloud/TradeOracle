import requests
import os

# Function to fetch data for a ticker and save it to a CSV file
def fetch_ticker_data(symbol, api_key):
    # Replace 'YOUR_ALPHA_VANTAGE_API_KEY' with your actual API key
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&datatype=csv&apikey={api_key}"

    try:
        # Make API request
        response = requests.get(url)
        
        # Save data to CSV file
        filename = f'{symbol}_daily_prices.csv'
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Data for {symbol} saved to {filename}")
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")

# List of tickers
symbols = ['CAH', 'CVX', 'Z', 'FSLR', 'MCD', 'WEAT', 'ONON', 'MRVL', 'BOX', 'PLTR',
           'ENPH', 'DDOG', 'TSM', 'TOST', 'EWZ', 'CUBE', 'TGT', 'GPS', 'DIS', 'AXP',
           'ETSY', 'CRM', 'FIS', 'FCX', 'ADI', 'RUN']
api_key = 'GC3YN4T4N234HL43'
for symbol in symbols:
    fetch_ticker_data(symbol, api_key)

#Group1:CAH,CVX,Z,FSLR,MCD,WEAT,ONON,MRVL,BOX,PLTR,ENPH,DDOG,TSM,TOST,EWZ,CUBE,TGT,GPS,DIS,AXP,ETSY,CRM,FIS,FCX,ADI,RUN
#Group2:NET,GDXJ,EBAY,GM,TEAM,JD,MGM,GOLD,AMD,SPWR,DAL,ULTA,KBH,BA,FIVE,GLD,M,TWLO,GOOG,NOW,TWTR,GT,NUE,C,HLT,LULU
#Group3:LYFT,TPR,CVNA,WW,PANW,Cl,DASH,HIMS,TTWO,PAAS,ALLY,PHG,LAZR,FL,AI,CL,SU,MLCO,ZS,BLMN,AA,BMBL,SNOW,YEXT,MTCH
#Group4:WBD,ZTS,TCOM,EXPE,VFC,ELF,OKTA,MSFT,CROX,MT,AXTA,HOG,ORCL,CAT,SHOP,CPRI,UNH,META,CCL,PYPL,MDB,U,FTCH,CHWY,ROST
#Group5:SIX,AFRM,CF,SE,LEN,S,MAR,CSX,NVDA,PATH,AAPL,TTD,PINS,SBUX,TRIP,NTNX,KR,TQQQ,JWN,UBER,ABT,FDX,CCJ,AMZN
#Group6:OXY,ZEN,KO,EW,PAGS,SEAS,UPST,LYV,SNAP,PFE,BBAI,ZI,SEDG,QQQ,WIX,MRK,DT,NKE,GOOGL,DDD,QCOM,DELL