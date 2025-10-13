from fastapi import APIRouter

from app.core.errors import AppError
from app.core.metrics import track_performance
from app.features.models import FeatureCreate, FeatureResp, VoteCreate
from app.features.store import feat_store

router = APIRouter(prefix="/features", tags=["features"])


@router.get("/", response_model=list[FeatureResp])
@track_performance("GET /features")
def get_all():
    return feat_store.get_all()


@router.get("/top", response_model=list[FeatureResp])
@track_performance("GET /features/top")
def get_top():
    return feat_store.get_top()


@router.post("/", response_model=FeatureResp)
@track_performance("POST /features")
def create(feat: FeatureCreate):
    return feat_store.create_feat(feat.title, feat.desc)


@router.get("/{feat_id}", response_model=FeatureResp)
@track_performance("GET /features/{id}")
def get_one(feat_id: int):
    feat = feat_store.get_by_id(feat_id)
    if not feat:
        raise AppError(code="not_found", msg="Feature not found", status=404)
    return feat


@router.post("/{feat_id}/vote")
@track_performance("POST /features/{id}/vote")
def add_vote(feat_id: int, vote: VoteCreate):
    if not feat_store.get_by_id(feat_id):
        raise AppError(code="not_found", msg="Feature not found", status=404)

    vote_data = feat_store.add_vote(feat_id, vote.value, user_id=1)
    return {"message": "Vote recorded", "vote_id": vote_data["id"]}
