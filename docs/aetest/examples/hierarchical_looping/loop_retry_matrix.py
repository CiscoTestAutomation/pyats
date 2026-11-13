"""Review every retry placement around zero through three loop dimensions.

Intentional failures demonstrate retry recovery and exhaustion. Each task ends
with an audit of all 90 scenario traces, and writes a JSON artifact alongside
its logs. No testbed or device connections are used.
"""
import itertools
import json
import logging
from pathlib import Path

from pyats import aetest
from pyats.aetest.base import Source

logger = logging.getLogger(__name__)
parameters = {'observations': []}
DIMENSIONS = ({'outer': ['r1', 'r2']}, {'inner': ['p1', 'p2']}, {'leaf': ['s1', 's2']})
PROFILES = ('passed', 'fail_once', 'recover_outer', 'exhausted', 'errored_once', 'skipped')
TARGETS = ('testcase', 'test', 'subsection')


def specifications():
    for target in TARGETS:
        for depth in range(len(DIMENSIONS) + 1):
            for active in itertools.product((False, True), repeat=depth + 1):
                bits = ''.join(str(int(value)) for value in active)
                name = '{}_D{}_R{}'.format(target, depth, bits)
                plan = 'target'
                for boundary in reversed(range(depth + 1)):
                    if active[boundary]:
                        plan = 'retry{}({})'.format(boundary, plan)
                    if boundary:
                        plan = 'loop{}({})'.format(boundary - 1, plan)
                yield {'name': name, 'target': target, 'depth': depth,
                       'boundaries': [i for i, value in enumerate(active) if value], 'plan': plan}


def decorate(target, spec):
    for boundary in reversed(range(spec['depth'] + 1)):
        if boundary in spec['boundaries']:
            target = aetest.retry(retries=1, retry_wait=0, section_results=['failed', 'errored'])(target)
        if boundary:
            target = aetest.loop(**DIMENSIONS[boundary - 1])(target)
    return target


def expected_calls(spec, profile):
    base = 2 ** spec['depth']
    spans = [2 ** (spec['depth'] - boundary) for boundary in reversed(spec['boundaries'])]
    if profile == 'exhausted':
        return base * (2 ** len(spans))
    if profile in ('fail_once', 'errored_once'):
        return base + (spans[0] if spans else 0)
    if profile == 'recover_outer':
        return base + sum(spans[:2])
    return base


def make_probe(spec, marker):
    def probe(self, section, observations, profile, outer=None, inner=None, leaf=None, retry_count=0):
        previous = [event for event in observations if event['scenario'] == spec['name']]
        ordinal = len(previous) + 1
        first_leaf = outer in (None, 'r1') and inner in (None, 'p1') and leaf in (None, 's1')
        leaf_ordinal = 1 + sum(event['outer'] == outer and event['inner'] == inner and event['leaf'] == leaf
                               for event in previous)
        outcome = 'passed'
        if profile == 'skipped':
            outcome = 'skipped'
        elif profile == 'exhausted' or (profile == 'fail_once' and ordinal == 1):
            outcome = 'failed'
        elif profile == 'recover_outer' and first_leaf and leaf_ordinal <= 2:
            outcome = 'failed'
        elif profile == 'errored_once' and ordinal == 1:
            outcome = 'errored'
        invocation = self if spec['target'] == 'testcase' else section
        event = dict(spec, scenario=spec['name'], profile=profile, ordinal=ordinal, outer=outer, inner=inner, leaf=leaf,
                     retry_count=retry_count or 0,
                     uid=str(invocation.uid), uid_path=list(invocation.uid.list), outcome=outcome)
        observations.append(event)
        logger.info('MATRIX TRACE %s', json.dumps(event, sort_keys=True))
        getattr(section, outcome)('Review injection: {} / {} / call {}'.format(profile, spec['plan'], ordinal))

    probe.__name__ = spec['name']
    return marker(probe)


def make_case(spec):
    class MatrixCase(aetest.Testcase):
        @aetest.setup
        def setup(self, outer=None, inner=None, leaf=None, retry_count=0):
            logger.info('MATRIX SETUP scenario=%s uid=%s outer=%s inner=%s leaf=%s retry_count=%s',
                        spec['name'], self.uid, outer, inner, leaf, retry_count)

        @aetest.cleanup
        def cleanup(self, outer=None, inner=None, leaf=None, retry_count=0):
            logger.info('MATRIX CLEANUP scenario=%s uid=%s outer=%s inner=%s leaf=%s retry_count=%s',
                        spec['name'], self.uid, outer, inner, leaf, retry_count)

    MatrixCase.__name__ = spec['name']
    MatrixCase.check = make_probe(spec, aetest.test)
    MatrixCase.check.source = Source(MatrixCase.check, objcls=MatrixCase)
    return decorate(MatrixCase, spec)


class SectionCases(aetest.Testcase):
    """Each test section evaluates one placement plan."""


class SubsectionCases(aetest.CommonCleanup):
    """Subsection scenarios run after testcase scenarios, including failures."""

    @aetest.subsection
    def zz_audit(self, observations, profile, review_directory=None):
        errors = []
        summary = []
        for spec in specifications():
            events = [event for event in observations if event['scenario'] == spec['name']]
            expected = expected_calls(spec, profile)
            unique = len({event['uid'] for event in events}) == len(events)
            correct = len(events) == expected and unique
            row = dict(spec, profile=profile, expected_calls=expected, actual_calls=len(events),
                       unique_uids=unique, audit='passed' if correct else 'failed')
            summary.append(row)
            logger.info('MATRIX AUDIT %s', json.dumps(row, sort_keys=True))
            if not correct:
                errors.append(row)
        document = {'profile': profile, 'scenarios': summary, 'observations': observations,
                    'audit': 'failed' if errors else 'passed'}
        if review_directory:
            path = Path(review_directory) / ('matrix_{}.json'.format(profile))
            path.write_text(json.dumps(document, indent=2, sort_keys=True) + '\n')
            logger.info('MATRIX ARTIFACT %s', path)
        if errors:
            self.failed('Trace audit mismatches: {}'.format(errors))
        self.passed('All 90 scenario traces match the expected replay counts and have unique UIDs.')


for _spec in specifications():
    if _spec['target'] == 'testcase':
        globals()[_spec['name']] = make_case(_spec)
    elif _spec['target'] == 'test':
        _probe = decorate(make_probe(_spec, aetest.test), _spec)
        _probe.source = Source(_probe, objcls=SectionCases)
        setattr(SectionCases, _spec['name'], _probe)
    else:
        _probe = decorate(make_probe(_spec, aetest.subsection), _spec)
        _probe.source = Source(_probe, objcls=SubsectionCases)
        setattr(SubsectionCases, _spec['name'], _probe)
