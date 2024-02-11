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

llm = OpenAI(openai_api_key='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',
             openai_organization='org-JmTkwXW5KD9MhhWngn5cUec6')

# OPENAI_API_KEY = getpass()
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# template = """Generate a short two sentence description of the following CPT procedure name that explains what it is.
# Be accurate, concise and use easy to understand terminology.  The first sentence should explain what it is,
# and the second sentence should give a short example of when or why it might be done.
#
# CPT name: {procedure_name}
# """

template = """
Give a 1 sentence description of  the following CPT procedure code. The description should be accurate but understandable to a person with no medical training, and should include a friendly name for the procedure. The friendly name should be in the description and not a separate sentence.

CPT name: {procedure_description}
"""

prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(prompt=prompt, llm=llm)

df = pd.read_csv('data/cpt_codes_with_desc.csv')
df['short_desc'] = ""

for i in tqdm(range(df.shape[0])):
    cpt_name = df.loc[i]['name']
    ans = llm_chain.run(cpt_name)
    df.at[i, 'short_desc'] = ans

    if i % 10 == 0:
        print(f"Saving intermediate dataset: {i}/{df.shape[0]}")
        df.to_csv('data/cpt_codes_with_short_desc.csv', index=False)

df.to_csv('data/cpt_codes_with_short_desc.csv', index=False)
