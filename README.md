# commerce - An interactive eBay-like auction site built entirely with Django

This is my submssion for Project 2 of CS50's Web Programming with Python and Javascript.

You can see a run-through [here](https://www.youtube.com/watch?v=HI2hkXNx8jk)

# To run:
1. Make sure you have [python3 and django installed](https://docs.djangoproject.com/en/3.2/intro/install/) in your current environment
2. cd into the directory you want this repository to exist in, then run `git clone https://github.com/jacobsHandling/commerce.git` to clone it there.
3. `cd` into commerce 
4. Run `python3 manage.py migrate` to apply migrations
5. Create a superuser account by running `python3 manage.py createsuperuser`, and filling out the requested fields. You can also register regular user accounts from the UI, but a superuser account will allow you to use the admin interface.
6. Run `python3 manage.py runserver`
7. Access the web app locally at http://127.0.0.1:8000 in your browser
8. You can also access the site admin interface at http://127.0.0.1:8000/admin/ with your superuser account
   - To allow users to add categories to their listings, you'll first want to create those categories using this admin interface
