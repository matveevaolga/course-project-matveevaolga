import re

from pydantic import BaseModel, Field, field_validator

TITLE_EMPTY_ERROR = "Title cannot be empty"
TITLE_DANGEROUS_ERROR = "Title contains potentially dangerous content"
DESC_EMPTY_ERROR = "Description cannot be empty"
DESC_TOO_LONG_ERROR = "Description too long"
DESC_UNSAFE_ERROR = "Description contains unsafe content"
VOTE_VALUE_ERROR = "Vote value must be between 1 and 5"


class FeatureBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Feature title")
    desc: str = Field(
        ..., min_length=1, max_length=500, description="Feature description"
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError(TITLE_EMPTY_ERROR)

        dangerous_patterns = [
            r"<script",
            r"javascript:",
            r"on\w+=",
            r"'.*--",
            r";.*--",
            r"'.*;",
            r"union.*select",
            r"drop.*table",
            r"\bor\b",
            r"\band\b",
            r"\bselect\b",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError(TITLE_DANGEROUS_ERROR)

        dangerous_chars = ["'", '"', ";", "--", "/*", "*/"]
        for char in dangerous_chars:
            if char in v:
                raise ValueError(TITLE_DANGEROUS_ERROR)

        return v.strip()

    @field_validator("desc")
    @classmethod
    def validate_desc(cls, v):
        if not v or not v.strip():
            raise ValueError(DESC_EMPTY_ERROR)

        if len(v) > 500:
            raise ValueError(DESC_TOO_LONG_ERROR)

        dangerous_tags = ["script", "iframe", "object", "embed"]
        for tag in dangerous_tags:
            if f"<{tag}" in v.lower():
                raise ValueError(DESC_UNSAFE_ERROR)

        return v.strip()


class FeatureCreate(FeatureBase):
    pass


class FeatureUpdate(FeatureBase):
    pass


class FeatureResp(FeatureBase):
    id: int
    votes_count: int = 0


class VoteBase(BaseModel):
    value: int = Field(..., ge=1, le=5, description="Vote value between 1-5")

    @field_validator("value")
    @classmethod
    def validate_vote_value(cls, v):
        if v not in [1, 2, 3, 4, 5]:
            raise ValueError(VOTE_VALUE_ERROR)
        return v


class VoteCreate(VoteBase):
    pass


class VoteResp(VoteBase):
    id: int
    user_id: int
    feature_id: int
