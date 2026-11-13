"""Default and explicit eligibility for every AEtest result and target kind."""
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
        for policy in ('default', 'explicit'):
            for outcome in RESULTS:
                yield {'name': '{}_{}_{}'.format(target, policy, outcome),
                       'target': target, 'policy': policy, 'outcome': outcome}


def decorate(target, spec):
    target = aetest.loop(inner=[1, 2])(target)
    target = aetest.loop(outer=['a', 'b'])(target)
    options = {'retries': 1, 'retry_wait': 0}
    if spec['policy'] == 'explicit':
        options['section_results'] = list(RESULTS)
    return aetest.retry(**options)(target)


def make_probe(spec, marker):
    def probe(self, section, observations, outer, inner, retry_count=0):
        invocation = self if spec['target'] == 'testcase' else section
        event = dict(spec, outer=outer, inner=inner, retry_count=retry_count,
                     uid=str(invocation.uid), uid_path=list(invocation.uid.list))
        observations.append(event)
        logger.info('ELIGIBILITY TRACE %s', json.dumps(event, sort_keys=True))
        getattr(section, spec['outcome'])('Eligibility injection: ' + spec['name'])
    probe.__name__ = spec['name']
    return marker(probe)


def make_case(spec):
    class EligibilityCase(aetest.Testcase):
        pass
    EligibilityCase.__name__ = spec['name']
    EligibilityCase.check = make_probe(spec, aetest.test)
    EligibilityCase.check.source = Source(EligibilityCase.check, objcls=EligibilityCase)
    return decorate(EligibilityCase, spec)


class SectionCases(aetest.Testcase):
    pass


class SubsectionCases(aetest.CommonCleanup):
    @aetest.subsection
    def zz_audit(self, observations, review_directory):
        rows = []
        for spec in specifications():
            events = [event for event in observations if event['name'] == spec['name']]
            retry = spec['policy'] == 'explicit' or spec['outcome'] == 'failed'
            expected = [(outer, inner, attempt) for attempt in range(2 if retry else 1)
                        for outer in ('a', 'b') for inner in (1, 2)]
            actual = [(event['outer'], event['inner'], event['retry_count']) for event in events]
            correct = actual == expected and len({event['uid'] for event in events}) == len(events)
            rows.append(dict(spec, expected_calls=len(expected), actual_calls=len(events),
                             audit='passed' if correct else 'failed'))
        document = {'scenarios': rows, 'observations': observations,
                    'audit': 'passed' if all(row['audit'] == 'passed' for row in rows) else 'failed'}
        (Path(review_directory) / 'eligibility.json').write_text(json.dumps(document, indent=2) + '\n')
        logger.info('ELIGIBILITY AUDIT %s', json.dumps(rows, sort_keys=True))
        if document['audit'] != 'passed':
            self.failed('Eligibility trace mismatch; see eligibility.json')
        self.passed('All 42 eligibility scenarios match their expected traces.')


for _spec in specifications():
    if _spec['target'] == 'testcase':
        globals()[_spec['name']] = make_case(_spec)
    else:
        _owner = SectionCases if _spec['target'] == 'test' else SubsectionCases
        _marker = aetest.test if _spec['target'] == 'test' else aetest.subsection
        _probe = decorate(make_probe(_spec, _marker), _spec)
        _probe.source = Source(_probe, objcls=_owner)
        setattr(_owner, _spec['name'], _probe)
