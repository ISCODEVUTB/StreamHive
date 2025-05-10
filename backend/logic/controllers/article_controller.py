import json
import os
from backend.logic.entities.article import Article

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(CURRENT_DIR, '..', '..', 'data', 'json')
DIR_DATA = os.path.abspath(DIR_DATA)


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
                content = f.read().strip()
                data = json.loads(content) if content else []
                data.append(new_article.to_dict())
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            return new_article.article_id
        except Exception as e:
            raise Exception(f"Error al agregar articulo: {e}")

    def get_all(self):
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error al obtener los articulos: {e}")
            return []

    def get_by_id(self, article_id: str):
        print(article_id)
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for article in data:
                    if article['article_id'] == article_id:
                        return article
        except Exception as e:
            print(f"Error al obtener articulo con su id '{article_id}': {e}")
        return None
    
    def update_article(self, article_id: str, updates: dict) -> bool:
        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)

                for i, article in enumerate(data):
                    if article['article_id'] == article_id:
                        data[i].update(updates)
                        f.seek(0)
                        f.truncate()
                        json.dump(data, f, indent=4)
                        return True

            return False  # No se encontró el artículo
        except Exception as e:
            print(f"Error al actualizar artículo con ID '{article_id}': {e}")
            return False
        
    def delete_article(self, article_id: str) -> bool:
        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                original_length = len(data)
                
                data = [article for article in data if article['article_id'] != article_id]
                
                if len(data) == original_length:
                    return False  # No se encontró el artículo

                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
                return True
        except Exception as e:
            raise Exception()