# Writing Functions

Everything in Dagger that does work is a
**function**: a method in your module's
code, written in your SDK language,
following one convention — it must be
*visible* to Dagger. This chapter reads
the two example functions every new module
is born with, then the two functions of
this guide's own module. All of it is
documented-only in this guide: the lab
could not run a function, and the code
below is presented as the project's
documentation presents it, checked line by
line against the documented API. It is in
the lab folder (`dagger-lab/module/`), and
its header says what it is.

## The shape of a function

In the Python SDK, a module is a class
marked `@object_type`, and a function is a
method marked `@function`. The marks are
the whole ceremony: Dagger inspects the
class, and each marked method becomes a
callable unit with typed arguments and a
typed result. (Go uses exported methods on
a struct; TypeScript uses decorators the
same way.)

The generated example a Python module
starts with, from the project's
documentation:

```python
import dagger
from dagger import dag, function, object_type

@object_type
class MyProject:
    @function
    def container_echo(self, string_arg: str) -> dagger.Container:
        """Returns a container that echoes whatever string argument is provided"""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])
```

Read it as a sentence. `dag` is the
client — your handle on the engine.
`dag.container()` starts describing a
container; `.from_("alpine:latest")` says
which image; `.with_exec(["echo",
string_arg])` adds a step to run. Nothing
has *happened* yet: the function returns
the description — a `dagger.Container`
value — and the engine works out the graph
of operations (chapter 2) and executes it
when the value is demanded. This
describe-first style is the idiom of the
whole API, in every SDK: chains of
`with_...` calls build a container,
directory or file description, and a final
call like `.stdout()`, `.publish()` or
`.export()` makes it real.

The second generated example adds the
other everyday ingredients — a directory
argument, and awaiting a result:

```python
    @function
    async def grep_dir(self, directory_arg: dagger.Directory, pattern: str) -> str:
        """Returns lines matching a pattern in the directory's files"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_directory("/src", directory_arg)
            .with_workdir("/src")
            .with_exec(["grep", "-R", pattern, "."])
            .stdout()
        )
```

Arguments arrive as Dagger types, not
paths: `directory_arg` is a `Directory`,
a snapshot of files the engine holds,
which `.with_directory("/src", ...)`
places inside the container. And because
`.stdout()` must ask the engine for a
finished result, the function is `async`
and awaits it. Returning a description
(container, directory, file) needs no
await; asking for a *value from inside the
work* (output, an exit code, a file's
contents) does.

## This guide's module

The lab's hand-written module,
`dagger-lab/module/main.py`, wraps the
verified wordcount project of chapter 4 in
two functions of the same shapes:

```python
@object_type
class Wordcount:
    @function
    async def test(self, source: dagger.Directory) -> str:
        """Run the project's unit tests in a Python container
        and return the test runner's output."""
        return await (
            dag.container()
            .from_("python:3.12-slim")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["python", "-m", "unittest", "-v"])
            .stdout()
        )

    @function
    def container(self, source: dagger.Directory) -> dagger.Container:
        """Return a container holding the project, ready to run
        wordcount.py or to be published as an image."""
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_entrypoint(["python", "wordcount.py"])
        )
```

Two design habits to copy, wherever you
go next:

- **The pipeline takes the source as an
  argument.** `test --source=.` hands the
  function whatever directory the caller
  means — your checkout today, a CI
  checkout tomorrow, a directory another
  function produced. Functions that reach
  out and grab the host filesystem by path
  give that portability away.
- **The toolchain is named in the
  function.** `python:3.12-slim` is the
  Python the tests run under — on your
  machine, on the CI server, next year.
  Compare the direct run of chapter 4,
  which used whatever Python the lab
  machine happened to have. Pinning like
  this is the mundane half of "works on my
  machine" going away.

What the lab *could* verify about this
code: the file is valid Python
(`python3 -m py_compile` accepts it), the
project it wraps passes its tests for real
(transcript t10), and every API call in it
matches the project's documented Python
SDK — the same calls the generated
examples use. What it could not verify is
the run itself. On a machine with an
engine, chapter 6 is how you would call
it.

## Functions calling functions

A function may call another — in code, not
in YAML. A `ci` function that runs the
tests and then builds the container is an
ordinary method calling two others, in the
project's docs' own pattern; functions
from *other* modules appear on `dag` by
their module's name, so a pipeline can
scan the image it just built with a
published security module and publish only
if the scan passes. Composition is not a
feature bolted on; it falls out of
functions being functions. Chapter 10's
recipes lean on this, and chapter 7 shows
why it matters in CI: the wrapper YAML
calls one function, and the *pipeline*
decides the rest.
