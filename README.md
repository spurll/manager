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

## Setup

Prior to running, you must create a JSON configuration file that specifies the processes
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
      "stop": "\"C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\Storage Emulator\\AzureStorageEmulator.exe\" stop"
    }
  ]
}
```

## Starting and Stopping Processes

Each process specified in the configuration file is assigned a number. To start the
process, press the appropriate key. To stop it, press the key again. If the configuration
file specifies a specific stop command, this command will be issued; if no stop command is
specified (or if the process has already been asked to stop and remains running), tsk will
attempt to force the process to stop by issuing a kill command (or using `taskkill` on
Windows).

## Logs

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

