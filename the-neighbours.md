# The Neighbours

Dagger's neighbours are the tools a
pipeline might otherwise be. Each comparison
below is a characterisation, not a
benchmark, and several of these tools are
not rivals so much as the ground Dagger
stands on or the wrappers it still needs.

## CI YAML (GitHub Actions, GitLab CI, and kin)

The incumbent. YAML pipelines are
*declarations in the hosting service's
dialect*: powerful, universally available,
and — the charges this guide is built on —
not runnable locally, not portable between
services, and written in a notation that
grows conditionals and string tricks as a
pipeline matures. Dagger's answer is not
to abolish the YAML but to demote it to a
wrapper (chapter 7). If your pipeline is
five lines and one service forever, the
YAML alone is honestly enough; the
crossover comes when the pipeline becomes
a program.

## Jenkins

The self-hosted elder: its scripted
pipelines are real code (Groovy) on your
own controller, which answers the
portability complaint differently — bring
your own server, keep it forever. What it
does not give you is the container-first
execution model or the local run: a
Jenkins pipeline still lives on the
controller. Teams with a Jenkins estate
and the staff to keep it have a working
answer already; Dagger's pitch is aimed at
everyone maintaining YAML on a hosted
service instead.

## Make, and shell scripts

The honest baseline every pipeline should
be compared against. A Makefile runs
locally, is portable across CI services
(any of them can call `make test`), and
needs no engine. Its limits are the
mirror of Dagger's strengths: it runs on
the host as the host is (tool versions are
your problem), it has no container model,
no typed values, no built-in caching
beyond file timestamps, and its
parallelism is a flag and a prayer. Many
Dagger adoptions keep a one-line Makefile
as the front door — `test: ; dagger call
test --source=.` — which is the two tools
in their right places.

## Docker and BuildKit, alone

Dagger's engine is built on BuildKit, and
a disciplined Dockerfile with multi-stage
builds already delivers pinned toolchains
and layer caching. What plain Docker
lacks is everything *around* the image:
running the tests as a first-class step
with values passed between stages,
services bound by name, secrets as a type,
and a programming language for the logic
connecting it all. If your pipeline truly
is "build this one image", a Dockerfile is
the smaller tool. The moment the pipeline
also tests, scans, migrates and publishes,
the glue has to live somewhere — Dagger's
claim is that it should live in code.

## Earthly, Nix, and the reproducibility wing

Earthly walks a nearby road — Dockerfile-
flavoured pipeline definitions with
caching and local runs — with a dedicated
syntax where Dagger chooses your existing
language. Nix goes further than either on
reproducibility, pinning not just tools
but their entire dependency ancestry, at
the price of a language and an ecosystem
that are a commitment of their own.
Dagger's bet is the middle: containers you
already understand, code you already
write, portability across the CI services
you already use. Readers whose pain is
specifically "the same inputs must give
bit-identical outputs, provably" should
look at Nix with respect; it is answering
a harder question than this guide's.
