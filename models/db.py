# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

#host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = [Field('oficina'),Field('dni'),Field('iniciales')]
auth.define_tables(username=True, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
#auth.settings.registration_requires_verification = False
#auth.settings.registration_requires_approval = False
#auth.settings.reset_password_requires_verification = True
auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('retrieve_username')
auth.settings.actions_disabled.append('request_reset_password')

auth.settings.remember_me_form=False
auth.settings.registration_requires_approval = True
auth.settings.on_failed_authorization = \
    URL('sin_autorizacion')
# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
#db = DAL(mysql://root:root@localhost/antecedentes-interno)
#http://localhost/antecedentes-interno/

db.define_table('paises',
    
    
    Field('pais'),

    format='%(pais)s'
    )
db.define_table('prontuario',
    
    
    Field('Tprontuario'),
    format='%(Tprontuario)s'
    
    )

db.define_table('padron',
       
    Field('Apellido',requires=IS_UPPER()),
    Field('Nombre',requires=IS_UPPER()),
    Field('Clase',requires=IS_UPPER()),
    Field('DocumentoNro',requires=IS_UPPER()),
    Field('Pasaporte',requires=IS_UPPER()),
    Field('IdPais',db.paises),
    Field('Genero',requires=IS_IN_SET(["M","F"])),
    Field('EstadoCivil',label='Estado Civil',requires=IS_IN_SET(["S","C","D","V"]),),         
    Field('Profesion',requires=IS_UPPER()),
    Field('Direccion',requires=IS_UPPER()),
    Field('IdProntuarioTipo',db.prontuario),
    Field('ProntuarioNro','integer'),
    Field('Observaciones',requires=IS_UPPER()))

db.define_table('solicitud',    
    Field('dni'),    
    Field('apellido',requires=IS_UPPER()),  
    Field('nombre',requires=IS_UPPER()),       
    Field('genero'),
    Field('tipo_prontuario'),   
    Field('prontuario'),
    Field('nro_certificado'),
    Field('estado_solicitud'),
    Field('fecha_solicitada','datetime',requires=[IS_NOT_EMPTY(),IS_DATETIME()]),
    Field('hora','datetime',requires=[IS_NOT_EMPTY(),IS_DATETIME()]),   
    Field('solicitado_por',requires=IS_UPPER()),#ante las autoridades q lo requieran
    Field('capitalinterior',requires=IS_IN_SET(["CAPITAL","INTERIOR",""]) ),
    Field('intervino',requires=IS_UPPER()),#usuario q carga
    Field('usuario',requires=IS_UPPER()),
    Field('ip_solicitante'),
    Field('ip_confeccion'),
    Field('t_antecedentes',requires=IS_IN_SET(["NO","SI"])),
    Field('antecedentes','text',requires=IS_UPPER()),
    )
db.define_table('historial',      
    Field('dni','integer'),
    Field('pasaporte'),    
    Field('nombre',requires=IS_UPPER()),    
    Field('apellido',requires=IS_UPPER()),
    Field('nro_certificado'),
    Field('capitalinterior'),
    Field('intervino',requires=IS_UPPER()),#usuario q carga
    Field('fecha','datetime'),
    Field('hora'),
    Field('solicitado_por',requires=IS_UPPER()),##ante las autoridades q lo requieran
    Field('t_antecedentes',requires=IS_IN_SET(["SI","NO",""])),
    Field('antecedentes','text',requires=IS_UPPER()),
    Field('nomape_retira'),
    Field('dni_retira','integer'),
   
    )
db.define_table('nro_certificado', 
    Field('nro_certificado','integer'),
    Field('anio','integer'),
    )
db.define_table('margenes', 
    Field('x','float'),
    Field('y','float'),
    )
db.define_table('entrega',
    Field('nom_ape',requires=IS_UPPER(),label="Nombre y Apellido de la Persona que Retira"),     
    Field('documento',label="Dni/Pasaporte de Quien Retira"),
    Field('fecha','datetime'),
    Field('nro_certificado'),
    Field('usuario'),


     )





#------------------------------------------------
#---------------Validadores------------------------
db.padron.IdPais.requires=IS_IN_DB(db,'paises','%(pais)s')
db.padron.IdProntuarioTipo.requires=IS_IN_DB(db,'prontuario','%(Tprontuario)s')
db.auth_user.oficina.requires=IS_IN_SET(['Turnos','Confeccion','Super'])
