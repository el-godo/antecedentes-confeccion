
from reportlab.pdfgen import canvas
# def encabezado():
# 	pdf="con_antecedentes.pdf"#largo,alto#defino como se va a llamar el arhivo pfg
# 	oficio=(612,1010) #configuro los tamaños de la hoja oficio 
# 	#A4=612.0, 792.0 
# 	doc = canvas.Canvas(pdf,pagesize=oficio)
# 	margen=db(db.margenes).select().first()
# 	x = margen.x
# 	largo=612.0	
# 	y =margen.y
# 	alto=1010  
	
# 	return dict()

def sin_antecedentes():
		#importo para poner la fecha
	from datetime import *    
    	hoyfecha=datetime.today() #capturo la fecha de hoy
    	dia=hoyfecha.day #capturo el dia
    	dia=str(dia)#paso el dia a string
    	mes=hoyfecha.month #capturo el mes
    	mes=str(mes)#paso el dia a string
    	#creo un diccionario para reemplazar el numero del mes por el nombre del mes
    	meses={"1":"ENERO","2":"FEBRERO","3":"MARZO","4":"ABRIL","5":"MAYO","6":"JUNIO","7":"JULIO","8":"AGOSTO","9":"SEPTIEMBRE","10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}
    	
    	qmes=meses[mes]# reemplazo el numero del mes en el diccionario mes
    	anio=hoyfecha.year #capturo el año
    	anio=str(anio)	#paso el año a string para pornerlo en el pdf
	ide_padron=request.args[1]	#traigo el argumento del id del padron
	ide_soli=request.args[0] 	#traigo el argumento del id de la solicitud
	dni=request.args[2] 		#traigo el dni de la persona
	DNI=str(dni)				#paso el dni a string para ponerlo en el pdf
	pa=db(db.padron.id==ide_padron).select().first() #realizo un set para sacar los datos de la tabla padron
	ape=pa.Apellido 	#capturo el apellido

	ape=ape+","			#le agrego una coma al apellido


	nom=pa.Nombre 		#capturo el nombre
	
	clase=pa.Clase 		#capturo la clase
	clase=str(clase) 	#paso la clase a string para ponerlo en el pdf
	dni=pa.DocumentoNro	#capturo el dni
	dni=str(dni)		#paso el dni a string para ponerlo en el pdf
	pasa=pa.Pasaporte	#capturo el pasaporte
	pasa=str(pasa)		#paso el pasaporte a string
	pesa=len(dni)
	valor=""
	if pesa==0:
		valor=pasa
	else:
		valor=dni


	nacion=pa.IdPais	#saco el id del pais 	
	paises=db(db.paises.id==nacion).select().first()# hago un set para sacar el pais
	pais=paises.pais 	#saco el nombre del pais
	vil={"S":"SOLTERO/A","C":"CASADO/A","D":"DIVORSIADO/A","V":"VIUDO/A"} #creo un diccionario 	
	civil=pa.EstadoCivil	# capturo el estado civil
	e_civil=vil[civil]#reemplazo en el diccionario vil	
	prof=pa.Profesion  #saco la profesion
	direc=pa.Direccion #saco la direccion
	clave={'1':"A.G.",'2':"C.I.",'3':"D.C.P.",'4':"D.E.",'5':"R.C.",'6':"S.P.",'0':None} #creo un diccionario para los tipos de prontuario
	tipo=pa.IdProntuarioTipo #saco el id del tipo de prontuario
	tipo=str(tipo)	#
	npront=pa.ProntuarioNro
	npront=str(npront)
	qtipo=clave[tipo]	
	sol=db(db.solicitud.id==ide_soli).select().first()
	solipor=sol.solicitado_por
	num=sol.nro_certificado
	capital=sol.capitalinterior
	intervino=sol.intervino
	fecha=sol.fecha_solicitada	
	user=sol.usuario
	tiene=sol.t_antecedentes
	ante=sol.antecedentes
	sol.update_record(estado_solicitud="Impreso")#cambio a estado impreso 
	#Importamos los modulos necesarios
	from reportlab.pdfgen import canvas# clase para crear el documento
	from reportlab.lib.colors import white,red,green,blue,gray,black#colores	
	from os import startfile	
	pdf="ej.pdf"#largo,alto#defino como se va a llamar el arhivo pfg
	certificado=(602,620) #configuro los tamaños de la hoja del certificado
	doc = canvas.Canvas(pdf,pagesize=certificado)
	margen=db(db.margenes).select().first()
	x = margen.x
	largo=602
	y =margen.y
	alto=620
	#sumo al apellidos
	cuanto_ape= len(ape) #cuento la cantidad de digitos
	cuanto_ape=float(cuanto_ape)
	cuanto_ape=(cuanto_ape*6)+x	#realizo esta operacion para q se acomode el nombre y no deje espacios
	

	

	doc.setFont("Courier", 10)#fuente de letra y tamaño
	doc.drawString(110+x,455+y,ape)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(cuanto_ape+120+x,455+y,nom)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(270+x,438+y,clase)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(373+x,438+y,valor)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(173+x,420+y,pais)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(380+x,420+y,e_civil)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(157+x,406+y,prof)#para poner texto valores x,y

	doc.setFont("Courier",9)	#fuente de letra y tamaño
	doc.drawString(160+x,390+y,direc)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(110+x,375+y,"CATAMARCA")#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(175+x,360+y,qtipo+npront)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(90+x,255+y,solipor)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(360+x,240+y,dia)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(160+x,225+y,qmes)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(360+x,225+y,anio)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(160+x,205+y,num)#para poner texto valores x,y

	doc.setFont("Courier",10)	#fuente de letra y tamaño
	doc.drawString(95+x,120+y,intervino)#para poner texto valores x,y
	doc.showPage()
	doc.save()
	startfile(pdf)
	redirect(URL(c='confeccion',f='menu_imprimir',args=[ide_soli,ide_padron,dni]))
                    
	return dict()
	


def dame_un_pdf():
	from datetime import *
	from reportlab.platypus import *
	from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
	from reportlab.rl_config import defaultPageSize
	from reportlab.lib.units import inch, mm
	from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
	from reportlab.lib import colors
	from uuid import uuid4
	from cgi import escape
	import os
	pdf="con_antecedentes.pdf"#largo,alto#defino como se va a llamar el arhivo pfg
	oficio=(612,1010) #configuro los tamaños de la hoja oficio
	doc = canvas.Canvas(pdf,pagesize=oficio)

	ide_padron=request.args[1]	#traigo el argumento del id del padron
	ide_soli=request.args[0] 	#traigo el argumento del id de la solicitud
	dni=request.args[2] 
	
	hoyfecha=datetime.today() #capturo la fecha de hoy
    	dia=hoyfecha.day #capturo el dia
     	dia=str(dia)#paso el dia a string
    	mes=hoyfecha.month #capturo el mes
    	mes=str(mes)#paso el dia a string

    	#creo un diccionario para reemplazar el numero del mes por el nombre del mes
    	meses={"1":"ENERO","2":"FEBRERO","3":"MARZO","4":"ABRIL","5":"MAYO","6":"JUNIO","7":"JULIO","8":"AGOSTO","9":"SEPTIEMBRE","10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}
    	
    	qmes=meses[mes]# reemplazo el numero del mes en el diccionario mes
    	anio=hoyfecha.year #capturo el año
    	anio=str(anio)	#paso el año a string para pornerlo en el pdf
    ####################################################################################################################################
    	pa=db(db.padron.id==ide_padron).select().first() #realizo un set para sacar los datos de la tabla padron

	ape=pa.Apellido 	#capturo el apellido
	ape=ape+","			#le agrego una coma al apellido
	nom=pa.Nombre 		#capturo el nombre
	clase=pa.Clase 		#capturo la clase
	clase=str(clase) 	#paso la clase a string para ponerlo en el pdf
	dni=pa.DocumentoNro	#capturo el dni
	dni=str(dni)		#paso el dni a string para ponerlo en el pdf
	pasa=pa.Pasaporte	#capturo el pasaporte
	pasa=str(pasa)		#paso el pasaporte a string
	valor=""
	q=""
	valor=len(dni) #calculo q contiene dni
	if valor ==0:
		valor=pasa
		q=" PASAPORTE: "
	else:
		valor=dni
		q=" D.N.I. : " 

	nacion=pa.IdPais	#saco el id del pais 	
	paises=db(db.paises.id==nacion).select().first()# hago un set para sacar el pais
	pais=paises.pais 	#saco el nombre del pais
	vil={"S":"SOLTERO/A","C":"CASADO/A","D":"DIVORSIADO/A","V":"VIUDO/A"} #creo un diccionario 	
	civil=pa.EstadoCivil	# capturo el estado civil
	e_civil=vil[civil]#reemplazo en el diccionario vil	
	prof=pa.Profesion  #saco la profesion
	direc=pa.Direccion #saco la direccion
	clave={'1':"A.G.",'2':"C.I.",'3':"D.C.P.",'4':"D.E.",'5':"R.C.",'6':"S.P.",'0':None} #creo un diccionario para los tipos de prontuario
	tipo=pa.IdProntuarioTipo #saco el id del tipo de prontuario
	tipo=str(tipo)	#
	npront=pa.ProntuarioNro
	npront=str(npront)
	qtipo=clave[tipo]
	######################################################################################################################################	
	sol=db(db.solicitud.id==ide_soli).select().first()
	solipor=sol.solicitado_por
	num=sol.nro_certificado
	capital=sol.capitalinterior
	intervino=sol.intervino
	fecha=sol.fecha_solicitada	
	user=sol.usuario
	tiene=sol.t_antecedentes
	ante=sol.antecedentes
	#cambio el estado a impreso
	sol.update_record(estado_solicitud="Impreso")

	#cargo las imagenes###################################################################################################

    	#Users\Policia\
	imagen_logo = Image("C:\\Users\\Policia\\Desktop\\web2py\\applications\\antecedentesplataforma\\static\\images\\encabezado.jpg", width=500, height=80)
	imagen_firma = Image("C:\\Users\\Policia\\Desktop\\web2py\\applications\\antecedentesplataforma\\static\\images\\firma.jpg", width=500, height=100)
	##############################################################################################################################

	###############################################################################################################################
	#tabla
	datos = (
        ('INTERVINO', ''),
        (intervino,''),
        ('',''),
        ('','')
    	)
	tabla = Table(data = datos,
              style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.black),
                       ('BOX',(0,0),(-1,-1),2,colors.black),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                       ('ALIGNMENT', (0,0), (-1,1), 'CENTER'),
                       ('TOPPADDING  ', (0,0), (-1,1), ), #TOP, MIDDLE o BOTTOM
                       ],
                        hAlign='LEFT'#alinar a la izquierda
              )
	###############################################################################################################################    	
    	

    	styles = getSampleStyleSheet()

    	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY,fontName='Helvetica',fontSize=10))


    	#archivotmp=os.path.join(request.folder,'private',str(uuid4()))
    	doc = SimpleDocTemplate(pdf)#archivotmp)
    	story = []
    	espacio=""
    	story.append(imagen_logo)    	
    	#story.append(Paragraph(escape(texto),styles["Justify"]))
    	story.append(Spacer(1,0.5*inch))
    	story.append(Paragraph(escape("Los funcionarios policiales que suscriben Certifican:"),styles["Justify"]))
    	story.append(Spacer(1,0.5*inch))
    	story.append(Paragraph(escape("Que "+ape+nom+" Clase: "+clase+q+valor+" de Nacionalidad "+pais
    		+" de estado civil: "+e_civil+" de profesión  "+prof+" con domicilio: "+direc
    		+" Se encuentra identificado/a en esta Policia bajo el Prontuario: "+qtipo+" Nº "+npront ),styles["Justify"]))
    	story.append(Spacer(1,0.5*inch))
    	
    	story.append(Paragraph(escape("OBSERVACIONES:"),styles["Justify"]))
    	story.append(Paragraph(escape(ante),styles["Justify"]))
    	story.append(Spacer(1,0.5*inch))

    	story.append(Paragraph(escape("A solicitud de la parte interesada y al solo efecto de ser presentada en : "+
    		solipor+"."+"Expiden el presente en la Ciudad de San Fernando del Valle de Catamarca(R.A.), con fecha: "
    		+dia+"/"+mes+"/"+anio +" Cert. Nº "+num),styles["Justify"]))
    	story.append(Spacer(1,0.5*inch))
    	story.append(Paragraph(escape("Se expide conforme Ley Nº4663, Art.8 Inc.'C'.-"),styles["Justify"]))
    	story.append(Spacer(1,0.1*inch))    	
	story.append(tabla)
	story.append(imagen_firma)
    	doc.build(story)
    	os.system(pdf)
    	#data = open(archivotmp,"rb").read()
    	#os.unlink(archivotmp)
    	#response.headers['Content-Type']='application/pdf'
    	redirect(URL(c='confeccion',f='menu_imprimir',args=[ide_soli,ide_padron,dni]))

	return dict(valor=valor)

    	
    	
    	
    	

# def txt():
# 		#importo para poner la fecha
# 	from datetime import *
# 	import os
    
#     	hoyfecha=datetime.today() #capturo la fecha de hoy
#     	dia=hoyfecha.day #capturo el dia
#     	dia=str(dia)#paso el dia a string
#     	mes=hoyfecha.month #capturo el mes
#     	mes=str(mes)#paso el dia a string
#     	#creo un diccionario para reemplazar el numero del mes por el nombre del mes
#     	meses={"1":"ENERO","2":"FEBRERO","3":"MARZO","4":"ABRIL","5":"MAYO","6":"JUNIO","7":"JULIO","8":"AGOSTO","9":"SEPTIEMBRE","10":"OCTUBRE","11":"NOVIEMBRE","12":"DICIEMBRE"}
    	
#     	qmes=meses[mes]# reemplazo el numero del mes en el diccionario mes
#     	anio=hoyfecha.year #capturo el año
#     	anio=str(anio)	#paso el año a string para pornerlo en el pdf
# 	ide_padron=request.args[1]	#traigo el argumento del id del padron
# 	ide_soli=request.args[0] 	#traigo el argumento del id de la solicitud
# 	dni=request.args[2] 		#traigo el dni de la persona
# 	DNI=str(dni)				#paso el dni a string para ponerlo en el pdf
# 	pa=db(db.padron.id==ide_padron).select().first() #realizo un set para sacar los datos de la tabla padron
# 	ape=pa.Apellido 	#capturo el apellido
# 	ape=ape+","			#le agrego una coma al apellido
# 	nom=pa.Nombre 		#capturo el nombre
# 	clase=pa.Clase 		#capturo la clase
# 	clase=str(clase) 	#paso la clase a string para ponerlo en el pdf
# 	dni=pa.DocumentoNro	#capturo el dni
# 	dni=str(dni)		#paso el dni a string para ponerlo en el pdf
# 	pasa=pa.Pasaporte	#capturo el pasaporte
# 	pasa=str(pasa)		#paso el pasaporte a string
# 	nacion=pa.IdPais	#saco el id del pais 	
# 	paises=db(db.paises.id==nacion).select().first()# hago un set para sacar el pais
# 	pais=paises.pais 	#saco el nombre del pais
# 	vil={"S":"SOLTERO/A","C":"CASADO/A","D":"DIVORSIADO/A","V":"VIUDO/A"} #creo un diccionario 	
# 	civil=pa.EstadoCivil	# capturo el estado civil
# 	e_civil=vil[civil]#reemplazo en el diccionario vil	
# 	prof=pa.Profesion  #saco la profesion
# 	direc=pa.Direccion #saco la direccion
# 	clave={'1':"A.G.",'2':"C.I.",'3':"D.C.P.",'4':"D.E.",'5':"R.C.",'6':"S.P.",'0':None} #creo un diccionario para los tipos de prontuario
# 	tipo=pa.IdProntuarioTipo #saco el id del tipo de prontuario
# 	tipo=str(tipo)	#
# 	npront=pa.ProntuarioNro
# 	npront=str(npront)
# 	qtipo=clave[tipo]	
# 	sol=db(db.solicitud.id==ide_soli).select().first()
# 	solipor=sol.solicitado_por
# 	num=sol.nro_certificado
# 	capital=sol.capitalinterior
# 	intervino=sol.intervino
# 	fecha=sol.fecha_solicitada	
# 	user=sol.usuario
# 	tiene=sol.t_antecedentes
# 	ante=sol.antecedentes
	
# 	file = open("txt.txt", "w")
# 	file.write("Los Funcionarios Policiales que suscriben Certifican: \n")
# 	file.write( "\n" )
# 	file.write( "" +os.linesep)#espacion en blanco
# 	file.write("Que "+ ape+ nom + " Clase " +clase +" D.N.I. Nº :" +dni +" de nacionalidad:"+ os.linesep)
# 	file.write(pais+" de estado civil: "+e_civil+" de profesion: "+prof+ os.linesep)
# 	file.write("con domicilio: "+direc+ os.linesep)

# 	file.write("Se encuentra indentificado/a en esta policia bajo Promtuario:"+ os.linesep )
# 	file.write(qtipo+" "+npront+ os.linesep )
# 	file.write("Observaciones:"+os.linesep )
	
# 	file.write(ante)
# 	file.write("A solicitud de la parte interesada y al solo efecto de ser presentada en: "+ os.linesep)
# 	file.write( solipor+"." +os.linesep)
# 	file.write( "Expiden el presente en la Ciudad de San Fernando del Valle de Catamarca(R.A.), con fecha:"+dia+"/"+mes+"/"+anio +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "Cert. Nº"+num +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "Se expide conforme Ley Nº4663, Art.8 Inc.'C' " +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "" +os.linesep)
# 	file.write( "-----------------------------------------------"+"                          "+"	------------------------------------------------" +os.linesep)
# 	file.write( "       Jefe Div. Ant. Personales"+"                          	"+"Jefe Depto.Inv. Judiciales (D-5)" +os.linesep)	
# 	file.close()
# 	#redirect(URL(c='imprimir',f='con_antecedentes',args=[ide_soli,ide_padron,dni]))
# 	return dict(ante=ante)

# def con_antecedentes():
# 	ide_padron=request.args[1]	#traigo el argumento del id del padron
# 	ide_soli=request.args[0] 	#traigo el argumento del id de la solicitud
# 	dni=request.args[2] 
# 	from reportlab.pdfgen import canvas# clase para crear el documento
# 	from reportlab.lib.colors import white,red,green,blue,gray,black#colores	
# 	from os import startfile
# 	from reportlab.lib.utils import ImageReader
# 	import StringIO
# 	import PIL.Image
# 	from reportlab.lib.styles import getSampleStyleSheet
# 	from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
# 	from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# 	import os
# 	from io import open
# 	import reportlab.rl_config
# 	reportlab.rl_config.warnOnMissingFontGlyphs = 0
# 	from reportlab.pdfbase import pdfmetrics
# 	from reportlab.pdfbase.ttfonts import TTFont
# 	from textwrap import wrap
# 	pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
# 	pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
# 	pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
# 	pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))	
# 	pdf="con_antecedentes.pdf"#largo,alto#defino como se va a llamar el arhivo pfg
# 	oficio=(612,1010) #configuro los tamaños de la hoja oficio 
# 	#A4=612.0, 792.0 
# 	doc = canvas.Canvas(pdf,pagesize=oficio)
# 	margen=db(db.margenes).select().first()
# 	x = margen.x
# 	largo=612.0	
# 	y =margen.y
# 	alto=1010  
# 	estilos = getSampleStyleSheet()
# 	style = estilos['BodyText']	
# 	encabezado=[]
# 	header1=doc.drawImage("d:\\web2py\\applications\\antecedentesplataforma\\static\\images\\escudo1.jpg",80,950,50,50)#insertar imagen
# 	doc.setFont("Helvetica-Bold", 18)#fuente de letra y tamaño
# 	encabezado.append(header1)
# 	header2=doc.drawString(150+x,970+y,"CERTIFICADO DE ANTECEDENTES")#para poner texto valores x,y
# 	encabezado.append(header2)
# 	header3=doc.drawImage("d:\\web2py\\applications\\antecedentesplataforma\\static\\images\\escudo_policia.jpg",480,950,50,50)#insertar imagen
# 	encabezado.append(header3)
# 	doc.setFont("Courier-BoldOblique", 11)#fuente de letra y tamaño
# 	doc.drawString(210+x,950+y,"VALIDO POR SEIS MESES")#para poner texto valores x,y	
# 	#doc.drawText(text)	
# 	from reportlab.platypus import *
# 	story=[]	
# 	textoArchivo = open("txt.txt", "r")  # Abrimos un archivo de texto
# 	text=""
# 	textobject = doc.beginText(40,890)  # Iniciamos el textobject
# 	textobject.setTextOrigin(40, 890)  # Ubicamos el cursor donde dibujar
# 	textobject.setFont("VeraIt", 8)
# 	for i in textoArchivo:
# 		#i = i.replace("\n","")  # Remplazamos el salto de linea
# 		#textobject.textLine( i)  # Dibujamos la linea
# 		p = Paragraph(i, style)
#  		story.append(p)
#  		story.append(Spacer(1,0.2))
	  
# 	#textobject.setCharSpace(0.1)  # Espacio entre caracteres 
# 	#textobject.setWordSpace(0.2)  # Espacio entre palabras	   
# 	#wraped_text = "\n".join(wrap(text, 80)) # 80 is line width
# 	doc.drawText(textobject)  # Dibujamos el texto pasando un objeto de texto
# 	doc.build(story)
# 	#doc.showPage()
# 	doc.save()	
# 	#startfile(pdf)   
# 	return dict()
def margenes():
	#de esta funcion puedo configurar el las unidades x e y de los margenes
	margen=db(db.margenes.id==1).select().first()
	x=margen.x
	y=margen.y
	form=SQLFORM.factory(
	Field('x','bolean',label="X ,o Horizontal",default=x),
	Field('y','bolean',label="Y ,o Vertical",default=y),
		)
	if form.accepts(request,session):
    		response.flash = 'formulario aceptado'
    		margen.update_record(x=form.vars.x,y=form.vars.y)
    		redirect(URL(c='imprimir',f='margenes')
    			)
    		
    		
    	elif form.errors:
        	response.flash = 'el formulario tiene errores'
    	else:
        	response.flash = 'por favor complete el formulario'  



	return dict(form=form)







	



	




	

	
 
 

	

    
	



	
	














	
