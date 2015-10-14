# Studio

Studio is an infrastructure for recording workload patterns.

The infrastructure illustrates the recording technique with respect to two
benchmark suites, namely,

* [PARSEC](http://parsec.cs.princeton.edu) and
* [SPEC CPU2006](https://www.spec.org/cpu2006).

Following the illustration, Studio can be extended to record other programs.

## Installation

The following software is assumed to be available:

* [Redis](http://redis.io) and
* [SQLite](https://sqlite.org).

Refer to the corresponding websites for further instructions.

The underlying simulation is based on [Sniper](http://snipersim.org). Therefore,
Sniper should be properly installed as well. This process is described on the
[Getting Started](http://snipersim.org/w/Getting_Started) page.

Sniper provides a tight integration with the aforementioned benchmark suites.
However, the benchmarks should be installed separately, which is described on
the [Download Benchmarks](http://snipersim.org/w/Download_Benchmarks) page.

The final component to install is
[Recorder](https://github.com/learning-on-chip/recorder), which is the tool that
collects data from Sniper and performs the actual recording of workload
patterns. The tool is a part of
[Toolbox](https://github.com/learning-on-chip/toolbox). The installation
instructions of Toolbox are given on the corresponding page.

Finally, in order to discover the locations of Sniper, the benchmarks, and
Toolbox, Studio relies on the following three environment variables, which
should be set accordingly:

* `SNIPER_ROOT` (should point at Sniper’s directory),
* `BENCHMARKS_ROOT` (should point at the benchmarks’ directory), and
* `TOOLBOX_ROOT` (should point at Toolbox’s directory).

## Contributing

1. Fork the project.
2. Implement your idea.
3. Open a pull request.
