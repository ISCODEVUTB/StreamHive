import json
import os
from backend.logic.entities.comment import Comment

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'backend', 'data')


class CommentController:
    def __init__(self):
        self.file = os.path.join(DIR_DATA, 'storage.json')
        if not os.path.exists(self.file):
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add(self, new_comment: Comment) -> Comment:
        with open(self.file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.append(new_comment.to_dict())  # 👈 guarda usando to_dict()
            f.seek(0)
            json.dump(data, f, indent=4)
        return new_comment

    def get_all(self) -> str:
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return json.dumps(data, indent=4)

    def get_by_id(self, comment_id: int):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for comment_dict in data:
                if comment_dict.get("id") == comment_id:
                    return comment_dict
        return None
