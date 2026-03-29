from typing import Dict, List


class FeatureStore:
    def __init__(self):
        self.features: Dict[int, dict] = {}
        self.votes: Dict[int, dict] = {}
        self.feature_votes: Dict[int, List[int]] = {}
        self.user_votes: Dict[int, List[int]] = {}
        self._feat_cnt = 1
        self._vote_cnt = 1

    def get_all(self):
        return list(self.features.values())

    def get_by_id(self, feat_id: int) -> dict:
        return self.features.get(feat_id)

    def create_feat(self, title: str, desc: str) -> dict:
        feat_id = self._feat_cnt
        self.features[feat_id] = {
            "id": feat_id,
            "title": title,
            "desc": desc,
            "votes_count": 0,
        }
        self._feat_cnt += 1
        return self.features[feat_id]

    def update_feat(self, feat_id: int, title: str, desc: str) -> dict:
        if feat_id in self.features:
            self.features[feat_id]["title"] = title
            self.features[feat_id]["desc"] = desc
            return self.features[feat_id]
        return None

    def delete_feat(self, feat_id: int) -> bool:
        if feat_id in self.features:
            del self.features[feat_id]
            vote_ids_to_delete = [
                vote_id
                for vote_id, vote in self.votes.items()
                if vote["feature_id"] == feat_id
            ]
            for vote_id in vote_ids_to_delete:
                del self.votes[vote_id]
            return True
        return False

    def add_vote(self, feat_id: int, value: int, user_id: int) -> dict:
        vote_id = self._vote_cnt
        self.votes[vote_id] = {
            "id": vote_id,
            "feature_id": feat_id,
            "value": value,
            "user_id": user_id,
        }

        # Update vote count
        if feat_id in self.features:
            self.features[feat_id]["votes_count"] += value

        self._vote_cnt += 1
        return self.votes[vote_id]

    def get_top(self):
        features = list(self.features.values())
        return sorted(features, key=lambda x: x["votes_count"], reverse=True)[:10]


feat_store = FeatureStore()
