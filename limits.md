# Limits

What Dagger cannot do, and what it asks of
you in return — the chapter the rest of
the guide has been promising. This guide
is unusually placed to write it: its lab
met the first limit head-on and never got
past it.

## Nothing happens without a container runtime

Dagger's engine is a container, and every
unit of work is a container. A machine
that cannot run containers — a restricted
sandbox, a nested environment without the
needed privileges, an architecture the
engine image does not cover — cannot use
Dagger at all. Not slowly, not partially:
the CLI installs, the help pages print,
and the first real command stops at the
engine's door, exactly as chapters 3 and 4
recorded. "The pipeline runs anywhere"
means, precisely, *anywhere containers
run*. On today's infrastructure that is
nearly everywhere a pipeline would want to
be — and it is a floor, not a detail, and
a team adopting Dagger should test its
runners for it on day one (CI systems that
forbid privileged containers are the
recurring real-world case; the documented
answer is an externally provisioned
engine, chapter 7).

## The engine is privileged

The engine container runs with
`--privileged` — it must, to start
containers of its own — and it holds your
pipeline's secrets while it works and your
cache afterwards. That is a real security
posture to accept, not a footnote: a
privileged container is most of the way to
root on its host. Run the engine where you
would run Docker itself (the same trust,
in practice), be thoughtful about engines
shared between teams, and treat borrowed
Daggerverse modules (chapter 10) as code
running inside that posture — because it
is.

## The local run is local

"The same pipeline" is true of the
pipeline: functions, containers, inputs.
It is not true of the world around it.
Your laptop and the CI runner differ in
CPU architecture (an ARM laptop and an
x86 runner build different binaries unless
the pipeline says otherwise — multi-platform
builds are supported and must be asked
for), in network (a step that reaches an
internal service reaches it from one
machine and not the other), and in the
secrets present. Dagger narrows "works on
my machine" to the pipeline itself, which
is most of the disease — not all of it.

## A young, fast-moving tool

The version line in chapter 3 says
0.21.11: a pre-1.0 project that ships
often and still changes its API between
minor versions. Modules record their
engine version, and the CLI enforces the
pairing, so old pipelines keep working
with their own engine — but the surface
you write against evolves, SDKs trail the
engine at different speeds, and community
SDKs trail further. Budget for upgrades
the way you would for any young
infrastructure tool, and expect this
guide's details to age faster than its
model.

## The pipeline is code — with code's costs

Everything chapter 1 celebrated has a
price side. A pipeline in a real language
can be over-engineered like any program:
abstractions nobody needed, a framework
where a function would do. It needs its
own tests and its own review discipline.
Debugging moves from "read the YAML,
push, wait" to real debugging — better in
every way except that it asks for a
programmer's skills at the moment of
failure, which not every pipeline owner
has or wants. And the first run on any
machine is the slowest: an engine image of
about 650 MB, plus your base images,
before the caching of chapter 8 starts
paying rent. Small projects with small
pipelines may honestly never recover the
admission price; chapter 11's Makefile
comparison is the honest benchmark to hold
it against.

## What it will not do at all

Dagger does not host anything, schedule
anything, or watch your repository — no
engine, no run; the CI service remains
(chapter 7). It does not deploy or operate
the things it builds: publishing an image
is its last act, and running that image is
Docker's, Kubernetes' or a platform's
chapter. It does not make a pipeline
correct: a function that tests the wrong
thing will test it reproducibly, in
parallel, with excellent caching, on every
machine you own.
