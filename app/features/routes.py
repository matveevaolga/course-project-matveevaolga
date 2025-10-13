from fastapi import APIRouter

from app.core.errors import AppError
from app.features.models import FeatureCreate, FeatureResp, FeatureUpdate, VoteCreate
from app.features.store import feat_store

router = APIRouter(prefix="/features", tags=["features"])


@router.get("/", response_model=list[FeatureResp])
def get_all():
    return feat_store.get_all()


@router.get("/stats")
def get_stats():
    features = feat_store.get_all_features()
    votes = feat_store.get_all_votes()

    total_features = len(features)
    total_votes = len(votes)

    avg_votes_per_feature = total_votes / total_features if total_features > 0 else 0
    total_vote_value = sum(vote["value"] for vote in votes)

    most_voted = None
    if features:
        most_voted_feature = max(features, key=lambda x: x["votes_count"])
        most_voted = {
            "id": most_voted_feature["id"],
            "title": most_voted_feature["title"],
            "votes_count": most_voted_feature["votes_count"],
        }

    return {
        "total_features": total_features,
        "total_votes": total_votes,
        "total_vote_value": total_vote_value,
        "avg_votes_per_feature": round(avg_votes_per_feature, 2),
        "most_voted_feature": most_voted,
    }


@router.get("/top", response_model=list[FeatureResp])
def get_top():
    return feat_store.get_top()


@router.post("/", response_model=FeatureResp)
def create(feat: FeatureCreate):
    return feat_store.create_feat(feat.title, feat.desc)


@router.get("/{feat_id}", response_model=FeatureResp)
def get_one(feat_id: int):
    feat = feat_store.get_by_id(feat_id)
    if not feat:
        raise AppError(code="not_found", msg="Feature not found", status=404)
    return feat


@router.put("/{feat_id}", response_model=FeatureResp)
def update(feat_id: int, feat: FeatureUpdate):
    updated_feat = feat_store.update_feat(feat_id, feat.title, feat.desc)
    if not updated_feat:
        raise AppError(code="not_found", msg="Feature not found", status=404)
    return updated_feat


@router.delete("/{feat_id}")
def delete(feat_id: int):
    success = feat_store.delete_feat(feat_id)
    if not success:
        raise AppError(code="not_found", msg="Feature not found", status=404)
    return {"message": "Feature deleted"}


@router.post("/{feat_id}/vote")
def add_vote(feat_id: int, vote: VoteCreate):
    if not feat_store.get_by_id(feat_id):
        raise AppError(code="not_found", msg="Feature not found", status=404)

    vote_data = feat_store.add_vote(feat_id, vote.value, user_id=1)

    return {"message": "Vote recorded", "vote_id": vote_data["id"]}
