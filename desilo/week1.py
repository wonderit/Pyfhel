"""
Client/Server demo with Pyfhel
========================================

Context Parameters shows how several parameters affect performance.
"""
import numpy as np
import time
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from pathlib import Path
import os

# Using a temporary dir as a "secure channel"
# This can be changed into real communication using other python libraries.
# secure_channel = tempfile.TemporaryDirectory()

sec_con = Path(os.getcwd()) / 'tmp'

if not os.path.isdir(sec_con):
    os.mkdir(sec_con)
pk_file = sec_con / "mypk.pk"
contx_file = sec_con / "mycontx.con"
print(pk_file, contx_file)

def encrypted_evaluation(enc_data):
    enc_result = 0
    count = len(enc_data)
    for enc_x in enc_data:
        if enc_result == 0:
            enc_result = enc_x
        else:
            enc_result = enc_result + enc_x
    enc_result = enc_result / count
    return enc_result

# experiment start

import pandas as pd

experiment = [
    {
        'n_count': 1000,
        'enc_avg': 0,
        'enc_time': 0,
        'enc_avg_time': 0,
        'avg': 0
    },

    {
        'n_count': 10000,
        'enc_avg': 0,
        'avg': 0
    },

    {
        'n_count': 100000,
        'enc_avg': 0,
        'avg': 0
    }
]

for i, exp in enumerate(experiment):
    print(f"Start {i + 1}th Experiment !!")

    # data from data provider :
    plain_vector = np.random.randint(10, 80, size=exp['n_count']).tolist()

    # Create Context
    HE = Pyfhel()
    HE.contextGen(p=1964769281, m=8192, base=2, sec=192, flagBatching=True)
    HE.keyGen()
    HE.rotateKeyGen(60)
    HE.relinKeyGen(60, 4)

    # encrypt data
    t_start = time.time()
    enc_vec = [HE.encryptFrac(x) for x in plain_vector]
    t_end = time.time()

    experiment[i]['enc_time'] = t_end - t_start
    print(f"Encrypting data took {(t_end - t_start):.4f} seconds")

    # encrypted evaluation
    t_start = time.time()
    encrypted_average = encrypted_evaluation(enc_vec)
    avg_result = HE.decryptFrac(encrypted_average)
    t_end = time.time()

    experiment[i]['enc_avg'] = avg_result
    experiment[i]['avg'] = np.average(plain_vector)

    experiment[i]['enc_avg_time'] = t_end - t_start
    print(f"Encryption average took {(t_end - t_start):.4f} seconds")


exp_df = pd.DataFrame(experiment)
print(exp_df)