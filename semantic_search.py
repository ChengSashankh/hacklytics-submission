import json
import os.path
from typing import List

from flask_cors import CORS
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from flask import Flask, request, jsonify
from sqlalchemy import String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text

import geopy.distance
from uuid import uuid4

class Base(DeclarativeBase):
    pass


class HospitalGeneralPrices(Base):
    __tablename__ = 'hospital_general_prices'

    cpt_code: Mapped[str] = mapped_column(primary_key=True)
    hospital_id: Mapped[int] = mapped_column()
    procedure: Mapped[str] = mapped_column(String(256))
    charges: Mapped[float] = mapped_column()
    discounted_charges: Mapped[float] = mapped_column()
    min_negotiated: Mapped[float] = mapped_column()
    max_negotiated: Mapped[float] = mapped_column()

    def __repr__(self):
        return f"Price(cpt_code={self.cpt_code}, hospital_id={self.hospital_id} +other fields)"


engine = create_engine(
    "")

loader = CSVLoader(
    file_path='./data/cpt_codes_with_desc.csv',
    source_column='desc'
)

print("Loading embeddings")
embeddings = OpenAIEmbeddings(api_key='',
                              organization='')
print("Loaded embeddings")

if os.path.exists('faiss_index'):
    print('Loading faiss index...')
    db = FAISS.load_local('faiss_index', embeddings)
else:
    print("Loading documents")
    documents = loader.load()
    print("Loaded {} documents".format(len(documents)))

    print("Building vector database")
    db = FAISS.from_documents(documents, embeddings)
    print("Done")

print("Saving vector database locally")
db.save_local('faiss_index')
print("Done")


def query_complaint(complaint: str):
    return db.similarity_search_with_score(complaint)


def get_complaint_from_search_text(search_text: str):
    # TODO: Use a prompt template to convert arbitrary input text into a structured format
    return search_text


def get_locations_by_cpt(cpt_codes: List[str]):
    where_clause = ", ".join([f"\'{c}\'" for c in cpt_codes])
    with engine.connect() as con:
        print(
            f"SELECT c.cpt_code, h.hospital_id, h.address, h.hospital_name, h.latitude, h.longitude, hgp.procedure, hgp.charges, hgp.discounted_charges, hgp.min_negotiated, hgp.max_negotiated FROM hospital_general_prices hgp JOIN cms c ON hgp.cpt_code = c.cpt_code JOIN hospitals h ON h.hospital_id = hgp.hospital_id WHERE hgp.CPT_CODE IN ({where_clause})")
        statement = text(
            f"SELECT c.cpt_code, h.hospital_id, h.address, h.hospital_name, h.latitude, h.longitude, hgp.procedure, hgp.charges, hgp.discounted_charges, hgp.min_negotiated, hgp.max_negotiated FROM hospital_general_prices hgp JOIN cms c ON hgp.cpt_code = c.cpt_code JOIN hospitals h ON h.hospital_id = hgp.hospital_id WHERE hgp.CPT_CODE IN ({where_clause})")
        rs = con.execute(statement)
        return rs.all()


def get_prices_by_cpt_and_hospital(cpt_codes: List[str], hospital_id: str):
    cpt_where_clause = ", ".join([f"\'{c}\'" for c in cpt_codes])
    with engine.connect() as con:
        print(
            f"SELECT * FROM hospital_insurance_prices hip JOIN hospitals h ON h.hospital_id = hip.hospital_id JOIN insurance i ON hip.provider_id = i.provider_id WHERE hip.CPT_CODE IN ({cpt_where_clause}) AND h.hospital_id = '{hospital_id}'")
        statement = text(
            f"SELECT * FROM hospital_insurance_prices hip JOIN hospitals h ON h.hospital_id = hip.hospital_id JOIN insurance i ON hip.provider_id = i.provider_id WHERE hip.CPT_CODE IN ({cpt_where_clause}) AND h.hospital_id = '{hospital_id}'")
        rs = con.execute(statement)
        return rs.all()


def get_prices_by_cpt_and_insurance(cpt_codes: List[str], insurance_id: str):
    cpt_where_clause = ", ".join([f"\'{c}\'" for c in cpt_codes])
    with engine.connect() as con:
        print(
            f"SELECT * FROM hospital_insurance_prices hip JOIN hospitals h ON h.hospital_id = hip.hospital_id JOIN insurance i ON hip.provider_id = i.provider_id WHERE hip.CPT_CODE IN ({cpt_where_clause}) AND i.provider_id = '{insurance_id}'")
        statement = text(
            f"SELECT * FROM hospital_insurance_prices hip JOIN hospitals h ON h.hospital_id = hip.hospital_id JOIN insurance i ON hip.provider_id = i.provider_id WHERE hip.CPT_CODE IN ({cpt_where_clause}) AND i.provider_id = '{insurance_id}'")
        rs = con.execute(statement)
        return rs.all()



def get_short_desc_by_cpt(cpt_code: str):
    sql = text( f"SELECT c.short_description FROM CMS c WHERE c.CPT_CODE = '{cpt_code}'")
    with engine.connect() as con:
        rs = con.execute(sql)
        return rs.all()[0]._asdict()['short_description']


app = Flask(__name__)
cors = CORS(app)

from functools import wraps
from flask import request, abort

# The actual decorator function
def require_appkey(view_function):
    key = "1ec0fb84-220a-4287-a70b-13f887c902b1"

    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == key:
            return view_function(*args, **kwargs)
        else:
            print(request.args)
            abort(401)
    return decorated_function


@app.route('/search', methods=["POST"])
@require_appkey
def search():
    query = request.json['query']
    complaint = get_complaint_from_search_text(query)
    result = query_complaint(complaint)
    print (result[0][0])
    result_dict = [{"desc": doc[0].page_content.split('\n')[1],
                    "cpt_code": doc[0].page_content.split('\n')[0].split('cpt_code: ')[-1],
                    "metadata": doc[0].metadata} for doc in result]

    for r in result_dict:
        r['short_desc'] = get_short_desc_by_cpt(r['cpt_code'])

    return jsonify(result_dict)


@app.route('/locations/byCptAndHospital', methods=["POST"])
@require_appkey
def get_locations_by_cpt_hospital():
    codes = request.json['cpt_codes']
    user_lat = request.json['user_lat']
    user_lon = request.json['user_lon']
    hospital_id = request.json['hospital_id']
    locations = [l._asdict() for l in get_prices_by_cpt_and_hospital(codes, hospital_id)]
    # locations = [l for l in locations if calculate_distance(user_lat, user_lon, l['latitude'], l['longitude']) < 150.0]
    return locations


@app.route('/locations/byCptAndInsurance', methods=["POST"])
@require_appkey
def get_locations_by_cpt_insurance():
    codes = request.json['cpt_codes']
    user_lat = request.json['user_lat']
    user_lon = request.json['user_lon']
    insurance_id = request.json['insurance_id']
    locations = [l._asdict() for l in get_prices_by_cpt_and_insurance(codes, insurance_id)]
    locations = [l for l in locations if calculate_distance(user_lat, user_lon, l['latitude'], l['longitude']) < 150.0]
    return locations


@app.route('/locations/', methods=["POST"])
@require_appkey
def get_locations():
    codes = request.json['cpt_codes']
    user_lat = request.json['user_lat']
    user_lon = request.json['user_lon']
    locations = [l._asdict() for l in get_locations_by_cpt(codes)]
    locations = [l for l in locations if calculate_distance(user_lat, user_lon, l['latitude'], l['longitude']) < 150.0]
    return locations


def calculate_distance(point_a_lat, point_a_lon, point_b_lat, point_b_lon):
    return geopy.distance.geodesic((point_a_lat, point_a_lon), (point_b_lat, point_b_lon)).mi


if __name__ == '__main__':
    #app.config.from_pyfile('config.cfg')
    app.run()
