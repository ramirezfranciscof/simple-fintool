# simple-fintool

Simple tool to do some processing of finantial instruments.


## Set up

The package can be downloaded from github:

```
git clone git@github.com:ramirezfranciscof/simple-fintool.git
```

And easily installed by first setting a virtual environment:

```
python -m venv /path/to/environment
source /path/to/environment/bin/activate
```

And then running the following command in the root application folder:

```
pip install -e .
```

Alternatively, it can be run inside a docker container using the included Dockerfile:

```
docker build -f .dockenv/Dockerfile -t workimg-fintool:v0.1 .
```

And then the container can be started by:

```
docker run -it -p 8000:8000 --name workenv-fintool workimg-fintool:v0.1
```

To access the container one can either open the jupyter lab interface that is started in the container (going to the browser to `http://127.0.0.1:8888/lab?token=...`, see below).

```
[I 2024-02-25 20:46:19.942 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2024-02-25 20:46:19.943 ServerApp]

    To access the server, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/jpserver-1-open.html
    Or copy and paste one of these URLs:
        http://35fa392b1e8b:8888/lab?token=a2f69f33837ac2921ebc4b28cbc0d3b2935038e29c870884
        http://127.0.0.1:8888/lab?token=a2f69f33837ac2921ebc4b28cbc0d3b2935038e29c870884
```

There one can open a jupyter lab terminal.
Alternatively, one can directly log in from the terminal of the host computer by running:

```
docker exec -it workenv-fintool bash #/bin/sh
```

Both terminal environments will already have the tool pre-installed and ready to use.


## Usage

The first thing one needs to do to use the tool is to start up an sqlite database:

```
fintool database setup
```

Multipliers can be added and updated to the database like this:

```
fintool database update --name INSTRUMENT1 --value 2.0
```

Now everything is ready to process an input file:

```
fintool process --source data/example_input.txt
```

The underlying engine of this original version uses base python methods and structures, but an alternative to enable pandas is included:

```
fintool process --pandas --source data/example_input.txt
```


## Performance tests

In order to test the performance and scalability of the application, it was applied to files consisting in multiples copies of the original set of data.
The big sets of data are not included in the repository, but can be regenerated easily (see/execute script `data/cmdgen_examples.sh`).

|                   | Copies of original | Total rows | Size (mb) | Time (s) [normal] | Time (s) [pandas] |
|-------------------|--------------------|------------|-----------|-------------------|-------------------|
| example_base0.txt | 1                  | 14'826     | 0.5       | 0.60              | 0.55              |
| example_long1.txt | 10                 | 148'260    | 4.8       | 0.75              | 0.90              |
| example_long2.txt | 100                | 1'482'600  | 48        | 2.40              | 3.50              |
| example_long3.txt | 1000               | 14'826'000 | 480       | 20.00             | 28.0              |

Although the first small files seem to be dominated by setup times, the biggest files seem to indicate a lineal scaling with the number of rows.
Using normal python methods or pandas does not seem to make much of a difference in this case.
The tests performed seem to indicate that the application can process data at an approximate rate of 1GB/min.

A more in depth performance analysis was performed using the `cProfile` tool.
These can be reproduced with the scripts in `data/cmdrun_textN_norm.sh` and `data/cmdrun_textN_pand.sh`.
An initial analysis of the results (`perflog0_*` filesin `perfdata`) indicated that the main bottleneck of the program was in the conversion from the string `01-Jan-1996` to a `datetime.date` object.
Changing the tool to parse dates inside `datetime` for a less versatile and robust (but faster, as long as all dates respect the same exact formatting) manual parsing.

After solving this, now the main `process_file` method is the current bottleneck.
Attempting to separate away parts of the procedure to detect a target for performance optimization were unsuccessfull (see `simple_fintool/engine/core_engine_split.py` and `perfdata/perflog3_split.txt`).

A second level of optimization would target the way in which the database multipliers are currently being fetched (for which further design feedback from clients is required).
For the pandas version, the database multipliers are not the problem but the bottleneck is more difficult to identify (it seems to still be related to the generation of the datetime object or related filters).


## Application design

The `fintool` application has 4 main modules:

 - `cmdline`: command line interface so that users can easily use the application.
 - `database`: the models/tables for the multiplier data, utility function to give safe access to the database context manager, and a general database manager than can be used to easily access the multipliers (either directly or from a temporary cache).
 - `engine`: it contains the core logic of the application (see below).
 - `engine_df`: an alternative version of the engine, with the same general structure but using pandas to access the data in chunks instead of one line at a time.

The core engine is a service class that goes through the csv input and feeds the data to the `DataAnalizer` corresponding to each instrument.
Each instrument has its own `DataAnalizer` object of the appropriate class, as indicated by the task instructions:
 - `TotalMean` for "INSTRUMENT1"
 - `MonthSpecificMean` for "INSTRUMENT2"
 - `MaxPriceSpread` for "INSTRUMENT3"
 - `DefaultAnalizer` for all the rest

Each object will take a data row and process the data according to what is necessary to produce its output.
