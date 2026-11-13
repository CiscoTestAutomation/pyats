"""Looped targets with no retry decorator, using the job's CLI policy fixture.

The job calls the real RetryPlugin parser before each task. This allows several
CLI policies in one archive, including qualified selectors and zero overrides.
"""
import json
import logging
from pathlib import Path

from pyats import aetest
from pyats.aetest.base import Source

logger = logging.getLogger(__name__)
parameters = {'observations': []}
RESULTS = ('passed', 'passx', 'failed', 'errored', 'blocked', 'skipped', 'aborted')
TARGETS = ('testcase', 'test', 'subsection')


def specifications():
    for target in TARGETS:
        for outcome in RESULTS:
            yield {'name': '{}_{}'.format(target, outcome), 'target': target, 'outcome': outcome}


def decorate(target):
    return aetest.loop(outer=['a', 'b'])(aetest.loop(inner=[1, 2])(target))


def make_probe(spec, marker):
    def probe(self, section, observations, outer, inner, retry_count=0):
        invocation = self if spec['target'] == 'testcase' else section
        event = dict(spec, outer=outer, inner=inner, retry_count=retry_count,
                     uid=str(invocation.uid), uid_path=list(invocation.uid.list),
                     section_uid=str(section.uid), section_uid_path=list(section.uid.list))
        observations.append(event)
        logger.info('CLI TRACE %s', json.dumps(event, sort_keys=True))
        getattr(section, spec['outcome'])('CLI eligibility injection: ' + spec['name'])
    probe.__name__ = 'check' if spec['target'] == 'testcase' else spec['name']
    return marker(probe)


def make_case(spec):
    class CliCase(aetest.Testcase):
        pass
    CliCase.__name__ = spec['name']
    CliCase.check = make_probe(spec, aetest.test)
    CliCase.check.source = Source(CliCase.check, objcls=CliCase)
    return decorate(CliCase)


class SectionCases(aetest.Testcase):
    pass


class SubsectionCases(aetest.CommonCleanup):
    @aetest.subsection
    def zz_audit(self, observations, cli_profile, review_directory):
        rows = []
        for spec in specifications():
            events = [event for event in observations if event['name'] == spec['name']]
            retries = 0
            if cli_profile == 'selected' and spec['outcome'] in ('failed', 'errored'):
                retries = 1
            elif cli_profile == 'override2' and spec['outcome'] in ('failed', 'errored'):
                retries = 2
            elif cli_profile == 'testsection' and spec['target'] == 'test' and spec['outcome'] == 'failed':
                retries = 1
            expected = [(outer, inner, attempt) for attempt in range(retries + 1)
                        for outer in ('a', 'b') for inner in (1, 2)]
            if cli_profile == 'testsection' and spec['target'] == 'testcase' and spec['outcome'] == 'failed':
                # The class is excluded, but each ordinary check section is
                # selected. Existing CLI behavior retries that section locally.
                expected = [(outer, inner, attempt) for outer in ('a', 'b')
                            for inner in (1, 2) for attempt in range(2)]
            actual = [(event['outer'], event['inner'], event['retry_count']) for event in events]
            unique = len({(event['uid'], event['section_uid']) for event in events}) == len(events)
            correct = actual == expected and unique
            rows.append(dict(spec, expected_calls=len(expected), actual_calls=len(events),
                             audit='passed' if correct else 'failed'))
        document = {'profile': cli_profile, 'scenarios': rows, 'observations': observations,
                    'audit': 'passed' if all(row['audit'] == 'passed' for row in rows) else 'failed'}
        (Path(review_directory) / ('cli_' + cli_profile + '.json')).write_text(
            json.dumps(document, indent=2) + '\n')
        logger.info('CLI AUDIT %s', json.dumps(rows, sort_keys=True))
        if document['audit'] != 'passed':
            self.failed('CLI trace mismatch; see cli_' + cli_profile + '.json')
        self.passed('All 21 CLI scenarios match their expected traces.')


for _spec in specifications():
    if _spec['target'] == 'testcase':
        globals()[_spec['name']] = make_case(_spec)
    else:
        _owner = SectionCases if _spec['target'] == 'test' else SubsectionCases
        _marker = aetest.test if _spec['target'] == 'test' else aetest.subsection
        _probe = decorate(make_probe(_spec, _marker))
        _probe.source = Source(_probe, objcls=_owner)
        setattr(_owner, _spec['name'], _probe)
