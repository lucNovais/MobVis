<img src="images/full_logo.svg" width=403.16 height=80 />

<div align="justify">
MobVis is an open source Python library for perform analysis about mobility data in a simple way.
With this framework, it is possible to extract metrics and visualize data from different sources.

MobVis mainly uses the [ Pandas ](https://pandas.pydata.org/) library for data processing, and [ Plotly ](https://plotly.com/) for data visualization.
</div>

## :mag: Contents

1. [ Documentation ](#book-documentation) 
2. [ Installation ](#computer-installation)
   1. [ Windows installation ](#windows-installation)
   2. [ Linux installation ](#linux-installation)
3. [ Citing ](#newspaper-citing)
4. [ Collaborators ](#envelope-collaborators)

## :book: Documentation

<p>
  The MobVis docs page is still under development. Until then, use this README and the docstrings in the source code to get your bearings.
</p>

## :wrench: Inslatation

In this section, you will be presented with a step-by-step guide on how to install the library locally. This library uses some other packages to work, which are listed below:

- pandas - 1.5.2
- scipy - 1.9.3
- plotly - 5.11.0
- kaleido - 0.2.1

### Windows Instalation

The Windows Instalation guide is still under development.

### Linux Instalation

To install this library on Debian Linux variants (Ubuntu, Mint, etc), simply follow the following steps:

1. Clone the repository using the command:

```bash
git clone https://github.com/lucNovais/MobVis.git
```

2. Move to the library folder:

```bash
cd MobVis
```

3. Create a Python virtual environment:

```bash
python3 -m venv venv
```

4. Start the environment:

```bash
source venv/bin/activate
```

5. Install the libraries necessary for MobVis to work:

```bash
pip install -r requirements.txt
```

6. Install MobVis locally:

```bash
pip install .
```
These are all the steps necessary to have an environment configured to start using MobVis. As a recommendation, I suggest carrying out developments in a `Jupyter Notebook`.

## :newspaper: Citing

<p>
  The quotes for this project are yet to come ;)
</p>

## :envelope: Collaborators

[ Lucas Novais da Silva ](https://www.instagram.com/luc.novais/): <a href="mailto:lucas.novais@aluno.ufop.edu.br">lucas.novais@aluno.ufop.edu.br</a>
<br>
[ Bruno Pereira dos Santos ](): <a href="mailto:bruno.ps@ufop.edu.br">bruno.ps@ufop.edu.br</a>
<br>
[ Vinicius F. S. Mota ](): <a href="mailto:vinicius.mota@inf.ufes.br">vinicius.mota@inf.ufes.br</a>
<br>
[ Paulo H. L. Rettore ](): <a href="mailto: paulo.lopes.rettore@fkie.fraunhofer.de">paulo.lopes.rettore@fkie.fraunhofer.de</a>
