# Caching and Speed

A pipeline that reruns everything, every
time, teaches its owners to run it less
often. Dagger's answer is structural
rather than configured, and it follows
from chapter 2's graph: this chapter
explains the mechanism as the
documentation describes it. Documented-only
in this guide — the lab never completed a
run, so it measured no cache hits, and it
says so rather than borrowing numbers.

## Cache by construction

Every operation the engine performs —
pull this image, mount this directory, run
this command — is identified by its exact
inputs: the image digest, the contents of
the directory, the command and its
environment. When a function runs, the
engine walks the graph it built and asks,
for each operation, *have I done exactly
this before?* If yes, the stored result is
reused and the step reports itself cached;
if no, it runs, and its result joins the
store. This is the same principle as
Docker's layer cache, generalised from
image layers to every value in the
pipeline — a test run is cached on the
source it tested, not on the accident of
which Dockerfile line produced it.

Three practical consequences:

- **Change is local.** Edit one file and
  only the operations whose inputs include
  that file rerun. The test step reruns;
  the base image pull and the toolchain
  install do not.
- **The cache is shared by everything on
  the engine.** Two modules, two branches,
  your laptop's morning runs and its
  afternoon runs — one store, keyed by
  content, so identical work is done once
  per machine, not once per project.
- **Order stops mattering for speed.**
  There is no cache-warming choreography
  to maintain, no "put the slow step
  first" folklore; the graph knows what
  depends on what.

## Parallel by construction

The same graph gives the second half: an
operation starts when its inputs are
ready, not when the previous line of a
script finishes. A module whose `ci`
function tests the project, builds its
documentation and lints its code runs
those three as parallel branches unless
one genuinely consumes another's output —
and functions written in an async style
(the Python SDK's `async` functions of
chapter 5) can fan work out inside a
single call. In YAML this took matrices
and job graphs to approximate; here it is
what the description already says.

## Where the cache lives, and the CI problem

The store is the engine's data volume —
`/var/lib/dagger` in the provisioning
command of chapter 3. On your laptop it
persists between runs and reboots, which
is why a second `dagger call test` on an
unchanged project is fast. In CI it hits
the classic problem: **a fresh runner has
an empty engine**, and the first run there
pays full price — image pulls included —
unless the cache is carried. The
documented answers are Dagger Cloud's
cache sharing (the engine syncs cache data
to the service, so runners start warm) and
managed runners with persistent engines;
self-hosted runners with a long-lived
engine get the same effect by keeping the
volume. Judge any of these by the honest
metric: the *second* run's time, since the
first run on any cold machine — the lab's
two-minute engine pull is the emblem — is
the price of admission, not the steady
state.

## What caching cannot do

Cached results are only as trustworthy as
their keys, and two honest caveats belong
in this chapter. A step whose real inputs
are not in its description — a command
that reads the clock, the network, or a
host path the function did not declare —
can be served a stale result it no longer
deserves; the discipline of declaring
inputs (chapter 5's habit of taking the
source as an argument) is what keeps the
cache honest. And a cache cannot make a
slow operation fast the first time: the
engine pull, the big base image, the long
test suite all cost what they cost, once
per distinct set of inputs. Dagger's
promise is narrower and better — that you
pay each distinct cost once, and can see
in the run's tree exactly which steps you
paid for.
