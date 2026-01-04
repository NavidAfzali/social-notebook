**Social Notebook**

**By Mohammad Navid Afzali**

A social note-taking web application built with Django where users can write daily notes, share them publicly, and interact through comments and likes.

**Features**
- User authentication (signup, login, logout)
- Create, update, delete notes
- Public / private notes
- Comment & reply system
- Like system
- Search notes
- Clean UI with Bootstrap

**Tech Stack**
- Python
- Django
- SQLite
- Bootstrap 5

**Installation**

```bash
git clone https://github.com/your-username/social-notebook.git
cd social-notebook
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
