import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import numpy as np
from trait_distribution import trait_distribution 
import json

cred = firebase_admin.credentials.Certificate("/homes/tm21/Documents/key_for_all_tokens_store.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL':'https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/'
    })

ref = db.reference('/')

bored_apes = ref.order_by_key().start_at('boredape').limit_to_first(1).get()
# bored_apes_list = list(bored_apes.items())

id_list = []
metadata_list = []

for id, meta in bored_apes.items():
    id_list.append(id)
    metadata_temp = json.dumps(meta["metadata"])
    metadata_temp = metadata_temp.replace("\\","")
    print(metadata_temp)

    
    metadata_temp = json.loads(metadata_temp)
    # metadata_temp = json.dumps(metadata_temp["attributes"])
    # metadata_list.append(metadata_temp)
    # metadata_list.append(json.dumps(meta["metadata"]))
    # metadata_list = [metadata.replace("\\", "") for metadata in metadata_list]
    

print(metadata_list)

# unique_header_list, trait_values_distribution = trait_distribution(id_list, metadata_list)

# print(unique_header_list)
# print(trait_values_distribution)

