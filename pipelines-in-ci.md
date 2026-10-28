# Pipelines in CI

Chapter 1's promise, cashed: once the
pipeline is a module, the CI server stops
being the pipeline's home and becomes its
doorbell. This chapter shows the shape of
that arrangement for GitHub Actions — the
pattern the project's own documentation
and action use — and names what changes
and what does not. Documented-only in
this guide: the lab ran no CI, and the
workflow below is the documented pattern,
not a transcript.

## The thin wrapper

A Dagger pipeline in GitHub Actions is a
workflow with three steps: check out the
code, install or invoke Dagger, call the
function. The project's official GitHub
action compresses the last two:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        uses: dagger/dagger-for-github@v8
        with:
          verb: call
          args: test --source=.
```

Everything a reader of this guide should
notice is what is *absent*: no setup
steps for a language toolchain (the
function's container carries it), no test
command spelled in YAML (the function is
the command), no second copy of the
pipeline for local use. Adding the build
and publish stages adds calls, not a new
dialect:

```yaml
  publish:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish image
        uses: dagger/dagger-for-github@v8
        with:
          verb: call
          args: publish --source=. --tag=${{ github.sha }}
        env:
          REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}
```

The `env:` line is the secret pattern of
chapter 9 arriving on schedule: the value
stays in the CI service's secret store,
and the function receives it as a Dagger
`Secret` because the argument is declared
as one and referenced as `env:...`.

Other CI systems wear the same shape with
different wrapping: a GitLab job whose
script installs the CLI (`curl -fsSL
https://dl.dagger.io/dagger/install.sh |
BIN_DIR=/usr/local/bin sh`) and runs
`dagger call test --source=.`; a Jenkins
stage doing the same. In each case the CI
system needs one ability — running Docker
(or providing an engine, chapter 2) — and
the pipeline it triggers is byte-for-byte
the one from your laptop.

## What the CI server still does

Dagger does not replace the CI service,
and pretending otherwise is how teams end
up surprised. The service still provides:

- **Triggers and scheduling** — pushes,
  pull requests, cron, manual runs.
- **Machines** — the runners the engine
  itself runs on, and their limits.
- **Secrets storage and permissions** —
  who may publish, whose tokens exist.
- **The record** — statuses on pull
  requests, notifications, the red and
  green marks people actually look at
  (Dagger Cloud's checks can enrich this;
  the service's own checks remain the
  floor).

What moves is the *logic*: conditionals,
tool versions, build steps, test commands,
packaging. That is the part that used to
exist only inside one vendor's YAML, in a
language nobody could run locally —
the part whose bugs were debugged by
pushing commits named "fix ci" eleven
times in a row. With the logic in a
module, "fix ci" becomes an ordinary code
change: reproduce locally with `dagger
call`, fix the function, and the wrapper
never changes.

## dagger check, and the engine question

Two documented extras complete the
picture. **`dagger check`** runs a module's
declared checks as one command — the
project's answer to "run everything CI
would run" — and Dagger Cloud offers a
managed integration that wires checks into
pull requests with trace links. And
**provisioning**: hosted runners that can
start the engine container work as-is;
environments that cannot (nested sandboxes
of the kind that stopped this guide's lab)
need an externally provisioned engine —
chapter 2's runner host variable — which
managed Dagger runners also provide. The
lab's wall is, in other words, a known
shape with a known door on real
infrastructure; it only looks absolute
from inside a sandbox like this one.
