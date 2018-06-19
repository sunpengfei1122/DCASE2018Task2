import torch
import numpy as np
import shutil
import pickle
import librosa
import logging
import os
from network import *
from waveResnet import *
from MTO_network import *


def save_data(filename, data):
    """Save variable into a pickle file

    Parameters
    ----------
    filename: str
        Path to file

    data: list or dict
        Data to be saved.

    Returns
    -------
    nothing

    """
    pickle.dump(data, open(filename, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    # pickle.dump(data, open(filename, 'w'))


def load_data(filename):
    """Load data from pickle file

    Parameters
    ----------
    filename: str
        Path to file

    Returns
    -------
    data: list or dict
        Loaded file.

    """

    return pickle.load(open(filename, "rb"), encoding='latin1')



def create_logging(log_dir, filemode):

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    i1 = 0

    while os.path.isfile(os.path.join(log_dir, "{:04d}.log".format(i1))):
        i1 += 1

    log_path = os.path.join(log_dir, "{:04d}.log".format(i1))
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_path,
                        filemode=filemode)

    # Print to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    return logging


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def  __init__(self):
        self.reset()

    def  reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].view(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res


def save_checkpoint(state, is_best, fold, filename='../model/checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        best_name = '../model/model_best.' + str(fold) + '.pth.tar'
        shutil.copyfile(filename, best_name)

    # def make_submission():
#     # Make a submission file
#     top_3 = np.array(LABELS)[np.argsort(-predictions, axis=1)[:, :3]]
#     predicted_labels = [' '.join(list(x)) for x in top_3]
#     test['label'] = predicted_labels
#     test[['label']].to_csv(PREDICTION_FOLDER + "/predictions_%d.csv"%i)

def run_method_by_string(name):
    p = globals().copy()
    p.update(globals())
    method = p.get(name)
    if not method:
        raise NotImplementedError('Method %s not implement' % name)
    return method


def make_dirs():
    # data_dir = '../data-22050'
    # prediction_dir = '../prediction_dir'
    # log_dir = '../log'
    # model_dir = '../model_dir'
    # submission_dir = '../submission_dir'
    dirs = ['../data-22050', '../prediction', '../log', '../model',
            '../model', '../submission']

    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)
            print('Make dir: %s' %dir)

