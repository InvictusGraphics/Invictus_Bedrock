import json
from shutil import copyfile
import os

paths = json.load(open('paths.json'))
path_source = os.path.join(paths['invictus_java'], "assets/minecraft/textures")
path_target = os.path.join(paths['invictus_bedrock'], "textures") 

# Load mappings from the output of map.py
mappings = {}
with open('map.json', 'r') as infile:
    mappings = json.load(infile)

# Move each file relative to path_source, to the mapped path relative to path_target
for source, target in mappings.items():

	path_source_image = os.path.join(path_source, source.strip("\\"))
	path_target_image = os.path.join(path_target, target.strip("\\"))

	print(path_source_image)

	# Error checking- file must exist in source, and make sure folder is made
	if os.path.exists(path_source_image):
		if not os.path.exists(os.path.dirname(path_target_image)):
			os.makedirs(os.path.dirname(path_target_image))

		copyfile(path_source_image, path_target_image)

		# Keep the mcmeta file if it exists
		if os.path.exists(path_source_image + '.mcmeta'):
			copyfile(path_source_image + '.mcmeta', path_target_image + '.mcmeta')
