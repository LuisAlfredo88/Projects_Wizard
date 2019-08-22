from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from shutil import copytree as copydir
from os import path, listdir
from json import dumps as json_encode

DB_CONFIG = {
	'PROTOCOL' : 'mysql+pymysql',
	'HOST' : '127.0.0.1',
	'USER' : 'root',
	'PASS' : '',
	'DB' : 'acl_gestor'
}

class ProjectInfo():
	"""docstring for ProjectInfo"""
	def __init__(self, **entries):
		self.__dict__.update(entries)

	def __str__(self):
		return json_encode(self.__dict__)
		

class ProjectStructure():
	"""docstring for ProjectStructure"""

	acl_template = 'structure_template/acl_template/'
	folder_template = 'structure_template/folder_template/'

	class PROJECT_TYPE():
		PRUEBA = 'pruebas'
		REPORTE ='reportes'

	def __init__(self, flask_app):
		self.Base = automap_base()
		self.flask_app = flask_app

		# engine
		engine = create_engine("{PROTOCOL}://{USER}:{PASS}@{HOST}/{DB}?charset=utf8".format(**DB_CONFIG))

		# reflect the tables
		self.Base.prepare(engine, reflect=True)

		# Session object
		self.session = Session(engine)

	def load_project_info_from_json(json):
		self.project_info = json

	def read_tables(self):
		DataSources = self.Base.classes.acl_data_source
		data_folder = self.get_data_source()

		# guardar el nombre sin extension de los archivos .fil y .fmt en el directorio de tablas
		files = [ file[:-4] for file in listdir(data_folder) if '.fil' in str.lower(file) or '.fmt' in str.lower(file)]

		# para guardar la frecuencia con la que aparecen los nombres de las tablas
		freq = {}

		for f in files: # por cada nombre de tabla....
			freq[f] = freq.get(f, 0) + 1 # ... guardamos la cantidad de veces que aparece

		single_f = [f for f in freq if freq[f] == 2] # obtenemos solo los que aparecen dos veces
													 # (existe el .fmt y el .fil)

		return self.session.query(DataSources).filter(DataSources.name.in_(single_f)).all()

	def get_data_source(self):
		AclConfiguration = self.Base.classes.acl_configuration
		repository = self.session.query(AclConfiguration).filter_by(name='repository').one()
		return repository.value

	def get_project_dst(self):
		Repositories = self.Base.classes.repositories
		dsts = self.session.query(Repositories).all()
		return dsts

	def get_modules(self):
		Modules = self.Base.classes.modules
		modules = self.session.query(Modules).all()
		return modules

	def generate_project_at(self, dst, project_type):
		src = path.join(self.flask_app.root_path, self.folder_template, project_type)
		copydir(src, dst)

