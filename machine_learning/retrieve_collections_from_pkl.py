import pickle
import pathlib
# from collection_class import Collection

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

def retrieve_certain_collection(name):
    with open(str(pathlib.Path(__file__).parent.resolve()) + 
        '/collections_pkl_folder/' + name +
        '_collection_class.pkl', 'rb') as f:
           data = pickle.load(f)
    return data