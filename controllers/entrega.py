################### modulos de entrega de certificados############################ 

def entrega():
	from gluon.serializers import json          #importo json
    	setsoli=db(db.solicitud.estado_solicitud=="Impreso").select()    #realizo un set de los registros con estado confeccion
    	co=json(setsoli)                                                    #trasformo el set a formato json
    	return dict(co=co)
def menu():
	ide_soli=request.args[0]
	return dict(ide_soli=ide_soli)
def solicitante():
	from datetime import date,time,datetime
	fecha=datetime.now()
	quien=auth.user.id            #atrapo el usuario logueado
    	user=db(db.auth_user.id==quien).select().first()#pregunto quien esta logueado
    	usuario_nombre=user.first_name
    	usuario_apellido=user.last_name
    	usuario=usuario_nombre+" "+usuario_apellido#concateno cadena para generar el nombre del usuario
    		
	ide_soli=request.args[0]
	setsoli=db(db.solicitud.id==ide_soli).select().first()
	nom=setsoli.nombre
	ape=setsoli.apellido
	DNI=setsoli.dni
	estado=setsoli.estado_solicitud
	ncerti=setsoli.nro_certificado
	capi_inte=setsoli.capitalinterior
	intervino=setsoli.intervino
	usuario=usuario
	solipor=setsoli.solicitado_por
	t_antecedentes=setsoli.t_antecedentes
	antecedentes=setsoli.antecedentes
	#######padron###
	set_pad=db((db.padron.DocumentoNro==DNI)|(db.padron.Pasaporte==DNI)).select().first()
	dni=set_pad.DocumentoNro
	pasa=set_pad.Pasaporte
	nom_ape=nom+" "+ape
	############
	db.entrega.insert(nom_ape=nom_ape,documento=dni,nro_certificado=ncerti,fecha=fecha,usuario=usuario)#inserto en la tabla entrega los datos de quien recibe
	# #############	
	setsoli.update_record(fecha_solicitada=fecha,estado_solicitud="Retirado")#actualizo los datos en la tabla solicitud
	# #############
	db.historial.insert(dni=dni,pasaporte=pasa,nombre=nom,apellido=ape,nro_certificado=ncerti,capitalinterior=capi_inte,
	intervino=intervino,fecha=fecha,solicitado_por=solipor,t_antecedentes=t_antecedentes,antecedentes=antecedentes,
	nomape_retira=nom+" "+ape,dni_retira=DNI
	)
    	return dict()
def form():
	ide_soli=ide_soli=request.args[0]
	form=form=SQLFORM.factory(
		Field('documento',label="Dni/Pasaporte de Quien retira",requires=IS_UPPER()),
		Field('nom_ape',label="Nombre y Apellido de Quien retira",requires=IS_UPPER()),

		)
	if form.accepts(request,session):
		db.entrega.insert(nom_ape=form.vars.nom_ape,documento=form.vars.documento)#inserto en la tabla entrega los datos de quien recibe
		redirect(URL(c='entrega',f='tercero',args=[ide_soli,form.vars.documento]))

    	
    	elif form.errors:
            response.flash = 'el formulario tiene errores'
    	else:
            response.flash = 'por favor complete el formulario'
    	return dict(form=form,ide_soli=ide_soli) 

def tercero():
	from datetime import date,time,datetime
	fecha=datetime.now()
	quien=auth.user.id            #atrapo el usuario logueado
    	user=db(db.auth_user.id==quien).select().first()#pregunto quien esta logueado
    	usuario_nombre=user.first_name
    	usuario_apellido=user.last_name
    	usuario=usuario_nombre+" "+usuario_apellido#concateno cadena para generar el nombre del usuario

	ide_soli=request.args[0]#atrapo el id de la tabla solicitud
	setsoli=db(db.solicitud.id==ide_soli).select().first()
	nom=setsoli.nombre
	ape=setsoli.apellido
	DNI=setsoli.dni
	estado=setsoli.estado_solicitud
	ncerti=setsoli.nro_certificado
	capi_inte=setsoli.capitalinterior
	intervino=setsoli.intervino
	usuario=usuario
	solipor=setsoli.solicitado_por
	t_antecedentes=setsoli.t_antecedentes
	antecedentes=setsoli.antecedentes
	#######padron###
	set_pad=db((db.padron.DocumentoNro==DNI)|(db.padron.Pasaporte==DNI)).select().first()
	dni=set_pad.DocumentoNro
	pasa=set_pad.Pasaporte
	############entrega
	ndocumento=request.args[1]
	set_entrega=db(db.entrega.documento==ndocumento).select().last()
	nom_ape_entrega=set_entrega.nom_ape	
	set_entrega.update_record(fecha=fecha,nro_certificado=ncerti,usuario=usuario)
	setsoli.update_record(fecha_solicitada=fecha,estado_solicitud="Retirado")#actualizo los datos en la tabla solicitud
	# #############
	db.historial.insert(dni=dni,pasaporte=pasa,nombre=nom,apellido=ape,nro_certificado=ncerti,capitalinterior=capi_inte,
	intervino=intervino,fecha=fecha,solicitado_por=solipor,t_antecedentes=t_antecedentes,antecedentes=antecedentes,
	nomape_retira=nom_ape_entrega,dni_retira=ndocumento
	)
	return dict()
