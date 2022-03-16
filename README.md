# :bar_chart: <span style="font-weight: bold;">Mob<span style="color: red;">Vis</span></span>

<div align="justify">
MobVis is an open source Python library for perform analysis about mobility data in a simple way.
With this framework, it is possible to extract metrics and visualize data from different sources.

MobVis mainly uses the [ Pandas ](https://pandas.pydata.org/) library for data processing, and [ Plotly ](https://plotly.com/) for data visualization.
</div>

## :mag: Contents

1. [ Documentation ](#book-documentation) 
2. [ Installation ](#computer-installation)
   1. [ conda installation ](#conda-installation)
   2. [ pip installation ](#pip-installation)
3. [ Examples ](#keyboard-examples)
4. [ Citing ](#newspaper-citing)
5. [ Collaborators ](#envelope-collaborators)

## :book: Documentation

Colocar aqui link para site de documentação oficial da biblioteca hospedado em algum servidor do github.io

## :computer: Installation

### conda installation

1. Create an conda environment
   ```bash
   conda env create -f mobvis_req.yml
   ```

2. Activate the environment
   ```bash
   conda activate mobvis
   ```

3. Install the library locally with pip
   ```bash
   cd ../
   ```

   ```bash
   pip install -e mobvis
   ```

### pip installation

1. Lorem ipsum dolor sit amet
2. Lorem ipsum dolor sit amet
3. Lorem ipsum dolor sit amet

## :keyboard: Examples

## Use case example

### 1. Importing the modules:


```python
import pandas as pd # Pandas is used to read the files from the computer

from mobvis.preprocessing.parser import Parser as par # The Parser module is used to convert the raw data to a standard format

from mobvis.metrics.utils.Locations import Locations as loc # The Locations module is used to find the Geo-locations of the trace, used by almost all metrics
from mobvis.metrics.utils.HomeLocations import HomeLocations as hloc # The HomeLocations module is used to find the Home-locations of the trace, used by some metrics
from mobvis.metrics.utils.Contacts import Contacts as cnt # The Contacts module is used to detect the Contacts between the nodes, used by Social metrics

from mobvis.metrics.utils.MetricBuilder import MetricBuilder as mb # The MetricBuilder module is used to instantiate the metrics 

from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *
```

### 2. Reading the raw example trace:


```python
trace = pd.read_csv('swim_siot_private.csv', header=None, delimiter=',')

trace.head()
```

### 3. Parsing the raw trace:


```python
parsed_trace = par.parse(raw_trace=trace, raw_trace_cols=['timestamp', 'id', 'x', 'y'], is_ordered=True) # See the `parse` method docstring for more information

parsed_trace.head()
```

### 4. Finding the requirements for the metrics (Geo-locations, Home-locations and Contacts):


```python
[trace_loc, loc_centers] = loc.find_locations(trace=parsed_trace, max_d=0.014, pause_threshold=10, dist_type="euclidean")

trace_loc.head()
```


```python
trace_homes = hloc.find_homes(trace_loc=trace_loc)

trace_homes.head()
```


```python
trace_contacts = cnt.detect_contacts(df=parsed_trace, radius=0.13, dist_type="euclidean")

trace_contacts.head()
```

### 5. Extracting the metrics:


```python
trace_trvd = mb.build_metric('TRVD', trace_loc=trace_loc, dist_type="Euclidean").extract()
trace_radg = mb.build_metric('RADG', trace=parsed_trace, trace_loc=trace_loc, sl_centers=loc_centers, homes=trace_homes, dist_type="Euclidean").extract()
trace_viso = mb.build_metric('VISO', trace_loc=trace_loc).extract()
trace_vist = mb.build_metric('VIST', trace_loc=trace_loc).extract()
trace_trvt = mb.build_metric('TRVT', trace_loc=trace_loc).extract()
trace_inco = mb.build_metric('INCO', contacts_df=trace_contacts).extract()
```

#### Some tabular data examples:


```python
trace_trvd.head()
```


```python
trace_radg.head()
```


```python
trace_trvt.head()
```


```python
trace_inco.head()
```

### 6. Visualizing the data:

#### Trace Plots:


```python
# This is an interactive graphic generated by Plotly:
#     - Click and drag the mouse for zoom to an area
#     - Double click to zoom out
#     - Double click on a Node ID on the left side to see only that specific node movements
#     - Double click back to restore the other nodes
#     - For more information, see Polotly documentation

plot_trace(trace=trace, initial_id=1, number_of_nodes=5, show_y_label=False)
```


```python
plot_trace3d(trace=trace, initial_id=1, nodes_list=[4, 5, 6], show_y_label=False) # On this plot, the nodes to be shown are specified by the `nodes_list` parameter
```


```python
plot_density(trace=trace, initial_id=1, number_of_nodes=50) # This graph is showing the density of all the movements of 50 of the 100 nodes on the trace
```


```python
plot_visit_order(trace_viso=trace_viso, initial_id=1, number_of_nodes=1) # Geo-locations visited by the 1º node in order
```

#### Metrics Plots:


```python
plot_metric_histogram(
    trace_trvd,
    initial_id=1,
    metric_type='TRVD',
    differ_nodes=False,
    show_title=False,
    show_y_label=True,
    max_users=100
)
```


```python
plot_metric_histogram(
    trace_radg,
    initial_id=1,
    metric_type='RADG',
    differ_nodes=False,
    show_title=False,
    show_y_label=True,
    max_users=100
)
```

### 7. Exporting the data:


```python

```


## :newspaper: Citing

<p>
   Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
</p>

## :envelope: Collaborators

[ Lucas Novais da Silva ](https://www.instagram.com/luc.novais/): <a href="mailto:lucas.novais@aluno.ufop.edu.br">lucas.novais@aluno.ufop.edu.br</a>