# tsk

Bare-bones cross-platform process dispatcher and manager.

# Usage

Create a configuration file, then run with:

```
python3 tsk.py [config]
```

where `config` is the (optional) path to a JSON configuration file, defaulting to
`~/.tsk.json`.

## Requirements

* Python 3.6+

## Configuration

Prior to running, you should create a JSON configuration file that specifies the processes
to be managed, and optionally the directory in which to place the logs:

```json
{
  "logs": "~\\.tsk.log",
  "log-archive": 5,
  "processes":
  [
    {
      "name": "DB",
      "cmd": "docker-compose up database",
      "stop": "docker-compose stop database",
      "cwd": "~\\workspace"
    },
    {
      "name": "Azure Storage Emulator",
      "cmd": "\"C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\Storage Emulator\\AzureStorageEmulator.exe\" start -inprocess",
      "stop": "\"C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\Storage Emulator\\AzureStorageEmulator.exe\" stop",
      "timeout": 10
    }
  ]
}
```

If tsk cannot find a configuration file at startup, it will create an example file.

### Process Fields

* `name`: The name tsk will use to refer to this process
* `cmd`: The command that will be issued to start the process
* `stop` (optional): The command that will be issued to stop the process
* `cwd` (optional): The directory to use as the current working directory for both `cmd`
  and `stop`
* `timeout` (optional): The number of seconds to wait after issuing `stop` before
  killing the process (defaults to 30 seconds)

# Managing Processes

Each process specified in the configuration file is assigned a number. If the process is
not running, pressing the associated key will start the process. If the process is already
running, pressing the key will stop the process.

## Process Status

The status listed for each process is updated when the screen is refreshed. To refresh,
simply press any key other than those listed for process management (e.g., spacebar).

## Stopping a Process

If the configuration file specifies a specific stop command for the process, attempting to
stop the process will result in this command being issued, at which point tsk will wait
for the process to stop. An optional `timeout` for the stop command may be specified
(defaulting to 30 seconds).

If no stop command is specified (or if the stop process times out), tsk will force the
process to stop by issuing a kill command.

# Logging

Each process is logged in its own log file in the specified `logs` directory.
If no `logs` directory is specified in the configuration file, it defaults to
`~/.tsk.log/`.

When a process is started, any existing log file is placed in a zip archive, and only the
last few are kept. The number of past logs to keep is specified by `log-archive` in the
configuration file (defaulting to 5).

# Thanks

Cross-platform `getch` implementation from [this Gist](https://gist.github.com/jfktrey/8928865)
by jfktrey.

# License Information

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

Remember: [GitHub is not my CV](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/).

