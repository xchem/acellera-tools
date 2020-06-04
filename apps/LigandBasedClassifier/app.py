"""
Copyright (C) 2020 Acellera Ltd. All Rights Reserved.

Academic License
HTMD Software Academic License Agreement v1.1

The HTMD software ("Software") has been developed by the contributing
researchers from Acellera and made available through Acellera for your
internal, non-profit research use.

Acellera allows researchers at your institution to run, display, copy and
modify Software on the following conditions:

1. The Software remains at your institution and is not published, distributed,
or otherwise transferred or made available to other than institution employees
and students involved in research under your supervision.

2. You agree to make results generated using Software available to other
academic researchers for non-profit research purposes. If you wish to obtain
Software for any commercial purposes, including fee-based service projects, you
will need to execute a separate licensing agreement with Acellera and pay a
fee. In that case please contact: info@acellera.com.

3. You retain in Software and any modifications to Software, the copyright,
trademark, or other notices pertaining to Software as provided by Acellera.

4. You provide Acellera with feedback on the use of the Software in your
research, and that Acellera are permitted to use any information you provide in
making changes to the Software. All bug reports and technical questions shall
be sent to the email address: info@acellera.com.

5. You acknowledge that Acellera and its licensees may develop modifications to
Software that may be substantially similar to your modifications of Software,
and that Acellera and its licensees shall not be constrained in any way by you
in Acellera's or its licensees' use or management of such modifications. You
acknowledge the right of  Acellera to prepare and publish modifications to
Software that may be substantially similar or functionally equivalent to your
modifications and improvements, and if you obtain patent protection for any
modification or improvement to Software you agree not to allege or enjoin
infringement of your patent by Acellera or by any of Acellera's licensees
obtaining modifications or improvements to Software from Acellera .

6. You agree to acknowledge the contribution Software make to your research,
and cite appropriate references about the Software in your publications.

7. Any risk associated with using the Software at your institution is with you
and your institution. Software is experimental in nature and is made available
as a research courtesy "AS IS," without obligation by Acellera to provide
accompanying services or support.

8. You consent to allow usage information of this software to be sent
to Acellera.

9. ACELLERA EXPRESSLY DISCLAIMS ANY AND ALL WARRANTIES REGARDING THE SOFTWARE,
WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES PERTAINING
TO NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
"""

import argparse
import os
import pandas as pd
import sys
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import average_precision_score
from rdkit import Chem
from rdkit.Chem import AllChem
from tqdm import tqdm
from sklearn.metrics import roc_curve, auc,recall_score,precision_score
from ax.service.managed_loop import optimize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.model_selection import StratifiedKFold
import logging
import pickle
import time
from moleculekit.tools.ligand_classifier.py import LigandBinderClassifier

def getArgParser():
    parser = argparse.ArgumentParser(description='Ligand-based binder/non-binder classifier based on XGBoost, '
                                                 'RDKit fingerprints and Ax-based '
                                                 'bayesian hyperparameter tuning.')

    parser.add_argument('csv', help='Input .csv for training/validation/prediction. Must include 2 '
                                      'comma-separated columns: smiles string and whether is binder (integer 1 '
                                      'for binder, integer 0 for non-binder)', type=argparse.FileType())

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--train', dest='train', action='store_true', help='Run training mode')
    group.add_argument('--validate', dest='validate', action='store_true', help='Run validation mode')
    group.add_argument('--predict', dest='predict', action='store_true', help='Run inference mode')
    parser.add_argument('--seed', dest='seed', action='store', default=0, type=int,
                        help='Random seed for XGBoost and Hyperparameter tuning')
    parser.add_argument('--model', dest='model', action='store', default=None, type=argparse.FileType(),
                        help='XGBoost model to use in prediction mode')
    parser.add_argument('--hp_trials', dest='hp_trials', action='store', default=100, type=int,
                        help='Number of hyperparameter (hp) search rounds (default: 100)')
    parser.add_argument('--optimization_metric', dest='optimization_metric', action='store', default='map', type=str,
                        help='Metric to be optimized by HP tuning: \'map\' (mean average precision), \'auc\' (area under the curve), \'aucpr\' '
                             '(area under precision-recall curve) or any other metric supported by XGBoost (see eval_metric in '
                             'https://xgboost.readthedocs.io/en/latest/parameter.html)(default: \'map\')')
    return parser

if __name__ == '__main__':
    parser = getArgParser()
    args, service = parser.parse_known_args()
    LigandBinderClassifier(args=vars(args)).run()
