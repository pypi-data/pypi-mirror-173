import torch
from regression_model.config.core import *
from regression_model.script import utility


@torch.no_grad() 
def make_pred(zscore, test_model, test_iter):
    test_model.eval()
    test_MAE, test_RMSE, test_MAPE, test_WAPE,std_mae, std_rmse, std_mape, max_error, y_true, y_pred = utility.evaluate_metric(test_model, test_iter, zscore)
    print((f'Dataset Link | MAE {test_MAE:.6f} std {std_mae:.6f} | RMSE {test_RMSE:.6f} std {std_rmse:.6f} \
| ACC {100-100*test_MAPE:.8f} % | MAPE {100*test_MAPE:.8f} std {100*std_mape:.8f} %| WAPE {100*test_WAPE:.8f} %'))
    return y_true, y_pred


def test_pred(sample_input_data):
    test_iter, zscore, model = sample_input_data    
    assert test_iter.dataset.tensors[1].shape[1] == 491

    y_true, y_pred = make_pred(zscore, model, test_iter)
    assert len(y_true) == len(y_pred)