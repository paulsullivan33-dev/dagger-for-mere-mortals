# Glossary

**Blueprint** — a module used as the
starting template for a new one
(`dagger init --blueprint=...`, chapter 4).

**Caching** — the engine's reuse of an
operation's stored result when it is asked
for exactly that operation again; keyed by
the operation's inputs (chapter 8).

**CI** — continuous integration: a service
that builds and tests every change to a
project. Dagger supplies the pipeline; a
CI service still supplies the trigger
(chapter 7).

**CLI** — the `dagger` command: the only
part you install, and the engine's remote
control (chapter 2).

**Container** — one of Dagger's core
types: a described container (image,
files, environment, commands) that a
function can return, publish or run.

**DAG** — directed acyclic graph: the
graph of operations the engine builds
from your function calls, giving
parallelism and caching their structure.
The source of the project's name
(chapter 2).

**dagger.json** — a module's declaration
file: name, SDK, engine version
(chapter 4).

**Dagger Cloud** — the project's optional
hosted service: run traces, shared cache,
and managed CI checks (chapter 2).

**Dagger Shell** — the interactive face:
the API as shell commands, for exploring
and one-off work (chapter 6).

**Daggerverse** — the public catalogue of
shared modules a pipeline can depend on
and call (chapters 2 and 10).

**Directory / File** — core types: a
snapshot of files, held by the engine and
passed between functions and containers —
never a path on the host (chapter 5).

**Engine** — the long-lived privileged
container that executes all pipeline work;
provisioned by the CLI as
`dagger-engine-<version>` (chapters 2
and 3).

**Function** — the unit of pipeline work:
a marked method in a module's code, with
typed arguments and a typed result,
callable from the CLI, CI, or other
functions (chapter 5).

**Module** — a directory of pipeline code
with a `dagger.json` at its root
(chapter 4).

**Provisioning** — the CLI's starting of
the engine: pull the image, run the
container, connect (chapter 3). Can also
be done by hand and pointed to with
`_EXPERIMENTAL_DAGGER_RUNNER_HOST`.

**SDK** — the generated client library
(Go, Python, TypeScript officially) that
module code uses to describe work to the
engine (chapter 2).

**Secret** — a core type whose value the
engine scrubs from outputs, passed by
reference (`env:...`, `file:...`) and
mounted or set only where needed
(chapter 9).

**Service** — a container run to be
talked to — a database during tests —
bound into another container under a name
and managed by the engine for the run's
lifetime (chapter 9).

**Trace** — the full record of a run,
viewable from the URL the CLI prints
(chapter 6).

**Wrapper** — the thin CI configuration
(three steps, chapter 7) whose only job
is to call the module's functions.
