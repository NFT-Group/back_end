import json
from machine_learning.retrieve_collections_from_pkl import retrieve_all_pickles_into_dict, retrieve_certain_collection

collection_dict = retrieve_certain_collection('boredape')
print(collection_dict)
ipfs = collection_dict['boredape'].ipfs_link_list[500]
print(ipfs)

# print(ipfs)

# collection_dict = retrieve_all_pickles_into_dict()
# print(collection_dict)
# ipfs = collection_dict['boredape'].ipfs_link_list[500]
# print(ipfs)
# trait_list = collection_dict['boredape'].trait_list_dict[500]
# print(trait_list)
# trait_list_json = json.loads(trait_list)
# print(trait_list_json)


trait_list = collection_dict['boredape'].metadata_list[500]
print(trait_list)
trait_list_json = json.loads(trait_list)
print(trait_list_json)
