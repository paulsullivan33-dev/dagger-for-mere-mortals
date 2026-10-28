# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 12 names what the tool
   cannot do: nothing works without a container runtime, the
   engine is privileged, the local run is local, the tool is
   young and fast-moving, and it neither hosts nor deploys.
8. **The rule is in the text, early.** This guide's governing
   fact — *no engine, no pipeline; the CLI alone does almost
   nothing* — is stated in chapter 1 and the README before any
   procedure depends on it, and the verification split it
   forces is repeated wherever a procedure is documented only.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is an Ubuntu 24.04 sandbox whose kernel
forbids the namespace operation containers are started with
(`setns` into a container mount namespace returns "operation
not permitted"). The lab established this rather than assuming
it: the Docker client was present but no daemon was running;
the lab started the daemon itself (with the vfs storage driver
and no bridge networking, the settings the sandbox tolerates),
after which Docker could pull images and create containers but
could not start any — `docker run hello-world` and `docker
start dagger-engine-v0.21.11` fail with the identical runc
error, kept as transcript t91. Dagger therefore could not
execute any pipeline work on this machine. The guide is written
in two clearly separated halves, and this ledger is the
boundary between them.

Run for real, with transcripts as evidence (Dagger CLI
**v0.21.11**, official release tarball for linux/amd64):

- Download of the release tarball and its verification against
  the project's published `checksums.txt` with `sha256sum -c`
  (t01), and `dagger version` reporting the CLI and its paired
  engine image (t00).
- `dagger --help` in full (t02), and the static help pages of
  `dagger init` (t04), `dagger functions` and `dagger develop`
  (t07).
- `dagger completion bash` generating its script with no
  engine present (t05).
- The engine's provisioning, watched end to end:
  `dagger core version` pulled
  `registry.dagger.io/engine:v0.21.11` completely (about
  650 MB, just under two minutes on this storage), issued the
  `docker run --name dagger-engine-v0.21.11 --privileged ...`
  command, which failed with exit status 125 because the
  container could not be started, and then waited at
  "connecting to engine" until the lab stopped it at 280
  seconds (t90, kept whole).
- `dagger init` in an empty folder: it begins with the same
  engine provisioning and wrote nothing at all before the lab
  stopped it — proof that scaffolding is engine work (t03).
- `dagger config` against a hand-written `dagger.json`, and
  `dagger call --help`, both failing at the engine in under a
  second with the engine container present but unstartable
  (t06, t08).
- The sample project the module wraps: `wordcount.py` and its
  three unit tests, run directly with Python 3.12.3, all
  passing (t10).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- Everything the engine does once started: executing
  functions, `dagger call` and Dagger Shell in operation,
  caching behaviour and timings, service bindings, secret
  scrubbing in real output, interactive debugging.
- The module scaffolding `dagger init` produces on a healthy
  machine (file layout and the two generated example
  functions, quoted in chapter 5 in the documentation's own
  form). This guide's example module in `dagger-lab/module/`
  was written by hand to that documented pattern; it is
  syntax-checked (`py_compile`) and labelled in its own header
  as never executed.
- The GitHub Actions workflows of chapter 7 and the other CI
  shapes, which follow the project's official action
  (`dagger/dagger-for-github`) and documentation.
- Self-provisioning the engine via
  `_EXPERIMENTAL_DAGGER_RUNNER_HOST`, Dagger Cloud features,
  and `dagger check`.
- The comparison tools in chapter 11 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
twenty-line word-count program with standard-library tests and
a two-line sample text. No example is modelled on any real
person, service or organisation.
