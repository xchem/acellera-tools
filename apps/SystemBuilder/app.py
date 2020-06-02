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

sys.setrecursionlimit(25000)
from htmd.tools.system_builder import SystemBuilder


def getArgParser():
    parser = argparse.ArgumentParser(description='Build a system for MD simulation with Amber forcefield.'
                                                 'The app can build globular system')

    requiredArgs = parser.add_argument_group('required args')

    requiredArgs.add_argument('-protein', dest='protein', action='store', type=str,
                        help='Input protein file (pdb)', default='')
    parser.add_argument('-ligand', dest='ligand', action='store', type=str,
                        help='Input ligand file (mol2)', default='')
    parser.add_argument('-ligprepi', dest='ligprepi', action='store', type=str,  nargs='+',
                        help='Amber ligand topology file (prepi)', default='')
    parser.add_argument('-ligfrcmod', dest='ligfrcmod', action='store', type=str, nargs='+',
                        help='Amber ligand parameters file (frcmod)', default='')
    parser.add_argument('-outdir', dest='outdir', action='store', type=str,
                        help='Output directory for completed builds. (default: ./build)', default='./build')
    parser.add_argument('-saltconc', dest='saltconc', action='store', type=float,
                        help='The salt concentration in molar (M). (default: 0)', default=0)
    parser.add_argument('-mindist', dest='mindist', action='store', type=float,
                        help='The minimum distance between the center and the edge of the box. The value will be applied'
                             'as minmax value for the solvation box.', default=0.0)

    return parser

if __name__ == '__main__':
    parser = getArgParser()

    args, service = parser.parse_known_args()
    SystemBuilder(args=vars(args)).run()


