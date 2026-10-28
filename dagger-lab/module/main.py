"""The example Dagger module for this guide: two functions over
the wordcount sample project in ../project.

Written by hand to the documented Python SDK pattern, because
this guide's lab could not run `dagger init` (init needs the
engine, and the lab machine could not start one — see the
guide's chapter 4 and criteria.md). It has NOT been executed:
the engine it needs never started on the lab machine. Treat it
as documentation-shaped code, checked against the Dagger
project's own examples, not as a transcript.
"""

import dagger
from dagger import dag, function, object_type


@object_type
class Wordcount:
    @function
    async def test(self, source: dagger.Directory) -> str:
        """Run the project's unit tests in a Python container
        and return the test runner's output."""
        return await (
            dag.container()
            .from_("python:3.12-slim")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_exec(["python", "-m", "unittest", "-v"])
            .stdout()
        )

    @function
    def container(self, source: dagger.Directory) -> dagger.Container:
        """Return a container holding the project, ready to run
        wordcount.py or to be published as an image."""
        return (
            dag.container()
            .from_("python:3.12-slim")
            .with_directory("/src", source)
            .with_workdir("/src")
            .with_entrypoint(["python", "wordcount.py"])
        )
