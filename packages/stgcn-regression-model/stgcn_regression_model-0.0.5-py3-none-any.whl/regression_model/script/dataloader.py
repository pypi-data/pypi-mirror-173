import os
import numpy as np
import pandas as pd
import scipy.sparse as sp
import torch
import math
from sklearn import preprocessing
import torch.utils as utils
from regression_model.config.core import *
from regression_model.script import utility



def load_adj(dataset_name):
    dataset_path = './data'
    dataset_path = os.path.join(dataset_path, dataset_name)
    adj = sp.load_npz(os.path.join(dataset_path, 'adj.npz'))
    adj = adj.tocsc()
    
    if dataset_name == 'metr-la':
        n_vertex = 207 # number of nodes
    elif dataset_name == 'pems-bay':
        n_vertex = 325
    elif dataset_name == 'pemsd7-m':
        n_vertex = 228

    return adj, n_vertex

def load_adj_link(dataset_name, dataset_path):
    dataset_path = os.path.join(dataset_path, dataset_name)
    adj = np.load(os.path.join(dataset_path, 'adj.npy'))
    
    if dataset_name == 'link':
        n_vertex = len(adj) # number of nodes

    return adj, n_vertex

def load_data(dataset_name, len_train, len_val, dataset_path):
    dataset_path = os.path.join(dataset_path, dataset_name)
    if dataset_name == 'link':
        vel = pd.read_csv(os.path.join(dataset_path, 'time.csv'))
    else:
        vel = pd.read_csv(os.path.join(dataset_path, 'vel.csv'))

    train = vel[: len_train]
    val = vel[len_train: len_train + len_val]
    test = vel[len_train + len_val:]
    return train, val, test

def data_transform(data, n_his, n_pred, device):
    # produce data slices for x_data and y_data

    n_vertex = data.shape[1]
    len_record = len(data)
    num = len_record - n_his - n_pred
    
    x = np.zeros([num, 1, n_his, n_vertex])
    y = np.zeros([num, n_vertex])
    
    for i in range(num):
        head = i
        tail = i + n_his
        x[i, :, :, :] = data[head: tail].reshape(1, n_his, n_vertex)
        y[i] = data[tail + n_pred - 1]

    return torch.Tensor(x).to(device), torch.Tensor(y).to(device)


def data_preparate(args, device, data_path):
    if args.dataset == 'link':
        adj, n_vertex = load_adj_link(args.dataset, data_path)
        gso = utility.calc_gso(adj, args.gso_type)
        if args.graph_conv_type == 'cheb_graph_conv':
            gso = utility.calc_chebynet_gso(gso)
        gso = gso.toarray()
    else:    
        adj, n_vertex = load_adj(args.dataset)
        gso = utility.calc_gso(adj, args.gso_type)
        if args.graph_conv_type == 'cheb_graph_conv':
            gso = utility.calc_chebynet_gso(gso)
        gso = gso.toarray()

    gso = gso.astype(dtype=np.float32)
    args.gso = torch.from_numpy(gso).to(device)
    print("gso datatype:", gso.dtype)
    print("gps data shape: ", gso.shape)
    dataset_path = os.path.join(data_path, args.dataset)

    if args.dataset == 'link':
        data_col = pd.read_csv(os.path.join(dataset_path, 'time.csv')).shape[0]
    else:
        data_col = pd.read_csv(os.path.join(dataset_path, 'vel.csv')).shape[0]
    # recommended dataset split rate as train: val: test = 60: 20: 20, 70: 15: 15 or 80: 10: 10
    # using dataset split rate as train: val: test = 70: 15: 15
    val_and_test_rate = 0.15

    len_val = int(math.floor(data_col * val_and_test_rate/2))
    len_test = int(math.floor(data_col * val_and_test_rate))
    len_train = int(data_col - len_val - len_test)

    # data_path = r'C:\Users\mizte\Documents\ea\tsb\gnn\deployment\data' # data path
    train, val, test = load_data(args.dataset, len_train, len_val, data_path)
    zscore = preprocessing.StandardScaler()
    train = zscore.fit_transform(train)
    val = zscore.transform(val)
    test = zscore.transform(test)

    x_train, y_train = data_transform(train, config.model_config.n_his, args.n_pred, device)
    x_val, y_val = data_transform(val, config.model_config.n_his, args.n_pred, device)
    x_test, y_test = data_transform(test, config.model_config.n_his, args.n_pred, device)
    train_data = utils.data.TensorDataset(x_train, y_train)
    train_iter = utils.data.DataLoader(dataset=train_data, batch_size=args.batch_size, shuffle=False)
    val_data = utils.data.TensorDataset(x_val, y_val)
    val_iter = utils.data.DataLoader(dataset=val_data, batch_size=args.batch_size, shuffle=False)
    test_data = utils.data.TensorDataset(x_test, y_test)
    test_iter = utils.data.DataLoader(dataset=test_data, batch_size=args.batch_size, shuffle=False)

    return n_vertex, zscore, train_iter, val_iter, test_iter, train_data, val_data, test_data