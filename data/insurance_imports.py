import pandas as pd
from sqlalchemy import create_engine, text

df = pd.read_csv('~/Downloads/insurance.csv')

engine = create_engine(
    "postgresql://kodqrbmcuqhgdi:b4c7907bedf57277731a6a867809b5d888cab348b9bd151ce2e0e6a227325079@ec2-44-213-151-75.compute-1.amazonaws.com:5432/dbgitidqah3a5l")

with engine.connect() as con:
    for i in range(df.shape[0]):
        # try:
        sql = f"INSERT INTO hospital_insurance_prices (hospital_id, cpt_code, provider_id, cost) VALUES ({df.loc[i]['hospital_id']}, '{df.loc[i]['cpt_code']}', {df.loc[i]['provider_id']}, {df.loc[i]['cost']});"
        print(sql)
        res = con.execute(text(sql))
        break
        # except Exception as e:
        #     print("Could not insert" + str(e))