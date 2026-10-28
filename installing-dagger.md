# Installing Dagger

Installing Dagger means installing one
program: the CLI. The engine arrives by
itself, as a container, the first time a
command needs it — which means the real
prerequisite is not Dagger at all but a
**working container runtime**, Docker in
the usual case. This chapter installs the
CLI the way the lab did, verifies the
download the way you should, and then
follows the engine's first arrival as far
as the lab machine allowed it to go.

## The requirement underneath

Dagger's engine runs as a privileged
Docker container, so first, on an ordinary
machine:

```bash
docker run --rm hello-world
```

If that prints its welcome message, your
floor is solid and the rest of this
chapter is a formality. If it does not,
fix that first — the series' Docker guide
is the place — because nothing later in
this book can route around it. This
guide's lab machine failed a sterner
version of this test, and this chapter
does not hide that: its Docker daemon had
to be coaxed into starting at all, it
could pull images and create containers,
and it could not *start* one. The lab
recorded the exact refusal (transcript
`dagger-lab/transcripts/t91-docker-start-fails.txt`):

```text
$ docker start dagger-engine-v0.21.11
Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error spawning mount remapping thread: mount source thread: join container mntns: setns: operation not permitted
```

That is a sandbox refusing the namespace
operation containers are built from. Most
readers will never see it; readers inside
restricted CI sandboxes and nested
containers may, and chapter 13 collects
the whole family of engine-start failures
in one place.

## The install script

The project's own route, from its
documentation, is a script that downloads
the right binary for your machine:

```bash
curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
```

`BIN_DIR` chooses where the `dagger`
binary lands; leave it off and the script
uses `./bin` in the current folder. Homebrew
(`brew install dagger`), and packages for
various systems, exist as well. All routes
deliver the same single binary.

## The lab's route: tarball and checksum

The lab downloaded the release tarball
directly and **verified it against the
project's published checksums** before
unpacking — a habit worth keeping for any
tool that will run privileged containers
on your behalf:

```bash
curl -LO https://github.com/dagger/dagger/releases/download/v0.21.11/dagger_v0.21.11_linux_amd64.tar.gz
curl -LO https://github.com/dagger/dagger/releases/download/v0.21.11/checksums.txt
grep linux_amd64.tar.gz checksums.txt | sha256sum -c -
tar -xzf dagger_v0.21.11_linux_amd64.tar.gz dagger
```

Check: the checksum verdict (transcript
`dagger-lab/transcripts/t01-checksum.txt`):

```text
$ sha256sum -c checksums.txt  # (filtered to the linux_amd64 line)
dagger_v0.21.11_linux_amd64.tar.gz: OK
```

And the binary introducing itself
(transcript t00):

```text
$ dagger version
dagger v0.21.11 (image://registry.dagger.io/engine:v0.21.11) linux/amd64
```

Notice what `dagger version` does *not*
do: it does not start the engine. It
reports the CLI's version and the engine
image the CLI is paired with. The pairing
matters — a module records the engine
version it was created with, and a much
older or newer CLI will say so rather than
guess.

## The engine's first arrival

The first command that needs the engine —
`dagger init`, `dagger call`,
`dagger core version`, almost anything —
sets the provisioning of chapter 2 in
motion. The lab ran `dagger core version`
and kept the whole attempt (transcript
t90). The shape of a first run, on any
machine:

1. **`docker ps`** — is an engine container
   already there? (On later runs, this is
   where the story resumes: the CLI finds
   its engine and connects, in about a
   second.)
2. **`docker pull registry.dagger.io/engine:v0.21.11`**
   — the engine image, about 650 MB on
   disk. On the lab's slow storage this
   took just under two minutes; on a normal
   machine, well under one. This step needs
   the network, once.
3. **`docker run --name dagger-engine-v0.21.11 ... --privileged`**
   — the engine starts, detached, set to
   restart always, with its cache volume.
4. **Connect** — the CLI opens its session
   to the engine and the command proceeds.

On the lab machine step 3 is where it
ended: Docker created the container and
refused to start it, the run reported
`exit status 125`, and the CLI waited at
"connecting to engine" until the lab
stopped it — the full, layer-by-layer
record is transcript t90, all 540 lines of
it, because in this series a failure you
can read beats a success you have to take
on faith.

Two things follow for ordinary installs.
First, **the engine stays**: it is a
container like any other, visible in
`docker ps`, stoppable and removable with
`docker stop` / `docker rm` (removing it
throws away the cache of chapter 8, not
your code). Second, **version upgrades are
image pulls**: a new CLI brings a new
engine version, provisions it the same
way, and the old engine container can be
removed once nothing uses it.

## What the CLI can do with no engine at all

A short, exact list, because chapter 4
depends on it — each of these the lab ran
with no engine in existence:

- `dagger version` (t00)
- `dagger --help`, and the static help of
  subcommands whose help is not generated
  from a module — `dagger init --help`
  (t04), `dagger functions --help` and
  `dagger develop --help` (t07)
- `dagger completion <shell>` — prints the
  shell's completion script (t05)

And the counter-list, also exact: `dagger
init`, `dagger config`, `dagger call`, and
even `dagger call --help` — whose help is
generated from *your module's* functions,
so it must load the module, so it needs
the engine — all begin at the engine's
door. The lab's fastest proof is
transcript t06: a hand-written
`dagger.json`, and `dagger config`
answering in 0.6 seconds:

```text
Error: start engine: failed to start container: failed to run command [docker start dagger-engine-v0.21.11]: exit status 1
```

On a healthy machine the same command
prints the module's configuration. The
lesson is not that the command is broken —
it is that *there is no offline mode*.
Dagger is its engine; the CLI is a
well-made remote control, and chapter 12
counts that as a limit, fairly.
