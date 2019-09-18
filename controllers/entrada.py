
def entrada():
    return dict()    
def ingreso():
	#poner un valor por defecto a un campo del formulario    
	form=SQLFORM.factory(    
    Field('valor',label="Ingrese Un Dni/Pasaporte",requires=IS_NOT_EMPTY(error_message='El campo puede estar vacío'))
    
    )         
    	if form.accepts(request,session):
    		response.flash = 'formulario aceptado'
    		redirect(URL(c='entrada',f='comprobacion',args=[form.vars.valor]))
    	elif form.errors:
        	response.flash = 'el formulario tiene errores'
    	else:
        	response.flash = 'por favor complete el formulario'  
	return dict(form=form)
def comprobacion():
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
        


    return dict(setpa=setpa,dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,genero=genero)

def convencional():
    #dnpa,apellido,nombre,tipo,nprontuario,genero
    dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
    apellido=request.args[1]
    nombre=request.args[2]
    tipo=request.args[3]
    nprontuario=request.args[4]
    genero=request.args[5]
    setsoli=db(db.solicitud.dni==dnpa).select()#pregunto si se encuentra el dni en la tabla solicitud
    if len(setsoli)>0:#si tiene almenos uno
        for x in setsoli:#recorro el set para sacar datos
            estado=x.estado_solicitud                                       
            intervino=x.intervino
            ide=x.id
        redirect(URL(c='entrada',f='tsolicitud',args=[dnpa,apellido,nombre,tipo,nprontuario,estado,intervino,ide,genero]))
        #redirecciono para ver si que tiempo de solicitud tiene
    else:
        #redirecciono si no  tiene registro en la tabla solicitud
        redirect(URL(c='entrada',f='sin_solicitud',args=[dnpa,apellido,nombre,genero,tipo,nprontuario]))#si no esta en la tabla padron redirecciona
    return dict(setsoli=setsoli,ide=ide)

def tsolicitud():
    from datetime import *
    from time import time
    from datetime import datetime
    #capturo paramertros  
    dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
    apellido=request.args[1]    
    nombre=request.args[2]
    tipo=request.args[3]
    nprontuario=request.args[4]
    estado=request.args[5]     
    intervino=request.args[6]
    ide=request.args[7]
    genero=request.args[8]    
         #tomo la fecha de hoy    
    hoyfecha= datetime.today()#capturo la hora de hoy    
    setsoli=db(db.solicitud.id==ide).select().first()#consulto si esta en la tabla solicitud
    turno_fecha= setsoli.fecha_solicitada #fecha en q solicito el turno
   

    #fecha_sacada=str(turno_fecha.day).zfill(2) + "/"  +str(turno_fecha.month).zfill(2) + "/" + str(turno_fecha.year).zfill(2) #concateno la fecha solicitada y muestro en 2 digitos

    turno_hora=setsoli.hora  
    
    if (turno_fecha==None):#si la fecha esta vacia redirecciono y genero una nueva solicitud        
        redirect(URL(c='entrada',f='nueva_solicitud',args=[dnpa,apellido,nombre,tipo,nprontuario,estado,intervino,ide,genero]))    
    elif (turno_fecha!=None):                 
        if hoyfecha<turno_fecha: #comparo las fechas para ver si hay error 
            redirect(URL(c='errores',f='error_fecha',args=[hoyfecha,turno_fecha]))
        if ((estado=="Anulado")|(estado=="Completado")|(estado=="Retirado")): #pregunto si tiene una solicitud para mostrarla al usuario
            redirect(URL(c='entrada',f='nueva_solicitud',args=[dnpa,apellido,nombre,tipo,nprontuario,estado,intervino,ide,genero]))                       
        elif((estado=="Archivo")|(estado=="Confeccion")|(estado=="Pendiente")): # si tiene solicitud avisa q hay solicitud
            print("muestro")     
                            
    return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,estado=estado,intervino=intervino,hoyfecha=hoyfecha,
        setsoli=setsoli,ide=ide,genero=genero,turno_fecha=turno_fecha,
        turno_hora=turno_hora)

def sin_solicitud():    
    #recojo los valores

    dnpa=request.args(0)
    apellido=request.args(1)
    nombre=request.args(2)
    tipo=request.args(4)
    nprontuario=request.args(5)
    genero=request.args(3)  
    
    
    
    #lleno valores en blanco
    estado=""
    intervino=""
    
    db.solicitud.insert(dni=dnpa,apellido=apellido,nombre=nombre,genero=genero,tipo_prontuario=tipo,prontuario=nprontuario,estado_solicitud=estado,intervino=intervino)
    #consulto para sacar el id y quien intervino
    comprobar=db(db.solicitud.dni==dnpa).select().first()
    #busco y saco el id para mandar parametro args
    ide=comprobar.id
    intervino=comprobar.intervino




    redirect(URL(c='entrada',f='tsolicitud',args=[dnpa,apellido,nombre,tipo,nprontuario,estado,intervino,ide,genero]))
  
    return dict()  

def nueva_solicitud():  
    dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
    apellido=request.args[1]
    nombre=request.args[2]
    tipo=request.args[3]
    nprontuario=request.args[4]
    estado=request.args[5]     
    intervino=request.args[6]
    ide=request.args[7]
    genero=request.args[8]
    return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,estado=estado,
        ide=ide,genero=genero)


def form_solicitud():
    from datetime import *
    from time import time
    from datetime import datetime
    dnpa=request.args[0]#recojo los datos que vengo trayendo de dni
    apellido=request.args[1]
    nombre=request.args[2]
    tipo=request.args[3]
    nprontuario=request.args[4]
    estado=request.args[5]       
    ide=request.args[6]
    genero=request.args[7]
    hoyfecha=datetime.today()#tomo la fecha de hoy
    hora=datetime.today()         
    quien=auth.user.id
    user=db(db.auth_user.id==quien).select().first()#pregunto quien esta logueado
    usuario_nombre=user.first_name
    usuario_apellido=user.last_name
    usuario=usuario_nombre+" "+usuario_apellido#concateno cadena para generar el nombre del usuario
    soli=db(db.solicitud.id==ide).select().first()
    #genero una nueva entrada en la tabla solicitud
    soli.update_record(dni=dnpa,apellido=apellido,nombre=nombre,tipo_prontuario=tipo,prontuario=nprontuario,
        estado_solicitud="Pendiente",usuario=usuario,fecha_solicitada=hoyfecha,hora=hora,genero=genero)    
    
    return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,estado=estado,ide=ide,
        usuario_nombre=usuario_nombre,usuario=usuario,hora=hora,hoyfecha=hoyfecha)

        
def form_ver_estado():
    #poner un valor por defecto a un campo del formulario    
    form=SQLFORM.factory(    
    Field('valor','string',label="Ingrese Un Dni/Pasaporte",requires=IS_NOT_EMPTY(error_message='El campo puede estar vacío'))
    
    )         
    if form.accepts(request,session):
            response.flash = 'formulario aceptado'
            redirect(URL(c='entrada',f='ver_estado',args=[form.vars.valor]))
    elif form.errors:
            response.flash = 'el formulario tiene errores'
    else:
            response.flash = 'por favor complete el formulario'  
    return dict(form=form)

def sin_resultados():
    
    return dict()
def ver_estado():
    dnpa=request.args[0]#recojo los datos que vengo trayendo de dni/pasaporte
    setsoli=db(db.solicitud.dni==dnpa).select() #realizo un set para ver si esta en la tabla
    tiene=len(setsoli) #pregunto si si hay resultados
    

    if tiene>0:
        #creo un diccionario de la tabla tipo
        dicc={'1':"A.G.",'2':"C.I.",'3':"D.C.P",'4':"D.E",'5':"R.C",'6':"S.P.",'0':None}
        for x in setsoli:
             
            apellido=x.apellido
            nombre=x.nombre
            te=x.tipo_prontuario          #saco el tipo de prontuario  
            te=str(te)
            nprontuario=x.prontuario      #saco el numero de prontuario
            estado=x.estado_solicitud       #saco estadi
            fecha=x.fecha_solicitada        #saco fecha
            fechaa=str(fecha.day).zfill(2) + "/"  +str(fecha.month).zfill(2) + "/" + str(fecha.year)#concateno la fecha solicitada y muestro en 2 digitos
            #tipo=dicc[te]                   #reemplazo el id por el elemento en el diccionario
            tipo=""
            ide=x.id                        #saco id
           
        if((estado=="Pendiente")|(estado=="Confeccion")):#pregunto por el estado y muestro solo si no esta anulado completado o nulo
            print"mostrar"
        elif ((estado=="Completado")|(estado=="Anulado")|(estado=="")):                
            redirect(URL(c='entrada',f='sin_resultados'))                             
    else:
        redirect(URL(c='entrada',f='sin_resultados'))          
                


    return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,estado=estado,ide=ide,te=te,
        fechaa=fechaa)
def ver(): #aca puedo ver quien retiro el certificado
    dnpa=request.args[0]#tomo
    set_hitory=db((db.historial.dni==dnpa)|(db.historial.pasaporte==dnpa)).select().last() 
    #set_hitory=(db(db.historial.dni==dnpa).select().last() or db(db.historial.pasaporte==dnpa)).select().last()
    nom=set_hitory.nombre
    ape=set_hitory.apellido
    ncer=set_hitory.nro_certificado
    fecha=set_hitory.fecha
    fecha=str(fecha.day).zfill(2) + "/"  +str(fecha.month).zfill(2) + "/" + str(fecha.year)+ " a hs" + str(fecha.hour).zfill(2) + ":" + str(fecha.minute).zfill(2) #concateno la fecha solicitada y muestro en 2 digitos

    retira_nom=set_hitory.nomape_retira
    retira_dni=set_hitory.dni_retira
    return dict(ape=ape,dnpa=dnpa,nom=nom,ncer=ncer,fecha=fecha,retira_nom=retira_nom,retira_dni=retira_dni)

def preg_anular():#pregunta si quiere anular la solucitud
    ide=request.args[0]
    dnpa=request.args[1]
    apellido=request.args[2]
    nombre=request.args[3]
    tipo=request.args[4]
    nprontuario=request.args[5]
    estado=request.args[6]
    tipo=request.args[7]
    
    return dict(ide=ide,dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario,estado=estado)

def anular():
    ide=request.args[0]#saco id
    dnpa=request.args[1] #saco dni/pasaporte
    apellido=request.args[2]
    nombre=request.args[3]
    tipo=request.args[4]
    nprontuario=request.args[5]
    estado=request.args[6]
    
    setsoli=db(db.solicitud.id==ide).select() #armo un set
    for x in setsoli:#recorro el set

        x.update_record(estado_solicitud='Anulado') #y cambio el estado a anulado
    return dict(dnpa=dnpa,apellido=apellido,nombre=nombre,tipo=tipo,nprontuario=nprontuario
        ,estado=estado)
    


def web():

    return dict()



          

