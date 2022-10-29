"""
entry point of the application / top level script to execute
"""
from blog_api import create_app

if __name__ == "__main__":
    app = create_app()
    app.run()


def my_method(name):
    print(f'this is the new method {name}')
