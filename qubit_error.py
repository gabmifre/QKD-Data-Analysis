# -*- coding: utf-8 -*-
"""
"""

import h5py
import hist_helper as hp

"""
Returns list of errors for early and late time-bin qubits.
Error is calculated as:
    qubit error = (# entries in other bin) / (# entries in both bins)
"""
def allQubitErrorRate(file: h5py.File, print_mode: int=0, hist_num: int=0):
    a = file.attrs
    qubit_seq = a['qubit_seq'].decode('UTF-8')
    
    early_start = early_end = late_start = late_end = 0
    early_counts = late_counts = 0
    error = 0
    errors = []
    last_idx_early = last_idx_late = 0
    
    for i in range(len(qubit_seq)):
        error = '-'
        
        qubit = qubit_seq[i]
        if qubit == 'P':
            pass
        elif qubit == '0':
            pass
        else:
            early_start = (i * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num])
            early_end = (i * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_integration_windows'][hist_num])
            late_start = (i * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_phases'][hist_num])
            late_end = (i * a['qkd_param_qubit_times'][hist_num] + a['qkd_param_offsets'][hist_num] + a['qkd_param_integration_windows'][hist_num] + a['qkd_param_phases'][hist_num])
            
            (early_counts, last_idx_early) = hp.integrateHistCounts(file['hists']['time'], early_start, early_end, last_idx_early)
            (late_counts, last_idx_late) = hp.integrateHistCounts(file['hists']['time'], late_start, late_end, last_idx_late)
            
            if qubit == 'E':
                error = late_counts / (early_counts + late_counts)
                errors.append(error)
            elif qubit == 'L':
                error = early_counts / (early_counts + late_counts)
                errors.append(error)
            else:
                print('WARNING: unknown qubit found in sequence')

        if print_mode == 2:
            print('Qubit #' + str(i+1) + ': ' + qubit + '\n\t err: ' + str(error))
    if print_mode == 1:
        print('Qubit errors: ', str(errors))

    return errors