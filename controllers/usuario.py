
#--------------------------------------------------------------------

@auth.requires_login()
@auth.requires(auth.has_membership('Administrador'))
def editar():
    #--Atrapo el id del usuario
    usu = int(request.args[0])

    #--Creo un set para traer los datos del id pasado
    set_usu = db(db.auth_user.id == usu).select()


    #--Construyo mi SQLFORM
    formulario = SQLFORM(db.auth_user,usu,showid=False)
    

    if formulario.process().accepted:
        redirect(URL(c='default',f='index'))
        response.flash = 'Formulario aceptado'
    elif formulario.errors:
        response.flash = 'Formulario con errores'
    else:
        response.flash = 'Completar el formulario'



    return dict(usu=usu, set_usu=set_usu, formulario=formulario)


@auth.requires_login()
@auth.requires(auth.has_membership('Administrador'))
def nuevo():

     #--Armo el formulario para la carga de los usuarios
    formulario = SQLFORM(db.auth_user)
    if formulario.process().accepted:
        response.flash = 'formulario aceptado'
        redirect(URL(c='default',f='index'))
    elif formulario.errors:
        response.flash = 'el formulario tiene errores'
    else:
        response.flash = 'por favor complete el formulario'
    return dict(formulario=formulario)
    

@auth.requires(auth.has_membership('Administrador'))
def eliminar():
    #--Atrapo el id del usuario
    usu = int(request.args[0])

    #--Creo un set para traer los datos del id pasado
    set_usu = db(db.auth_user.id == usu).select()


    #--Construyo mi SQLFORM
    formulario = SQLFORM(db.auth_user,usu,showid=False,deletable=True)
    

    if formulario.process().accepted:
        redirect(URL(c='default',f='index'))
        response.flash = 'Formulario aceptado'
    elif formulario.errors:
        response.flash = 'Formulario con errores'
    else:
        response.flash = 'Completar el formulario'



    return dict(usu=usu, set_usu=set_usu, formulario=formulario)