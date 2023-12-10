from flask import Flask, render_template, url_for, request, flash
from website import create_app



# Running application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)


