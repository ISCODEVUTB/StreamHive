import json
import os
from backend.logic.entities.movie_list import MovieList

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'data')


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
            data = json.load(f)
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
            data_str = json.dumps(data)
        return data_str

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

    def update(self, movie_list_id: str, updated_movie_list: MovieList) -> bool:
        """
        Update an existing movie list.
        
        Args:
            movie_list_id: The ID of the movie list to update.
            updated_movie_list: A MovieList object with updated information.
        
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        with open(self.file, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            
            # Search for the index of the movie list
            for index, movie_list in enumerate(data):
                # Search the movie list by its id
                if movie_list.get("id") == movie_list_id:
                    # Update the movie list in the position found
                    data[index] = updated_movie_list.to_dict()  # Change the dictionary for the updated one
                    f.seek(0)
                    json.dump(data, f, indent=4)  # Save the changes made
                    return True  # Updated done successfully
        
        return False  # Movie list not found