## SystemBuilder tool 
 
Using planemo (installation instructions available at https://planemo.readthedocs.io/en/latest/installation.html#conda-experimental), a galaxy app can be created and tested with the following commands:

```planemo test --conda_ensure_channels iuc,bioconda,defaults,conda-forge,anaconda,acellera SystemBuilder.xml```

```planemo serve --host 0.0.0.0 --port 8080 --conda_ensure_channels iuc,bioconda,defaults,conda-forge,acellera SystemBuilder.xml```

You should then be able to navigate to http://127.0.0.0:8080/ and run SystemBuilder as a Galaxy tool.

Running these commands with a conda environment activated can cause problems, even if it is the "base" environment. Planemo must be installed out of any conda environment.


