#%%
import datetime
import json
import time

import pandas as pd
import requests


# %%
def get_response (**kwargs):
    url = "https://www.tabnews.com.br/api/v1/contents/"
    resp = requests.get(url, params=kwargs)
    return resp


def save_data (data, option= 'json'):
    now = datetime.datetime.now().strftime( "%Y%m%d_%H%M%S.%f")

    if option == 'json':
        with open (f'data/contents/json/{now}.json', 'w') as open_file:
            json.dump(data,open_file, indent=4)

    elif option == 'parquet':
        df = pd.DataFrame(data)
        df.to_parquet(f'data/contents/json/(now).parquet', index=False)



# %% 

page = 1
date_stop = pd.to_datetime('2025-03-05').date()
while  True:
    print(page)
    resp = get_response(page = page, per_page = 100, strategy = 'new')
    if resp.status_code==200:
        data = resp.json()
        save_data(data)

        date = pd.to_datetime(data[-1]['updated_at']).date()

        if len(data)< 100 or date < date_stop:
            print('menor que 100 ou data indisponivel')
            break

        print("Sucesso!")
        page += 1
        time.sleep(2)  
    else:
         time.sleep(30)   
# %%
