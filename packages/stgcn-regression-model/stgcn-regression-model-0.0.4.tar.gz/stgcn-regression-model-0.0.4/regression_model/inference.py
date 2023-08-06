import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils as utils
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.sampler import RandomSampler

import os
import random
import numpy as np
import argparse
import matplotlib.pyplot as plt
from script import utility
import pickle
import matplotlib.lines as mlines
from pathlib import Path
import pandas as pd
from regression_model.config.core import *



def set_env(seed):
    # Set available CUDA devices
    # This option is crucial for an multi-GPU device
    os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1'
    # os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    # os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':16:8'
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    os.environ['PYTHONHASHSEED']=str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True)

def get_parameters():
    parser = argparse.ArgumentParser(description='STGCN')
    parser.add_argument('--enable_cuda', type=bool, default=True, help='enable CUDA, default as True')
    parser.add_argument('--seed', type=int, default=42, help='set the random seed for stabilizing experiment results')
    parser.add_argument('--dataset', type=str, default='link', choices=['metr-la', 'link'])
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--plot_stop', type=str, default='0_0_6')
    parser.add_argument('--error_route', type=str, default='6')
    args = parser.parse_args()
    # print('Test configs: {}'.format(args))

    # For stable experiment results
    set_env(args.seed)

    # Running in Nvidia GPU (CUDA) or CPU
    if args.enable_cuda and torch.cuda.is_available():
        # Set available CUDA devices
        # This option is crucial for multiple GPUs
        # 'cuda' ≡ 'cuda:0'
        device = torch.device('cpu')
        print('running on CPU')
    else:
        device = torch.device('cpu')
        print('running on CPU')
    
    return args, device

@torch.no_grad() 
def test(zscore, loss, model, test_iter):
    model.eval()
    test_MSE = utility.evaluate_model(model, loss, test_iter)
    test_MAE, test_RMSE, test_MAPE, test_WAPE,std_mae, std_rmse, std_mape, max_error, y_true, y_pred = utility.evaluate_metric(model, test_iter, zscore)
    print((f'Test loss(MSE) {test_MSE:.6f} | MAE {test_MAE:.6f} std {std_mae:.6f} | RMSE {test_RMSE:.6f} std {std_rmse:.6f} \
| ACC {100-100*test_MAPE:.8f} % | MAPE {100*test_MAPE:.8f} std {100*std_mape:.8f} %| WAPE {100*test_WAPE:.8f} %'))
    return y_true, y_pred

def plotting_index(y_true, y_preds, time_index, stop, stations, show_plot = True):
    with open(stations, 'rb') as f:
        stations = pickle.load(f)
    stop_num = stations.index(stop)

    y_sample = y_true[:, stop_num]
    y_pred_sample = y_preds[:, stop_num]

    with open(time_index, "rb") as f:
        index = pickle.load(f)
    index = index[-len(y_true)-1:-1]

    plt.figure(figsize=(17,10))
    plt.plot(index, y_sample, 'o',label='Ground Truth', color='green')
    plt.plot(index, y_sample,label='Ground Truth', color='green')
    plt.plot(index, y_pred_sample, 'o',label='Predictions', color='red')
    plt.plot(index, y_pred_sample, label='Predictions', color='red')
    plt.xlabel('time')
    plt.ylabel('Link_time(sec)')
    plt.legend(loc="upper left")
    plt.title(f'station: {stop}')
    if show_plot:
        plt.show()
    return index

def plotting(y_true, y_preds, stop, stations):
    with open(stations, 'rb') as f:
        stations = pickle.load(f)
    stop_num = stations.index(stop)

    y_sample = y_true[:, stop_num]
    y_pred_sample = y_preds[:, stop_num]

    plt.figure(figsize=(17,10))
    plt.plot(y_sample,label='Ground Truth', color='green')
    plt.plot(y_pred_sample, label='Predictions', color='red')
    plt.xlabel('time_step')
    plt.ylabel('Link_time(sec)')
    plt.legend(loc="upper left")
    plt.title(f'station: {stop}')
    plt.show()

def show_error(true, pred, time_index):

    with open(time_index, "rb") as f:
        idx = pickle.load(f)
    idx = idx[-len(true)-1:-1]

    with open(os.path.join(DATASET_DIR, 'link', 'stations'), 'rb') as f:
        stations = pickle.load(f)
    err = []
    error_route_list = ['6', '56', '133', '35']
    for error_route in error_route_list:
        path_list = ['0','1']
        if error_route == '35':
            path_list = ['0']
        MAE, ACC, RMSE, MAPE, max_error, max_row, max_col, max_error_true, max_error_pred = [], [], [], [], [], [], [], [], []
        for path in path_list:
            route = path+ '_' + error_route
            station_result = [i for i in stations if i.endswith(route)]
            col = [i for i,v in enumerate(stations) if v in station_result]
            y_true = true[:, col]
            y_pred = pred[:, col]
            d = np.abs(y_true-y_pred)
            mae = d.mean()
            mape = np.abs((y_true-y_pred)/y_true).mean()
            mse = d**2
            ind = np.unravel_index(np.argmax(d, axis=None), d.shape)
            max_row.append(idx[ind[0]])
            max_col.append(station_result[ind[1]])
            max_error.append(d[ind])
            max_error_true.append(y_true[ind])
            max_error_pred.append(y_pred[ind])
            MAE.append(mae)
            MAPE.append(mape*100)
            RMSE.append(np.sqrt(mse.mean()))
            ACC.append((1-mape)*100)

        err.append(pd.DataFrame([MAE, RMSE, MAPE, ACC, max_row, max_col, max_error, max_error_true, max_error_pred]))
    error = pd.concat(err,axis=1).T
    metrics = ['MAE', 'RMSE','MAPE', 'ACC', 'max_error_time', 'max_error_link', 'max_abs_error', 'max_error_true', 'max_error_pred']
    error.columns = metrics
    error.reset_index(inplace=True)
    error.rename(columns={'index':'path'}, inplace=True)
    error.index = np.repeat(error_route_list,2)[:-1]
    error.reset_index(inplace=True)
    error.rename(columns={'index':'route'}, inplace=True)
    error = error.sort_values('route').reset_index(drop=True)
    round_col = ['MAE', 'max_abs_error', 'RMSE', 'MAPE', 'ACC', 'max_error_pred']
    error[round_col] = error[round_col].astype(float).apply(lambda x: pd.Series.round(x,2))
    return error, stations

def confidence(true, pred, error_metric='rmse', test_plot=True):
    diff = np.abs(pred.T - true.T)
    error = np.abs(((true.T-pred.T)/true.T)).tolist()
    mae_nn = np.mean(np.array(diff))
    rmse_nn = np.sqrt((np.array(diff)**2).mean())
    mape_nn = np.mean(np.array(error))
    total_error_list = [mae_nn, rmse_nn, mape_nn*100, (1-mape_nn)*100]
    total_error = pd.DataFrame(total_error_list, columns=['total'])
    total_error.index = ['MAE','RMSE', 'MAPE', 'ACC']

    if error_metric =='mae':
        e_nn = np.mean(diff, axis=1) # per link
    else:
        e_nn = np.sqrt(np.mean((diff**2),axis=1)) # per link

    _, ax = plt.subplots()
    ax.violinplot(
        list(e_nn), showmeans=True, showmedians=False, showextrema=False, widths=1.0
    )

    ax.set_xlabel("Scaled distribution amplitude")
    ax.set_ylabel(f'{error_metric}')
    ax.set_title("Distribution over segments: NN pred")
    # plt.legend(handles=(line1, line2), title="Prediction Model", loc=2)
    plt.savefig(os.path.join(DATASET_DIR, 'link', 'inference_out', 'distributed_error_plot.png'))
    if test_plot == True:
        plt.show()
    return total_error
    


if __name__ == "__main__":
    args, device = get_parameters()

    # Input
    test_data = torch.load(os.path.join(TEST_DATA_DIR, 'test_data.pt'))
    test_iter = utils.data.DataLoader(dataset=test_data, batch_size=args.batch_size, shuffle=False)
    print("Test data shape:", test_iter.dataset.tensors[0].shape, test_iter.dataset.tensors[1].shape)


    # Output path
    true_path = Path(os.path.join(DATASET_DIR, 'link','true.npy'))
    pred_path = Path(os.path.join(DATASET_DIR, 'link','pred.npy'))


    # Prediction
    loss = nn.MSELoss()
    zscore = torch.load(os.path.join(TEST_DATA_DIR, 'zscore.pt'))
    model = torch.load(os.path.join(TRAINED_MODEL_DIR, config.model_config.test_model))
    y_true, y_pred = test(zscore, loss, model, test_iter)
    true = np.concatenate(y_true, axis=0)
    pred = np.concatenate(y_pred, axis=0)
    np.save(true_path, true)
    np.save(pred_path, pred)


    # Show errors per route
    null = pd.read_csv(os.path.join(DATASET_DIR, 'link','null.csv'))
    error, stations = show_error(true,pred, os.path.join(DATASET_DIR, 'link', 'time_index'))
    print(null)
    print(error)
    error.to_csv(os.path.join(DATASET_DIR, 'link', 'inference_out', 'error_metrics_path_lv.csv'), index=False)
    

    # plotting
    index=[]
    if config.model_config.test_plot == True:
        index = plotting_index(y_true=true, y_preds=pred, time_index=os.path.join(DATASET_DIR, 'link', 'time_index'), 
                                stop=args.plot_stop, stations=os.path.join(DATASET_DIR, 'link', 'stations'), show_plot=False)
    total_error = confidence(true, pred, error_metric='rmse', test_plot=config.model_config.test_plot)
    total_error.to_csv(os.path.join(DATASET_DIR, 'link', 'inference_out', 'total_error.csv'))
    print(total_error)
    if len(index)>0:
        prediction = pd.DataFrame(pred)
        prediction.index=index
        prediction.columns = stations
        prediction.to_csv(os.path.join(DATASET_DIR, 'link', 'inference_out', 'pred_result.csv'), index=True, header=True)