# Calling Functions

Functions are called three ways: from the
command line with `dagger call`, from a
terminal with **Dagger Shell**, and from
other functions in code (chapter 5). This
chapter is about the first two — the ways
a person, or a CI wrapper, drives a
pipeline. It is documented-only in this
guide: every call below needs the engine,
and the lab's transcripts show the calls
reaching the engine's door and no further.
The command *shapes*, though, are pinned
down by help text the lab did capture, and
by the project's documentation.

## Listing what a module offers

```bash
dagger functions
```

prints the functions of the module in the
current directory (or of the module named
with `-m`), with their arguments — the
discovery command, and the first one to
run in an unfamiliar module. Its help page
is static, and the lab captured it
(transcript
`dagger-lab/transcripts/t07-functions-help.txt`);
the listing itself is generated from the
loaded module, so the command proper needs
the engine, like everything that touches a
module.

## dagger call

```bash
dagger call test --source=.
dagger call container --source=. export --path=./image.tar
dagger call container-echo --string-arg="hello from a container"
```

The grammar is the module's shape, spelled
on the command line:

- The function's name, with dashes where
  the code has underscores (`container_echo`
  in Python is `container-echo` here).
- Each argument as `--name=value`.
  Directories and files are given as paths
  on the host and handed over as Dagger
  values; secrets are given as references
  (`env:NAME`, `file:path`, chapter 9), never
  as literal values if you can help it.
- A function that returns a `Container`,
  `Directory` or `File` is not finished at
  its name: you chain a *terminal* command
  — `export`, `publish`, `stdout` and their
  kin — to say what should become of the
  value. A function returning a string or a
  number simply prints it.

Calls chain across functions, too:
`dagger call build test` style sequences
and shell-like pipelines are how a single
command line runs a whole pipeline. What
you get back is the run's progress tree —
each operation, its timing, its cache
status (chapter 8) — and, for failures,
the failing step's output, with the option
of opening a terminal inside the failed
container to inspect it where it fell
(the `--interactive` flag of the main help
page, transcript t02; a debugging aid the
documentation is proud of, and this guide
could not try).

One verified oddity belongs here. The help
for `dagger call` is *not* static: it is
generated from the module being called, so
asking for it loads the module, which
starts the engine. The lab's request
(transcript
`dagger-lab/transcripts/t08-call-help-needs-engine.txt`)
reads, in full, as an engine-start attempt
ending in the family error:

```text
Error: start engine: failed to start container: failed to run command [docker start dagger-engine-v0.21.11]: exit status 1
```

Keep that in mind when a `dagger` command
behaves surprisingly on a broken machine:
even its questions go through the engine.

## Dagger Shell

`dagger` with no subcommand — or
`dagger -c '<command>'` for a single
shot — opens **Dagger Shell**, an
interactive shell whose commands are the
API itself, named like the types:
`container`, `directory`, `host`, and your
modules' functions alongside them, chained
with pipes and the shell's own syntax.
It is the exploratory face of the same
engine: the place to discover what a
container holds, try a chain before
committing it to a function, or drive a
one-off job. Completion, history and help
live inside it. Documented-only here —
the shell, too, begins by connecting.

## Reading a run

Whether from `call` or the shell, a run
reports itself the same way, and the lab's
failed attempts are, usefully, legible
examples of the format (transcript t03):
numbered steps in a tree, each step's
command and its duration, `DONE` or
`ERROR` against the branch that decided
the outcome, and a trace URL at the end
(the trace is the run's full record;
chapter 2 covers Dagger Cloud's part in
it). Two habits follow. Read a failed run
from the first `ERROR` upward — the tree
shows which branch failed and which were
still in flight. And remember that the
progress display is a *rendering*: in
scripts and CI logs, `--silent` and the
plain output modes give you the same facts
as text (the flags are on the captured
help page, transcript t02).
