## LigandBasedClassifier tool 

Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,anaconda,pytorch,avarela,acellera LigandClassifier.xml```

```planemo serve --host 0.0.0.0 --port 8080 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,anaconda,pytorch,avarela,acellera LigandClassifier.xml```

You should then be able to navigate to http://127.0.0.1:8080/ and run LigandBasedClassifier as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.

To test locally, install the environment with conda:

```conda env create -f environment.yml```

and the run:

```python app.py test-data/input.csv --validate --hp_trials 5```
