import gspread
import pandas as pd
import os
import requests
from google.oauth2 import service_account
# from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
secret_file = os.path.join(os.getcwd(), 'client_secret.json')

credentials = service_account.Credentials.from_service_account_file(
    secret_file, scopes=scope)

gc = gspread.authorize(credentials)

sht1 = gc.open_by_key('1Jgsf-5wtsCdyDiIp-P_EZbnoT6Ya_0URC3I8s1-5GeM')

df = pd.DataFrame(sht1.worksheet("Fontes").get_all_values()[1:])
df.columns = df.iloc[0]
df.drop(df.index[0], inplace=True)

header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
          "AppleWebKit/537.36 (KHTML, like Gecko)"
          "Chrome/54.0.2840.71 Safari/537.36",
          "upgrade-insecure-requests": "1",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
          "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
          "accept-encoding": "gzip, deflate, br",
          "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
          "cache-control": "max-age=0"}

res = requests.get(df['Competitor Link'].iloc[0], headers=header)

soup = BeautifulSoup(res.text, "html.parser")

price = soup.find("div", {"class": "preco_normal"}).text.replace("R$", "")
print(price)
sht1.worksheet("Fontes").update_acell('C3', price)
