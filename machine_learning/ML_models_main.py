from retrieve_collections_from_pkl import retrieve_all_pickles_into_dict
from ML_models_functions import random_forest_reg
from sklearn.model_selection import train_test_split
from analysis import analyse_results
import pickle



collection_dict = retrieve_all_pickles_into_dict()
bored_apes = collection_dict['boredape']
preprocessed_df = bored_apes.preprocessed_df

x = preprocessed_df.drop(['ethprice'], axis=1)
x = x.sort_index(axis=1, ascending=True) # IMPORTANT LINE OF CODE TO ENSURE LINEUP
y = preprocessed_df['ethprice']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.10, shuffle=False)
y_pred, y_test, model = random_forest_reg(x_train, x_test, y_train, y_test)
analyse_results(y_pred, y_test, 'boredape')

with 

# filename = "bored_apes_model.pkl"
# pickle.dump(model, open(filename, 'wb'))

# loaded_model = pickle.load(open(filename, 'rb'))
# y_pred = loaded_model.predict(x_test)
# analyse_results(y_pred, y_test, 'BoredApes')

# prediction = loaded_model.predict(x)

# ref = db.reference('boredape4372')
# data_for_input = ref.get()
# print(data_for_input)

# # data_for_input_json = pd.DataFrame.from_dict(data_for_input, orient="records")
# data_for_input_json = pd.DataFrame([data_for_input])

# data_for_input_json = data_for_input_json.drop(['NameOfCollection', 'ethprice'], axis=1)
# data_for_input_json['timestamp'] = 0
# print(data_for_input_json)

# price_prediction = loaded_model.predict(data_for_input_json)
# print(price_prediction)