## MDSimulator tool 
 
Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera MDSimulator.xml```

```planemo serve --host 0.0.0.0 --port 8090 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera MDSimulator.xml```

You should then be able to navigate to http://127.0.0.0:8090/ and run MDsimulator as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.

