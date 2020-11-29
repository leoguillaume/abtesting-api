import numpy as np
from scipy.stats import norm, chi2, ttest_ind, mannwhitneyu

def utils(n_control: int, n_test: int, c_control: int, c_test: int):
    p_control = c_control / n_control
    p_test = c_test / n_test
    variation = (c_test - c_control) / c_control
    return p_control, p_test, variation

def ztest(n_control: int, n_test: int, c_control: int, c_test: int):

    p_control, p_test, variation = utils(n_control, n_test, c_control, c_test)
    var_control = (p_control * (1 - p_control)) / n_control
    var_test = (p_test * (1 - p_test)) / n_test
    score = (p_test - p_control) / np.sqrt(var_test + var_control)
    pvalue = norm.sf(np.absolute(score))
    return p_control, p_test, variation, score, pvalue

def chi2test(n_control: int, n_test: int, c_control: int, c_test: int):

    p_control, p_test, variation = utils(n_control, n_test, c_control, c_test)
    p = (c_control + c_test) / (n_control + n_test)
    O = np.array([n_control - c_control, n_test - c_test, c_control, c_test])
    T = np.array([n_control - (n_control * p), n_test - (n_test * p), n_control * p, n_test * p])
    score = np.sum(np.square(T-O)/T)
    pvalue = chi2.sf(np.absolute(score), df = 1)
    return p_control, p_test, variation, score, pvalue

def MWUtest(n_control: int, n_test: int, c_control: int, c_test: int):

    p_control, p_test, variation = utils(n_control, n_test, c_control, c_test)
    d_control = np.zeros(n_control)
    d_control[:c_control] = 1
    d_test = np.zeros(n_test)
    d_test[:c_test] = 1
    score, pvalue = mannwhitneyu(d_control, d_test)
    return p_control, p_test, variation, score, pvalue

def ttest(n_control: int, n_test: int, c_control: int, c_test: int):
    p_control, p_test, variation = utils(n_control, n_test, c_control, c_test)
    d_control = np.zeros(n_control)
    d_control[:c_control] = 1
    d_test = np.zeros(n_test)
    d_test[:c_test] = 1
    score, pvalue = ttest_ind(d_control, d_test)
    return p_control, p_test, variation, score, pvalue
