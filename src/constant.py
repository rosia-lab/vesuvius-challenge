from os.path import join, exists, abspath
from os import pardir
from os import sep

# MODEL VARIABLES
MODEL_NAME = 'EfficientUNetV2_M'
# NUM_BLOCKS = 3
EPOCHS = 5
BATCH_SIZE = 16
LEARNING_RATE = 1e-2
BCE_WEIGHT = 0.5
DICE_THRESHOLD = 0.5

# DATASET VARIABLES
TILE_SIZE = 256
NUM_SLICES = 10
START_SLICE = 27
REVERSE_SLICES = False
SELECTION_THR = 0.05
AUGMENTATION = True
TRAIN_FRAGMENTS = ['1', '3']
VAL_FRAGMENT = '2'

# KAGGLE DIRECTORIES
KAGGLE_WORKING_DIR = join(abspath(sep), 'kaggle', 'working')
KAGGLE_INPUT_DIR = join(abspath(sep), 'kaggle', 'input')

KAGGLE_TRAIN_FRAGMENTS_PATH = join(KAGGLE_INPUT_DIR, 'vesuvius-challenge-ink-detection', 'train')
KAGGLE_TEST_FRAGMENTS_PATH = join(KAGGLE_INPUT_DIR, 'vesuvius-challenge-ink-detection', 'test')
KAGGLE_TILES_PATH = join(KAGGLE_INPUT_DIR, 'vesuvius-challenge-256x256-tiles', 'train')

# COOKIECUTTER DIRECTORIES
COOKIECUTTER_MODELS_DIR = 'models'
COOKIECUTTER_SUBMISSIONS_DIR = 'submissions'
COOKIECUTTER_TRAIN_FRAGMENTS_PATH = join('data', 'raw', 'train')
COOKIECUTTER_TEST_FRAGMENTS_PATH = join('data', 'raw', 'test')

PARENT_TRAIN_FRAGMENTS_PATH = join(pardir, pardir, 'data', 'raw', 'train')
PARENT_TEST_FRAGMENTS_PATH = join(pardir, pardir, 'data', 'raw', 'test')

# NOTEBOOKS DIRECTORIES
NOTEBOOK_TRAIN_FRAGMENTS_PATH = join(pardir, 'data', 'raw', 'train')
NOTEBOOK_TEST_FRAGMENTS_PATH = join(pardir, 'data', 'raw', 'test')

# DIRECTORIES
MODELS_DIR = KAGGLE_WORKING_DIR if exists(KAGGLE_WORKING_DIR) else COOKIECUTTER_MODELS_DIR
SUBMISSION_DIR = KAGGLE_WORKING_DIR if exists(KAGGLE_WORKING_DIR) else COOKIECUTTER_SUBMISSIONS_DIR

TRAIN_FRAGMENTS_PATH = KAGGLE_TRAIN_FRAGMENTS_PATH if exists(KAGGLE_TRAIN_FRAGMENTS_PATH) \
    else COOKIECUTTER_TRAIN_FRAGMENTS_PATH if exists(COOKIECUTTER_TRAIN_FRAGMENTS_PATH) \
    else PARENT_TRAIN_FRAGMENTS_PATH if exists(PARENT_TRAIN_FRAGMENTS_PATH) \
    else NOTEBOOK_TRAIN_FRAGMENTS_PATH

TEST_FRAGMENTS_PATH = KAGGLE_TEST_FRAGMENTS_PATH if exists(KAGGLE_TEST_FRAGMENTS_PATH) \
    else COOKIECUTTER_TEST_FRAGMENTS_PATH if exists(COOKIECUTTER_TEST_FRAGMENTS_PATH) \
    else PARENT_TEST_FRAGMENTS_PATH if exists(PARENT_TEST_FRAGMENTS_PATH) \
    else NOTEBOOK_TEST_FRAGMENTS_PATH
