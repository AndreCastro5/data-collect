#%%
import requests
import datetime
import json
import pandas as pd
import time
# %%
class Collector:
    def __init__(self,url,instance_name):
        self.url = url 
        self.instance_name = instance_name

    def get_content(self,**kwargs):
        resp = requests.get(self.url, params=kwargs)
        return resp
    
    def save_parquet(self, data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        df = pd.DataFrame(data)
        df.to_parquet(f"data/{self.instance_name}/parquet/{now}.parquet", index=False)
    
    def save_json(self,data):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
        with open(f"data/{self.instance_name}/json/{now}.json",'w') as open_file:
            json.dump(data,open_file)

    def save_data(self, data, format ='json'):
        if format == 'json':
            self.save_json(data)

        elif format == 'parquet':
            self.save_parquet(data)

    def get_and_save(self, save_format='json', **kwargs):
        resp = self.get_content(**kwargs)
        if resp.status_code == 200:
            try:
                data = resp.json()
            except json.JSONDecodeError:
                print('Erro ao decodificar Json. Resposta da API', resp.text)
                return None
                
            self.save_data(data, save_format)
            return data
        else:
                 print(f"Request sem sucesso: {resp.status_code}")
                 print("Resposta da API:", resp.text)
                 return None

    def auto_exec(self,save_format ='json', date_stop='2000-01-01'):
        page = 1
        while True:
            print(page)
            data = self.get_and_save(save_format=save_format,
                                     page = page,
                                     per_page = 100)
            if data == None:
                print('Erro ao coletar dados ... aguardando.')
                time.sleep(60*5)

            else:
                data_last = pd.to_datetime(data[-1]['published_at']).date()
                if data_last<pd.to_datetime(date_stop).date():
                    break
                elif len(data)<100:
                    break
                page += 1
                time.sleep(5)


#%%

url = "https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/" 
collect = Collector(url,'episodios')
collect.auto_exec()


# %%
