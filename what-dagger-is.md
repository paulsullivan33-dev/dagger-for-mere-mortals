# What Dagger Is

Most projects of any size have a
**pipeline**: a list of things that must
happen, in order, before the work can be
trusted. Run the tests. Build the program.
Package it into a container image. Publish
the image. On a developer's own machine
those steps live in shell commands and
memory. On a **CI server** (CI is
*continuous integration* — a service that
builds and tests every change) they live
in a YAML file written in the CI service's
own dialect: GitHub Actions YAML, GitLab
CI YAML, and so on. The two lists drift
apart, and the difference has a name every
programmer knows: *works on my machine*.

**Dagger is a tool for writing the
pipeline once, as code, and running it
identically in both places.** You write
**functions** in a real programming
language — Go, Python or TypeScript are
the official choices — and each function
describes work done inside **containers**:
start from this image, add my source code,
run this command. A program called the
**Dagger Engine** carries out the work.
The CI server's job shrinks to a thin
wrapper that calls your functions, so the
pipeline logic lives in your repository,
in a language your editor and your tests
understand, instead of in a hosting
service's YAML.

Two consequences follow, and they are the
whole point:

- **The pipeline runs locally.** The same
  `dagger call test` you run on your laptop
  is what the CI server runs. You can debug
  a failing pipeline before pushing, with a
  real debugger, instead of pushing and
  reading logs.
- **Every step happens in a container the
  function describes.** The tools the
  pipeline needs — a specific Python, a
  specific compiler — are pinned in code,
  not left to whatever happens to be
  installed on a shared CI runner.

## The honest note, stated before everything else

This series runs its tools for real and
says plainly what it could not run. This
guide's lab machine could not start a
single container — its sandbox forbids the
operation containers are made of — and
Dagger does *all* of its work in
containers. So this guide is in two
halves, and each chapter keeps them
separate:

- **Verified in the lab:** the Dagger CLI
  itself — installing it, checking its
  download against the project's published
  checksums, its version and help text, and
  the engine's first arrival, which the lab
  watched in detail: the engine image
  (about 650 MB) downloaded completely,
  and the engine container was created —
  and then could not be started. The exact
  error is a transcript in the lab folder
  and the subject of chapter 13.
- **Taught from the documentation:**
  everything past the engine's door —
  writing modules, calling functions,
  caching, secrets, CI wiring. Wherever a
  procedure is documented only, the text
  says so, and `criteria.md` keeps the full
  ledger.

If your machine can run Docker — most
ordinary machines can — the documented
half is the part you will simply do, and
the verified half tells you what the first
minutes look like, including the failure
shapes worth recognising. Chapter 12 is
frank about the deeper point: Dagger's
power and Dagger's main limit are the same
fact, that nothing at all happens without
a working container runtime.

## A familiar shape

Dagger has two pieces you will meet in
chapter 2: the **CLI**, the `dagger`
command, which is all you install; and the
**engine**, a container the CLI starts for
you on first use and then talks to. Your
pipeline code lives in a **module**: a
folder holding a small configuration file,
`dagger.json`, and source code in one of
the SDK languages. Functions from a module
can call functions from other modules —
there is a public library of them, the
**Daggerverse** — and everything is glued
together by one API: ask for a container,
a directory, a file, a secret, and chain
the operations.

A first taste, after installing
(chapter 3), on a machine where Docker
runs:

```bash
cd my-project
dagger init --sdk=python
dagger functions
dagger call container-echo --string-arg="hello"
```

The first command turns the folder into a
module and generates example code. The
second lists the functions the module
offers. The third runs one: the generated
example that starts an Alpine container
and echoes your string from inside it.
None of these three ran on the lab
machine — the first of them already needs
the engine, which is itself a finding, and
chapter 4 walks it in detail. The commands
above are the documented shape of a first
session, shown here so this chapter's
model has names attached.

Check — the part of a first session the
lab *could* perform, the CLI introducing
itself (transcript
`dagger-lab/transcripts/t00-version.txt`):

```text
$ dagger version
dagger v0.21.11 (image://registry.dagger.io/engine:v0.21.11) linux/amd64
```

Read that line closely; it teaches the
architecture. The CLI is version 0.21.11,
and it names the engine it wants — not a
program on your disk, but a container
image, `registry.dagger.io/engine`, at the
matching version. Chapter 3 follows that
image home.

## Who it is for

The developer whose CI YAML has become a
program in its own right — conditionals,
loops faked with matrices, strings copied
between files — and who would rather write
that program in a language with functions
and types. The team that maintains the
same pipeline in two CI dialects. The
careful beginner who wants to run the real
pipeline before pushing, not after. The
common thread is a pipeline that has
outgrown its YAML.

## What it is not

Dagger is not a CI service: it runs no
machines for you, watches no repositories,
and sends no notifications. Your existing
CI (chapter 7) remains the trigger and the
scheduler; Dagger replaces the *contents*
of the steps. It is not a container tool
in Docker's sense either — you will not
use it to run a web server in production.
It builds, tests and publishes; running
the result is somebody else's chapter (the
series' Docker and Kubernetes guides live
there). And it is not free of its own
platform: the engine is a privileged
container, and chapter 12 counts that cost
plainly.
