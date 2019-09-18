def confeccion():
	return dict()
def por_sistema():
	from gluon.serializers import json			#importo json
	setsoli=db(db.solicitud.estado_solicitud=="Confeccion").select()	#realizo un set de los registros con estado confeccion
	co=json(setsoli)													#trasformo el set a formato json

	return dict(co=co)
def procesar():	
	from datetime import date,time,datetime
	fecha=datetime.now()	
	quien=auth.user.id            #atrapo el usuario logueado
    	user=db(db.auth_user.id==quien).select().first()#pregunto quien esta logueado
    	usuario_nombre=user.first_name
    	usuario_apellido=user.last_name
    	usuario=usuario_nombre+" "+usuario_apellido#concateno cadena para generar el nombre del usuario
    	iniciales=user.iniciales    	
	clave={'1':"A.G.",'2':"C.I.",'3':"D.C.P.",'4':"D.E.",'5':"R.C.",'6':"S.P.",'0':None}
	valor={'A.G.':"1",'C.I.':"2",'D.C.P.':"3",'D.E.':"4",'R.C.':"5",'S.P.':"6",None:'0'}
    	#ultimo=db(db.solicitud).select().last()	
    	#u=ultimo.id									
	ide_soli=int(request.args[0])#atrapo id
	setsoli=db(db.solicitud.id==ide_soli).select().last()	#realizo un ser para sacar datos de la tabla
	dnpa_soli=setsoli.dni  	#dni/pasaporte de la tabla solicitud
	soli_por_soli=setsoli.solicitado_por					#solicitado por de la tabla solicitud
	capital_soli=setsoli.capitalinterior
	tiene=setsoli.t_antecedentes
	anteceden=setsoli.antecedentes					
	setpadron=db((db.padron.DocumentoNro==dnpa_soli)|(db.padron.Pasaporte==dnpa_soli)).select().first()
	ide_padron=setpadron.id 								#saco el id de la persona en la tabla padron
	dni_padron=setpadron.DocumentoNro
	pasa_padron=setpadron.Pasaporte
	apellido_padron=setpadron.Apellido
	nombre_padron=setpadron.Nombre
	Profesion_padron=setpadron.Profesion
	te=setpadron.IdProntuarioTipo		#tipo de padron
	te=str(te)#convierto a string
	tipo=clave[te]#reemplazo en el diccionario para sacar el tipo a mostrar en el formulario
	tipo=str(tipo)#paso a cadena el tipo de prontuario para mostrar en el formulario	
	num_padron=setpadron.ProntuarioNro
	domi_padron=setpadron.Direccion
	prof_padron=setpadron.Profesion
	civil_padron=setpadron.EstadoCivil
	clase_padron=setpadron.Clase
	pais_padron=setpadron.IdPais
	pais_padron=pais_padron	
	tpront=""
	qtipo=""
	
	
	
	#realizo un factory para modificar los valores a imprimir	
	form=SQLFORM.factory(
	Field('dni','integer',label="Ingrese el Dni",default=dni_padron,),
	Field('pasaporte',label="Ingrese el Pasaporte",default=pasa_padron),
	Field('tipo',label="Tipo de Prontuario",requires=IS_IN_SET(["A.G.","C.I.","D.C.P.","D.E.","R.C.","S.P."],error_message='Error escoja una opcion'),default=tipo),
	Field('nprontuario','integer',label="Nº de Prontuario",default=num_padron),
	Field('apellido',label="Apellido",default=apellido_padron),
	Field('nombre',label='Nombre',default=nombre_padron),
	Field('domicilio',label='Domicilio',default=domi_padron),
	Field('e_civil',label='Estado Civil',requires=IS_IN_SET(["S","C","D","V"],error_message='Error escoja'),default=civil_padron),
	Field('clase','int',label='Clase',default=clase_padron,requires=IS_INT_IN_RANGE(1900,2100,error_message='Error la clase debe ser ej: 1942')),
	Field('Profesion',default=Profesion_padron),
	Field('pais',label='Pais',requires=IS_IN_DB(db,'paises.id', '%(pais)s',zero=T('Seleccione la Nacionalidad'),error_message='Error Seleccione una Nacionalidad'),default=pais_padron),
	
                                 
	Field('soli_por',label='Solicitado Por',default=soli_por_soli),
	Field('intervino',label='Intervino',default=iniciales),
	Field('donde',label="Localidad",requires=IS_IN_SET(["CAPITAL","INTERIOR"],error_message='Error escoja una opcion'),default=capital_soli),
	Field('t_antece',label="Tiene Antecedentes",requires=IS_IN_SET(["NO","SI"],error_message='Error escoja una opcion'),default=tiene),
	Field('antecedentes','text',default=anteceden,label='Antecedentes'),)

    	if form.accepts(request,session):
    		#tomo el valor q toma el campo del form tipo 
    		tpront=form.vars.tipo
    		tpront=str(tpront)
    		qtipo=valor[tpront]
    		qtipo=str(qtipo)  		
    		
        	#actualizo los campos en la tabla padron
        	setpadron.update_record(
        		Direccion=form.vars.domicilio,Clase=form.vars.clase,
        		IdPais=form.vars.pais,Profesion=form.vars.Profesion)

        	setsoli.update_record(solicitado_por=form.vars.soli_por,intervino=form.vars.intervino
        		,capitalinterior=form.vars.donde,estado_solicitud="Completado",usuario=usuario,
        		antecedentes=form.vars.antecedentes,t_antecedentes=form.vars.t_antece,fecha_solicitada=fecha,hora=fecha)

        	db.historial.insert(dni=form.vars.dni,pasaporte=form.vars.pasaporte,nombre=form.vars.nombre,
        		apellido=form.vars.apellido,capitalinterior=form.vars.donde,intervino=form.vars.intervino,
        		t_antecedentes=form.vars.t_antece,antecedentes=form.vars.antecedentes,fecha=fecha,hora=fecha      	
        		) 
        	redirect(URL(c='confeccion',f='pre_imprimir',args=[ide_soli,ide_padron,dni_padron,pasa_padron]))
    	elif form.errors:
            response.flash = 'el formulario tiene errores'
    	else:
            response.flash = 'por favor complete el formulario' 

	return dict(dnpa_soli=dnpa_soli,iniciales=iniciales,dni_padron=dni_padron
 	,pasa_padron=pasa_padron,apellido_padron=apellido_padron,nombre_padron=nombre_padron,tipo=tipo
 	,num_padron=num_padron,domi_padron=domi_padron,prof_padron=prof_padron,civil_padron=civil_padron
 	,clase_padron=clase_padron,pais_padron=pais_padron,ide_soli=ide_soli,capital_soli=capital_soli,
 	soli_por_soli=soli_por_soli,ide_padron=ide_padron,form=form,clave=clave,valor=valor,qtipo=qtipo,

 	)


 	
def pre_imprimir():
	from datetime import date,time,datetime
	#tomo los argumentos del id padron y id tabla solicitud
	ide_padron=request.args[1]

	ide_soli=request.args[0]
	dni=request.args[2]
	pasa=request.args[3]
	histo=db((db.historial.dni==dni)|(db.historial.pasaporte==pasa)).select().last()#realizo un set preuntnado por el dni o pasaporte en la tabla historial
	
	ide_histo=histo.id #obtengo el id q posee en la tabla historial
	soli=db(db.solicitud.id==ide_soli).select().first()
	#realizo un set para sacar el ultimo numero de certificado		
	hfecha=datetime.now()	#saco la fecha de hoy
	hfecha=hfecha.year #saco el año de la fecha de hoy
	fecha=str(hfecha)#realizo los siguientes pasos para para sacar los ultimos 2 digitos
	fecha=fecha[2:4]
	fecha=int(fecha)#ultimos 2 digitos de la fecha de hoy
	cert=db(db.nro_certificado.id==1).select().first() #hago un set para ver el ultimo certificado y el año
	c_anio=cert.anio
	c_n=cert.nro_certificado
	c_n=c_n+1
	if c_anio==fecha:
		cert.update_record(nro_certificado=c_n)#actualizo en la base de datos de certificados
		c_n=str(c_n)
		c_anio=str(c_anio)
		nc=c_n+"/"+c_anio
		soli.update_record(nro_certificado=nc) #actualizo en la base de datos de solicitud
		histo.update_record(nro_certificado=nc)	#actualizo en el historial
	elif c_anio!=fecha:	
		cert.update_record(anio=fecha,nro_certificado=1)
		fecha=str(fecha)
		nc="1/"+fecha
		soli.update_record(nro_certificado=nc)
		histo.update_record(nro_certificado=nc)	#actualizo en el historial
	redirect(URL(c='confeccion',f='menu_imprimir',args=[ide_soli,ide_padron,dni]))
	

	return dict(ide_padron=ide_padron,ide_soli=ide_soli,hfecha=hfecha,c_n=c_n,fecha=fecha,histo=histo,dni=dni)
def menu_imprimir():
	ide_soli=request.args[0]
	ide_padron=request.args[1]
	dnpa_soli=request.args[2]


	return dict(ide_soli=ide_soli,ide_padron=ide_padron,dnpa_soli=dnpa_soli)
def reimprimir():
	from gluon.serializers import json			#importo json
	setsoli=db(db.solicitud.estado_solicitud=="Impreso").select()	#realizo un set de los registros con estado confeccion
	co=json(setsoli)													#trasformo el set a formato json

	return dict(co=co)
def re_armado():
	#ide_soli,ide_padron,dni_padron
	from datetime import date,time,datetime
	fecha=datetime.now()	
	quien=auth.user.id            #atrapo el usuario logueado
    	user=db(db.auth_user.id==quien).select().first()#pregunto quien esta logueado
    	usuario_nombre=user.first_name
    	usuario_apellido=user.last_name
    	usuario=usuario_nombre+" "+usuario_apellido#concateno cadena para generar el nombre del usuario
    	iniciales=user.iniciales
    	ide_soli=int(request.args[0])#atrapo id

	setsoli=db(db.solicitud.id==ide_soli).select().last()
	dnpa_soli=setsoli.dni

	setsoli=db(db.solicitud.id==ide_soli).select().last()
	dnpa_soli=setsoli.dni
	setpadron=db((db.padron.DocumentoNro==dnpa_soli)|(db.padron.Pasaporte==dnpa_soli)).select().last()
	ide_padron=setpadron.id
	
	redirect(URL(c='confeccion',f='menu_imprimir',args=[ide_soli,ide_padron,dnpa_soli]))
	return dict()
def modificar_padron():#por aqui ingreso para modificar los datos de una persona en el padron a excepcion del dni
	#poner un valor por defecto a un campo del formulario    
	form=SQLFORM.factory(    
    Field('valor',label="Ingrese Un Dni/Pasaporte",requires=IS_NOT_EMPTY(error_message='El campo puede estar vacío'))
    
    )         
    	if form.accepts(request,session):
    		response.flash = 'formulario aceptado'
    		redirect(URL(c='padron',f='modificar',args=[form.vars.valor]))
    	elif form.errors:
        	response.flash = 'el formulario tiene errores'
    	else:
        	response.flash = 'por favor complete el formulario'  
	return dict(form=form)
	
		
	

		