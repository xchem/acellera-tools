## MDSimulator tool 
 
Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera,psi4 MDSimulator.xml```

```planemo serve --host 0.0.0.0 --port 8090 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera,psi4 MDSimulator.xml```

You should then be able to navigate to http://127.0.0.0:8090/ and run MDsimulator as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.

To run locally:

```conda env create -f environment.yml```, activate the environment, and then run:

```cp -r ../SystemBuilder/ready2MD .```, to copy the protein-ligand system that we build in the current directory and, finally:

```python app.py -inputdir ready2MD/build_1 -constraints protein-ligand --use-gpu -runtime 10 -equiltime 2 -ligresname UNL -outdir MDprotocol```
to launch the MD simulation of the system, with 10 nanoseconds of production after 2 ns of equilibration.
