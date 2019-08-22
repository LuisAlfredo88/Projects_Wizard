from flask import Blueprint, redirect, render_template, url_for, request
from json import loads as json_decode

from app import app
from app.main_module.models import ProjectStructure, ProjectInfo

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("")
def index():
    return redirect(url_for('routes.inicio'))

@routes.route("inicio")
def inicio():
	projectstructure = ProjectStructure(app)

	tables = projectstructure.read_tables()
	destines = projectstructure.get_project_dst()
	modules = projectstructure.get_modules()

	context = { 'tables' : tables, 'destines' : destines, 'modules' : modules}
	return render_template('index.html', context=context)

@routes.route("tables")
def tables():
	projectstructure = ProjectStructure(app)

	tables = projectstructure.read_tables()
	context = { 'tables' : tables}
	return render_template('tables.html', context=context)

@routes.route("generate", methods=['POST'])
def generate():
	projectstructure = ProjectInfo(**request.json)
	return str(projectstructure)

app.register_blueprint(routes)
