import time

from util import *
from config import *
import os
from network import *
import numpy as np

config = Config()
# attrs = '\n'.join('%s:%s'%item for item in vars(config).items())
#
#
#
# s = 'resnet101_m'
# model = run_method_by_string(s)()
# print(model)

# logging = create_logging('../log', filemode='w')
#
# logging.info(os.path.abspath(__file__))
# logging.info(attrs)


# logmel = np.ones((2,3))
# print(logmel)
# logmel = np.pad(logmel, ((0, 0),(0, 4)), "constant")
# print(logmel)

data, _ = librosa.load('../audio_test/0b0427e2.wav', config.sampling_rate)
# melspec = librosa.feature.melspectrogram(data, config.sampling_rate,
#                                          n_fft=config.n_fft, hop_length=config.hop_length,
#                                          n_mels=config.n_mels)
# logmel = librosa.core.power_to_db(melspec)
print(data.shape)