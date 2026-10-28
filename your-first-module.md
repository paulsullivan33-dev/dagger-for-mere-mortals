# Your First Module

A **module** is where your pipeline lives:
an ordinary project folder, made special
by one small file. This chapter creates
one the documented way, shows exactly
where this guide's lab had to stop, and
then walks the result on paper — clearly
labelled — so the chapters after this one
have something concrete to talk about.

## Creating a module

From the project's documentation: stand in
(or name) the folder that should become a
module, choose an SDK, and run:

```bash
dagger init --sdk=python
```

Useful variations, from `dagger init
--help` (transcript
`dagger-lab/transcripts/t04-init-help.txt`,
one of the help pages the lab could read
without an engine):

```bash
dagger init --sdk=go my-pipeline        # in a new folder
dagger init --sdk=typescript            # TypeScript instead
dagger init --blueprint=github.com/example/blueprint
```

A **blueprint** is another module used as
the starting template — the shape of a
pipeline someone else already got right.

What `init` then does, per the
documentation: it starts the engine (the
ceremony of chapter 3), writes
**`dagger.json`**, installs the SDK into
the folder — for Python, a `pyproject.toml`,
a generated `sdk/` package, and your code
under `src/<module_name>/` with a
`main.py` — and generates **two example
functions**, so a fresh module does
something before you write a line:
`container-echo`, which runs `echo` in an
Alpine container, and `grep-dir`, which
searches a directory's files for a pattern
and returns the matches. Chapter 5 reads
both.

## Where the lab stopped

The lab ran the plain command in an empty
folder and kept the transcript
(`dagger-lab/transcripts/t03-init-plain.txt`).
It is worth knowing what a first `init`
looks like from the inside, because on a
slow machine you will watch the same
screen: connect, engine, image pull —
hundreds of layer lines — engine start.
The lab's copy of that transcript runs to
442 lines, nearly all of it the engine
image arriving. At the engine's start the
lab's story ends the way chapter 3
described: the container existed and would
not start, and the lab stopped the command
after a minute with nothing written to the
folder at all:

```text
$ ls -la
total 0
```

No `dagger.json`, no scaffold, no partial
module. That emptiness is itself the
chapter's verified content, and it is more
useful than it looks:

- **`init` is not a local scaffolding
  tool.** The SDK installation and code
  generation are work the *engine* does —
  the CLI asks, the engine generates. A
  machine that cannot start the engine
  cannot even begin a module the official
  way.
- **Nothing is half-created.** The failure
  happens before any file is written, so
  there is no broken state to clean up:
  fix the engine problem, run the same
  command again.

## The module, on paper

Since the lab could not generate one, this
guide's example module was **written by
hand**, to the documented pattern, and it
lives in the lab folder at
`dagger-lab/module/` — `dagger.json` and
`main.py`, with a banner comment in the
code saying exactly that. It is *not* a
transcript and has never been executed;
treat it the way you would treat an
example in the project's own docs, which
is where its shape comes from. The
`dagger.json` is three facts:

```json
{
  "name": "wordcount",
  "engineVersion": "v0.21.11",
  "sdk": {
    "source": "python"
  }
}
```

- **`name`** — the module's name. Function
  calls and other modules refer to the
  module by it.
- **`engineVersion`** — the engine version
  the module was created with. The CLI
  checks this: a module is a contract with
  a particular engine, and mismatches are
  reported, not silently absorbed.
- **`sdk.source`** — the language the
  functions are written in.

One more proof that `dagger.json` alone is
not a working offline module: the lab
wrote exactly this file into a folder and
asked for `dagger config` — the command
that merely reads a module's configuration.
It went straight to the engine and failed
there in 0.6 seconds (transcript t06). The
file is a *declaration*, and declarations
are interpreted by the engine; there is no
mode in which the CLI reads it alone. On a
machine with a running engine, the same
command lists the module's configuration
and dependencies — documented-only here.

## The sample project

The module exists to serve a project, and
the lab's project is real, small and
verified: `dagger-lab/project/` holds
`wordcount.py` — a twenty-line program
that counts lines, words and characters in
a text file, in the spirit of the Unix
`wc` — its tests, and a two-line sample
text. Its tests are the one part of this
guide's pipeline story that ran end to end
(transcript
`dagger-lab/transcripts/t10-project-tests-local.txt`):

```text
$ python3 -m unittest -v
test_empty (test_wordcount.CountTests.test_empty) ... ok
test_one_line (test_wordcount.CountTests.test_one_line) ... ok
test_two_lines (test_wordcount.CountTests.test_two_lines) ... ok
OK
$ python3 wordcount.py sample.txt
2 9 44 sample.txt
```

Run directly, on the lab machine, with
plain Python — which is precisely what a
pipeline is supposed to improve on: the
same tests, run inside a container the
function describes, with a pinned Python,
identically on every machine. That
improvement is chapter 5's function, and
on the lab machine it remains a sentence
in the documentation tense. The project,
at least, is proven ready for it.
