# `stl-repair`

Use blender to repair STLs

**Usage**:

```console
$ stl-repair [OPTIONS] FILEPATH COMMAND [ARGS]...
```

**Arguments**:

* `FILEPATH`: The path to either a single STL file to repair or a directory full of stls  [required]

**Options**:

* `-o, --output PATH`: Where to write repaired files to  [required]
* `-s, --suffix TEXT`: Suffix to append to output files  [default: _fixed]
* `--debug`: Print extra information for debugging.
* `--version`: Print version number.
* `--help`: Show this message and exit.

**Commands**:

* `repair_stls`

## `stl-repair repair_stls`

**Usage**:

```console
$ stl-repair repair_stls [OPTIONS] FILEPATH
```

**Arguments**:

* `FILEPATH`: The path to either a single STL file to repair or a directory full of stls  [required]

**Options**:

* `-o, --output PATH`: Where to write repaired files to  [required]
* `-s, --suffix TEXT`: Suffix to append to output files  [default: _fixed]
* `--debug`: Print extra information for debugging.
* `--version`: Print version number.
* `--help`: Show this message and exit.
