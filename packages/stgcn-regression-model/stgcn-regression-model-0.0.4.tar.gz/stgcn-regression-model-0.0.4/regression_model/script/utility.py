import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import os
import torch
from regression_model.config.core import *


plt.style.use('ggplot')

def calc_gso(dir_adj, gso_type):
    n_vertex = dir_adj.shape[0]

    if sp.issparse(dir_adj) == False:
        dir_adj = sp.csc_matrix(dir_adj)
    elif dir_adj.format != 'csc':
        dir_adj = dir_adj.tocsc()

    id = sp.identity(n_vertex, format='csc') # identity matrix

    # Symmetrizing an adjacency matrix
    adj = dir_adj + dir_adj.T.multiply(dir_adj.T > dir_adj) - dir_adj.multiply(dir_adj.T > dir_adj)
    #adj = 0.5 * (dir_adj + dir_adj.transpose())
    
    if gso_type == 'sym_renorm_adj' or gso_type == 'rw_renorm_adj' \
        or gso_type == 'sym_renorm_lap' or gso_type == 'rw_renorm_lap':
        adj = adj + id
    
    if gso_type == 'sym_norm_adj' or gso_type == 'sym_renorm_adj' \
        or gso_type == 'sym_norm_lap' or gso_type == 'sym_renorm_lap':
        row_sum = adj.sum(axis=1).A1
        row_sum_inv_sqrt = np.power(row_sum, -0.5)
        row_sum_inv_sqrt[np.isinf(row_sum_inv_sqrt)] = 0.
        deg_inv_sqrt = sp.diags(row_sum_inv_sqrt, format='csc')
        # A_{sym} = D^{-0.5} * A * D^{-0.5}
        sym_norm_adj = deg_inv_sqrt.dot(adj).dot(deg_inv_sqrt)

        if gso_type == 'sym_norm_lap' or gso_type == 'sym_renorm_lap':
            sym_norm_lap = id - sym_norm_adj
            gso = sym_norm_lap
        else:
            gso = sym_norm_adj

    elif gso_type == 'rw_norm_adj' or gso_type == 'rw_renorm_adj' \
        or gso_type == 'rw_norm_lap' or gso_type == 'rw_renorm_lap':
        row_sum = np.sum(adj, axis=1).A1
        row_sum_inv = np.power(row_sum, -1)
        row_sum_inv[np.isinf(row_sum_inv)] = 0.
        deg_inv = np.diag(row_sum_inv)
        # A_{rw} = D^{-1} * A
        rw_norm_adj = deg_inv.dot(adj)

        if gso_type == 'rw_norm_lap' or gso_type == 'rw_renorm_lap':
            rw_norm_lap = id - rw_norm_adj
            gso = rw_norm_lap
        else:
            gso = rw_norm_adj

    else:
        raise ValueError(f'{gso_type} is not defined.')

    return gso

def calc_chebynet_gso(gso):
    if sp.issparse(gso) == False:
        gso = sp.csc_matrix(gso)
    elif gso.format != 'csc':
        gso = gso.tocsc()

    id = sp.identity(gso.shape[0], format='csc')
    eigval_max = max(eigsh(A=gso, k=6, which='LM', return_eigenvectors=False))

    # If the gso is symmetric or random walk normalized Laplacian,
    # then the maximum eigenvalue is smaller than or equals to 2.
    if eigval_max >= 2:
        gso = gso - id
    else:
        gso = 2 * gso / eigval_max - id

    return gso


def cnv_sparse_mat_to_coo_tensor(sp_mat, device):
    # convert a compressed sparse row (csr) or compressed sparse column (csc) matrix to a hybrid sparse coo tensor
    sp_coo_mat = sp_mat.tocoo()
    i = torch.from_numpy(np.vstack((sp_coo_mat.row, sp_coo_mat.col)))
    v = torch.from_numpy(sp_coo_mat.data)
    s = torch.Size(sp_coo_mat.shape)

    if sp_mat.dtype == np.float32 or sp_mat.dtype == np.float64:
        return torch.sparse_coo_tensor(indices=i, values=v, size=s, dtype=torch.float32, device=device, requires_grad=False)
    else:
        raise TypeError(f'ERROR: The dtype of {sp_mat} is {sp_mat.dtype}, not been applied in implemented models.')

def evaluate_model(model, loss, data_iter):
    model.eval()
    l_sum, n = 0.0, 0
    with torch.no_grad():
        for x, y in data_iter:
            y_pred = model(x).view(len(x), -1)
            l = loss(y_pred, y)
            l_sum += l.item() * y.shape[0]
            n += y.shape[0]
        mse = l_sum / n
    return mse

def evaluate_metric(model, data_iter, scaler):
    y_true = list()
    y_predictions = list()
    model.eval()
    with torch.no_grad():
        mae, sum_y, mape, mse = [], [], [], []
        r2 = []
        for x, y in data_iter:
            y_scaled = scaler.inverse_transform(y.cpu().numpy())
            y_pred_scaled = scaler.inverse_transform(model(x).view(len(x), -1).cpu().numpy())

            y_true.append(y_scaled)
            y_predictions.append(y_pred_scaled)

            y = y_scaled.reshape(-1)
            y_pred = y_pred_scaled.reshape(-1)
            d = np.abs(y - y_pred)
            mae += d.tolist()
            sum_y += y.tolist()
            mape += (d / y).tolist()
            mse += (d ** 2).tolist()
        MAE = np.array(mae).mean()
        MAPE = np.array(mape).mean()
        RMSE = np.sqrt(np.array(mse).mean())
        WAPE = np.sum(np.array(mae)) / np.sum(np.array(sum_y))
        std_mae = np.std(np.array(mae))
        std_rmse = np.std(np.sqrt((np.array(mse))))
        std_mape = np.std(np.array(mape))
        max_error = np.max(mae)
        # max_argmax = np.argmax(mae)

        #return MAE, MAPE, RMSE
        return MAE, RMSE, MAPE, WAPE,std_mae, std_rmse, std_mape, max_error, y_true, y_predictions

def load_data(model_path = 'best_model.pth', zscore_path = 'zscore.pt'):
    model = torch.load(os.path.join(TRAINED_MODEL_DIR, model_path))
    scaler = torch.load(os.path.join(TEST_DATA_DIR, zscore_path))
    return model, scaler

def make_prediction(model, scaler, one_pred_x):
    model.eval()
    with torch.no_grad():
        pred = model(one_pred_x).view(len(one_pred_x), -1).cpu().numpy()
        scaled_pred = scaler.inverse_transform(pred)
    return scaled_pred

def SaveBestModel(save_model_path, best_valid_loss, current_valid_loss, epoch, model, datetime):
    if epoch == 0:
        best_valid_loss = current_valid_loss

    if current_valid_loss < best_valid_loss:
        best_valid_loss = current_valid_loss
        print(f"\nBest validation loss: {best_valid_loss} at epoch {epoch}")
        torch.save(model, os.path.join(save_model_path,f'best_model_{datetime}.pth'))
        return best_valid_loss, epoch

    return best_valid_loss, None

def save_model(save_model_path, model, datetime):
    """
    Function to save the trained model to disk.
    """
    print(f"Saving final model...")
    torch.save(model, os.path.join(save_model_path,f'final_model_{datetime}.pth'))

def save_plots(plot_path, train_loss, valid_loss, datetime):
    """
    Function to save the loss and accuracy plots to disk.
    """ 
    # loss plots
    plt.figure(figsize=(10, 7))
    plt.plot(
        train_loss, color='orange', linestyle='-', 
        label='train loss'
    )
    plt.plot(
        valid_loss, color='red', linestyle='-', 
        label='validataion loss'
    )
    plt.xlabel('Epochs')
    plt.ylabel('Loss(MSE)')
    plt.legend()
    plt.savefig(os.path.join(plot_path, f'loss_{datetime}.png'))


