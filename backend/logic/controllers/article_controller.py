import json
import os
from backend.logic.entities.article import Article

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'backend', 'data')


class ArticleController:
    def __init__(self):
        self.file = os.path.join(DIR_DATA, 'storage_article.json')
        if not os.path.exists(self.file):
            try:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except Exception as e:
                print(f"Error al crear el articulo: {e}")
                raise

    def add(self, new_article: Article) -> Article:
        if not isinstance(new_article, Article):
            raise ValueError("El objeto proporcionado no es una instancia de Articulo.")

        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data.append(new_article.to_dict())
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            return new_article.id
        except Exception as e:
            print(f"Error al agregar articulo: {e}")
            return ""

    def get_all(self):

        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error al obtener los articulos: {e}")
            return []

    def get_by_id(self, article_id: str):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for article in data:
                    if article.get("id") == int (article_id):
                        return article
        except Exception as e:
            print(f"Error al obtener articulo con su id '{article_id}': {e}")
        return None
