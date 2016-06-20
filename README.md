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

In order to discover the locations of Sniper and the benchmarks, Studio relies
on the following three environment variables, which should be set accordingly:

* `SNIPER_ROOT` (should point at Sniper’s directory) and
* `BENCHMARKS_ROOT` (should point at the benchmarks’ directory).

Finally, the collection of data from Sniper and recording of workload patterns
is delegated to [Recorder](https://github.com/learning-on-chip/recorder). The
tool is included in this repository and should be compiled as follows:

```bash
make install
```

## Contribution

1. Fork the project.
2. Implement your idea.
3. Open a pull request.
