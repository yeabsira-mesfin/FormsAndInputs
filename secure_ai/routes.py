from typing import Literal

from fastapi import BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from .auth import identity, require_role
from .evaluation import run_evaluation


class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    split: Literal['dev','test'] = 'test'


def register(app):
    store = app.state.store

    @app.post('/api/evaluations', status_code=201)
    def run(body: EvaluationRequest, user=Depends(identity)):
        require_role(user, 'admin','analyst')
        if not store.consume('evaluation:' + user['id'], 10, 60):
            raise HTTPException(429, 'Evaluation limit reached')
        report = run_evaluation(body.split)
        record_id = store.save(user['tenant'], 'evaluation', report)
        store.audit(user, 'evaluation.run', record_id)
        return dict(id=record_id, **report)

    @app.get('/api/evaluations')
    def reports(user=Depends(identity)):
        return [{k:v for k,v in r.items() if k != 'rows'} for r in store.records(user['tenant'], 'evaluation')]

    @app.get('/api/evaluations/{record_id}')
    def report(record_id: str, user=Depends(identity)):
        row = store.record(user['tenant'], 'evaluation', record_id)
        if not row:
            raise HTTPException(404, 'Report not found')
        return row
