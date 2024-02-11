import pandas as pd
from sqlalchemy import create_engine, text

df = pd.read_csv('~/Downloads/insurance.csv')

engine = create_engine(
    "")

with engine.connect() as con:
    for i in range(df.shape[0]):
        # try:
        sql = f"INSERT INTO hospital_insurance_prices (hospital_id, cpt_code, provider_id, cost) VALUES ({df.loc[i]['hospital_id']}, '{df.loc[i]['cpt_code']}', {df.loc[i]['provider_id']}, {df.loc[i]['cost']});"
        print(sql)
        res = con.execute(text(sql))
        break
        # except Exception as e:
        #     print("Could not insert" + str(e))