import json
import os

from datetime import datetime, timezone

from backend.logic.entities.movie_list import MovieList

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATA = os.path.join(CURRENT_DIR, '..', '..', 'data')
DIR_DATA = os.path.abspath(DIR_DATA)


class MovieListController(object):

    def __init__(self):
        self.file = os.path.join(DIR_DATA, 'storage_movie_lists.json')
        if not os.path.exists(self.file):
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def add(self, new_movie_list: MovieList) -> MovieList:
        """
        Add a new movie list to the storage.
        """
        with open(self.file, 'r+', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data.append(new_movie_list.to_dict())
            f.seek(0)
            json.dump(data, f, indent=4)
        return new_movie_list

    def get_all(self):
        """
        Retrieve all movie lists.
        """
        # Opening JSON file
        with open(self.file, 'r', encoding='utf-8') as openfile:
            # Reading from json file
            data = json.load(openfile)
        return data

    def get_by_id(self, movie_list_id: str):
        """
        Get a movie list by its UUID (string).
        """
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for movie_list in data:
                if movie_list.get("id") == movie_list_id:
                    return movie_list
        return None
    
    def remove(self, movie_list_id: str) -> bool:
        with open(self.file, "r+", encoding="utf-8") as f:
            data = json.load(f)

            # Buscar directamente en data
        
            new_movies_list = [m for m in data if m["id"] != movie_list_id]

            if len(data) == len(new_movies_list):
                print("Movie list not found.")
                return False

            data = new_movies_list

            # Guardar cambios
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
            f.flush()
            return True
        

    def add_movie(self, movie_list_id: str, movie_id: str) -> bool:
        with open(self.file, "r+", encoding="utf-8") as f:
            data = json.load(f)

            # Buscar la lista directamente en data
            for movie_list in data:
                if movie_list["id"] == movie_list_id:
                    if any(str(m["movie_id"]) == str(movie_id) for m in movie_list.get("movies", [])):
                        print("Movie already in list.")
                        return False

                    movie_list.setdefault("movies", []).append({
                        "movie_id": movie_id,
                        "added_at": datetime.now(timezone.utc).isoformat()
                    })

                    # Guardar cambios
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                    f.flush()
                    return True

            print("Movie list not found.")
            return False
    

    def remove_movie(self, movie_list_id: str, movie_id: str) -> bool:
        with open(self.file, "r+", encoding="utf-8") as f:
            data = json.load(f)

            # Buscar directamente en data
            for movie_list in data:
                if movie_list["id"] == movie_list_id:
                    movies = movie_list.get("movies", [])
                    new_movies = [m for m in movies if m["movie_id"] != movie_id]

                    if len(movies) == len(new_movies):
                        print("Movie not found in list.")
                        return False

                    movie_list["movies"] = new_movies

                    # Guardar cambios
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                    f.flush()
                    return True

            print("Movie list not found.")
            return False