import pickle
import pathlib

list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]

def retrieve_all_pickles_into_dict():
    collection_dict = {}
    for name in list_of_names:
        with open(str(pathlib.Path(__file__).parent.resolve()) + 
            '/collections_pkl_folder/' + name +
            '_collection_class.pkl', 'rb') as f:
                data = pickle.load(f)
                collection_dict[name] = data
    return collection_dict

collection_dict = retrieve_all_pickles_into_dict()
print(collection_dict['boredape'].transactions_df)