# Recipes

Short, named jobs, each in the pattern of
the chapters before it. Everything here
needs the engine; in this guide all of it
is documented-only, as `criteria.md`
records.

## Run the tests before you push

The recipe the tool exists for. In the
project's module:

```bash
dagger call test --source=.
```

The function runs the suite in its pinned
container (chapter 5). The CI server will
run the identical call (chapter 7), so a
green run at your desk is the pipeline's
green run, not a rehearsal of it. Make it
a habit with a shell alias or a Makefile
target — and notice that the *Makefile*
has shrunk to one honest line, which is
where chapter 11 picks the story up.

## Build the image, publish on the branch that counts

One function builds the container
(chapter 5's `container`), a second
publishes it. Locally you inspect the
build; in CI the wrapper adds the publish
call only on the main branch (chapter 7's
workflow), with the registry password
arriving as a `Secret`. Tag with the
commit identifier, not `latest`, so every
image can be traced to the code that made
it.

## Borrow a module from the Daggerverse

Your module can depend on a published one
and call its functions from yours — a
vulnerability scanner over the image you
just built, a deployer for your platform:

```bash
dagger install github.com/example/scan-module
```

after which the module's functions are
reachable in your code (chapter 5) and
from the command line with `-m`. Read a
borrowed module the way you would read a
library: it runs with your pipeline's
powers, including your secrets, so its
source is part of your supply chain —
pin versions, and prefer modules whose
code you have actually opened.

## Debug at the scene of the failure

When a step fails, ask for a terminal
instead of a log:

```bash
dagger call test --source=. --interactive
```

(or break at a chosen point in a function
with the documented terminal calls). You
land in a shell inside the failed
container, with its filesystem and
environment as the step left them — the
difference between reading a witness
statement and visiting the scene. In CI
this is a local tool; its real gift is
that the local reproduction is faithful
enough for the visit to mean something.

## One pipeline, two CI systems

A project that must live on GitHub Actions
*and* GitLab keeps one module and two thin
wrappers (chapter 7). Moving house later
is the same recipe read backwards: write
the new system's wrapper, delete the old
one, and the pipeline — tests, build,
publish, secrets, services — does not
change a line. This is the recipe to show
a sceptic, because its YAML-era equivalent
is "rewrite the pipeline and re-debug it
in production".
