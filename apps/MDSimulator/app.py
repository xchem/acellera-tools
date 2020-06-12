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
import shutil
import sys
import numpy as np
from glob import glob
from tqdm import trange, tqdm
from htmd.units import convert
from htmd.projections.metric import Metric
from fragalysis.apps.mdsimulator.md_simulator import MDSimulator
from time import sleep

sys.setrecursionlimit(25000)
import matplotlib
matplotlib.use('Agg')

ACEMD_EXE = 'acemd3'
TIMESTEP = 4
SIMTYPE_ID = {'globular': 0, 'membrane': 1}
TOT_STEP = [3, 5]
CURR_STEP = [{'Equilibration': 1, 'Production': 2, 'Analysis': 3}, {'Equilibration_1': 1, 'Equilibration_2': 2, 'Equilibration_3': 3, 'Production': 4, 'Analysis': 5}]


def getArgParser():
    parser = argparse.ArgumentParser(description='Performs a simple run simulation: Equilibration and Production')

    requiredArgs = parser.add_argument_group('required args')

    requiredArgs.add_argument('-inputdir', dest='inputdir', action='store', type=str, help='Input build directory',
                              metavar='FILE',
                              required=True)
    requiredArgs.add_argument('-runtime', dest='runtime', type=int, required=True,
                              help='The simulation time (of each simulation) in ns', )
    parser.add_argument('-outdir', dest='outdir', action='store', type=str, help='Output directory for completed runs',
                        default='./outdir')
    parser.add_argument('-numruns', dest='numruns', action='store', type=int, help='Number of independent simulations',
                        default=1)
    parser.add_argument('-equiltime', dest='equiltime', action='store', type=str, default='auto',
                        help='The simulation time (of each simulation) in ns. Default value for globular systems 3ns, ' \
                             'for membrane systems 15ns')
    parser.add_argument('-ligresname', dest='ligresname', action='store', type=str, default='',
                        help='Ligand resname. It will be used to apply to that residue the constrain during '
                             'the equilibration phase if set to True and for the flat bottom potential in '
                             'membrane system')
    parser.add_argument('--use-gpu', dest='use_gpu', action='store_true',
                        help='Whether use GPU.')
    parser.add_argument('-constraints', dest='constraints', action='store', type=str, default='protein',
                        help='Atoms selection to apply a constrain.', choices=('protein', 'protein-ligand'))

    return parser

if __name__ == '__main__':
    parser = getArgParser()

    args, service = parser.parse_known_args()
    MDSimulator(args=vars(args)).run()
    #python app.py -inputdir test-data/build_system -runtime 2 -outdir myout -equiltime 2 --use-gpu -constraints protein
    #python app.py -inputdir test-data/build_ligprot -runtime 2 -outdir myprotlig -equiltime 2 -ligresname MOL --use-gpu -constraints protein-ligand
