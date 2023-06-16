# Social Network Analysis

This is a Python program that simulates a social network analysis system. It allows users to create users, create posts, establish friendships between users, and perform various operations to analyze the social network.

## Requirements

- Python 3.x
- PyQt5
- tabulate

## Installation

1. Clone the repository or download the code files.
2. Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

## Usage

To run the program, execute the following command:

```
python social_network.py
```

The program will open a graphical user interface (GUI) that provides various options to interact with the social network.

## Features

### User Management

- Create a new user by providing a name, user ID, and location.
- Create posts associated with a user.
- Display user information, including user ID, name, location, number of posts, and number of friends.
- Display post information for a specific user, including the content and number of likes.

### Friendship Management

- Add a friendship between two users by specifying their user IDs.
- Remove a friendship between two users by specifying their user IDs.
- Show the friends list for a specific user.

### Likes

- Add likes to a friend's posts by specifying the user ID and friend's user ID.
- Display the number of likes for a specific user.


## Acknowledgments

- The program is implemented using the PyQt5 library for the graphical user interface.
- The `tabulate` library is used to display user information in a tabular format.
- The program uses various data structures such as a binary search tree, hash table, and graph to manage users, friendships, and post data.

Feel free to explore and modify the code to suit your needs!
