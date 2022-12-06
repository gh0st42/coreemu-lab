coreemu-lab
===========

*coreemu-lab* (short: *clab*) is an environment for automated evaluation of networking software.
It should work headless on any platform that can run [Docker](https://www.docker.com/) and with X11 it has been successfully tested on Linux and macOS.

The main features provided by *clab*:

- emulated network nodes based upon Linux namespaces (provided through [coreemu](https://github.com/coreemu/core)
- support for ns2 movement traces
- interactive [stop-motion movement](https://github.com/gh0st42/core-automator) helper
- monitoring services
    - process stats
    - network stats
    - position and contact traces
- [helpers](https://github.com/gh0st42/core-helpers) for automation and random message/data generation
- automated data collection after experiment
- report and plot generation
- full experiment configurations for headless runs
- extensible environment
    - it's all automated through shell scripts
    - python with pandas/matplotlib is available
    - many useful CLI helpers are available (`sysstat`, `rg`, `jq`, `bwm-ng`, `gnuplot`, `tcpdump`, ...)
- interactive mode with *coreemu* GUI
- providing ssh service and *coreemu* gRPC

We are currently lacking documentation, except for this way too short readme, the example in `data/` and the source code itself. 
There is a scientific publication in progress that will showcase *clab* and we are working on some easy to follow tutorials.

## General Overview

       ╔═════════════════════════════════════╗ ╔══════════════════════╗
       ║ core-experiment workflow            ║ ║ Shared Volume        ║
       ║                                     ║ ║ ┌─────────────┐      ║
       ║ 1. load config        ◀─────────────╬─╬─│ config      │      ║
       ║                                     ║ ║ └─────────────┘      ║
       ║ 2. init coreemu       ◀───────┐     ║ ║ ┌─────────────┐      ║
       ║                               └─────╬─╬─│ topology    │      ║
       ║ 3. (start app)        ◀────────┐    ║ ║ └─────────────┘      ║
       ║                                │    ║ ║        ▲  ┌──────────╩──┐
       ║ 4. start monitoring   ◀────────┤    ║ ║        └──│ movements   │
       ║                                │    ║ ║           └──────────╦──┘
       ║ 5. (warmup phase)              │    ║ ║  ┌─────────────┐     ║
       ║                                ├────╬─╬──│ (apps)      │     ║
       ║ 6. simulation run              │    ║ ║  └─────────────┘     ║
       ║                                │    ║ ║  ┌─────────────┐     ║
       ║ 7. stop app & monitoring       ├────╬─╬──│ (custom)    │     ║
       ║                                │    ║ ║  └─────────────┘     ║
       ║ 8. collect data                │    ║ ║                      ║
       ║                                │    ║ ║   ┌ ─ ─ ─ ─ ─ ─ ┐    ║
       ║ 9. analyze results    ◀────────┴────╬─╬──▶  results/         ║
       ║                                     ║ ║   └ ─ ─ ─ ─ ─ ─ ┘    ║
       ║ 10. shutdown                        ║ ║                      ║
       ║                                     ║ ║   ┌ ─ ─ ─ ─ ─ ─ ┐    ║
       ║                                     ╠─╬──▶  log              ║
       ║                                     ║ ║   └ ─ ─ ─ ─ ─ ─ ┘    ║
       ║                                     ║ ║                      ║
       ║                                     ║ ║                      ║
       ╚═════════════════════════════════════╝ ╚══════════════════════╝

## Installation

### Requirements

- [Docker](https://www.docker.com/)
- Linux kernel modules needed: *ebtables* and/or *sch_netem* 
- Optionally: X11

### Installing *clab*
- Download *clab* starter: `curl https://raw.githubusercontent.com/gh0st42/coreemu-lab/main/clab > clab`
- Make it executable: `chmod a+x ./clab`
- Copy it to your PATH
- Ready to use it

**BEWARE:** *First time starting might take a while as the (big) docker images have to be downloaded!*

### Updating

Just refresh the docker image on your system: `docker pull gh0st42/coreemu-lab`

## Running *clab*

For a quick interactive session, e.g., to design a new scenario and save it as an xml topology, just invoke `clab` without any parameters.

Optionally, it can be called with the first parameter being a directy that should be shared between docker and your host system: `clab /tmp/shared`

If the shared directory contains an `expirement.conf` it has precedence and whatever is configured in there will be performed, e.g., headless or with GUI can be set in the config file.

Furthermore, any more parameter will start an interactive terminal session without *coreemu* gui: `clab /tmp/shared -i`

This is helpful to debug services or retrigger the plotting of graphs if you do not want all dependencies on your host system.

## Helpers within *coreemu-lab*

### Periodic File Generator

`periodic-file-generator` - can be used in scripts to generate text or binary files of various sizes
```
usage: /usr/local/bin/periodic-file-generator <txt|bin> <min_size> <max_size> <min_delay> <max_delay> <output_dir>
 for text:     sizes mean number of words with lorem ipsum
 for binary:   sizes mean number of kilobytes
 for delay:    time in seconds to wait before next file is generated
```

### Core Helpers

[Helper scripts](https://github.com/gh0st42/core-helpers) for core network emulator

* `cbash <nodename>` - open bash
* `ccc` - core crash checker, greps for any FATALs
* `cda <cmd>` - core daemonize all
* `cea <cmd>` - core execute all
* `cpa <cmd>` - core parallel all
* `gf <size> <filename>` - generate file, e.g. `gf 10M /tmp/10m.file`

If `<cmd>` contains spaces or variables `"[..]"` or `'[..]'` might be needed.

### Core Automator

Interactive [stop-motion movement](https://github.com/gh0st42/core-automator) helper scripts to record and playback different node positions.

`core-record.py` - record current node layout to a file (default: appending)

`core-automator.py` - replay a recorded position file, sleep between steps (default: 1s) - is called if `AUTOMATOR` is set in `experiment.conf`

`core-mobility-studio.py` - simple tk GUI to record and playback position files - displayed via X11

### bonnmotion

[Bonnmotion](https://sys.cs.uos.de/bonnmotion/index.shtml) is included to generate different movement files. 
It can be used by starting an interactive session (e.g., `clab /tmp/shared -i`) and calling it within the docker container.
Detailed examples on how to generate and convert differt movement files can be found in the official [documentation](https://sys.cs.uos.de/bonnmotion/doc/README.pdf).

```
# bm
BonnMotion 3.0.1

OS: Linux 5.4.0-81-generic
Java: Private Build 1.8.0_292


Help:
  -h                            Print this help

Scenario generation:
  -f <scenario name> [-I <parameter file>] <model name> [model options]
  -hm                           Print available models
  -hm <module name>             Print help to specific model

Application:
  <application name> [Application-Options]
  -ha                           Print available applications
  -ha <application name>        Print help to specific application
```

### Acknowledging this work

If you use this software in a scientific publication, please cite the following paper:

```BibTeX
@INPROCEEDINGS{Baum2110:Coreemu,
AUTHOR={Lars {Baumg{\"a}rtner} and Tobias Meuser and Bastian Bloessl},
TITLE="coreemu-lab: An Automated Network Emulation and Evaluation Environment",
BOOKTITLE="2021 IEEE Global Humanitarian Technology Conference (GHTC) (GHTC 2021)",
ADDRESS=virtual,
DAYS=19,
MONTH=oct,
YEAR=2021,
KEYWORDS="Network Simulation; Disruption-Tolerant Networking; Automated Evaluation"
}
```

## Contributing

If you fix any bugs, have implemented other monitoring services or generate nice reports that might be helpful for others, please feel free to open a PR! 
