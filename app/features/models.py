from pydantic import BaseModel


class FeatureBase(BaseModel):
    title: str
    desc: str


class FeatureCreate(FeatureBase):
    pass


class FeatureUpdate(FeatureBase):
    pass


class FeatureResp(FeatureBase):
    id: int
    votes_count: int = 0


class VoteBase(BaseModel):
    value: int


class VoteCreate(VoteBase):
    pass


class VoteResp(VoteBase):
    id: int
    user_id: int
    feature_id: int
