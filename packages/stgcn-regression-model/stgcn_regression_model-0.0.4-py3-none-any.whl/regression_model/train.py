import logging
import os
import argparse
import random
import tqdm
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim

from regression_model.script import dataloader, utility, earlystopping
from regression_model.model import models
from datetime import datetime
import matplotlib.pyplot as plt
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
    parser.add_argument('--dataset', type=str, default='link', choices=['metr-la', 'pems-bay', 'pemsd7-m', 'link'])
    parser.add_argument('--n_pred', type=int, default=1, help='the number of time interval for predcition, default as 1')
    parser.add_argument('--Kt', type=int, default=3, help='Kernel size of temporal block (casual convolution) = (Kt,1)')
    parser.add_argument('--stblock_num', type=int, default=2)
    parser.add_argument('--act_func', type=str, default='glu', choices=['glu', 'gtu'])
    parser.add_argument('--Ks', type=int, default=3, choices=[3, 2], help='Kernel size of Spatial block')
    parser.add_argument('--graph_conv_type', type=str, default='cheb_graph_conv', choices=['cheb_graph_conv', 'graph_conv'])
    parser.add_argument('--gso_type', type=str, default='sym_norm_lap', choices=['sym_norm_lap', 'rw_norm_lap', 'sym_renorm_adj', 'rw_renorm_adj'])
    parser.add_argument('--enable_bias', type=bool, default=True, help='default as True')
    parser.add_argument('--droprate', type=float, default=0.5)
    parser.add_argument('--lr', type=float, default=0.001, help='learning rate')
    parser.add_argument('--weight_decay_rate', type=float, default=0.0005, help='weight decay (L2 penalty)')
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--opt', type=str, default='adam', help='optimizer, default as adam')
    parser.add_argument('--step_size', type=int, default=10, help='period of learning rate decay')
    parser.add_argument('--gamma', type=float, default=0.95)
    parser.add_argument('--patience', type=int, default=30, help='early stopping patience')
    args = parser.parse_args()
    print('Training configs: {}'.format(args))
    logger.info('Training configs: {}'.format(args))

    # For stable experiment results
    set_env(args.seed)

    # Running in Nvidia GPU (CUDA) or CPU
    if args.enable_cuda and torch.cuda.is_available():
        # Set available CUDA devices
        # This option is crucial for multiple GPUs
        # 'cuda' ≡ 'cuda:0'
        device = torch.device('cuda')
        print('running on GPU')
    else:
        device = torch.device('cpu')
        print('running on CPU')
        
    # output layers
    Ko = config.model_config.n_his - (args.Kt - 1) * 2 * args.stblock_num

    # blocks: settings of channel size in st_conv_blocks and output layer,
    # using the bottleneck design in st_conv_blocks
    blocks = []
    blocks.append([1])
    for l in range(args.stblock_num):
        blocks.append([64, 16, 64])
    if Ko == 0:
        blocks.append([128])
    elif Ko > 0:
        blocks.append([128, 128])
    blocks.append([1])
    
    return args, device, blocks

def prepare_model(args, blocks, n_vertex):
    loss = nn.MSELoss()
    es = earlystopping.EarlyStopping(mode='min', min_delta=0.0, patience=args.patience)

    if args.graph_conv_type == 'cheb_graph_conv':
        model = models.STGCNChebGraphConv(args, blocks, n_vertex).to(device)
    else:
        model = models.STGCNGraphConv(args, blocks, n_vertex).to(device)

    if args.opt == "rmsprop":
        optimizer = optim.RMSprop(model.parameters(), lr=args.lr, weight_decay=args.weight_decay_rate)
    elif args.opt == "adam":
        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay_rate, amsgrad=False)
    elif args.opt == "adamw":
        optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay_rate, amsgrad=False)
    else:
        raise NotImplementedError(f'ERROR: The optimizer {args.opt} is not implemented.')

    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=args.step_size, gamma=args.gamma)

    return loss, es, model, optimizer, scheduler


def train(loss, optimizer, scheduler, es, model, train_iter, val_iter, datetime, epochs, save_final=True, save_plot=True):
    best_valid_loss = None
    train_losses, val_losses = [], []
    for epoch in range(epochs):
        l_sum, n = 0.0, 0  # 'l_sum' is epoch sum loss, 'n' is epoch instance number
        model.train()
        for x, y in tqdm.tqdm(train_iter):
            y_pred = model(x).view(len(x), -1)  # [batch_size, num_nodes]
            l = loss(y_pred, y)
            optimizer.zero_grad()
            l.backward()
            optimizer.step()
            scheduler.step()
            l_sum += l.item() * y.shape[0]
            n += y.shape[0]

        train_losses.append(l_sum/n)

        val_loss = val(model, val_iter)
        val_losses.append(val_loss)

        # Save best model
        best_valid_loss, best_epoch = utility.SaveBestModel(save_model_path = TRAINED_MODEL_DIR, 
                                        best_valid_loss = best_valid_loss,current_valid_loss = val_loss, 
                                        epoch=epoch, model=model, datetime=datetime)
        if best_epoch != None:
            logger.info(f"Best validation loss: {best_valid_loss} at epoch {best_epoch}")
        # GPU memory usage
        gpu_mem_alloc = torch.cuda.max_memory_allocated() / 1000000 if torch.cuda.is_available() else 0
        t = torch.cuda.get_device_properties(0).total_memory
        r = torch.cuda.memory_reserved(0)
        a = torch.cuda.memory_allocated(0)
        f = r-a  # free inside reserved
        print('Epoch: {:03d} | Lr: {:.20f} |Train loss: {:.6f} | Val loss: {:.6f} | GPU occupy: {:.6f} MiB'.\
            format(epoch+1, optimizer.param_groups[0]['lr'], l_sum / n, val_loss, gpu_mem_alloc))
        print(f"t:{t/1000000}, r:{r/1000000}, a:{a/1000000}, f:{f/1000000}")
        if es.step(val_loss):
            print('Early stopping.')
            logger.info(f'Early stopping at epoch {epoch}')
            break
    if save_final == True:
        utility.save_model(TRAINED_MODEL_DIR, model, datetime=datetime)
    if save_plot == True:
        utility.save_plots(PLOT_DIR, train_losses, val_losses, datetime)
    
    last_epoch = epoch+1
    logger.info(f'Last epoch: {last_epoch}')
    return model

@torch.no_grad()
def val(model, val_iter):
    model.eval()
    l_sum, n = 0.0, 0
    for x, y in val_iter:
        y_pred = model(x).view(len(x), -1)
        l = loss(y_pred, y)
        l_sum += l.item() * y.shape[0]
        n += y.shape[0]
    return torch.tensor(l_sum / n)

@torch.no_grad() 
def test(zscore, loss, model, test_iter, args):
    model.eval()
    test_MSE = utility.evaluate_model(model, loss, test_iter)
    test_MAE, test_RMSE, test_MAPE, test_WAPE,std_mae, std_rmse, std_mape, max_error, y_true, y_pred = utility.evaluate_metric(model, test_iter, zscore)
    logger.info(f'Dataset {args.dataset:s} | Test loss(MSE) {test_MSE:.6f} | MAE {test_MAE:.6f} std {std_mae:.6f} | RMSE {test_RMSE:.6f} std {std_rmse:.6f} \
| ACC {100-100*test_MAPE:.8f} % | MAPE {100*test_MAPE:.8f} std {100*std_mape:.8f} %| WAPE {100*test_WAPE:.8f} % | MAX_ERROR {max_error:.8f}\n')
    print((f'Dataset {args.dataset:s} | Test loss(MSE) {test_MSE:.6f} | MAE {test_MAE:.6f} std {std_mae:.6f} | RMSE {test_RMSE:.6f} std {std_rmse:.6f} \
| ACC {100-100*test_MAPE:.8f} % | MAPE {100*test_MAPE:.8f} std {100*std_mape:.8f} %| WAPE {100*test_WAPE:.8f} % | MAX_ERROR {max_error:.8f}'))
    return y_true, y_pred

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    y_true +=  1e-18 #add small values to true velocities to avoid division by zeros
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def plotting(y_true, y_preds, stop_num=0):
    y_sample = y_true[:, stop_num]
    y_pred_sample = y_preds[:, stop_num]

    plt.figure(figsize=(17,10))
    plt.plot(y_sample, label='Ground Truth')
    plt.plot(y_pred_sample, label='Predictions')
    plt.xlabel('time_step')
    plt.ylabel('Link_time(sec)')
    plt.legend(loc="upper left")
    plt.show()



if __name__ == "__main__":
    # Logging
    logger = logging.getLogger('STGCN_TRAIN')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_handler = logging.FileHandler('stgcn.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    args, device, blocks = get_parameters()


    # dataset
    data_path = DATASET_DIR
    n_vertex, zscore, train_iter, val_iter, test_iter, train_data, val_data, test_data = dataloader.data_preparate(args, device, data_path)
    print('Train shape:', train_iter.dataset.tensors[0].shape, train_iter.dataset.tensors[1].shape)
    print("Validation shape:", val_iter.dataset.tensors[0].shape, val_iter.dataset.tensors[1].shape)
    print("Test shape:", test_iter.dataset.tensors[0].shape, test_iter.dataset.tensors[1].shape)
    logger.info(f'Train shape: {train_iter.dataset.tensors[0].shape}, {train_iter.dataset.tensors[1].shape}')
    logger.info(f"Validation shape: {val_iter.dataset.tensors[0].shape}, {val_iter.dataset.tensors[1].shape}")
    logger.info(f"Test shape: {test_iter.dataset.tensors[0].shape}, {test_iter.dataset.tensors[1].shape}")
    torch.save(test_data, os.path.join(TEST_DATA_DIR,'test_data.pt')) # save data
    torch.save(zscore, os.path.join(TEST_DATA_DIR,'zscore.pt')) # save zscore


    # prep model & train
    loss, es, model, optimizer, scheduler = prepare_model(args, blocks, n_vertex)
    datetime = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
    model = train(loss, optimizer, scheduler, es, model, train_iter, val_iter, datetime, config.model_config.epochs)


    # Test
    if config.model_config.epochs > 1:
        model_path = os.path.join(TRAINED_MODEL_DIR,f"best_model_{datetime}.pth")
    else:
        model_path = os.path.join(TRAINED_MODEL_DIR,f"final_model_{datetime}.pth")
    model = torch.load(model_path)
    y_true, y_pred = test(zscore, loss, model, test_iter, args)

    print(y_true[0].shape)
    true = np.concatenate(y_true, axis=0)
    pred = np.concatenate(y_pred, axis=0)
    print("concat pred shape:", pred.shape)
    print("concat true shape:", true.shape)
    print('Training shape:', train_iter.dataset.tensors[0].shape, train_iter.dataset.tensors[1].shape)
    print("Testing shape:", test_iter.dataset.tensors[0].shape, test_iter.dataset.tensors[1].shape)
    if config.model_config.train_plot == True:
        plotting(y_true=true, y_preds=pred, stop_num=config.model_config.plot_stop_num)


