from kafrcnn.datasets.imdb_vocS_cocoC import imdb_vocS_cocoC

"""Factory method for easily getting imdbs by name."""
__sets = {}


"""
# Read arguments from the config file
config_file = 'config/drive-bc-config.json'
img_set_path = get_args(config_file, 'training').train_list
imdb_name = get_args(config_file, 'training').imdb_name

# Parse the custom imdb name
split = os.path.splitext(os.path.basename(img_set_path))[0]
imdb_set, year, _ = imdb_name.split('_')

# Set up custom set passed from the config file
name = imdb_set + '_{}_{}'.format(year, split)
print name
__sets[name] = (lambda split=split,
                year=year: imdb_vocS_cocoC(split, year, img_set_path))

# Set the default train and test files... idk if we need this
for year in ['8888']:
    for split in ['train', 'test']:
        name = 'cococustom_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split,
                        year=year: imdb_vocS_cocoC(split, year, img_set_path))
"""


def get_imdb(name, img_set_path):
    """Get an imdb (image database) by name."""
    _, year, split = name.split('_')
    __sets[name] = (lambda split=split,
                    year=year: imdb_vocS_cocoC(split, year, img_set_path))

    if not __sets.has_key(name):
        raise KeyError('Unknown dataset: {}'.format(name))

    return __sets[name]()


def list_imdbs():
    """List all registered imdbs."""
    return __sets.keys()
