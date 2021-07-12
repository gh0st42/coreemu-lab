coreemu-lab
===========

*coreemu-lab* (short: *clab*) is an environment for automated evaluation of networking software.
It should work headless on any platform that can run [Docker](https://www.docker.com/) and with X11 it has been successfully tested on Linux and macOS.

The main features provided by *clab*:

- emulated network nodes based upon Linux namespaces (provided through [coreemu](https://github.com/coreemu/coreemu)
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

## Contributing

If you fix any bugs, have implemented other monitoring services or generate nice reports that might be helpful for others, please feel free to open a PR! 