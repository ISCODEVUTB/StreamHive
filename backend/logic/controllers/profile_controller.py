import json
import os
from backend.logic.entities.profile import Profile

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'data')


class ProfileController(object):

    def __init__(self):
        self.file = os.path.join(DIR_DATA, 'storage_profile.json')
        if not os.path.exists(self.file):
            try: 
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            except Exception as e:
                print(f"Error al crear el archivo: {e}")
                raise

    def add(self, new_profile: Profile) -> str:
        """
        Add a new profile to the storage.
        """
        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data.append(new_profile.to_dict())
                f.seek(0)
                json.dump(data, f, indent=4)
            return new_profile
        except Exception as e: 
            print(f"Error al agregar perfil: {e}")
            return ""

    def get_all(self):
        """
        Retrieve all profiles.
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error al obtener perfiles: {e}")
            return []

    def get_by_id(self, profile_id: str):
        """
        Get a movie list by its UUID (string).
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for profile in data:
                    if profile.get("profile_id") == profile_id:
                        return profile
        except Exception as e:
            print(f"Error al obtener perfil con ID {profile_id}: {e}")
        return None

    def update(self, profile_id: str, updated_profile: Profile) -> bool:
        """
        Update an existing profile.
        
        Args:
            profile_id: The ID of the profile to update.
            updated_profile: A Profile object with updated information.
        
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                
                # Search for the index of the profile
                for index, profile in enumerate(data):
                    if profile.get("profile_id") == profile_id: 
                        # Update the profile in the position found
                        data[index] = updated_profile.to_dict()
                        f.seek(0)
                        json.dump(data, f, indent=4)
                        return True  # Updated done successfully
        except Exception as e:
            print(f"Error al actualizar perfil con ID {profile_id}: {e}")
        
        return False  # Profile not found