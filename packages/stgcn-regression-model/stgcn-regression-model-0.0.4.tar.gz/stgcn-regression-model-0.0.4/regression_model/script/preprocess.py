import pandas as pd
import numpy as np
import math

def prep_data(data_path, freq = '30min'):
        for path in ['go','back']:
                data = pd.read_csv(data_path).drop(['gps_imei'],axis=1).reset_index(drop=True)
                data = data[(data['path'] == path)]

                link_name_list = data.link_name.tolist()
                line_direction_link_order = []
                for i in range(len(link_name_list)):
                        if len(link_name_list[i]) <= 6 and len(link_name_list[i]) >= 5:
                                line_direction_link_order.append(link_name_list[i][0:2])
                        if len(link_name_list[i]) <= 4:
                                line_direction_link_order.append(link_name_list[i][0:1])
                        if len(link_name_list[i]) >= 7:
                                line_direction_link_order.append(link_name_list[i][0:3])
                data['LineDirectionLinkOrder'] = line_direction_link_order
                data['LineDirectionLinkOrder'] = data['LineDirectionLinkOrder'].astype(int)
        
                data.columns = ['LinkName', 'LinkTravelTime', 'DateTime', 'LineDirectionCode', 'routes', 'LineDirectionLinkOrder']

                # data = data[(0 <= data['LineDirectionLinkOrder']) & (data['LineDirectionLinkOrder'] < limit_stop)]
                # assert len(data['LinkName'].unique()) == limit_stop

                # filter time
                data['DateTime'] = pd.to_datetime(data['DateTime'])
                data['Time_hms'] = data['DateTime'].dt.strftime("%H:%M:%S")
                data = data[data['Time_hms']>= '06:00:00']
                data = data[data['Time_hms']<= '19:00:00']
                data = data.drop('Time_hms', axis=1)

                data.sort_values('DateTime', inplace = True)
                ix = pd.DatetimeIndex(pd.to_datetime(data['DateTime'])).floor(freq)
                data['DateTimeReference'] = pd.to_datetime(ix)
                if path == 'go':
                        all_df = data
                else:
                        all_df = pd.concat([all_df,data],axis=0)

        
        all_df.replace(['go','back'], [0,1], inplace=True)

        cols = ['LineDirectionLinkOrder', 'LineDirectionCode', 'routes']
        all_df['LinkRef'] = all_df[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

        return all_df.reset_index(drop=True)


def fit_scale(data, freq = '30min', smooth = 1, masking=True):
    means = { }
    scales = { }
    low = { }
    upr = { }
    for k, v in data.sort_values(['routes', 'LineDirectionCode', 'LineDirectionLinkOrder']).groupby('LinkRef', sort = False):
        v_nonan = v[~np.isnan(v['LinkTravelTime'])]

        low[k] = v['LinkTravelTime'].quantile(0.1)
        upr[k] = v['LinkTravelTime'].quantile(0.9)

        ix_ref = pd.DatetimeIndex(pd.to_datetime(v['DateTimeReference']))
        v_ = v.set_index(ix_ref)
        # print(v_[v_.LinkRef=='1_2'].sort_values('DateTime'))

        mean = v_[(low[k] <= v_['LinkTravelTime']) & (v_['LinkTravelTime'] <= upr[k])]['LinkTravelTime'].resample(freq).mean()
        mean = mean.interpolate().rolling(window = smooth, center = True).mean() # linear interpolation
        means[k] = mean 
        #scales[k] = v_[(low[k] < v_['LinkTravelTime']) & (v_['LinkTravelTime'] < upr[k])]['LinkTravelTime'].std()
        scales[k] = 1

    # means_df = pd.DataFrame(data = means)
    means_df = pd.DataFrame(data = means).fillna(method='pad').fillna(method='bfill')

    # Masking
    if masking==True:
        means_df = means_df[means_df.index.hour>=6]
        means_df = means_df[means_df.index.hour<=19]
    means_df = means_df[means_df.columns.drop(list(means_df.filter(regex='_1_35')))]
    return (means_df, scales, low, upr, ix_ref)


def fit_scale_no_inter(data, freq = '30min', fillna=False, masking=True):
    means = { }
    scales = { }
    low = { }
    upr = { }
    for k, v in data.sort_values(['routes', 'LineDirectionCode', 'LineDirectionLinkOrder']).groupby('LinkRef', sort = False):
        v_nonan = v[~np.isnan(v['LinkTravelTime'])]

        low[k] = v['LinkTravelTime'].quantile(0.1)
        upr[k] = v['LinkTravelTime'].quantile(0.9)

        ix_ref = pd.DatetimeIndex(pd.to_datetime(v['DateTimeReference']))
        v_ = v.set_index(ix_ref)
        # print(v_[v_.LinkRef=='1_2'].sort_values('DateTime'))

        mean = v_[(low[k] <= v_['LinkTravelTime']) & (v_['LinkTravelTime'] <= upr[k])]['LinkTravelTime'].resample(freq).mean()
        # mean = mean.interpolate().rolling(window = smooth, center = True).mean() # linear interpolation
        means[k] = mean
        scales[k] = 1

    if fillna==False:
        means_df = pd.DataFrame(data = means)
    else:
        means_df = pd.DataFrame(data = means).fillna(method='pad').fillna(method='bfill')

    # Masking
    if masking==True:
        means_df = means_df[means_df.index.hour>=6]
        means_df = means_df[means_df.index.hour<=19]
    means_df = means_df[means_df.columns.drop(list(means_df.filter(regex='_1_35')))]
    return (means_df, scales, low, upr, ix_ref)

def adj_prep(means):
    adj = []
    all_stop_num = means.columns
    for i in range(len(all_stop_num)-1):
        tmp = np.zeros(len(all_stop_num))
        info_current = all_stop_num[i].split('_')
        info_next = all_stop_num[i+1].split('_')
        if i > 0:
            info_prev = all_stop_num[i-1].split('_')

        tmp[i] = 1
        if info_current[1] == info_next[1] and info_current[2] == info_next[2]:
            tmp[i+1] = 1
            if i > 0:
                tmp[i-1] = 1
        if info_current[1] == info_next[1] and info_current[2] != info_next[2]:
            tmp[i+1] = 0
            if i > 0:
                tmp[i-1] = 1
        if info_current[1] != info_next[1] and info_current[2] == info_next[2]:
            tmp[i+1] = 0
            if i > 0:
                tmp[i-1] = 1
        if i > 0:
            if info_prev[1] != info_current[1] or info_prev[2] != info_current[2]:
                tmp[i-1]=0

        adj.append(tmp)

        if i == len(all_stop_num)-2:
            tmp = np.zeros(len(all_stop_num))
            tmp[i+1] = 1
            adj.append(tmp)
    adj = pd.DataFrame(adj, columns = means.columns)
    return adj

def null_values(means, means_no_inter, p=0):
    null_col = means_no_inter.isnull().sum().sort_values(ascending=False)
    val = math.floor(means_no_inter.shape[0]*(p/100))
    null_len = len(null_col[null_col>val])
    # print(f'Number of stations with null that has null values more than {p}% or {val} rows: {null_len} rows or {math.floor(null_len*100/len(null_col))}%')
    
    null = pd.DataFrame(null_col).reset_index()
    null.rename(columns={0:'num_null'},inplace=True)
    null[['station_num','path','route']] = null['index'].str.split('_',2,expand=True)
    null = null.drop('index', axis=1)
    large_null = null[null.num_null > val]
    group_large_null = large_null.groupby(['route','path']).sum()

    num_cells=[]
    for route in ['6', '56', '133', '35']:
        path_list = ['0','1']
        if route == '35':
            path_list = ['0']
        for path in path_list:
            route_num = path + '_' + route
            col = [i for i in means.columns.tolist() if i.endswith(route_num)]
            # print(col)
            num_cells.append(len(col)*len(means))
    num_cells = pd.DataFrame(num_cells, columns=['num_cells'])
    num_cells['route'] = np.repeat(['6', '56', '133', '35'],2)[:-1]
    num_cells['path'] = np.array(['0','1','0','1','0','1','0'])
    g = group_large_null.reset_index()
    g = g.sort_values('route').reset_index(drop=True)
    g['total_cells'] = num_cells.sort_values('route').reset_index(drop=True)['num_cells']
    g['percent'] = g['num_null']*100/g['total_cells']
    g['percent'] = g['percent'].round(decimals=2)
    return g