# Studio

Studio is an infrastructure for recording workload patterns.

The infrastructure currently illustrates the recording technique with respect to
two benchmark suites, namely,

* [PARSEC](http://parsec.cs.princeton.edu) and
* [SPEC CPU2006](https://www.spec.org/cpu2006).

Following the illustration, Studio can be extended to record other programs.

## Installation

The following software is assumed to be installed:

* [Redis](http://redis.io) and
* [SQLite](https://sqlite.org).

Refer to the corresponding websites for further instructions.

The underlying simulation is based on [Sniper](http://snipersim.org). Therefore,
Sniper should be installed as well. This process is described
[here](http://snipersim.org/w/Getting_Started). Sniper should be installed
together with the benchmarks, which is described
[here](http://snipersim.org/w/Download_Benchmarks).

Having installed Sniper and the benchmarks, the following two environment
variables should be set:

* `SNIPER_ROOT` (points at Sniper’s directory) and
* `BENCHMARKS_ROOT` (points at the benchmarks’ directory).
