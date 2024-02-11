import json

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects import postgresql

engine = create_engine(
    "")

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

