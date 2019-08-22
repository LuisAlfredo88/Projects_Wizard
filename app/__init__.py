from flask import Flask, render_template

# App Instance
app = Flask(__name__)

# Configuration
app.config.from_object('config.Config')

# registre routes
from app.main_module.routes import routes