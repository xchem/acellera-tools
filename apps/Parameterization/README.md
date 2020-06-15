## Parameterization tool 
 
Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera,psi4,anaconda Parameterize.xml```

```planemo serve --host 0.0.0.0 --port 8080 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera,psi4,anaconda Parameterize.xml```

You should then be able to navigate to http://127.0.0.0:8080/ and run Parameterization as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.

To run Parameterize locally, first, create and activate the environment:

```conda env create -f environment.yml```

and then run:

```parameterize --no-dihed --charge-type Gasteiger --seed 01 test-data/pipeline_protlig.mol2```

to parameterize the ligand molecule that we will use in our protein-ligand protocol.



