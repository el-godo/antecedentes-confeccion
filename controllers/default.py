# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from gluon.serializers import json


@auth.requires_login()
def index():
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    

    ## Atrapo el id del usaurio logueado
    quien = auth.user.id

    ## Creo un set para sacar la ofician donde trabaja
    usuario = db(db.auth_user.id==quien).select().first()

    if usuario.oficina == "Super":
        set_usuario = db(db.auth_user).select()
        mf = json(set_usuario)
    elif usuario.oficina == "Confeccion":
        redirect(URL(c='default',f='panel'))
    
    return dict(set_usuario=set_usuario, mf=mf, usuario=usuario)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())
def panel():
    return dict()


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()




