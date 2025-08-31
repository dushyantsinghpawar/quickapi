import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db
from ..model import load_model
from ..security import get_current_user

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/predict", response_model=schemas.IrisOut)
def predict(
    payload: schemas.IrisIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    model, target_names = load_model()
    x = np.array(
        [
            [
                payload.sepal_length,
                payload.sepal_width,
                payload.petal_length,
                payload.petal_width,
            ]
        ],
        dtype=float,
    )
    proba = model.predict_proba(x)[0]
    idx = int(proba.argmax())
    label = target_names[idx]
    probs = {target_names[i]: float(proba[i]) for i in range(len(target_names))}

    # log to Postgres
    rec = models.Prediction(
        user_id=current_user.id,
        features={
            "sepal_length": payload.sepal_length,
            "sepal_width": payload.sepal_width,
            "petal_length": payload.petal_length,
            "petal_width": payload.petal_width,
        },
        pred_label=label,
        pred_confidence=float(proba[idx]),
    )
    db.add(rec)
    db.commit()
    return {"label": label, "probabilities": probs}
