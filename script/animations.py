import json
import os
from PIL import Image

paths = json.load(open('paths.json'))
path_invictus = os.path.join(paths['invictus_bedrock'], "textures")
path_flipbook = os.path.join(paths['invictus_bedrock'], "textures", "flipbook_textures.json")

# Find the animations
animation_paths = []
for root, dirs, files in os.walk(path_invictus, topdown=False):
    for name in files:
        if name[-6:] == 'mcmeta':
            animation_paths.append(os.path.join(root, name))

# Build the flipbook json
flipbook_json = []
for path in animation_paths:
    with open(path, 'r') as infile:

        texture = path.replace(paths['invictus_bedrock'], '').replace('\\', '/').replace('.png.mcmeta', '').strip('/')
        animation = {
            'flipbook_texture': texture,
            'atlas_tile': texture.split('/')[-1]
        }

        mcmeta = json.load(infile)['animation']
        if 'frametime' in mcmeta:
            animation['ticks_per_frame'] = mcmeta['frametime']

        if 'frames' in mcmeta:
            animation['frames'] = mcmeta['frames']

        if 'interpolate' in mcmeta:
            animation['interpolate'] = mcmeta['interpolate']

        flipbook_json.append(animation)


if not os.path.exists(os.path.dirname(path_flipbook)):
    os.makedirs(os.path.dirname(path_flipbook))

with open(path_flipbook, 'w') as outfile:
    json.dump(flipbook_json, outfile, indent=4)


# Now create mipmaps
for path in animation_paths:
    image_path = path.replace('.mcmeta', '')
    mipmap_path = image_path[:-4] + '_mipmap' + image_path[-4:]

    animation_image = Image.open(image_path)
    width, _ = animation_image.size
    animation_mipmap = animation_image.crop((0, 0, width, width)).save(mipmap_path)

    # Remove the .mcmeta file
    # os.remove(path)
