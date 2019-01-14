# tsk

Bare-bones cross-platform process dispatcher and manager.

# Usage

```
python3 tsk.py [-h] [config]
```

## Optional Arguments

* `config`: the path to a JSON configuration file (it defaults to `~/.tsk.json`)

## Requirements

* Python 3.6+

## Setup

Prior to running, you must create a JSON configuration file that specifies the processes
to be managed, and optionally the directory in which to place the logs:

```json
{
  "logs": "~\\.tsk.log",
  "processes":
  [
    {
      "name": "DB",
      "cmd": "docker-compose up database",
      "pwd": "~\\workspace"
    },
    {
      "name": "Azure Storage Emulator",
      "cmd": "\"C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\Storage Emulator\\AzureStorageEmulator.exe\" start -inprocess",
      "pwd": null
    }
  ]
}
```

## Logs

Each process is logged in its own log file in the specified `logs` directory.
Any existing log files are appended (meaning that they can get large).

If no `logs` directory is specified in the configuration file, it defaults to
`~/.tsk.log/`.

# Thanks

Cross-platform `getch` implementation from [this Gist](https://gist.github.com/jfktrey/8928865)
by jfktrey.

# License Information

Written by Gem Newman. [Website](http://spurll.com) | [GitHub](https://github.com/spurll/) | [Twitter](https://twitter.com/spurll)

This work is licensed under the [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/).

Remember: [GitHub is not my CV](https://blog.jcoglan.com/2013/11/15/why-github-is-not-your-cv/).

