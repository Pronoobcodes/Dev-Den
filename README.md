# Blog Platform with Real-Time Chat

A Django-based blog platform with user authentication, posts, a voting system, and real-time private messaging using WebSockets.

## Features

- 👥 **User Accounts** - Registration, login, and profile management with avatars
- 📝 **Posts & Comments** - Create, edit, and delete posts with category organization
- 👍 **Voting System** - Upvote and downvote posts with separate vote tracking
- 💬 **Real-Time Chat** - Private messages between users using WebSockets
- 🏷️ **Categories** - Organize posts by topics
- 🔍 **Search** - Find posts by title, description, or category
- 📱 **Responsive Design** - Works on desktop and mobile devices

## Tech Stack

- **Backend**: Django 5.2
- **WebSocket**: Django Channels 4.3 + Daphne ASGI
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Media**: Pillow for image handling

## Installation

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pronoobcodes/Dev-Den.git
   cd Blog2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

   The app will be available at `http://localhost:8000`

## Project Structure

```
Blog2/
├── blogApp/              # Main app with models, views, forms
│   ├── models.py         # Post, User, Message, PrivateMessage
│   ├── views.py          # All view logic
│   ├── urls.py           # URL routing
│   ├── forms.py          # Form definitions
│   └── templates/        # HTML templates
├── chat/                 # WebSocket/Channels app
│   ├── consumers.py       # WebSocket handlers
│   ├── routing.py         # WebSocket URL patterns
│   └── models.py          # Chat models
├── blogProject/          # Project settings
│   ├── settings.py        # Django configuration
│   ├── asgi.py            # ASGI config (Channels)
│   └── wsgi.py            # WSGI config
├── static/               # CSS, JavaScript, media
│   ├── css/style.css
│   ├── js/
│   └── media/
└── manage.py             # Django management
```

## Key Models

### User
- Extended Django User model
- Full name, username, email, bio, avatar

### Post
- Title, description, category
- Created by user, timestamps
- Upvotes/downvotes (ManyToMany)
- Participants tracking

### Message
- Comments on posts
- User, post, body, timestamps

### PrivateMessage
- Direct messages between users
- Sender, recipient, body, read status
- Timestamps for ordering

## URL Routes

### Posts & Content
- `/` - Home/feed
- `/post/<id>/` - View post with comments
- `/create-post/` - Create new post
- `/update-post/<id>/` - Edit post
- `/delete-post/<id>/` - Delete post

### Voting
- `/upvote-post/<id>/` - Upvote post
- `/downvote-post/<id>/` - Downvote post

### Messages
- `/messages/<username>/` - Chat with user
- `/messages/<username>/send/` - Send message

### User
- `/profile/<id>/` - User profile
- `/update-user/` - Edit profile
- `/login/` - Login page
- `/register/` - Register page
- `/logout/` - Logout

### Discovery
- `/categories/` - Browse categories
- `/activity-page/` - Recent activities

## WebSocket Endpoints

- `ws://localhost:8000/ws/pm/<username>/` - Private chat with user

Messages are persisted to database and synced in real-time across connected clients.

## Configuration

### Settings (blogProject/settings.py)

Key settings:
```python
INSTALLED_APPS = [
    'daphne',          # ASGI server (must be first)
    'channels',        # WebSocket support
    'blogApp',         # Main app
    'chat',            # Chat app
    # ... Django default apps
]

ASGI_APPLICATION = 'blogProject.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```


## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub
