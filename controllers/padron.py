def form1():

	return dict()
def sin():
	dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
	return dict(dnpa=dnpa)
def nuevo():
	dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
	form = SQLFORM.factory(
        Field('quees', label='Dni/Pasaporte',requires=IS_IN_SET(["DNI","PASAPORTE"])),
        
         )
        if form.process().accepted:
       		response.flash = 'formulario aceptado'
       		redirect(URL(c='padron',f='form',args=[form.vars.quees,dnpa,form.vars.genero,form.vars.estado_c]))	   		
        
       			
	return dict(form=form)
def form():
	from gluon.serializers import json
 	quees=request.args[0]#si es dni o pasaporte
 	valor=request.args[1]#recojo los datos que vengo trayendo de dni
 	genero=request.args[2]#recojo el genero
 	estado=request.args[3]#recojo el estado civil
 	DNI=""
 	PASA=""
 	if quees =="DNI":
 		DNI=valor
 		
 	else:
 		PASA=valor
 	

	form=SQLFORM.factory(#realizo el formulario a mano
	Field('dni','integer',label="Ingrese el Dni",default=DNI),
	Field('pasaporte',label="Ingrese el Pasaporte",default=PASA),
	Field('tipo','reference prontuario',requires=IS_IN_DB(db,'prontuario','%(Tprontuario)s')),
	Field('nprontuario','integer',label="Nº de Prontuario"),
	Field('apellido',label="Apellido",requires=IS_UPPER()),
	Field('nombre',label='Nombre',requires=IS_UPPER()),
	Field('domicilio',label='Domicilio',requires=IS_UPPER()),
	Field('e_civil',label='Estado Civil',requires=IS_IN_SET(["S","C","D","V"],error_message='Error escoja una opcion')),
	Field('clase','int',label='Clase',requires=IS_INT_IN_RANGE(1900,2100,error_message='Error la clase debe ser ej: 1942')),
	Field('profesion',requires=IS_UPPER()),
	Field('pais',label='Pais',requires=IS_IN_DB(db,'paises.id', '%(pais)s',zero=T('Seleccione la Nacionalidad'),error_message='Error Seleccione una Nacionalidad'),default=1),
	Field('genero',requires=IS_IN_SET(["M","F"])),
	Field('Observaciones','text'),
	)

	

	if form.accepts(request,session):
		db.padron.insert(DocumentoNro=form.vars.dni,Pasaporte=form.vars.pasaporte,Apellido=form.vars.apellido,Nombre=form.vars.nombre,IdPais=form.vars.pais,Genero=form.vars.genero,EstadoCivil=form.vars.e_civil,Profesion=form.vars.profesion,
			Direccion=form.vars.domicilio,Clase=form.vars.clase,IdProntuarioTipo=form.vars.tipo,ProntuarioNro=form.vars.nprontuario)
		redirect(URL(c='padron',f='mensaje'))
	elif form.errors:
            response.flash = 'el formulario tiene errores'
    	else:
            	response.flash = 'por favor complete el formulario' 
	return dict(form=form) 

def mensaje():#mesaje de carga realizada



	return  dict()
# def form():	
# 	from gluon.serializers import json
# 	quees=request.args[0]#si es dni o pasaporte
# 	dnpa=request.args[1]#recojo los datos que vengo trayendo de dni
# 	genero=request.args[2]#recojo el genero
# 	estado=request.args[3]#recojo el estado civil
	
# 	if quees =="DNI":
# 		db.padron.DocumentoNro.default = dnpa
# 	else:
# 		db.padron.Pasaporte.default=dnpa
# 	db.padron.Genero.default = genero
# 	db.padron.EstadoCivil.default = estado
# 	#db.padron.IdPais.default = 1
# 	#--Creo el formulario de carga para el expediente
# 	form = SQLFORM(db.padron,fields=["DocumentoNro","Pasaporte",'Apellido','Nombre',"Genero",'Clase','Profesion','Direccion','Observaciones'
# 		,'IdProntuarioTipo',"ProntuarioNro","EstadoCivil"])
# 	#formulario.add_button('Cancelar', URL('../../asesoria/panel'))
# 	if form.process().accepted:
# 		redirect(URL(c='entrada',f='ingreso'))
# 	elif form.errors:
# 		response.flash='El formulario tiene errores'
# 	else:
# 		response.flash = 'Debe completar el formulario'	

# 	pais=db(db.paises).select()
# 	paises=json(pais)
# 	return dict(form=form,quees=quees,estado=estado,paises=paises)
def modificar():
	dnpa=request.args[0]
    	clave={'1':"A.G.",'2':"C.I.",'3':"D.C.P",'4':"D.E",'5':"R.C",'6':"S.P.",'0':None}    
    	setpa=db((db.padron.DocumentoNro==dnpa)|(db.padron.Pasaporte==dnpa)).select()
    	tiene=len(setpa)
    	if tiene==0:
        	redirect(URL(c='padron',f='sin',args=[dnpa]))#si no esta en la tabla padron redirecciona
    	else:#si esta en la tabla padron mustro los datos
        	for x in setpa:
            		apellido=x.Apellido
            	nombre=x.Nombre
            	tipo=x.IdProntuarioTipo
            	tipo=str(tipo)#convierto a string
            	tipo=clave[tipo]#reemplazo en el diccionario para sacar el tipo a mostrar en el formulario
            	tipo=str(tipo)#paso a cadena el tipo de prontuario para mostrar en el formulario    
            	nprontuario=x.ProntuarioNro 
            	genero=x.Genero
            	ide=x.id 
	return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,genero=genero,ide=ide)	
def form_modificar():
	
	
	ide=request.args[0]
	set_padron=db(db.padron.id==ide).select().first()#realizo set para sacar los datos de la persona a modificar
	nom=set_padron.Nombre
	ape=set_padron.Apellido

	dni=set_padron.DocumentoNro#saco el dni de la persona
	pasa=set_padron.Pasaporte#saco el pasaporte de la persona
	tipo=set_padron.IdProntuarioTipo#saco el id del tipo de prontuario
	
	

	pront=set_padron.ProntuarioNro #saco el nro de prontuario
	direcc=set_padron.Direccion #saco la direccion
	sexo=set_padron.Genero #saco el genero
	prof=set_padron.Profesion #saco la profesion
	e_civil=set_padron.EstadoCivil #saco el estado civil
	clase=set_padron.Clase #saco la clase
	pais=set_padron.IdPais #saco la nacionalidad
	paises=db(db.paises.pais==pais).select()




	form=SQLFORM.factory(#realizo el formulario a mano
	Field('dni','integer',label="Ingrese el Dni",requires=IS_NOT_EMPTY(error_message='El campo puede estar vacío'),default=dni),
	Field('pasaporte',label="Ingrese el Pasaporte",default=pasa),
	Field('tipo','reference prontuario',requires=IS_IN_DB(db,'prontuario','%(Tprontuario)s'),default=tipo),
	Field('nprontuario','integer',label="Nº de Prontuario",default=pront,),
	Field('apellido',label="Apellido",default=ape,requires=IS_UPPER()),
	Field('nombre',label='Nombre',default=nom,requires=IS_UPPER()),
	Field('domicilio',label='Domicilio',default=direcc,requires=IS_UPPER()),
	Field('e_civil',label='Estado Civil',requires=IS_IN_SET(["S","C","D","V"],error_message='Error escoja una opcion'),default=e_civil),
	Field('clase','int',label='Clase',requires=IS_INT_IN_RANGE(1900,2100,error_message='Error la clase debe ser ej: 1942'),default=clase),
	Field('profesion',default=prof,requires=IS_UPPER()),
	Field('pais',label='Pais',requires=IS_IN_DB(db,'paises.id', '%(pais)s',zero=T('Seleccione la Nacionalidad'),error_message='Error Seleccione una Nacionalidad'),default=pais),
	Field('genero',requires=IS_IN_SET(["M","F"]),default=sexo),
	)
	

	if form.accepts(request,session):
		set_padron.update_record(Nombre=form.vars.nombre,IdPais=form.vars.pais,Genero=form.vars.genero,EstadoCivil=form.vars.e_civil,Profesion=form.vars.profesion,
			Direccion=form.vars.domicilio,Clase=form.vars.clase,IdProntuarioTipo=form.vars.tipo,ProntuarioNro=form.vars.nprontuario)
		redirect(URL(c='padron',f='mensaje_datos'))
	elif form.errors:
            response.flash = 'el formulario tiene errores'
    	else:
            	response.flash = 'por favor complete el formulario' 	
	return dict(ide=ide,ape=ape,nom=nom,form=form,dni=dni,tipo=tipo)
def mensaje_datos():
		#mensaje de datos modificados
	return dict()
