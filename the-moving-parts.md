# The Moving Parts

Dagger looks like one command, but a run
involves five pieces. Knowing which piece
holds what is the difference between "the
pipeline is broken" and "the engine never
started" — a real distinction, as this
guide's own lab learned (chapter 13).

## The CLI

The **`dagger` command** is the only thing
you install: one static program, no
dependencies of its own. It parses your
command, finds or starts an engine, loads
your module, and shows you the run —
progress as a tree of steps, each with its
timing, and a link to a trace of the run
afterwards. Some commands are the CLI
alone and work anywhere: `dagger version`,
`dagger --help`, and the shell-completion
generator all answered on the lab machine
with no engine present (transcripts
t00–t02, t05). Almost everything else —
including, surprisingly, `dagger init` and
`dagger config` — begins by connecting to
an engine; chapter 4 shows the lab proving
exactly that.

## The engine

The **Dagger Engine** is where work
happens. It is distributed as a container
image (`registry.dagger.io/engine`), and
the CLI provisions it for you: on the
first command that needs it, the CLI pulls
the image through your container runtime
and starts it as a long-lived, privileged
container named `dagger-engine-<version>`.
From then on the CLI talks to it over its
API, and later commands reuse it.

The lab watched this happen, once, in full
(transcript
`dagger-lab/transcripts/t90-engine-attempt.txt`):

```text
5   : ┆ ┆ ┆ exec docker pull registry.dagger.io/engine:v0.21.11
...
5   : ┆ ┆ ┆ [1m53s] | Status: Downloaded newer image for registry.dagger.io/engine:v0.21.11
6   : ┆ ┆ ┆ exec docker run --name dagger-engine-v0.21.11 -d --restart always -v /var/lib/dagger --privileged registry.dagger.io/engine:v0.21.11 --debug --debugaddr 127.0.0.1:6060
6   : ┆ ┆ ┆ [1.0s] | WARNING: IPv4 forwarding is disabled. Networking will not work.
```

That `docker run` line is worth reading:
the engine is **privileged** (it must be —
it starts containers of its own, through a
copy of BuildKit, the same builder that
powers Docker's own builds), it keeps its
data in a volume at `/var/lib/dagger`
(that is where the cache of chapter 8
lives), and it is set to restart always.
On the lab machine the story ends one step
later — the container was created and
refused to start — but on an ordinary
machine this is the whole ceremony, and it
happens once.

You can also provision the engine yourself
and point the CLI at it (the
`_EXPERIMENTAL_DAGGER_RUNNER_HOST`
environment variable) — on a shared CI
runner, or in Kubernetes. That is
documented-only in this guide.

## Modules and functions

Your pipeline code lives in a **module**:
a directory whose root holds
**`dagger.json`** — name, chosen SDK, the
engine version it was made with — plus the
source code. The unit of work is the
**function**: an ordinary method in your
chosen language, marked so Dagger can see
it (in Python, a decorator; chapter 5).
Functions take arguments and return
results of Dagger's core types —
`Container`, `Directory`, `File`,
`Secret`, `Service` — or plain strings and
numbers. A function can be called from the
command line (`dagger call`), from another
function in the same module, or from a
function in a different module written in
a different language: the API underneath
is the same for every SDK, so a Python
pipeline can call a Go module's function
and hand it a directory.

Underneath, the engine builds a **directed
acyclic graph** (DAG — the source of the
name) of the operations your function
asked for: this container from that image,
with this directory mounted, running these
commands. Independent branches of the
graph run in parallel, and every result is
cached by its exact inputs — chapter 8 is
about what that buys you.

## The SDKs

The official SDKs are **Go**, **Python**
and **TypeScript**; community SDKs exist
for other languages (PHP, Java, Rust,
.NET and more, at varying maturity). The
SDK is what `dagger init --sdk=...`
installs into your module: it generates
the client code your functions use to talk
to the engine, so your code imports a
`dag` object and chains calls —
`dag.container().from_(...)` in Python,
`dag.Container().From(...)` in Go. Your
language's normal tooling applies: types,
tests, a debugger, libraries.

## The shell

Recent versions add **Dagger Shell**: an
interactive (and scriptable) shell whose
commands are the same API — type the chain
instead of writing a function, handy for
exploring. `dagger -c '...'` runs one
shell command. It is the same engine
underneath, and it needs the engine just
as much: nothing in this guide's lab could
run it, and its details here are
documented-only.

## The Daggerverse and Dagger Cloud

The **Daggerverse** is the project's
public catalogue of shared modules — a
function for scanning an image, deploying
to a platform, running a linter — which
your module can depend on and call like
its own (chapter 10 has the shape of
this). **Dagger Cloud** is the optional
hosted service: runs are traced there (the
CLI prints a trace URL for each run; the
trace works without an account for setup,
and an account keeps history and enables
the `dagger check` CI integration of
chapter 7). Nothing in this guide requires
an account, and the lab disabled telemetry
for its runs.

## Who holds what, when it breaks

- The **CLI** holds the conversation and
  the display; it does no building itself.
- The **engine** holds the cache, the
  containers, and the truth about a run.
  If it is not running, nothing else in
  this chapter can save you.
- The **container runtime** (usually
  Docker) holds the engine. It is the
  floor everything stands on — and the
  lab's floor is exactly where its story
  stops (chapters 13 and 14).
- The **module** holds the pipeline logic,
  in your repository, in your language —
  which is the arrangement the whole tool
  exists to give you.
