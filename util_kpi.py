

import pandas as pd
import numpy as np
from multiprocessing import Pool
from functools import partial
import re
import psutil

def safediv(x, y):
    if abs(y) > 0.000001:
        return x/y
    return 0


def replace_term(str_formula, term):

    # 정규 표현식 패턴 생성
    pattern = rf"(?<!\w){term}(?!\w)"
    # pattern = rf"(?<=\b)(?<!\['|\")({term})(?!\b|'\]|\")"

  # 정규 표현식 치환
    return re.sub(pattern, f"x['{term}']", str_formula)



def transform_formula(formula, list_terms):
    formula_for_eval = formula
    # print('\n [1] formula_for_eval:', formula_for_eval)
    for term in list_terms:
        # formula_for_eval = formula_for_eval.replace(term, f"x['{term}']")
        formula_for_eval = replace_term(formula_for_eval, term)
    # print('\n [2] formula_for_eval:', formula_for_eval)
    return formula_for_eval



# def generate_kpi_series(str_kpi_formula, df_data):
#     return df_data.apply(lambda x: eval(transform_formula(str_kpi_formula, x.index)), axis=1)

def extract_terms(input_str):
    return re.findall(r'[a-zA-Z0-9_]+', input_str)

def extract_unique_metric_terms_from_formula(input_str):
    list_terms =re.findall(r'[a-zA-Z0-9_]+', input_str)
    if 'safediv' in list_terms:
        list_terms.remove('safediv')
    list_terms = sorted(list(set(list_terms)))
    return list_terms


def generate_kpi_series(str_kpi_formula, df_data):

    list_terms = list(set(extract_terms(str_kpi_formula)))
    if 'safediv' in list_terms:
        list_terms.remove('safediv')
    # print('list_terms:', list_terms)
    
    return df_data.apply(lambda x: eval(transform_formula(str_kpi_formula, list_terms)), axis=1)

def generate_kpi_series_multiprocess(str_kpi_formula, df_data, n_process = None):
    if n_process is None:
        n_process = max(1, int(psutil.cpu_count()*0.9))
    else:
        n_process = min(n_process, int(psutil.cpu_count()*0.9))

    df_split = np.array_split(df_data, n_process)
    pool = Pool(n_process)
    partial_func = partial(generate_kpi_series, str_kpi_formula)
    df = pd.concat(pool.map(partial_func, df_split))
    pool.close()
    pool.join()

    return df
    

def generate_contribution_series(kpi_name, list_terms, df_data_and_kpi,):

    df_contribution = pd.DataFrame()

    for term in list_terms:
        df_contribution[term] = df_data_and_kpi[term]/df_data_and_kpi[kpi_name]
    
    return df_contribution


def generate_contribution_series_multiprocess(kpi_name, list_terms, df_data_and_kpi, n_process = None):
    if n_process is None:
        n_process = max(1, int(psutil.cpu_count()*0.9))
    else:
        n_process = min(n_process, int(psutil.cpu_count()*0.9))

    df_split = np.array_split(df_data_and_kpi, n_process)
    pool = Pool(n_process)
    partial_func = partial(generate_contribution_series, kpi_name, list_terms)
    df = pd.concat(pool.map(partial_func, df_split))
    pool.close()
    pool.join()

    return df


def cal_corr_btw_ts(ts_1, ts_2):
    return  np.corrcoef(ts_1, ts_2)

def get_highest_corr_ts(df, target_mertic, list_candidate_mertic, absolute=False, corr_method='pearson'):

    ds_corr = df[[target_mertic]+list_candidate_mertic].corr(method=corr_method)[target_mertic].drop(target_mertic, axis=0)
    if absolute:
        arg_max_index = ds_corr.abs().argmax()
    else:
        arg_max_index = ds_corr.argmax()

    return ds_corr.index[arg_max_index], ds_corr.iloc[arg_max_index]


def indentify_correlated_metric_term_with_kpi(df, kpi_name, dict_kpi_formula):
    list_metric_terms = extract_unique_metric_terms_from_formula(dict_kpi_formula[kpi_name]["formula"])
    metric_term, corr_coeff = get_highest_corr_ts(df[[kpi_name] + list_metric_terms], kpi_name, list_metric_terms, absolute=True)
    return metric_term, corr_coeff


def extract_degraded_samples(timeseries, th_percentile, degradation_direction='postive'):
    if degradation_direction == 'postive':
        degraded_samples = timeseries[timeseries >= np.percentile(timeseries, th_percentile)]
    elif degradation_direction == 'negative':
        degraded_samples = timeseries[timeseries <= np.percentile(timeseries, th_percentile)]
    else:
        print('Wrong degradation direction setting')
        return None

    return degraded_samples.index, degraded_samples.values