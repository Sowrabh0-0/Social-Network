import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QColor
from tabulate import tabulate
from collections import defaultdict

class User:
    def __init__(self, name, user_id, location):
        self.name = name
        self.user_id = user_id
        self.location = location
        self.posts = []
        self.friends = []
        self.likes = 0

    def add_post(self, post):
        self.posts.append(post)

    def remove_post(self, post):
        if post in self.posts:
            self.posts.remove(post)

    def add_friend(self, friend):
        self.friends.append(friend)

    def remove_friend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)

    def get_number_of_posts(self):
        return len(self.posts)

    def get_number_of_friends(self):
        return len(self.friends)
     
    def add_like(self):
        self.likes += 1

    def get_likes(self):
        return self.likes

class Post:
    def __init__(self, content):
        self.content = content
        self.likes = 0

    def add_like(self):
        self.likes += 1

    def remove_like(self):
        if self.likes > 0:
            self.likes -= 1


class SocialNetwork:
    def __init__(self):
        self.users = {}  # Dictionary to store user objects
        self.user_bst = BST()  # Binary Search Tree to store users
        self.user_hash_table = HashTable()  # Hash Table to store users
        self.friend_graph = Graph()  # Graph to represent friendships

    def add_user(self, user):
        if user.user_id not in self.users:
            self.users[user.user_id] = user
            self.user_bst.insert(user)
            self.user_hash_table.insert(user.user_id, user)

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            self.user_bst.remove(user_id)
            self.user_hash_table.remove(user_id)

    def add_friendship(self, user_id1, user_id2):
        if user_id1 in self.users and user_id2 in self.users:
            user1 = self.users[user_id1]
            user2 = self.users[user_id2]
            if user2 not in user1.friends:  # Check if the friend already exists
                user1.add_friend(user2)
                user2.add_friend(user1)
                self.friend_graph.add_edge(user_id1, user_id2)
                return True
        return False

    def remove_friendship(self, user_id1, user_id2):
        if user_id1 in self.users and user_id2 in self.users:
            user1 = self.users[user_id1]
            user2 = self.users[user_id2]
            user1.remove_friend(user2)
            user2.remove_friend(user1)
            self.friend_graph.remove_edge(user_id1, user_id2)

    def get_friends_list(self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            friends_list = []
            for friend in user.friends:
                friends_list.append(friend.user_id)
            return friends_list
        return []

    def get_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        return None
    
    def add_likes(self, user_id, friend_id):
        if user_id in self.users and friend_id in self.users:
            user = self.users[user_id]
            friend = self.users[friend_id]
            friend.add_like()
            print(f"User {user_id} added a like for friend {friend_id}.")
        else:
            print("User ID does not exist.")
    
    def get_likes(self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            likes = user.get_likes()
            print(f"User {user_id} has {likes} likes.")
        else:
            print("User ID does not exist.")


class BSTNode:
    def __init__(self, user):
        self.user = user
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, user):
        if self.root is None:
            self.root = BSTNode(user)
        else:
            self._insert_recursive(self.root, user)

    def _insert_recursive(self, node, user):
        if user.user_id < node.user.user_id:
            if node.left is None:
                node.left = BSTNode(user)
            else:
                self._insert_recursive(node.left, user)
        elif user.user_id > node.user.user_id:
            if node.right is None:
                node.right = BSTNode(user)
            else:
                self._insert_recursive(node.right, user)

    def remove(self, user_id):
        self.root = self._remove_recursive(self.root, user_id)

    def _remove_recursive(self, node, user_id):
        if node is None:
            return node

        if user_id < node.user.user_id:
            node.left = self._remove_recursive(node.left, user_id)
        elif user_id > node.user.user_id:
            node.right = self._remove_recursive(node.right, user_id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min(node.right)
                node.user = successor.user
                node.right = self._remove_recursive(node.right, successor.user.user_id)

        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.user


class HashTable:
    def __init__(self):
        self.size = 10
        self.table = defaultdict(list)

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        hash_value = self._hash(key)
        self.table[hash_value].append(value)

    def remove(self, key):
        hash_value = self._hash(key)
        if key in self.table[hash_value]:
            self.table[hash_value].remove(key)

    def search(self, key):
        hash_value = self._hash(key)
        return self.table[hash_value]


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, user_id1, user_id2):
        self.graph[user_id1].append(user_id2)
        self.graph[user_id2].append(user_id1)

    def remove_edge(self, user_id1, user_id2):
        if user_id1 in self.graph:
            self.graph[user_id1].remove(user_id2)
        if user_id2 in self.graph:
            self.graph[user_id2].remove(user_id1)

    def get_friends(self, user_id):
        if user_id in self.graph:
            return self.graph[user_id]
        return []


class SocialNetworkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.social_network = SocialNetwork()
        self.init_ui()
    

    def init_ui(self):
        self.setWindowTitle("Social Network Analysis")
        self.setGeometry(200, 200, 800, 600)

        title_label = QLabel("Social Network")
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)

        # Create widgets
        self.create_user_button = QPushButton("Create User")
        self.create_post_button = QPushButton("Create Post")
        self.add_friendship_button = QPushButton("Add Friendship")
        self.remove_friendship_button = QPushButton("Remove Friendship")
        self.display_user_info_button = QPushButton("Display User Info")
        self.display_post_info_button = QPushButton("Display Post Info")
        self.display_user_table_button = QPushButton("Display User Table")
        self.show_friends_list_button = QPushButton("Show Friends List")
        self.add_likes_button = QPushButton("Add Likes")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.create_user_button)
        layout.addWidget(self.create_post_button)
        layout.addWidget(self.add_friendship_button)
        layout.addWidget(self.remove_friendship_button)
        layout.addWidget(self.display_user_info_button)
        layout.addWidget(self.display_post_info_button)
        layout.addWidget(self.display_user_table_button)
        layout.addWidget(self.show_friends_list_button)
        layout.addWidget(self.add_likes_button)
        # Set main layout
        self.setLayout(layout)

        # Set font and color properties
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.create_user_button.setFont(font)
        self.create_post_button.setFont(font)
        self.add_friendship_button.setFont(font)
        self.remove_friendship_button.setFont(font)
        self.display_user_info_button.setFont(font)
        self.display_post_info_button.setFont(font)
        self.display_user_table_button.setFont(font)
        self.show_friends_list_button.setFont(font)
        self.add_likes_button.setFont(font)



        self.setStyleSheet("""
            background-color: #e9e0d4;
            QPushButton {
                background-color: #e9e0d4;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e9e0d4;
            }
            """)
    

        # Set window color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#42bd9a"))
        self.setPalette(palette)

        # Connect buttons to their respective functions
        self.create_user_button.clicked.connect(self.create_user)
        self.create_post_button.clicked.connect(self.create_post)
        self.add_friendship_button.clicked.connect(self.add_friendship)
        self.remove_friendship_button.clicked.connect(self.remove_friendship)
        self.display_user_info_button.clicked.connect(self.display_user_info)
        self.display_post_info_button.clicked.connect(self.display_post_info)
        self.display_user_table_button.clicked.connect(self.display_user_table)
        self.show_friends_list_button.clicked.connect(self.show_friends_list)
        self.add_likes_button.clicked.connect(self.add_likes)


        self.show()

    def create_user(self):
        name, ok = QInputDialog.getText(self, "Create User", "Enter user name:")
        if ok and name:
            user_id, ok = QInputDialog.getInt(self, "Create User", "Enter user ID:")
            if ok:
                location, ok = QInputDialog.getText(self, "Create User", "Enter user location:")
                if ok and location:
                    user = User(name, user_id, location)
                    self.social_network.add_user(user)
                    QMessageBox.information(self, "Create User", "User created successfully!")

    def create_post(self):
        user_id, ok = QInputDialog.getInt(self, "Create Post", "Enter user ID:")
        if ok:
            content, ok = QInputDialog.getText(self, "Create Post", "Enter post content:")
            if ok and content:
                user = self.social_network.get_user(user_id)
                if user:
                    post = Post(content)
                    user.add_post(post)
                    QMessageBox.information(self, "Create Post", "Post created successfully!")
                else:
                    QMessageBox.warning(self, "Create Post", "User not found!")

    def add_friendship(self):
        user_id, ok = QInputDialog.getInt(self, "Add Friendship", "Enter your user ID:")
        if ok:
            friend_id, ok = QInputDialog.getInt(self, "Add Friendship", "Enter your friend's user ID:")
            if ok:
                self.social_network.add_friendship(user_id, friend_id)
                QMessageBox.information(self, "Add Friendship", "Friendship added successfully!")


    def remove_friendship(self):
        user_id, ok = QInputDialog.getInt(self, "Remove Friendship", "Enter your User ID:")
        if ok:
            friend_id, ok = QInputDialog.getInt(self, "Remove Friendship", "Enter Friend's User ID:")
        if ok:
            self.social_network.remove_friendship(user_id, friend_id)
            QMessageBox.information(self, "Remove Friendship", "Friendship removed successfully!")


    def display_user_info(self):
        user_id, ok = QInputDialog.getInt(self, "Display User Info", "Enter user ID:")
        if ok:
            user = self.social_network.get_user(user_id)
            if user:
                info = f"User ID: {user.user_id}\nName: {user.name}\nLocation: {user.location}\n" \
                       f"Number of Posts: {user.get_number_of_posts()}\nNumber of Friends: {user.get_number_of_friends()}"
                QMessageBox.information(self, "User Info", info)
            else:
                QMessageBox.warning(self, "Display User Info", "User not found!")

    def display_post_info(self):
        user_id, ok = QInputDialog.getInt(self, "Display Post Info", "Enter user ID:")
        if ok:
            user = self.social_network.get_user(user_id)
            if user:
                posts = user.posts
                if posts:
                    info = ""
                    for i, post in enumerate(posts):
                        info += f"Post {i + 1}:\n{post.content}\nLikes: {post.likes}\n\n"
                    QMessageBox.information(self, "Post Info", info)
                else:
                    QMessageBox.information(self, "Post Info", "No posts found.")
            else:
                QMessageBox.warning(self, "Display Post Info", "User not found!")

    def display_user_table(self):
        user_table = []
        for user_id, user in self.social_network.users.items():
            user_table.append([user_id, user.name, user.location, user.get_number_of_friends()])
        headers = ["User ID", "Name", "Location", "Number of Friends"]
        table = tabulate(user_table, headers, tablefmt="grid")
        QMessageBox.information(self, "User Table", table)

    def show_friends_list(self):
        user_id, ok = QInputDialog.getInt(self, "Show Friends List", "Enter user ID:")
        if ok:
            friends_list = self.social_network.get_friends_list(user_id)
            if friends_list:
                QMessageBox.information(self, "Friends List", str(friends_list))
            else:
                QMessageBox.warning(self, "Show Friends List", "User not found or no friends found!")

    def add_likes(self):
        user_id, ok = QInputDialog.getInt(self, "Add Likes", "Enter your User ID:")
        if ok:
            friend_id, ok = QInputDialog.getInt(self, "Add Likes", "Enter Friend's User ID:")
        if ok:
            self.social_network.add_likes(user_id, friend_id)
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SocialNetworkGUI()
    sys.exit(app.exec())
