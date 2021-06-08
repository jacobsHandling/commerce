# commerce - An interactive eBay-like auction site built with Django

This is my submssion for Project 2 of CS50's Web Programming with Python and Javascript.

You can see a run-through [here](https://www.youtube.com/watch?v=rLX47ni5X8E)

# To run:
1. Make sure you have [python3 and django installed](https://docs.djangoproject.com/en/3.2/intro/install/) in your current environment
2. CD into the directory you want this repository to exist in, then run `git clone git@github.com:jacobsHandling/commerce.git` to clone it there.
3. Run `python3 manage.py migrate` to apply migrations
4. Create a superuser account by running `python3 manage.py createsuperuser`, and filling out the requested fields. You can also register regular user accounts from the UI, but a superuser account will allow you to use the admin interface.
5. Run `python3 manage.py runserver`
6. Access the web app locally at http://127.0.0.1:8000 in your browser
7. You can also access the site admin at http://127.0.0.1:8000/admin/ with your superuser account
