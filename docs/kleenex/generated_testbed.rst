.. _kleenex_generated_testbed:

Generated Testbed Configuration
===============================

Clean stages sometimes discover topology information that was not present in
the input testbed.  For example, a stage may create a peer device, discover an
interface, or determine a link after connecting to a device.  Kleenex provides
a generated-testbed collector for publishing this information from a Clean
worker back to the parent process.

The collector is an output channel from Clean.  It does not replace the active
testbed in a worker, and it does not allow a stage to mutate the parent
testbed directly.  After successful cleaning, Kleenex combines the collected
fragments with the input testbed configuration and validates the result with
the pyATS topology loader.


How it works
------------

Kleenex runs device cleaners in worker processes.  A collector is created for
each cleaner and shared with that cleaner's stages:

.. code-block:: text

    Clean stage
        |
        | testbed_config.add(...)
        v
    TestbedConfigCollector (worker)
        |
        | serializable worker result
        v
    KleenexEngine (parent)
        |
        | ordered overlay and topology validation
        v
    generated and merged testbed YAML artifacts

With Genie Clean, the collector is injected into every stage as the reserved
``testbed_config`` parameter.  A stage can therefore publish topology without
depending on Kleenex worker or engine objects.

The collector is available when using the current pyATS and GenieLibs
implementations.  Clean implementations should continue to work when paired
with an older pyATS installation: in that case ``testbed_config`` may be
absent or ``None`` and a stage should treat it as optional if compatibility is
required.


Publishing fragments from a stage
----------------------------------

Use ``add`` for a loader-shaped fragment, or ``add_device`` for the common case
of adding one device and its topology:

.. code-block:: python

    from genie.libs.clean import BaseStage


    class GeneratePeer(BaseStage):
        """Publish a peer discovered during Clean."""

        exec_order = ['generate']

        def generate(self, testbed_config=None):
            """Add the discovered peer when the collector is available."""
            if testbed_config is None:
                return

            testbed_config.add_device(
                'generated-peer',
                {'os': 'linux', 'type': 'virtual'},
                topology={
                    'interfaces': {
                        'eth0': {'link': 'generated-link'},
                    },
                },
                source='discover-peer',
            )

The equivalent generic form is:

.. code-block:: python

    testbed_config.add(
        {
            'devices': {
                'generated-peer': {
                    'os': 'linux',
                    'type': 'virtual',
                },
            },
            'topology': {
                'generated-peer': {
                    'interfaces': {
                        'eth0': {'link': 'generated-link'},
                    },
                },
            },
        },
        source={'device': device.name, 'stage': 'GeneratePeer'},
    )

``source`` is optional provenance metadata.  It is retained in the generated
artifact comments and used in conflict warnings, but is not merged into the
testbed configuration.


Accepted configuration shape
-----------------------------

The collector accepts the three root sections understood by the pyATS topology
loader:

* ``testbed``
* ``devices``
* ``topology``

``links`` and ``segments`` belong inside ``topology`` when the topology schema
requires them there.  They are not valid root-level collector sections:

.. code-block:: yaml

    # Valid
    topology:
        links:
            generated-link:
                interfaces:
                    - generated-peer:eth0
        segments:
            generated-segment:
                interfaces:
                    - generated-peer:eth0

    # Invalid: links and segments are not accepted here
    links: {}
    segments: {}

Fragments are validated before they are retained.  Values must be composed of
plain dictionaries, plain lists, scalar values, and scalar dictionary keys.
Recursive containers and arbitrary Python objects are rejected.  In particular,
do not pass ``OrderedDict`` or another dictionary/list subclass; use a regular
``dict`` or ``list`` instead so the artifact can be written by
``yaml.safe_dump``.

The reserved ``testbed_config`` stage parameter is owned by the Clean
integration.  A stage configuration must not use it to pass a replacement
dictionary.  With current pyATS, Genie injects the collector after configured
stage arguments so the collector cannot be overwritten.  With an older
pyATS that does not provide a collector, configured legacy values remain
available for compatibility.


Merge and ordering behavior
---------------------------

Each successful worker returns a serializable fragment and provenance.  The
parent Kleenex engine restores results in requested device order and overlays
fragments recursively:

* new keys are copied into the merged configuration;
* nested dictionaries are merged recursively;
* later fragments take precedence when a leaf conflicts;
* conflicting leaf values produce a warning identifying the source;
* the input testbed mapping is not modified in place.

Output from a failed Clean is discarded.  This prevents a partially completed
device clean from publishing topology that was not produced by a successful
Clean attempt.


Generated artifacts
-------------------

When generated configuration is present, Kleenex writes two files in the
run-information directory.  In Easypy, a task identifier is included in the
name when needed to keep concurrent tasks separate:

``testbed.clean.generated.yaml``
    A multi-document YAML file containing one generated fragment per
    successful worker.  Each document has provenance and collection order in
    YAML comments.

``testbed.clean.merged.yaml``
    A single loader-ready YAML document containing the input configuration
    overlaid with generated fragments.  Kleenex validates this document with
    the topology loader before applying it to runtime state.

For a task with identifier ``Task-1``, the corresponding names are
``testbed_Task-1.clean.generated.yaml`` and
``testbed_Task-1.clean.merged.yaml``.

The generated file is useful for investigating what individual workers
published.  The merged file is the canonical result to use when diagnosing
loader or topology validation failures.


Operational guidance
--------------------

When adding generated topology to a Clean stage:

1. Publish only loader-shaped data under ``testbed``, ``devices``, or
   ``topology``.
2. Keep every value serializable with standard YAML types.
3. Treat ``testbed_config`` as optional if the cleaner must support older
   pyATS versions.
4. Include stable ``source`` metadata so conflicts can be diagnosed.
5. Run the Clean path that owns the stage and inspect both generated artifacts.
6. Load the merged artifact with the pyATS topology loader before using it in
   a job.

Generated configuration is intended for topology discovered during cleaning.
Static topology belongs in the normal testbed file, while orchestration-owned
topology should remain under the orchestrator's control.
