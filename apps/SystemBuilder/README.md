## SystemBuilder tool 
 
Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,anaconda,acellera,psi4 SystemBuilder.xml```

```planemo serve --host 0.0.0.0 --port 8080 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera,psi4 SystemBuilder.xml```

You should then be able to navigate to http://127.0.0.0:8080/ and run SystemBuilder as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.


To run locally:

```conda env create -f environment.yml```, activate the environment, and then copy the files of the protonated protein and parameterized ligand to a folder:


```
mkdir build_protlig_system
cp ../ProteinPreparation/output.pdb build_protlig_system/
cp ../Parameterization/parameters/GAFF2/mol-orig.mol2 build_protlig_system/
cp ../Parameterization/parameters/GAFF2/mol.frcmod build_protlig_system/
```

now, you can run systembuilder to get the files needed tu run MD simulation.


```python app.py -protein build_protlig_system/output.pdb -ligand build_protlig_system/mol-orig.mol2 -ligfrcmod build_protlig_system/mol.frcmod -outdir ready2MD```
