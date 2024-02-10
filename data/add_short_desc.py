import json

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import postgresql

engine = create_engine(
    "postgresql://kodqrbmcuqhgdi:b4c7907bedf57277731a6a867809b5d888cab348b9bd151ce2e0e6a227325079@ec2-44-213-151-75.compute-1.amazonaws.com:5432/dbgitidqah3a5l")

with engine.connect() as con:
    df = pd.read_csv('cpt_codes_with_short_desc.csv')
    for i in range(df.shape[0]):
        sd = json.dumps(df.loc[i]['short_desc']).replace("'", "")
        cptcd = df.loc[i]['cpt_code']
        sql = text(f"""UPDATE cms SET short_description = '{sd}' WHERE cpt_code = '{cptcd}';""")
        # st = sql.bindparams(sd=df.loc[i]['short_desc'], cptcd=df.loc[i]['cpt_code'])
        # st.compile(
        #     dialect=postgresql.dialect(), compile_kwargs={'literal_binds': True}
        # )
        print (sql)
        # res = con.execute(sql)

