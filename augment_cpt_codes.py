# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from getpass import getpass
import os

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from tqdm import tqdm
import pandas as pd

llm = OpenAI(openai_api_key='', openai_organization='')

# OPENAI_API_KEY = getpass()
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

template = """Give a description of  the following CPT procedure code including a summary, uses of the procedure, 
some common reasons to perform the procedure and relevant medical conditions. Write it as a paragraph.
CPT Code: {cpt_code}

Summary: 
"""

prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

df = pd.read_csv('data/cpt_codes.csv')
df['desc'] = ""

for i in tqdm(range(df.shape[0])):
    cpt_name = df.loc[i]['name']
    ans = llm_chain.run(cpt_name)
    df.at[i, 'desc'] = ans

    if i % 10 == 0:
        print(f"Saving intermediate dataset: {i}/{df.shape[0]}")
        df.to_csv('data/cpt_codes_with_desc.csv', index=False)

df.to_csv('data/cpt_codes_with_desc.csv', index=False)
