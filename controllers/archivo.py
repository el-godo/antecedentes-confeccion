def form_archivo():
	from gluon.serializers import json	
	solicitud=db(db.solicitud.estado_solicitud=="Pendiente").select()	



	an=json(solicitud)
	
	
	return dict(an=an,solicitud=solicitud)
def procesar():
	#--Atrapo el id del usuario
	
	ide=int(request.args[0])#atrapo id
	setsoli=db(db.solicitud.id==ide).select()
	for x in setsoli:
    		x.update_record(estado_solicitud='Confeccion')
    	redirect(URL(c='archivo',f='form_archivo'))

	return dict(ide=ide,setsoli=setsoli)


