# Secrets and Services

Two needs arrive in every real pipeline
sooner or later: a step must use a
password it must not print, and a step
must talk to a database that exists only
while the tests run. Dagger gives both a
type of their own. This chapter explains
them from the project's documentation —
documented-only in this guide, like all
the engine's doings here.

## Secrets

A pipeline argument declared as
**`Secret`** is handled differently from a
string at every stage:

- **Getting it in.** The caller passes a
  *reference*, not a value: `env:NAME`
  (an environment variable on the host),
  `file:path` (a file's contents), or a
  secret-store reference. Chapter 7's CI
  wrapper uses the `env:` form, so the
  value itself lives in the CI service's
  secret store and in nothing else.
- **Using it.** Inside a function, a
  secret can be mounted into a container
  as a file, or set as an environment
  variable for a single step
  (`.with_secret_variable(...)`,
  `.with_mounted_secret(...)` in the SDK's
  naming pattern) — given to the one
  command that needs it, not smeared
  across the image.
- **Keeping it quiet.** The engine knows
  which values are secrets and scrubs them
  from its outputs: a command that echoes
  its password prints `***` in the run's
  record instead. Scrubbing is a safety
  net for accidents, not a licence for
  carelessness — a secret written into an
  image layer or a published artefact is
  out, whatever the logs say.

The contrast with CI YAML is worth
spelling out, because it is the everyday
win: in YAML, a secret is a string in an
environment, one careless `echo $TOKEN`
away from the public log, with masking
bolted on by pattern-matching. Here the
type system carries the fact: the function
signature in chapter 7 (`password:
Secret`) is the whole policy, readable in
code review.

## Services

A **service** is a container whose job is
to be talked to: a database, a message
queue, a copy of your own server. In a
function, a container can be started as a
service and **bound** into another
container under a name:

```python
db = (
    dag.container()
    .from_("mariadb:10.11")
    .with_env_variable("MARIADB_DATABASE", "app")
    .with_exposed_port(3306)
    .as_service()
)

result = await (
    dag.container()
    .from_("python:3.12-slim")
    .with_directory("/src", source)
    .with_service_binding("db", db)
    .with_env_variable("DATABASE_URL", "mysql://root@db/app")
    .with_exec(["python", "-m", "unittest", "-v"])
    .stdout()
)
```

The test container reaches the database
as the host name `db` — the binding name —
and the engine manages the service's whole
life: started before the step that binds
it, stopped when the run is done, never
published, never left running. Health
checks are part of the model: a bound
service is waited on until its ports
answer, rather than slept-and-hoped. And
because the service is part of the graph,
it is part of the caching story too — a
step's declared services are among its
inputs.

This is the piece that retires a familiar
pile of CI scaffolding: the `services:`
stanza in one dialect, the
docker-compose-up-and-pray script in
another, the "is the database up yet"
loop in a third. One description, in the
pipeline's own language, running the same
way on a laptop — where, for once, you can
watch it work before the CI server does.
