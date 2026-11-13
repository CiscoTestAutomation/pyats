"""One review job, six profiles, 252 loop/retry scenarios.

Expected failed/errored scenarios are intentional. Review each task's final
zz_audit subsection and matrix_<profile>.json artifact to verify replay counts.
"""
import json
import logging
from pathlib import Path
import shutil
import subprocess
import sys

from pyats import aetest

from pyats.easypy import run

logger = logging.getLogger(__name__)
PROFILES = ('passed', 'fail_once', 'recover_outer', 'exhausted', 'errored_once', 'skipped')


def _revision(directory):
    try:
        return subprocess.check_output(
            ['git', '-C', str(directory), 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def main(runtime):
    here = Path(__file__).resolve().parent
    destination = Path(runtime.directory)
    for name in ('loop_retry_matrix.py', 'loop_retry_matrix_job.py'):
        shutil.copy2(here / name, destination / name)
    manifest = {
        'core_commit': _revision(Path(aetest.__file__).resolve().parent),
        'example_commit': _revision(here), 'python_version': sys.version,
        'core_version': aetest.__version__,
        'loop_dimensions': [0, 1, 2],
        'retry_placements': 'Every subset of the boundaries before, between and after loops',
        'retry_configuration': {'retries': 1, 'retry_wait': 0, 'section_results': ['failed', 'errored']},
        'target_types': ['testcase', 'test', 'subsection'],
        'profiles': list(PROFILES), 'scenarios_per_profile': 42, 'total_scenarios': 252,
        'note': 'Failed and errored rows are deliberate; every zz_audit subsection should pass.',
    }
    (destination / 'matrix_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    logger.info('MATRIX MANIFEST %s', json.dumps(manifest, sort_keys=True))
    for profile in PROFILES:
        run(testscript=str(here / 'loop_retry_matrix.py'), taskid='matrix_{}'.format(profile),
            profile=profile, review_directory=str(destination))
