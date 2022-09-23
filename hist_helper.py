# -*- coding: utf-8 -*-
"""
Functions for plotting histograms and integrating data.
"""

import h5py
import matplotlib.pyplot as plt

"""
Plots a histogram given an h5py File and an int for that histogram (see code
                                                                    for correspondence).
Optional lines argument will plot vertical lines like in the GUI using
    metadata attributes.
NOTE: I believe the lines are only accurate for the time histogram, as I think
    they are produced differently for the phase histograms in the GUI.
"""
def plotHist(f: h5py.File, hist_num: int, lines: bool=False):
    data = f['hists']
    if hist_num == 0:
        data=data['time']
    elif hist_num == 1:
        data=data['phase_ok']
    else:
        data=data['phase_bad']

    plt.figure()
    plt.plot(data[0], data[1])
    plt.xlabel('time')
    plt.ylabel('counts')
    plt.title('hist #' + str(hist_num))

    if lines:
        a = f.attrs
        for i in range(2 * int(a['qkd_param_num_qubits'][hist_num])):
            if ((i+1) % 2):
                plt.axvline(x=(i/2 * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num]), color='g', ls='--', lw=1)
                plt.axvline(x=(i/2 * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_phases'][hist_num]), color='r', ls='--', lw=1)
            else:
                plt.axvline(x=((i-1)/2 * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_integration_windows'][hist_num]), color='g', ls='--', lw=1)
                plt.axvline(x=((i-1)/2 * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_integration_windows'][hist_num] + a['qkd_param_phases'][hist_num]), color='r', ls='--', lw=1)

    plt.show()

"""
Given an h5py Dataset with only two rows, plots that dataset.
"""
def plotHistOnly(data: h5py.Dataset):
    plt.figure()
    plt.plot(data[0], data[1])
    plt.xlabel('time (ps)')
    plt.ylabel('counts')
    plt.title('histogram')
    plt.show()
    
"""
Sums all counts in a histogram dataset that have a time value between
    'start' and 'end'.
The 'offset' tells us to start looking at indices beginning at that offset,
    and we return the index of the last valid datapoint as the next offset.
    This assumes all points are added sequentially.
Start must be less than or equal to end.
Returns a tuple of (total counts in the range, last valid index for offset).
"""
def integrateHistCounts(data: h5py.Dataset, start: float=0, end: float=0, offset: float=0):
    num_points = data.shape[1]
        
    curr_x = 0
    tot = 0
    last_i = 0
    for i in range(offset, num_points):
        curr_x = data[0][i]
        if curr_x >= start and curr_x <= end:
            tot += data[1][i]
            last_i = i
    return (tot, last_i)