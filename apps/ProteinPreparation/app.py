#!/usr/bin/env python3
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
import pickle
import re
from moleculekit.molecule import Molecule
from moleculekit.tools.preparation import proteinPrepare

sys.setrecursionlimit(25000)

class ProteinPreparator:
    def __init__(self, args):

        for arg, value in args.items():
            if value == '':
                args[arg] = None

        self.vars = argparse.Namespace(**args)
        self.vars.pH = float(self.vars.pH)
        self.vars.chain = "all" if not self.vars.chain else self.vars.chain


    def _loadPDB(self, pdb):
        m = Molecule(pdb)
        if self.vars.remove_water:
            if not self.vars.include_heteroatoms:
                prot_sel = "protein"
                if self.vars.chain != "all":
                    prot_sel = "protein and chain " + self.vars.chain
            else:
                prot_sel = "protein or not water"
                if self.vars.chain != "all":
                    prot_sel = "(protein or not water) and chain " + self.vars.chain
        else:
            if not self.vars.include_heteroatoms:
                prot_sel = "protein or water"
                if self.vars.chain != "all":
                    prot_sel = "(protein or water) and chain " + self.vars.chain
            else:
                prot_sel = "protein or water or not water"
                if self.vars.chain != "all":
                    prot_sel = "(protein or water or not water) and chain " + self.vars.chain
        m.filter(prot_sel)
        return m

    def _runFirstProteinPrepare(self):
        protprep, prepdetails = proteinPrepare(self.mol, pH=self.vars.pH, returnDetails=True)

        # return details
        prepdetails.data.to_csv( "details.csv")

        heteroatoms = []
        if self.vars.include_heteroatoms:
            heteroatoms = list(np.unique(protprep.get("resname", "not protein and not water")))

        # produce svg diagram
        svg_plot = prepdetails._get_pka_plot(pH=self.vars.pH, font_size=8)
        with open('protonation_diagram.svg', 'w') as f:
            f.write(svg_plot)

        # generate ans object
        ans = {
            'svg_plot': svg_plot,
            'csv': 'details.csv',
            'protein': 'output.pdb',
            'prepData': prepdetails,
            'pH': self.vars.pH,
            'heteroatoms': heteroatoms
        }
        pickle.dump(ans, open("job_content.pickle", "wb"))

        # write result
        protprep.write("output.pdb")


    def checkCaps(self, protein):
        from numpy import sum as _sum
        aceAnameCorrect = np.array(['C', 'O', 'CH3'])
        nmeAnameCorrect = np.array(['N', 'CH3'])
        sel_base = 'resname ACE NME'
        sel = '{} and hydrogen'.format(sel_base)

        if _sum(protein.atomselect(sel_base)) == 0:
            print('No caps found. Skiping the caps check')
            return protein

        m = protein.copy()
        if _sum(m.atomselect(sel)) != 0:
            print('WARNING: Hydrogen found in caps. These atoms will be removed')
            m.remove(sel)

        # check if atomname are not correct
        aceAname = np.unique(m.get('name', 'resname ACE'))
        nmeAname = np.unique(m.get('name', 'resname NME'))
        if not np.array_equal(np.sort(aceAname), np.sort(aceAnameCorrect)) or \
                not np.array_equal(np.sort(nmeAname), np.sort(nmeAnameCorrect)):
            print('Not valid atom name for caps found. Will be modified')
            m.bonds = m._getBonds()

        # Check ACE caps
        if len(aceAname) > 0:
            aceResIds = np.unique(m.resid[np.where(m.resname == 'ACE')])
            nextResIds = np.array([m.resid[np.where(m.resid == a)[0][-1] + 1] for a in aceResIds])
            nextResIdsAsString = " ".join(nextResIds.astype(str).tolist())
            nextNidx = np.where(m.atomselect('resid {} and name  N'.format(nextResIdsAsString)))[0]

            for resace, nnext in list(zip(aceResIds, nextNidx)):

                aceIdxs = np.where(m.atomselect('resname ACE and resid {} and element C'.format(resace)))[0]
                aceIdx_O = np.where(m.atomselect('resname ACE and resid {} and element O'.format(resace)))[0]
                combs = [[a, nnext] for a in aceIdxs]

                bonds = m.bonds.tolist()
                for n, c in enumerate(combs):
                    c = list(c)
                    if c in bonds:
                        m.name[combs[n][0]] = aceAnameCorrect[0]
                    else:
                        m.name[combs[n][0]] = aceAnameCorrect[2]
                m.name[aceIdx_O] = aceAnameCorrect[1]

        # Check NME caps
        if len(nmeAname) > 0:
            nmeResIds = np.unique(m.resid[np.where(m.resname == 'NME')])
            prevResIds = np.array([m.resid[np.where(m.resid == n)[0][0] - 1] for n in nmeResIds])
            prevResIdsAsString = " ".join(prevResIds.astype(str).tolist())
            prevCidx = np.where(m.atomselect('resid {} and name  C'.format(prevResIdsAsString)))[0]

            for resnme, cprev in list(zip(nmeResIds, prevCidx)):
                nmeIdxs = np.where(m.atomselect('resname NME and resid {} and element N'.format(resnme)))[0]
                nmeIdx_C = np.where(m.atomselect('resname NME and resid {} and element C'.format(resnme)))[0]
                m.name[nmeIdxs] = nmeAnameCorrect[0]
                m.name[nmeIdx_C] = nmeAnameCorrect[1]
        return m


    def run(self):

        self.mol = self._loadPDB(self.vars.pdb)

        # check caps
        self.mol = self.checkCaps(self.mol)

        self._runFirstProteinPrepare()



def getArgParser():
    parser = argparse.ArgumentParser(description='Prepare a protein for MD simulations using PROPKA 3.1 for residue titration and PDB2PQR 2.1 to '
                                                 'optimize the hydrogen bond network.')

    requiredArgs = parser.add_argument_group('required args')

    requiredArgs.add_argument('-pdb', dest='pdb', action='store', type=str, help='.pdb file or PDB id.', required=True)
    parser.add_argument('-pH', dest='pH', action='store',
                        default=7.2, type=float, help='pH at which residues will be titrated (default: 7.2)')
    parser.add_argument('-chain', dest='chain', action='store',
                        default='', type=str,
                        help='chains to be used in ProteinPrepare (e.g.: -chain A B; default: all)')
    parser.add_argument('--remove-water', dest='remove_water', action='store_true',
                        help='ignore water molecules in the optimization (default: False)')
    parser.add_argument('--include-heteroatoms', dest='include_heteroatoms', action='store_true',
                        help='include heteroatoms in the optimization (default: False)')
    parser.add_argument('--debug', dest='debug', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('-outdir', dest='outdir', action='store', type=str, default='.',
                        help='The output folder where to write the results')

    return parser

if __name__ == '__main__':
    parser = getArgParser()
    args, service = parser.parse_known_args()
    ProteinPreparator(args=vars(args)).run()
