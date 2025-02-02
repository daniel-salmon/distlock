# distlock
Implements a distributed lock client and server.

# Table of Contents
- [Client](#client)
- [Server](#server)
- [Usage](#usage)
  - [Threaded Server](#threaded-server)
  - [Async Server](#async-server)

## Client <a name="client"></a>

## Server <a name="server"></a>

## Usage <a name="usage"></a>

You have two options for running the server: threaded or async. Both options use
gRPC for communication, the difference is only in how the server is implemented.

The complete usage is:
```sh
$ distlock --help

 Usage: python -m distlock [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version               --no-version             Print the version number and exit [default: no-version]                             │
│ --address                               TEXT     Address on which to run the server [default: [::]]                                  │
│ --port                                  INTEGER  Port on which to run the server [default: 50051]                                    │
│ --max-workers                           INTEGER  Maximum number of workers for multithreaded server. Does not matter when running    │
│                                                  with --run-async.                                                                   │
│                                                  [default: 5]                                                                        │
│ --run-async                                      Should the server be run async?                                                     │
│ --install-completion                             Install completion for the current shell.                                           │
│ --show-completion                                Show completion for the current shell, to copy it or customize the installation.    │
│ --help                                           Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Threaded Server <a name="threaded-server"></a>

The threaded server is the default and can be run with the following command:

```bash
$ distlock
```

You can configure how many workers the server will use by passing the
`--max-workers` flag.

### Async Server <a name="async-server"></a>

The async server can be toggled on by passing the `--run-async` flag, e.g.:

```bash
$ distlock --run-async
```

The async server does not run multiple workers, it runs a single worker that
handles all requests concurrently. Therefore the `--max-workers` flag is not
used.
