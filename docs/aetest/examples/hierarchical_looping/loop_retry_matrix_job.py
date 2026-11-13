"""One review job: 540 placement, 42 eligibility and 105 CLI scenarios.

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
from pyats.easypy.plugins.retry import RetryPlugin

logger = logging.getLogger(__name__)
PROFILES = ('passed', 'fail_once', 'recover_outer', 'exhausted', 'errored_once', 'skipped')
RESULTS = ('passed', 'passx', 'failed', 'errored', 'blocked', 'skipped', 'aborted')


def cli_policy(profile):
    selectors = {}
    for target in ('testcase', 'test', 'subsection'):
        prefix = {'testcase': '', 'test': 'SectionCases.', 'subsection': 'common_cleanup.'}[target]
        for outcome in RESULTS:
            selectors[prefix + target + '_' + outcome] = {'retries': 1, 'retry_wait': 0}
    policy = {'retries': 1, 'retry_wait': 0, 'section_results': ['failed', 'errored'],
              'testcases': selectors}
    if profile == 'excluded':
        policy['testcases'] = {'ThisTargetDoesNotExist': {}}
    elif profile in ('override0', 'override2'):
        policy.update(retries=4, retry_wait=20)
        for selector in selectors:
            selectors[selector] = {'retries': int(profile[-1]), 'retry_wait': 0}
    elif profile == 'testsection':
        policy = {'retries': 1, 'retry_wait': 0, 'sections': ['TestSection'], 'section_results': ['failed']}
    return policy


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
    for name in ('loop_retry_matrix.py', 'loop_retry_matrix_job.py',
                 'eligibility_matrix.py', 'cli_retry_matrix.py', 'audit_review_archive.py'):
        shutil.copy2(here / name, destination / name)
    cli_profiles = ('selected', 'excluded', 'override0', 'override2', 'testsection')
    manifest = {
        'core_commit': _revision(Path(aetest.__file__).resolve().parent),
        'example_commit': _revision(here), 'python_version': sys.version,
        'core_version': aetest.__version__,
        'loop_dimensions': [0, 1, 2, 3],
        'retry_placements': 'Every subset of the boundaries before, between and after loops',
        'retry_configuration': {'retries': 1, 'retry_wait': 0, 'section_results': ['failed', 'errored']},
        'target_types': ['testcase', 'test', 'subsection'],
        'profiles': list(PROFILES), 'scenarios_per_profile': 90, 'placement_scenarios': 540,
        'eligibility_scenarios': 42, 'cli_scenarios': 105, 'total_scenarios': 687,
        'cli_profiles': {profile: cli_policy(profile) for profile in cli_profiles},
        'note': 'Failed and errored rows are deliberate; every zz_audit subsection should pass.',
    }
    (destination / 'matrix_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    logger.info('MATRIX MANIFEST %s', json.dumps(manifest, sort_keys=True))
    original_data = getattr(runtime, 'retry_data', {})
    original_args = runtime.args.retry
    try:
        runtime.retry_data = {}
        for profile in PROFILES:
            run(testscript=str(here / 'loop_retry_matrix.py'), taskid='matrix_{}'.format(profile),
                profile=profile, review_directory=str(destination))
        run(testscript=str(here / 'eligibility_matrix.py'), taskid='eligibility',
            review_directory=str(destination))
        plugin = RetryPlugin(runtime=runtime)
        for profile in cli_profiles:
            runtime.args.retry = [json.dumps(cli_policy(profile))]
            runtime.retry_data = {}
            plugin.pre_job(None)
            if not runtime.retry_data:
                raise RuntimeError('RetryPlugin did not load the CLI policy for ' + profile)
            run(testscript=str(here / 'cli_retry_matrix.py'), taskid='cli_' + profile,
                cli_profile=profile, review_directory=str(destination))
    finally:
        runtime.retry_data = original_data
        runtime.args.retry = original_args
