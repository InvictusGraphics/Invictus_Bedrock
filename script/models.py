import json
import os

paths = json.load(open('paths.json'))
path_ported_model = os.path.join(paths['invictus_bedrock'], "models/mobs.json")
path_origin_model = os.path.join(paths['vanilla_bedrock'], "models/mobs.json")

# Load models
models = {}
with open(path_origin_model, 'r') as inputfile:
	models = json.load(inputfile)

# Destroy noses
geometries = ["geometry.villager", "geometry.vindicator", "geometry.villager.witch:geometry.villager", "geometry.npc"]

for geometry in geometries:
	for idx, bone in enumerate(models[geometry]["bones"]):
		if bone["name"] == "nose":
			models[geometry]["bones"].pop(idx)

if not os.path.exists(os.path.dirname(path_ported_model)):
	os.makedirs(os.path.dirname(path_ported_model))

with open(path_ported_model, 'w') as outfile:
    json.dump(models, outfile, indent=4)
