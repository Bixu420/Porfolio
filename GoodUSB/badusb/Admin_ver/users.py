

import json
import hashlib

class UserManager:
    def __init__(self, user_filename='team.json', config_filename='user_config.json'):
        self.user_filename = user_filename
        self.config_filename = config_filename
        self.user_data = self.load_user_data()
        self.user_config = self.load_user_config()

    def load_user_data(self):
        try:
            with open(self.user_filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def load_user_config(self):
        try:
            with open(self.config_filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_data(self, data):
        with open(self.user_filename, 'w') as file:
            json.dump(data, file)
            print('dump')

    def save_user_config(self, config1):
        with open(self.config_filename, 'w') as file:
            json.dump(config1, file)
            print('dump')

    def add_user(self, username, password, config_data=None):
        if username in self.user_data:
            print(f"User '{username}' already exists. Please choose a different username.")
            return

        hashed_password = self.hash_password(password)

        # Add the new user to the dictionaries
        self.user_data[username] = {'password': hashed_password}
        
        if config_data is not None:
            self.user_config = config_data

        # Save the updated user data and user configuration
        self.save_user_data()
        self.save_user_config()
        print(f"User '{username}' added successfully.")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

# Example usage
user_manager = UserManager()

new_username = 'tom'
new_password = 'tom'
new_config_data = {'threshold': '0.0170', 'showip': 'true', 'password': user_manager.hash_password('admin')}

#user_manager.add_user(new_username, new_password, new_rank,  new_config_data)

#print("Updated user data:")


#print("Updated user configuration:")
#print(user_manager.user_config)


#user_manager.get_password(username_to_add)



