# Troubleshooting

Symptom first, cause second. Unusually for
this series, the lab met the first three
entries personally and kept the receipts;
they are ordered the way a new install
meets them.

## Every command stops at "starting engine"

*The CLI installed, `dagger version`
prints — and anything real hangs or fails
around the engine's start.*

Work down the list, in order:

1. **Is Docker itself healthy?**
   `docker run --rm hello-world`. Dagger
   provisions its engine through Docker;
   a Docker that cannot run a container
   cannot run the engine, and the fault is
   Docker's, not Dagger's (chapter 3).
2. **Does the engine container exist, and
   in what state?** `docker ps -a` and look
   for `dagger-engine-<version>`. A state of
   `Created` — made but never started — is
   the signature of a runtime that can
   create containers but not start them
   (restricted sandboxes, some nested
   setups). Try `docker start
   dagger-engine-<version>` yourself: the
   daemon's own error is plainer than
   anything Dagger prints over it. The
   lab's was (transcript
   `dagger-lab/transcripts/t91-docker-start-fails.txt`):

   ```text
   Error response from daemon: failed to create task for container: ... runc create failed: ... join container mntns: setns: operation not permitted
   ```

   In plain words: the sandbox forbids the
   namespace operation containers are made
   of. No Dagger setting fixes that; the
   door is an engine provisioned somewhere
   containers *can* start (chapter 7), or
   a different machine.
3. **Did the first `docker run` fail
   outright?** In the lab's full attempt
   (transcript t90) the pull succeeded, the
   run reported `exit status 125`, and the
   CLI then waited at "connecting to
   engine" — the state to recognise is
   *a created-but-not-running engine plus
   a patient CLI*. Stop the command; the
   CLI will wait much longer than you
   should.

## "failed to start container ... docker start ... exit status 1"

The fast version of the same wall, seen
once an unstartable engine container
exists: later commands find it, try to
start it, and fail in under a second
(transcripts t06 and t08 — `dagger config`
and even `dagger call --help`). The
remedy is not in Dagger: remove the stuck
container (`docker rm
dagger-engine-<version>`) only after
fixing the runtime problem underneath, or
every command will recreate the same
corpse. On a machine where Docker runs
containers normally, this error instead
points at a damaged engine container, and
removing it so the CLI provisions a fresh
one is the whole fix.

## The first run takes minutes and prints an error about the engine image

Normal, once. The CLI inspects for the
engine image before pulling it; on a cold
machine that inspect fails, the step shows
as an error line, and the pull follows —
hundreds of layer lines and, on the lab's
storage, just under two minutes for about
650 MB (transcript t90). Judge a first run
by whether the pull *completes*, and
later runs by their connect step, which
should take about a second against the
already-running engine.

## dagger init writes nothing

`init` needs the engine — the SDK install
and code generation are engine work
(chapter 4). If the engine cannot start,
the folder stays empty and there is no
partial module to clean: the lab's `ls`
after a stopped `init` showed literally
nothing. Fix the engine problem and rerun
the same command. If the folder *does*
gain a `dagger.json` but generation stops,
`dagger develop` re-runs the SDK
installation against an existing module —
its help page is transcript t07.

## The CLI and the module disagree about versions

A module's `dagger.json` records its
engine version; a CLI far from that
version says so. The clean states are:
upgrade the CLI to the module's pairing,
or let the module be developed forward
(`dagger develop`, then the project's
upgrade path). What not to do is hand-edit
`engineVersion` to silence the message —
the pairing is a compatibility statement,
and the code generation under it is
versioned too.

## A step fails in CI that passed at your desk

Chapter 12's list, in the order to check
it: architecture (ARM desk, x86 runner —
ask the pipeline for the platform
explicitly); network (the step reaches
something only your desk can reach);
secrets (present in your environment,
absent or differently named in CI — the
`env:` reference resolves on the *calling*
machine); and cache (CI's cold engine
makes a step slow enough to hit a timeout
your warm desk never sees). The pipeline
is the same; its surroundings are not, and
the run's trace — local and CI runs both
produce one — is where the difference
shows.
