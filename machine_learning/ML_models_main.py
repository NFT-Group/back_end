from machine_learning.retrieve_collections_from_pkl import retrieve_all_pickles_into_dict
from machine_learning.ML_models_functions import random_forest_reg
from sklearn.model_selection import train_test_split
from analysis import analyse_results
import pickle
import pathlib

list_of_names = ["boredape", "boredapekennel", "clonex", "coolcat", "cryptoad", "doodle", "penguin", "punk"]

collection_dict = retrieve_all_pickles_into_dict()

for name in list_of_names:

    collection = collection_dict[name]
    try:
        preprocessed_df = collection.preprocessed_df
    except:
        continue

    x = preprocessed_df.drop(['ethprice', 'tokenID'], axis=1)
    if(name == 'cryptoad'):
        x = x.drop(['# Traits'], axis =1)
    x = x.sort_index(axis=1, ascending=True) # IMPORTANT LINE TO ENSURE LINEUP
    y = preprocessed_df['ethprice']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, shuffle=True)
    y_pred, y_test, model = random_forest_reg(x_train, x_test, y_train, y_test)
    analyse_results(y_pred, y_test, name)

    with open(str(pathlib.Path(__file__).parent.resolve()) + '/ML_models/random_forests/' + 
        name + '_RF.pkl', 'wb') as handle:
            pickle.dump(model, handle)
