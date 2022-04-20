<img src="images/full_logo.svg" width=403.16 height=80 />

<p>Vídeo de apresentação do MobVis (Salão de Ferramentas - SBRC 2022): <a>https://youtu.be/kcVeZX8Ukj0</a></p>

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
3. [ Examples ](#keyboard-examples)
4. [ Citing ](#newspaper-citing)
5. [ Collaborators ](#envelope-collaborators)

## :book: Documentation

<p>
  The MobVis docs page is still under development. Until then, use this README and the docstrings in the source code to get your bearings.
</p>

## :computer: Installation

### Requirements:

<ul>
  <li>Python 3.9
  <li>conda 4.12
  <li>pip 21.4
</ul>

### Windows Installation:

**1.** Clone the repository
   ```bash
   git clone https://github.com/lucNovais/MobVis.git
   ```

**2.** Move to the repository directory
   ```bash
   cd MobVis
   ```

**3.** Create a `conda` environment with the `requirements.yml` file
   ```bash
   conda env create -f windows_requirements.yml
   ```

**4.** Activate the environment
   ```bash
   conda activate mobvis-windows
   ```

**5.** Install the MobVis library locally
   ```bash
   pip install -e .
  ```

**6.** Jupyter notebooks are recomended for running the library
   ```bash
   conda install jupyterlab
   jupyter-lab
   ```

### Linux Installation:

**1.** Clone the repository
   ```bash
   git clone https://github.com/lucNovais/MobVis.git
   ```

**2.** Move to the repository directory
   ```bash
   cd MobVis
   ```

**3.** Create a `conda` environment with the `requirements.yml` file
   ```bash
   conda env create -f requirements.yml
   ```

**4.** Activate the environment
   ```bash
   conda activate mobvis
   ```

**5.** Install the MobVis library locally
   ```bash
   pip install -e .
  ```

**6.** Jupyter notebooks are recomended for running the library
   ```bash
   conda install jupyterlab
   jupyter-lab
   ```

## :keyboard: Examples

# <img src="images/small_logo.svg" width=60 height=60 /> MobVis
## Use case example

### 1. Importing the modules:


```python
# Pandas is used to read the files from the computer
import pandas as pd

# The Parser module is used to convert the raw data to a standard format
from mobvis.preprocessing.parser import Parser as par

# The Locations module is used to find the Geo-locations of the trace, used by almost all metrics
from mobvis.metrics.utils.Locations import Locations as loc
# The HomeLocations module is used to find the Home-locations of the trace, used by some metrics
from mobvis.metrics.utils.HomeLocations import HomeLocations as hloc
# The Contacts module is used to detect the Contacts between the nodes, used by Social metrics
from mobvis.metrics.utils.Contacts import Contacts as cnt

# The MetricBuilder module can be used to instantiate all the metrics 
from mobvis.metrics.utils.MetricBuilder import MetricBuilder as mb

# The metric and spatial plotters contains all the visualizations of MobVis
from mobvis.plots.metric_plotter import *
from mobvis.plots.spatial_plotter import *
```

### 2. Reading the raw example trace:


```python
trace = pd.read_csv('swim_siot_private.csv', names=['timestamp', 'id', 'x', 'y'], delimiter=',')

trace.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>timestamp</th>
      <th>id</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1888150</td>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1923820</td>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1923840</td>
      <td>1</td>
      <td>0.0676107</td>
      <td>0.699221</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2106950</td>
      <td>1</td>
      <td>0.0676107</td>
      <td>0.699221</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2106970</td>
      <td>1</td>
      <td>0.2034240</td>
      <td>0.463691</td>
    </tr>
  </tbody>
</table>
</div>



### 3. Parsing the raw trace:


```python
parsed_trace = par.parse(raw_trace=trace, is_ordered=True) # See the `parse` method docstring for more information

parsed_trace.head()
```

    Parsing the given DataFrame...
    Checking the raw trace columns...
    Fixing the timestamps...
    Shorter timestamp: 1728110.0
    Timestamps fixed!
    
    Successfully parsed!
    
            id  timestamp          x         y
    0        1   160040.0  0.0249873  0.651852
    1        1   195710.0  0.0249873  0.651852
    2        1   195730.0  0.0676107  0.699221
    3        1   378840.0  0.0676107  0.699221
    4        1   378860.0  0.2034240  0.463691
    ...    ...        ...        ...       ...
    13879  100   629990.0  0.4117910  0.446579
    13880  100   630010.0  0.5564900  0.293979
    13881  100   846090.0  0.5564900  0.293979
    13882  100   846110.0  0.5286780  0.419772
    13883  100   846610.0  0.5286780  0.419772
    
    [13884 rows x 4 columns]
    
    Elapsed time: 0.3478250503540039 seconds.
    
    




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>timestamp</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>160040.0</td>
      <td>0.0249873</td>
      <td>0.651852</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>195710.0</td>
      <td>0.0249873</td>
      <td>0.651852</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>195730.0</td>
      <td>0.0676107</td>
      <td>0.699221</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>378840.0</td>
      <td>0.0676107</td>
      <td>0.699221</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>378860.0</td>
      <td>0.2034240</td>
      <td>0.463691</td>
    </tr>
  </tbody>
</table>
</div>



### 4. Finding the requirements for the metrics (Geo-locations, Home-locations and Contacts):


```python
[trace_loc, loc_centers] = loc.find_locations(trace=parsed_trace, max_d=0.014, pause_threshold=10, dist_type="euclidean")

trace_loc.head()
```

    Finding the stay and geo locations...
    
    Parameters:
    Max Distance: 0.014
    Pause Threshold: 10
    Distance Formula: euclidean
            id          x         y  sl     gl    index  timestamp
    0        1  0.0249873  0.651852   0   True      0.0   160040.0
    1        1  0.0249873  0.651852   0   True      1.0   195710.0
    2        1  0.0676107  0.699221   1   True      2.0   195730.0
    3        1  0.0676107  0.699221   1   True      3.0   378840.0
    4        1   0.203424  0.463691   2  False      4.0   378860.0
    ...    ...        ...       ...  ..    ...      ...        ...
    13879  100   0.411791  0.446579  37  False  13879.0   629990.0
    13880  100    0.55649  0.293979  38   True  13880.0   630010.0
    13881  100    0.55649  0.293979  38   True  13881.0   846090.0
    13882  100   0.528678  0.419772  39  False  13882.0   846110.0
    13883  100   0.528678  0.419772  39  False  13883.0   846610.0
    
    [13884 rows x 7 columns]
    Locations found!
    
    Elapsed time: 4.299750328063965 seconds.
    
    




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>x</th>
      <th>y</th>
      <th>sl</th>
      <th>gl</th>
      <th>index</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
      <td>0</td>
      <td>True</td>
      <td>0.0</td>
      <td>160040.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
      <td>0</td>
      <td>True</td>
      <td>1.0</td>
      <td>195710.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0.0676107</td>
      <td>0.699221</td>
      <td>1</td>
      <td>True</td>
      <td>2.0</td>
      <td>195730.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0.0676107</td>
      <td>0.699221</td>
      <td>1</td>
      <td>True</td>
      <td>3.0</td>
      <td>378840.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0.203424</td>
      <td>0.463691</td>
      <td>2</td>
      <td>False</td>
      <td>4.0</td>
      <td>378860.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_homes = hloc.find_homes(trace_loc=trace_loc)

trace_homes.head()
```

    Finding the Home Locations...
    Home locations found!
    
    Elapsed time: 0.6084480285644531 seconds.
    
    




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>home_location</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
      <td>0.280775</td>
      <td>0.938994</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>8</td>
      <td>0.398246</td>
      <td>0.343223</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>43</td>
      <td>0.117753</td>
      <td>0.0431013</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>51</td>
      <td>0.818454</td>
      <td>0.36456</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>7</td>
      <td>0.961683</td>
      <td>0.587378</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_contacts = cnt.detect_contacts(df=parsed_trace, radius=0.13, dist_type="euclidean")

trace_contacts.head()
```

    Detecting the contacts between the nodes...
    
    Parameters:
    Contact Radius: 0.13
    Distance Formula: euclidean
    Contacts Detected!
       id1   id2         x1         y1         x2        y2 timestamp
    0  2.0  63.0   0.614517  0.0815663   0.652965  0.128888  720160.0
    1  2.0  85.0   0.529963   0.149233   0.622037  0.155485  781550.0
    2  3.0  73.0  0.0567702   0.147967  0.0629667  0.138837  750120.0
    3  4.0  44.0   0.464873   0.728179   0.402214   0.78985   95230.0
    4  4.0  46.0    0.43473   0.569507   0.423977  0.661822  258830.0
    Number of contacts: 53
    
    Elapsed time: 11.39995265007019 seconds.
    
    




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id1</th>
      <th>id2</th>
      <th>x1</th>
      <th>y1</th>
      <th>x2</th>
      <th>y2</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2.0</td>
      <td>63.0</td>
      <td>0.614517</td>
      <td>0.0815663</td>
      <td>0.652965</td>
      <td>0.128888</td>
      <td>720160.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2.0</td>
      <td>85.0</td>
      <td>0.529963</td>
      <td>0.149233</td>
      <td>0.622037</td>
      <td>0.155485</td>
      <td>781550.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.0</td>
      <td>73.0</td>
      <td>0.0567702</td>
      <td>0.147967</td>
      <td>0.0629667</td>
      <td>0.138837</td>
      <td>750120.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4.0</td>
      <td>44.0</td>
      <td>0.464873</td>
      <td>0.728179</td>
      <td>0.402214</td>
      <td>0.78985</td>
      <td>95230.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4.0</td>
      <td>46.0</td>
      <td>0.43473</td>
      <td>0.569507</td>
      <td>0.423977</td>
      <td>0.661822</td>
      <td>258830.0</td>
    </tr>
  </tbody>
</table>
</div>



### 5. Extracting the metrics:


```python
trace_trvd = mb.build_metric('TRVD', trace_loc=trace_loc, dist_type="Euclidean").extract()
trace_radg = mb.build_metric('RADG', trace=parsed_trace, trace_loc=trace_loc, sl_centers=loc_centers, homes=trace_homes, dist_type="Euclidean").extract()
trace_viso = mb.build_metric('VISO', trace_loc=trace_loc).extract()
trace_vist = mb.build_metric('VIST', trace_loc=trace_loc).extract()
trace_trvt = mb.build_metric('TRVT', trace_loc=trace_loc).extract()
trace_inco = mb.build_metric('INCO', contacts_df=trace_contacts).extract()
```

    
    Extracting the Travel Distance...
    Travel Distance extracted successfully!
    
    
    Elapsed time: 5.559073209762573 seconds.
    
    
    Extracting the Radius of Gyration...
    Radius of Gyration extracted successfully!
    
    Elapsed time: 0.7478008270263672 seconds.
    
    
    Extracting the Visit Order...
    Visit Order extracted successfully!
    
    Elapsed time: 1.1690409183502197 seconds.
    
    Extracting the Visit Time...
    Visit Time extracted successfully!
    
    
    Elapsed time: 4.305334806442261 seconds.
    
    
    Extracting the Travel Time...
    Travel Distance extracted successfully!
    
    
    Elapsed time: 3.552776575088501 seconds.
    
    
    Extracting the Inter-contact Time...
    
    Inter-contact Time extracted successfully!
    
    Elapsed time: 0.006001710891723633 seconds.
    
    

#### Some tabular data examples:


```python
trace_trvd.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>travel_distance</th>
      <th>init_sl</th>
      <th>final_sl</th>
      <th>ix</th>
      <th>iy</th>
      <th>fx</th>
      <th>fy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0.0637226521</td>
      <td>0</td>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
      <td>0.0676107</td>
      <td>0.699221</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>0.2718816532</td>
      <td>1</td>
      <td>2</td>
      <td>0.0676107</td>
      <td>0.699221</td>
      <td>0.203424</td>
      <td>0.463691</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0.2374839433</td>
      <td>2</td>
      <td>3</td>
      <td>0.203424</td>
      <td>0.463691</td>
      <td>0.0592504</td>
      <td>0.652404</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0.3622250357</td>
      <td>3</td>
      <td>4</td>
      <td>0.0592504</td>
      <td>0.652404</td>
      <td>0.280775</td>
      <td>0.938994</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0.3062901958</td>
      <td>4</td>
      <td>5</td>
      <td>0.280775</td>
      <td>0.938994</td>
      <td>0.121342</td>
      <td>0.67747</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_radg.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>home_location</th>
      <th>radius_of_gyration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>4</td>
      <td>0.3696662643</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>8</td>
      <td>0.3769005346</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>43</td>
      <td>0.282227782</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>51</td>
      <td>0.2953635671</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>7</td>
      <td>0.3258284219</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_trvt.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>init_sl</th>
      <th>final_sl</th>
      <th>t_exit</th>
      <th>t_arrival</th>
      <th>travel_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>195710.0</td>
      <td>195730.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>378840.0</td>
      <td>378860.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>378960.0</td>
      <td>378980.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>383090.0</td>
      <td>383110.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>4</td>
      <td>5</td>
      <td>599400.0</td>
      <td>599420.0</td>
      <td>20.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_inco.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id1</th>
      <th>id2</th>
      <th>intercontact_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35.0</td>
      <td>64.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>51.0</td>
      <td>72.0</td>
      <td>1350.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>51.0</td>
      <td>72.0</td>
      <td>20.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>72.0</td>
      <td>76.0</td>
      <td>400.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
trace_viso.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>x</th>
      <th>y</th>
      <th>sl</th>
      <th>visit_order</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0.0249873</td>
      <td>0.651852</td>
      <td>0</td>
      <td>1.0</td>
      <td>160040.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0.0676107</td>
      <td>0.699221</td>
      <td>1</td>
      <td>2.0</td>
      <td>195730.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0.203424</td>
      <td>0.463691</td>
      <td>2</td>
      <td>2.0</td>
      <td>378860.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1</td>
      <td>0.0592504</td>
      <td>0.652404</td>
      <td>3</td>
      <td>3.0</td>
      <td>378980.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>0.280775</td>
      <td>0.938994</td>
      <td>4</td>
      <td>4.0</td>
      <td>383110.0</td>
    </tr>
  </tbody>
</table>
</div>



### 6. Visualizing the data:

#### Trace Plots:


```python
fig = plot_trace(
    trace=parsed_trace,
    users_to_display=10
)
```

    
    Successfully generated plot!
    
<img src="images/plots/movements.png" width=740 height=560 />

```python

# On this plot, the nodes to be shown are specified by the `nodes_list` parameter
fig = plot_trace3d(trace=trace, specific_users=[4, 5, 6], show_y_label=False)
```

    
    Successfully generated plot!
    
<img src="images/plots/movements3d.png" width=740 height=560 />

```python
# This graph is showing the density of all the movements of 50 of the 100 nodes on the trace
fig = plot_density(trace=trace, users_to_display=50)
```

<img src="images/plots/density.png" width=600 height=560 />

```python
# Geo-locations visited by the 1º node in order
fig = plot_visit_order(trace_viso=trace_viso, users_to_display=1)
```

<img src="images/plots/viso.png" width=600 height=560 />    

#### Metrics Plots:


```python
fig = plot_metric_histogram(
    trace_trvd,
    metric_name='TRVD',
    differ_nodes=False,
    show_title=True,
    show_y_label=True,
    nbins=40
)
```

    Generating the TRVD histogram...
    
    Successfully generated histogram!
    
    Elapsed time: 4.03615665435791 seconds.
    
<img src="images/plots/trvd_hist.png" width=600 height=560 />

```python
fig = boxplot_metric(
    trace_radg,
    metric_name='RADG',
    differ_nodes=False,
    show_title=False,
    show_y_label=True
)
```

    Generating the RADG boxplot...
    
    Successfully generated boxplot!
    
    Elapsed time: 0.052931785583496094 seconds.
    
<img src="images/plots/radg_dist.png" width=600 height=560 />

```python
fig = plot_metric_dist(
    metric_df=trace_trvd,
    metric_name='TRVD',
    show_title=False,
    show_y_label=True
)
```

    Generating the TRVD distplot...
    0.02725285371828199
    
    Successfully generated distplot!
    

<img src="images/plots/trvd_dist.png" width=600 height=560 />

### 7. Exporting the data:


```python
from mobvis.utils.Exports import export_dataframe
from mobvis.utils.Exports import export_figure
```


```python
export_dataframe(df=trace_trvd, path='travel_distance.txt')
```


```python
export_figure(figure=fig, path='distplot.png')
```

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
