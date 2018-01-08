from PIL import Image
import numpy as np
import os
import json

path_origin = r"C:\Users\mike\AppData\Roaming\.minecraft\versions\17w50a\assets\minecraft\textures"
path_ported = r"C:\Users\mike\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\resource_packs\Vanilla_1.2.6\textures"

# How similar must the two files be?
matching_tolerance = .001

file_types = ["png", "tga"]


# Transparent regions should have zeroed RGB values
def rgb_clip(raw_image):
    if len(raw_image.shape) != 3 or raw_image.shape[2] != 4:
        return raw_image

    raw_image[raw_image[:, :, 3] == 0] = 0
    return raw_image


# Create a list of files to match against
candidates = []
for root, dirs, files in os.walk(path_ported, topdown=False):
    for name in files:
        if name[-3:] in file_types:
            candidates.append(os.path.join(root, name))


# Identify an image with shared binaries
def find_match(raw_legend):

    for candidate in candidates:
        raw_candidate = rgb_clip(np.array(Image.open(candidate)))


        if raw_candidate.shape == raw_legend.shape and np.allclose(raw_legend, raw_candidate, rtol=matching_tolerance):
            candidates.remove(candidate)
            return candidate


mappings = {}
not_matched = []

# Check every file for matches in the output directory
for root, dirs, files in os.walk(path_origin, topdown=False):
    for name in files:

        # Ignore files that aren't images
        if name[-3:] not in file_types:
            continue

        path_origin_image = os.path.join(root, name)

        raw = rgb_clip(np.array(Image.open(path_origin_image)))

        # Check for match for the given file
        match = find_match(raw)

        if match:
            print("matched      " + name)
            mappings[path_origin_image.replace(path_origin, "")] = match.replace(path_ported, "")
        else:
            print("no match for " + name)
            not_matched.append(path_origin_image.replace(path_origin, ""))


with open('map.json', 'w') as outfile:
    json.dump(mappings, outfile, indent=4)

with open('map_failed.json', 'w') as outfile:
    json.dump(not_matched, outfile, indent=4)