import firebase_admin 
from firebase_admin import db
import pathlib
from retrieve_collections_from_pkl import retrieve_certain_collection


cred_pull_tokens_key = str(pathlib.Path(__file__).parent.resolve()) + '/database_store_keys/key_for_all_tokens_store.json'
cred_pull_tokens = firebase_admin.credentials.Certificate(cred_pull_tokens_key)
tokens_app = firebase_admin.initialize_app(cred_pull_tokens, {
    'databaseURL':'https://alltokens-8ff48-default-rtdb.europe-west1.firebasedatabase.app/'
    })

ref = db.reference('/')
collection_tokens = ref.order_by_key().start_at('punk').get()
# print(collection_tokens)

collection_keys = list(collection_tokens.keys())

MAGIC_DICTIONARY = dict({
'Alien' : 'Type',
'Ape' : 'Type',
'Zombie' : 'Type',
'Female 1' : 'Type',
'Female 2' : 'Type',
'Female 3' : 'Type',
'Female 4' : 'Type',
'Male 1' : 'Type',
'Male 2' : 'Type',
'Male 3' : 'Type',
'Male 4' : 'Type',
'Beanie' : 'Hat',
'Choker' : 'Neck',
'Pilot Helmet' : 'Hat',
'Tiara' : 'Hat',
'Orange Side' : 'Hair',
'Buck Teeth' : 'Mouth',
'Welding Goggles' : 'Hat',
'Pigtails' : 'Hair',
'Pink With Hat' : 'Hair',
'Top Hat' : 'Hat',
'Spots' : 'Face',
'Rosy Cheeks' : 'Face',
'Blonde Short' : 'Hair',
'Wild White Hair' : 'Hair',
'Cowboy Hat' : 'Hat',
'Wild Blonde' : 'Hair',
'Straight Hair Blonde' : 'Hair',
'Big Beard' : 'Beard',
'Red Mohawk' : 'Hair',
'Half Shaved' : 'Hair',
'Blonde Bob' : 'Hair',
'Vampire Hair' : 'Hair',
'Clown Hair Green' : 'Hair',
'Straight Hair Dark' : 'Hair',
'Straight Hair' : 'Hair',
'Silver Chain' : 'Neck',
'Dark Hair' : 'Hair',
'Purple Hair' : 'Hair',
'Gold Chain' : 'Neck',
'Medical Mask' : 'Mouth',
'Tassle Hat' : 'Hat',
'Fedora' : 'Hat',
'Police Cap' : 'Hat',
'Clown Nose' : 'Nose',
'Smile' : 'Mouth',
'Cap Forward' : 'Hat',
'Hoodie' : 'Hat',
'Front Beard Dark' : 'Beard',
'Frown' : 'Mouth',
'Purple Eye Shadow' : 'Eye',
'Handlebars' : 'Beard',
'Blue Eye Shadow' : 'Eye',
'Green Eye Shadow' : 'Eye',
'Vape' : 'Accessory',
'Front Beard' : 'Beard',
'Chinstrap' : 'Beard',
'3D Glasses' : 'Eye',
'Luxurious Beard' : 'Beard',
'Mustache' : 'Beard',
'Normal Beard Black' : 'Beard',
'Normal Beard' : 'Beard',
'Eye Mask' : 'Eye',
'Goat' : 'Beard',
'Do-rag' : 'Hat',
'Shaved Head' : 'Hair',
'Muttonchops' : 'Beard',
'Peak Spike' : 'Hair',
'Pipe' : 'Accessory',
'VR' : 'Eye',
'Cap' : 'Hat',
'Small Shades' : 'Eye',
'Clown Eyes Green' : 'Eye',
'Clown Eyes Blue' : 'Eye',
'Headband' : 'Hat',
'Crazy Hair' : 'Hair',
'Knitted Cap' : 'Hat',
'Mohawk Dark' : 'Hair',
'Mohawk' : 'Hair',
'Mohawk Thin' : 'Hair',
'Frumpy Hair' : 'Hair',
'Wild Hair' : 'Hair',
'Messy Hair' : 'Hair',
'Eye Patch' : 'Eye',
'Stringy Hair' : 'Hair',
'Bandana' : 'Hat',
'Classic Shades' : 'Eye',
'Shadow Beard' : 'Beard',
'Regular Shades' : 'Eye',
'Horned Rim Glasses' : 'Eye',
'Big Shades' : 'Eye',
'Nerd Glasses' : 'Eye',
'Black Lipstick' : 'Mouth',
'Mole' : 'Face',
'Purple Lipstick' : 'Mouth',
'Hot Lipstick' : 'Mouth',
'Cigarette' : 'Accessory',
'Earring' : 'Ear'})

#print(MAGIC_DICTIONARY)

new_collection = dict()
for i in collection_keys:
	new_collection[i] = list()
	for j in collection_tokens[i]['metadata'].split(','):
		new_collection[i].append(dict(trait_type=MAGIC_DICTIONARY[j.strip()], value=j.strip()))

# Type: Alien, Ape, Zombie, Female, Male

print(new_collection)

#bored_apes = retrieve_certain_collection('boredape')
#print(bored_apes.trait_list_dict['100'])
# print(bored_apes.__dict__)
