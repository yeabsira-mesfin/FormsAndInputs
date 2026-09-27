import json

from secure_ai.evaluation import FIXTURE_PATH, run_evaluation
from test_security import login, setup


def test_dataset_has_120_unique_cases_and_family_holdout():
    rows=json.loads(FIXTURE_PATH.read_text())
    assert len(rows)==120 and len({r['id'] for r in rows})==120
    dev={r['family'] for r in rows if r['split']=='dev'}
    test={r['family'] for r in rows if r['split']=='test'}
    assert not dev.intersection(test)
    assert len(dev)==len(test)==12


def test_metrics_recomputed_from_results():
    result=run_evaluation('test')
    rows=result['rows']
    attacks=[r for r in rows if r['attack']]
    assert result['defended']['attack_success_rate']==sum(not r['defended_pass'] for r in attacks)/len(attacks)
    assert 0 < result['defended']['attack_success_rate'] < result['baseline']['attack_success_rate']
    assert result['false_positive_rate']>0  # Honest known limitation, not a perfect score.


def test_report_persists_and_is_tenant_scoped(setup):
    alpha=login(setup)
    res=alpha.post('/api/evaluations',json={'split':'test'})
    assert res.status_code==201
    report_id=res.json()['id']
    assert alpha.get('/api/evaluations/'+report_id).json()['case_count']==60
    beta=login(setup,'admin@beta.test')
    assert beta.get('/api/evaluations/'+report_id).status_code==404
    assert beta.get('/api/evaluations').json()==[]


def test_viewer_cannot_start_evaluations(setup):
    client=login(setup,'viewer@alpha.test')
    assert client.post('/api/evaluations',json={'split':'test'}).status_code==403


def test_invalid_split_and_extra_fields_rejected(setup):
    client=login(setup)
    assert client.post('/api/evaluations',json={'split':'private'}).status_code==422
    assert client.post('/api/evaluations',json={'split':'test','target_url':'http://169.254.169.254'}).status_code==422
