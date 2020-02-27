# Acellera-XChem fragalysis collaboration project

## Table of contents
1. [ Introduction ](#intro)
2. [ Protein preparation tool (MD) ](#protprep)
3. [ Parameterization tool (MD) ](#parameterize)
4. [ System building tool (MD) ](#systembuilder)
5. [ MD Simulation + Analysis (MD) ](#mdsimulation)
6. [ Ligand-based binder/non-binder classifier (ML) ](#classifier)
7. [ License ](#license)

<a name="intro"></a>
## 1. Introduction (MD)
This repository includes all the work done in collaboration between Acellera and XChem to port Acellera 
technology into the Fragalysis project.

The goals of the applications presented in this repository are to (a) either rationalize 
the binding of protein+fragment complexes or to (b) guide the user in the selection of further 
prospective ligands for experimental validation.

In order to do so, we make use of two of the key technologies offered by Acellera: (a) molecular dynamics 
(MD) simulations and (b) machine learning (ML). 

On the MD side of things, in this repo you will find an app to protonate and prepare a protein 
for MD, a tool for small fragment/ligand parameterization, a protein-ligand system builder, and 
a full-blown MD engine (Acemd) plus analysis tool which aim to shed light over protein-fragment complexes 
stability. 

On the ML side, we provide a complex ligand-based tool that can learn from an already existing list of
binders and non-binders to predict a probability/score given some new list of ligands.

In order to test the applications, a conda environment must be created using the provided environment.yml files
inside each app, using ```conda env create -f environment.yml```. Then, after activating the environment,
the appropiate tests can be run using the provided .sh scripts.

<a name="protprep"></a>
## 2. Protein preparation tool (MD)
The tool is available in `ProteinPreparation/app.py` and given a PDB file it uses `PropKa` for the protein
protonation and `PDB2PQR` for the hydrogen-bond network optimization. Protein residues will be protonated
in the most probable protonation state given a user-provided pH.    

_Reference:_
```
Martínez-Rosell, G., Giorgino, T., & De Fabritiis, G. (2017). 
PlayMolecule ProteinPrepare: a web application for protein preparation for molecular dynamics simulations. 
Journal of chemical information and modeling, 57(7), 1511-1516.
```

<a name="parameterize"></a>
## 3. Parameterization tool (MD)
The application presented here is `parameterize` a tool that already comes bundled with the `HTMD` package. 
While the tool allows to run complex QM calculations for dihedral parameter estimation, its simpler version allow the user to 
obtain GAFF-compatible parameters by running the tool with the `--no-min --no-dihed --no-dihed-opt --no-esp` flags.

_Reference:_
```
Galvelis, R., Doerr, S., Damas, J. M., Harvey, M. J., & De Fabritiis, G. (2019). 
A Scalable Molecular Force Field Parameterization Method Based on Density Functional Theory and Quantum-Level Machine Learning. 
Journal of chemical information and modeling, 59(8), 3485-3493.
```

<a name="systembuilderp"></a>
## 4. System building tool (MD)
The system building application is presented in `SystemBuilder/app.py`. It uses the functionality provided by the 
`HTMD` package to solvate, ionize and build protein-ligand systems and make them ready to run MD simulations.

_Reference:_
```
Doerr, S., Harvey, M. J., Noé, F., & De Fabritiis, G. (2016). 
HTMD: high-throughput molecular dynamics for molecular discovery. 
Journal of chemical theory and computation, 12(4), 1845-1852.
```

<a name="mdsimulation"></a>
## 5. MD Simulation + Analysis (MD)
The application present at `MDSimulator/app.py` represents a wrapper over the `acemd` MD simulation engine plus a short
script to analyze the stability of the protein-ligand complex in terms of RMSD over the simulation. For more information 
over the options available please run `MDSimulator/app.py --help`.

_References:_
```
Harvey, M. J., Giupponi, G., & Fabritiis, G. D. (2009). 
ACEMD: accelerating biomolecular dynamics in the microsecond time scale. 
Journal of chemical theory and computation, 5(6), 1632-1639.
```

```
Doerr, S., Harvey, M. J., Noé, F., & De Fabritiis, G. (2016). 
HTMD: high-throughput molecular dynamics for molecular discovery. 
Journal of chemical theory and computation, 12(4), 1845-1852.
```

<a name="classifier"></a>
## 6. Ligand-based binder/non-binder classifier (ML)
Given the initial results of a fragment screening, with a series of experimentally resolved 
binders and non-binders, in the application presented in `LigandBasedClassifier/app.py`
we provide a way to automatically learn features from the data available to prospectively discriminate
a new set of compounds and hopefully guide the user on what sensible next fragments to test.

Specifically, we use the `RDKit` library to extract fingerprints for each 
ligand (provided as a `smiles` string) and we use an `XGBoost` classifier to learn 
to discriminate binders from non-binders. The hyper parameters of the model are
automatically searched using the bayesian-optimization algorithm provided
 by `ax-platform` and the final model consists of an ensemble of tenths of 
 `XGBoost` models that have been optimized on a specific metric like `auc` or
 `map` (mean average precision). `map` has been made the default metric since 
 in drug discovery we usually don't care about "generally" ranking the compounds well (auc)
 but we care about doing good predictions (i.e. finding true binders) at the top 5-10% 
 of all predictions. `map` is therefore a proxy to achieve a good top 1-5% 
 enrichment. 
 
 The suggested way to use this application is to first train a model based on 
binders/non-binders found for a specific cluster/pocket of fragments and then cast predictions on a set
of suggested binders that might be extensions or derivatives of the binders. 
Since ML is generally "data-hungry", if the amount of data is low for a given crystallographic cluster of
 binders, then a more general model can be made by aggregating all the binders from all the 
 clusters/pockets of one individual protein. Note, however, that the general model would predict binding 
 on a per-protein basis instead of a per-pocket basis.  

<a name="license"></a>
## 7. License

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
 

