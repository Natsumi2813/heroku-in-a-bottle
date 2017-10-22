#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
import json
import urllib.request

from bottle import request, route, response, get, post, template, error, HTTPError, static_file
api = {'car': 'http://apis.is/car?number={}', 'company': 'http://apis.is/company?name={}'}
links = {'car': 'Car', 'company': 'Company'}


def get_api_data(api_):
    with urllib.request.urlopen(api_) as dump:
        data = json.loads(dump.read().decode())
    return data


@error(404)
def error404(error):
    return template('error.html')


@route('/')
def index():
    return template('inde.html')


@route('/404')
def rais_404():
    raise HTTPError(404)


@get('/<id>')
def get_api(id):
    try:
        return template('{}.html'.format(id), {'multi': False})
    except:
        raise HTTPError(404)


@post('/<id>')
def post_api(id):
    if len(list(request.forms)) > 0:
        item = [request.forms.get(b) for b in [x for x in request.forms]]
        info = get_api_data(api[id].format(item[0]))
        info['results'][0].update({'multi': True, 'id': id})
        return template('{}_p.html'.format(id), info['results'][0])
    else:
        info = get_api_data(api[id])
        info['results']['multi'] = False
        return template('', info)

@get('/s/<path:re:.*\.(png|jpg|json|css)>')
def static(path):
    return static_file(path, root='./st')

bottle.run(host='0.0.0.0', port=argv[1])
