import pickle
from PIL import Image
import yaml
import sys
import pandas as pd
import numpy as np

img_x, img_y, n_channels = 128, 128, 3

def main(config_file):
	with open(config_file, 'r') as f:
		config = yaml.load(f)

	# Load file of training image names and correct labels.
	train_set = pd.read_csv(config['train_set'])
	# Load file of test image names and dummy labels.
	test_set = pd.read_csv(config['test_set'])

	# Preprocess NN features.
	print("Preprocessing NN training set features...")
	train_features_nn = preprocess_nn(config['train_imgs'], train_set)
	pickle.dump( train_features_nn, open( config['train_features_nn'], "wb" ) )
	print("Done.")
	print("Preprocessing NN test set features...")
	test_features_nn = preprocess_nn(config['test_imgs'], test_set)
	pickle.dump( test_features_nn, open( config['test_features_nn'], "wb" ) )
	print("Done.")

# Load the train and test images.
# Helper function.
def preprocess_nn(folder_name, names_and_labels):
	imgs_matrix = np.zeros([len(names_and_labels), img_x, img_y, n_channels])
	for i, img_name in enumerate(names_and_labels['name'].iloc[:]):
		img_src = folder_name + str(img_name) + '.jpg'
		img = Image.open(img_src).resize((img_x, img_y)) # was 128x128
		# Resize and change pixel range from 0-255 to 0-1.
		imgs_matrix[i,:,:,:] = np.array(img.getdata()).reshape([img_x, img_y, n_channels]) / 255
	return imgs_matrix

if __name__ == "__main__":
	main(sys.argv[1])
