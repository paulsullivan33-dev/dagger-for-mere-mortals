# Dagger for Mere Mortals

Every project grows a **pipeline**: run the
tests, build the program, package it,
publish it. On your machine those steps
live in your head and your shell history.
On the CI server they live in a YAML file
written in that service's private dialect —
and the two lists drift apart until
somebody says the words *works on my
machine*. **Dagger** is a tool for writing
the pipeline once, as ordinary code in a
real programming language, and running it
in containers through one engine — so the
pipeline on your laptop and the pipeline
on any CI server are the same pipeline,
because they are the same functions.

This guide explains how that works: the
CLI you install and the **engine** it
starts for you, the **module** your
pipeline lives in, **functions** that take
a directory and return a tested container,
the caching and parallelism that fall out
of describing work instead of scripting
it, secrets and test databases handled as
types rather than strings, and the thin
wrapper that is all a CI service needs
once the logic has moved into your
repository. The limits are stated plainly,
including the largest one, which this
guide's own lab ran into head-first.

That limit governs how this guide was
made, and it is stated here rather than
discovered later: **Dagger does all of
its work in containers, and the lab
machine cannot start a container.** Its
sandbox forbids the operation containers
are made of. So the lab verified, for
real, everything up to the engine's door:
it installed the Dagger CLI (v0.21.11)
from the project's release tarball and
checked the download against the project's
published checksums; it read the CLI's
help and version; and it watched the
engine arrive — the full 650 MB image
pulled successfully, the engine container
created by name — and then fail to start,
with Docker's own error captured verbatim.
Everything past that door — writing and
calling functions, caching, secrets,
services, CI wiring — is taught from the
project's documentation and labelled as
documented-only wherever it appears.
`criteria.md` keeps the full ledger. On an
ordinary machine, where Docker runs
containers as a matter of course, the
documented half is simply what you will
do; the verified half is what your first
minutes look like, including the exact
shape of the failure you hope not to meet.

The guide's running example is a sample
project small enough to check by eye: a
twenty-line word-count program whose tests
the lab *did* run (with plain Python, the
way pipelines existed before engines), and
a two-function Dagger module written by
hand to the documented pattern, labelled
in its own header as never executed. No
fixture is modelled on any real person,
service or organisation.

## What this guide covers

- [**What Dagger is**](what-dagger-is.md) —
  the mental model: pipelines as code, one
  engine, and why the local run matters
- [**The moving parts**](the-moving-parts.md) —
  the CLI, the engine, modules and
  functions, the SDKs, the shell, the
  Daggerverse and Dagger Cloud
- [**Installing Dagger**](installing-dagger.md) —
  the install script, the lab's verified
  tarball-and-checksum route, and the
  engine's first arrival
- [**Your first module**](your-first-module.md) —
  `dagger init`, what a module contains,
  and where this guide's lab had to stop
- [**Writing functions**](writing-functions.md) —
  the shape of a function, the two
  generated examples read closely, and
  this guide's own module
- [**Calling functions**](calling-functions.md) —
  `dagger call`, Dagger Shell, and how to
  read a run's output tree
- [**Pipelines in CI**](pipelines-in-ci.md) —
  the thin GitHub Actions wrapper, what
  the CI server still does, and `dagger
  check`
- [**Caching and speed**](caching-and-speed.md) —
  caching by construction, parallelism by
  construction, and the cold-runner
  problem
- [**Secrets and services**](secrets-and-services.md) —
  secrets as a scrubbed type, and
  databases that live exactly as long as
  the tests
- [**Recipes**](recipes.md) — test before
  you push, publish on the right branch,
  borrow a module, debug at the scene,
  and one pipeline on two CI systems
- [**The neighbours**](the-neighbours.md) —
  CI YAML, Jenkins, Make, plain Docker,
  Earthly and Nix: what each does that
  Dagger doesn't, and vice versa
- [**Limits**](limits.md) — no containers,
  no Dagger; the privileged engine; the
  young, fast-moving API; and code's
  ordinary costs
- [**Troubleshooting**](troubleshooting.md) —
  the engine that will not start, in its
  several costumes, most of them met
  personally by this guide's lab
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Running the things a pipeline builds —
that is the Docker and Kubernetes guides'
country. Operating a CI service itself:
triggers, runner fleets and notifications
stay with the service, and chapter 7 says
what remains its job. Dagger Cloud as a
purchased platform is pointed at, not
taught. And the deep APIs of each SDK —
every core type and every method — belong
to the project's reference documentation;
this guide teaches the working core, in
one SDK, well enough that the reference
becomes readable.

## How to use this guide

Read chapter 1 for the model and the
honest note, and chapter 2 before
installing anything — knowing which piece
holds what turns the most common failure
("the engine never started") into a named
problem. Chapter 3 ends with a check you
can run in one minute: if `dagger version`
prints and `docker run hello-world`
works on your machine, you have already
cleared the bar this guide's lab could
not. Chapters 4 and 5 build the module;
chapter 6 runs it; chapter 7 is the one
that changes how your repository feels,
when the CI YAML shrinks to a wrapper. The
lab's transcripts live in
`dagger-lab/transcripts/`; its sample
project is `dagger-lab/project/` and its
hand-written module `dagger-lab/module/`;
its notes are `examples/lab-notes.txt`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Docker for Mere Mortals](https://paulsullivan33-dev.github.io/docker-for-mere-mortals/)
- [GitHub Actions for Mere Mortals](https://paulsullivan33-dev.github.io/github-actions-for-mere-mortals/)
- [Git for Mere Mortals](https://paulsullivan33-dev.github.io/git-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/dagger-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/dagger-for-mere-mortals/blob/main/LICENSE-CODE).
