"""Audit a loop/retry review archive using an independent standard-library model.

Run: python3 audit_review_archive.py /path/to/archive.zip --output audit.json
No pyATS packages or review-job modules are imported. The expected invocations,
UID paths, outcome selection and report rollups are calculated independently.
"""
import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

PROFILES = ('passed', 'fail_once', 'recover_outer', 'exhausted', 'errored_once', 'skipped')
TARGETS = ('testcase', 'test', 'subsection')
RESULTS = ('passed', 'passx', 'failed', 'errored', 'blocked', 'skipped', 'aborted')
VALUES = (('r1', 'r2'), ('p1', 'p2'), ('s1', 's2'))
ORDER = ('skipped', 'passed', 'passx', 'blocked', 'failed', 'errored', 'aborted')
FAILURES = []
CHECKED = Counter()


def aggregate(values):
    return max(values, key=ORDER.index) if values else None


def require(condition, label, detail=None):
    CHECKED[label] += 1
    if not condition:
        FAILURES.append({'check': label, 'detail': detail})


def expected_scenario(target, depth, boundaries, profile):
    name = '{}_D{}_R{}'.format(target, depth, ''.join(str(int(i in boundaries)) for i in range(depth + 1)))
    records = []
    visits = Counter()

    def execute(boundary, coordinates, attempts, previous_failures):
        """A boundary encloses a contiguous Cartesian-product block."""
        block_result = None
        initial_result = None
        limit = 2 if boundary in boundaries else 1
        for attempt in range(limit):
            start = len(records)
            current_attempts = dict(attempts)
            current_attempts[boundary] = attempt
            retrying_failed_scope = previous_failures or (attempt > 0 and initial_result in ('failed', 'errored'))
            if boundary < depth:
                child_results = [execute(boundary + 1, coordinates + (value,), current_attempts,
                                         retrying_failed_scope) for value in VALUES[boundary]]
                block_result = aggregate(child_results)
            else:
                visits[coordinates] += 1
                number = len(records) + 1
                first_leaf = all(value in ('r1', 'p1', 's1') for value in coordinates)
                outcome = 'passed'
                if profile == 'skipped':
                    outcome = 'skipped'
                elif profile == 'exhausted' or (profile == 'fail_once' and number == 1):
                    outcome = 'failed'
                elif profile == 'recover_outer' and first_leaf and visits[coordinates] <= 2:
                    outcome = 'failed'
                elif profile == 'errored_once' and number == 1:
                    outcome = 'errored'
                parts = ['{}[{}={}]'.format(name, ('outer', 'inner', 'leaf')[i], value)
                         for i, value in enumerate(coordinates)]
                uid = '/'.join(parts) if parts else name
                for index, retry_boundary in enumerate(boundaries):
                    value = current_attempts[retry_boundary]
                    if value:
                        suffix = '{}.{}'.format(index + 1, value) if len(boundaries) > 1 else str(value)
                        uid += ' [Retry {}]'.format(suffix)
                # A testcase includes passing setup and cleanup around its probe.
                block_result = aggregate(['passed', outcome]) if target == 'testcase' else outcome
                if block_result == 'passed' and retrying_failed_scope:
                    block_result = 'passx'
                records.append({
                    'outer': coordinates[0] if depth else None,
                    'inner': coordinates[1] if depth >= 2 else None,
                    'leaf': coordinates[2] if depth >= 3 else None,
                    'retry_count': current_attempts[boundaries[-1]] if boundaries else 0,
                    'uid': uid, 'outcome': outcome, 'report_result': block_result, 'ignore': False,
                })
            if attempt == 0:
                initial_result = block_result
            if block_result not in ('failed', 'errored') or attempt + 1 == limit:
                break
            for record in records[start:]:
                record['ignore'] = True
        if block_result == 'passed' and initial_result in ('failed', 'errored'):
            block_result = 'passx'
        return block_result

    final = execute(0, (), {}, False)
    return name, records, final


def flatten(section):
    yield section
    for child in section.get('sections', []):
        yield from flatten(child)


def expected_policy(target, outcome, policy, cli=False):
    name = '{}_{}'.format(target, outcome) if cli else '{}_{}_{}'.format(target, policy, outcome)
    retries = 0
    if not cli:
        retries = int(policy == 'explicit' or outcome == 'failed')
    elif policy in ('selected', 'override2') and outcome in ('failed', 'errored'):
        retries = 2 if policy == 'override2' else 1
    elif policy == 'testsection' and target == 'test' and outcome == 'failed':
        retries = 1
    records = []
    for attempt in range(retries + 1):
        for outer in ('a', 'b'):
            for inner in (1, 2):
                uid = '{}[outer={}]/{}[inner={}]'.format(name, outer, name, inner)
                if attempt:
                    uid += ' [Retry {}]'.format(attempt)
                records.append({'outer': outer, 'inner': inner, 'retry_count': attempt,
                                'uid': uid, 'outcome': outcome, 'report_result': outcome,
                                'ignore': attempt < retries})
    if cli and policy == 'testsection' and target == 'testcase' and outcome == 'failed':
        records = []
        for outer in ('a', 'b'):
            for inner in (1, 2):
                for attempt in range(2):
                    records.append({'outer': outer, 'inner': inner, 'retry_count': attempt,
                                    'uid': '{}[outer={}]/{}[inner={}]'.format(name, outer, name, inner),
                                    'outcome': outcome, 'report_result': outcome, 'ignore': False,
                                    'section_uid': 'check' + (' [Retry 1]' if attempt else ''),
                                    'child_ignore': attempt == 0, 'count_top': attempt == 0})
    elif cli and target == 'testcase':
        for record in records:
            record.update(section_uid='check', child_ignore=False)
    return name, records


def audit_task(task, data, scenarios):
    task_id = task['id']
    by_path = {tuple(section['idlist']): section for root in task['sections'] for section in flatten(root)}
    case_records = []
    grouped_records = {'test': [], 'subsection': []}
    require(data['audit'] == 'passed', 'artifact_audit', task_id)
    require({row['name'] for row in data['scenarios']} == {row[0] for row in scenarios},
            'scenario_coverage', task_id)
    require(all(row['audit'] == 'passed' for row in data['scenarios']), 'scenario_audits', task_id)
    for name, target, expected in scenarios:
        actual = [row for row in data['observations'] if row.get('scenario', row['name']) == name]
        require(len(actual) == len(expected), 'invocation_count', (task_id, name, len(expected), len(actual)))
        group_path = [task_id] + ([] if target == 'testcase' else [
            'SectionCases' if target == 'test' else 'common_cleanup'])
        for index, (observed, reference) in enumerate(zip(actual, expected)):
            detail = (task_id, name, index + 1)
            for field in ('outer', 'inner', 'leaf', 'retry_count', 'uid', 'outcome'):
                require(observed.get(field) == reference.get(field), 'trace_' + field,
                        (detail, reference.get(field), observed.get(field)))
            if 'ordinal' in observed:
                require(observed['ordinal'] == index + 1, 'trace_ordinal', detail)
            expected_path = tuple(group_path + [reference['uid']])
            require(tuple(observed['uid_path']) == expected_path, 'trace_uid_path', detail)
            entry = by_path.get(expected_path)
            require(entry is not None, 'reported_invocation', (detail, expected_path))
            if entry:
                require(entry['result']['value'] == reference['report_result'], 'reported_result',
                        (detail, reference['report_result'], entry['result']))
                require(bool(entry.get('ignore', False)) == reference['ignore'], 'reported_ignore',
                        (detail, reference['ignore'], entry.get('ignore', False)))
            if 'section_uid' in reference:
                child_uid = reference['section_uid']
                require(observed['section_uid'] == child_uid, 'trace_section_uid', detail)
                child_path = expected_path + (child_uid,)
                require(tuple(observed['section_uid_path']) == child_path, 'trace_section_path', detail)
                child = by_path.get(child_path)
                require(child is not None, 'reported_child', detail)
                if child:
                    require(child['result']['value'] == reference['outcome'], 'reported_child_result', detail)
                    require(bool(child.get('ignore', False)) == reference['child_ignore'],
                            'reported_child_ignore', detail)
        if target == 'testcase':
            case_records.extend(record for record in expected if record.get('count_top', True))
        else:
            grouped_records[target].extend(expected)
    values = [row['report_result'] for row in case_records if not row['ignore']]
    for target, records in grouped_records.items():
        group_values = [row['report_result'] for row in records if not row['ignore']]
        if target == 'subsection':
            group_values.append('passed')  # final audit subsection
        result = aggregate(group_values)
        group = next(section for section in task['sections'] if section['id'] == (
            'SectionCases' if target == 'test' else 'common_cleanup'))
        require(group['result']['value'] == result, 'group_rollup', (task_id, target, result, group['result']))
        values.append(result)
    counts = Counter(values)
    for key in RESULTS:
        require(task['summary'][key] == counts[key], 'task_summary_' + key,
                (task_id, counts[key], task['summary'][key]))
    require(task['summary']['total'] == len(values), 'task_summary_total', task_id)
    result = aggregate(values)
    require(task['result']['value'] == result, 'task_rollup', (task_id, result, task['result']))
    audits = [section for section in by_path.values() if section['id'] == 'zz_audit']
    require(len(audits) == 1 and audits[0]['result']['value'] == 'passed', 'reported_audit', task_id)
    return {'task': task_id, 'scenarios': len(scenarios), 'invocations': len(data['observations']),
            'expected_task_result': result, 'actual_task_result': task['result']['value']}, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    summary = []
    expected_overall = Counter()
    with ZipFile(args.archive) as bundle:
        members = {Path(name).name: name for name in bundle.namelist()}

        def read(name):
            return json.loads(bundle.read(members[name]))

        report = read('results.json')['report']
        tasks = {task['id']: task for task in report['tasks']}
        cli_profiles = ('selected', 'excluded', 'override0', 'override2', 'testsection')
        expected_tasks = {'matrix_' + profile for profile in PROFILES} | {'eligibility'} | {
            'cli_' + profile for profile in cli_profiles}
        require(set(tasks) == expected_tasks, 'task_profiles')
        for profile in PROFILES:
            scenarios = []
            for target in TARGETS:
                for depth in range(4):
                    for bits in itertools.product((0, 1), repeat=depth + 1):
                        boundaries = [i for i, enabled in enumerate(bits) if enabled]
                        name, expected, _ = expected_scenario(target, depth, boundaries, profile)
                        scenarios.append((name, target, expected))
            row, counts = audit_task(tasks['matrix_' + profile], read('matrix_' + profile + '.json'), scenarios)
            summary.append(row)
            expected_overall.update(counts)
        for profile in ('eligibility',) + cli_profiles:
            cli = profile != 'eligibility'
            scenarios = []
            for target in TARGETS:
                for policy in ((profile,) if cli else ('default', 'explicit')):
                    for outcome in RESULTS:
                        name, expected = expected_policy(target, outcome, policy, cli)
                        scenarios.append((name, target, expected))
            task_id = 'cli_' + profile if cli else profile
            row, counts = audit_task(tasks[task_id], read(task_id + '.json'), scenarios)
            summary.append(row)
            expected_overall.update(counts)
        for key in RESULTS:
            require(report['summary'][key] == expected_overall[key], 'overall_summary_' + key,
                    (expected_overall[key], report['summary'][key]))
        result = aggregate([row['expected_task_result'] for row in summary])
        require(report['result']['value'] == result, 'overall_result', report['result'])
        manifest = read('matrix_manifest.json')
        require(manifest['total_scenarios'] == sum(row['scenarios'] for row in summary), 'manifest_scenarios')
    output = {'archive': str(args.archive), 'scenarios': sum(row['scenarios'] for row in summary),
              'invocations': sum(row['invocations'] for row in summary), 'checks': dict(CHECKED),
              'failures': FAILURES, 'tasks': summary}
    if args.output:
        args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return bool(FAILURES)


if __name__ == '__main__':
    raise SystemExit(main())
