from pydantic import BaseModel, constr


class FeatureBase(BaseModel):
    title: constr(min_length=1, max_length=100)
    desc: constr(min_length=1, max_length=500)


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
