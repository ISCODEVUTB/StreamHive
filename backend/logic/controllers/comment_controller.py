import json
import os
import ast
from backend.logic.entities.comment import Comment

PATH = os.getcwd()
DIR_DATA = PATH + '{0}backend{0}data{0}'.format(os.sep)


class CommentController(object):
    def __init__(self):
        self.file = '{0}{1}'.format(DIR_DATA, 'storage.json')
        if not os.path.exists(self.file):
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add(self, new_comment: Comment) -> str:
        with open(self.file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.append(new_comment.__str__())  # Guardado como string
            f.seek(0)
            json.dump(data, f)
        return new_comment

    def get_all(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data_str = json.dumps(data)
        return data_str

    def get_by_id(self, comment_id: int):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for comment_str in data:
                comment_dict = ast.literal_eval(comment_str)
                if comment_dict.get("id") == comment_id:
                    return comment_dict
        return None
