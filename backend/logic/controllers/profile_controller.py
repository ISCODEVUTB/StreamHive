import json
import os
from backend.logic.entities.profile import Profile

PATH = os.getcwd()
DIR_DATA = os.path.join(PATH, 'data')


class ProfileController:

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
        Adds a new profile to the storage.

        :param new_profile: Profile object to be added.
        :return: The ID of the newly added profile, or empty string if failed.
        """
        if not isinstance(new_profile, Profile):
            raise ValueError("El objeto proporcionado no es una instancia de Profile.")

        try:
            with open(self.file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data.append(new_profile.to_dict())
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)
            return new_profile.profile_id
        except Exception as e:
            print(f"Error al agregar perfil: {e}")
            return ""

    def get_all(self):
        """
        Retrieve all profiles.

        :return: A list of profile dictionaries.
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
        Get a profile by its UUID.

        :param profile_id: The ID of the profile to retrieve.
        :return: The profile dict if found, None otherwise.
        """
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for profile in data:
                    if profile.get("profile_id") == profile_id:
                        return profile
        except Exception as e:
            print(f"Error al obtener perfil con ID '{profile_id}': {e}")
        return None


