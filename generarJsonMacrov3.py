#!/usr/bin/python
# -*- coding: utf-8 -*-
# Bash que permite leer un archivo JSON y
# Exportarlo a Zendesk por medio de las API

# El archivo JSON se genera usando Skyvia y luego transformandolo a JSON 
# usando la pagina https://www.convertcsv.com/csv-to-json.htm

import sys
import argparse
import getopt
import csv
import json
import codecs
import os
import re
import pyperclip
import numpy as np
import imp

imp.reload(sys)


def clear():  # También la podemos llamar cls (depende a lo que estemos acostumbrados)
    if os.name == "posix":
        os.system("clear")
    elif os.name == ("ce", "nt", "dos"):
        os.system("cls")


def ClipBoard(file):  # También la podemos llamar cls (depende a lo que estemos acostumbrados)
    if os.name == "posix":
        # print 'cat '+file+' | xclip -selection clipboard'
        os.system('cat '+file+' | xclip -selection clipboard')
    elif os.name == ("ce", "nt", "dos"):
        os.system("")

# sys.setdefaultencoding('utf8')


def salir(mensaje, leer):
    print("--- ERROR EN LA VALIDACION ---")
    print("Linea: " + str(leer.line_num))
    print("Mensaje: "+mensaje)
    print("------------------------------")
    # break
    # exit()


def generar_jsonv2(row_json, campo, custom_fields, cabecera, migrar, output):
    #print (custom_fields)
    # exit()
    # bueno
    if len(custom_fields) > 0:
        if campo == "custom_field_options":
            df = []
            df.append(custom_fields)
            row_json[campo] = df
            cabecera[migrar] = row_json

            #cabecera = custom_fields
            row_json[campo] = custom_fields

            output.append(row_json)
            cabecera[migrar] = output  # row_json
            # exit()
        else:
            row_json[campo] = custom_fields
#######
    if campo == "custom_field_options":
        df = []
        df.append(row_json)
        cabecera[migrar] = df
        row_json[campo] = custom_fields

        output.append(row_json)
        cabecera[migrar] = output
    else:
        df = []
        df.append(row_json)
        output.append(row_json)
        cabecera[migrar] = output  # row_json
    return cabecera


def generar_jsonv1(row_json, campo, custom_fields, cabecera, migrar, output):
    print(campo)
    exit()
# bueno
    if len(custom_fields) > 0:
        if campo == "custom_field_options":
            df = []
            df.append(custom_fields)
            row_json[campo] = df
            cabecera[migrar] = row_json

            print(custom_fields)

            #cabecera = custom_fields
            #row_json[campo] = custom_fields

            # output.append(row_json)
            # cabecera[migrar] = output #row_json
            exit()
        else:
            row_json[campo] = custom_fields
#######
    else:
        df = []
        df.append(row_json)
        output.append(row_json)
        cabecera[migrar] = output  # row_json
    return cabecera


def generar_archivo(output, archivo, i):
    file = archivo +i+ '.json'
    salida = open(file, 'w')
    # print salida
    json.dump(output,
              salida,
              sort_keys=False,
              ensure_ascii=False)
    # pyperclip.copy(sali|da)
    # Copia al Portapapeles el resultado del Archivo
    ClipBoard(file)

    # return archivo+`i`+'.json'
    return file


def recortar(palabra, buscar):
    palab = palabra.strip()
    posicion = palab.index(buscar)
    tamano = len(palab)
    return palab[posicion+1:tamano]

def convertir(dictionary, archivo, row, option):
    #dictionaryToJson = json.dumps(pythonDictionary)

    #jsonData = '{"name": "Frank", "age": 39}'
    #archivo2 = "TicketField_20201227.json"
    objeto = {}
    arreglo = []
    with open(dictionary) as origen:
        dictionary    = json.load(origen)
    #dictionary = {"360036732012":"000000000", "360028889271":"1111111111", "360013486511":"222222","360013523032":"333333" } 
    #dictionary = {"360013523032":"333333", "360013486511":"222222" } 
    i = 0
    with open(archivo) as file:
        data = json.load(file)
   
        for registro in data:  #Ej: { automations: [{  }]
            print("Registro: ",i+1)

            for actions in registro['Actions']: #Ej: "actions": [{ }]
                print(actions)
                for key in dictionary.keys(): 
                    actions['field'] = actions['field'].replace(key,dictionary[key])
                    actions['value'] = actions['value'].replace(key,dictionary[key])


            for actions in registro['actions']: #Ej: "actions": [{ }]
                for key in dictionary.keys():
                    ##print(actions['field']) 
                    actions['field'] = actions['field'].replace(key,dictionary[key])
                    #array_str = (map(str,actions['value'])) #Ej: "restriction": { ids: [] }
                    if (type(actions['value']) != list):
                        #print(actions['value'])
                        actions['value'] = actions['value'].replace(key,dictionary[key])
                    elif (type(actions['value']) == list):

                        if (actions['value']): 
                                array_str = list(map(str,actions['value'])) #Ej: "restriction": { ids: [] }
                                np_array = np.array(array_str)
                                for key in dictionary.keys():
                                    de = np.where(np_array == (key))
                                    if (len(de[0] != 0 )):
                                        for key2 in de:
                                            #print("se consiguio", key)
                                            #print("posicion: ",key2) 
                                            #print("::: ", dictionary) 
                                            #print("cambio por: ", dictionary[key]) 

                                            #sw = de[0]
                                            #print(de)

                                            #print(" dictionary[key]:",dictionary[key])
                                            array_str[int(key2)] = int(dictionary[key])
                                            #print(" array_str: ",array_str)

                                            actions['value'] = array_str
                                            #print("modificado: ",actions['value'])
                                            
            for actions in registro['conditions']['all']: #Ej: "actions": [{ }]
                for key in dictionary.keys(): 
                    actions['value'] = actions['value'].replace(key,dictionary[key])
                    actions['field'] = actions['field'].replace(key,dictionary[key])

            for actions in registro['conditions']['any']: #Ej: "actions": [{ }]
                for key in dictionary.keys(): 
                    actions['value'] = actions['value'].replace(key,dictionary[key])
                    actions['field'] = actions['field'].replace(key,dictionary[key])
     
            # print("//////")
            # print("= Actions -> Value: ")
            # print( registro['actions'])
            # print("//////")


#            for key in dictionary.keys():
#                registro['restriction']['ids'] = (array_str.replace(key,dictionary[key]))
            #    registro['restriction']['ids'] = (str(registro['restriction']['ids']).replace(key,dictionary[key]))

            #print(registro['restriction']['ids'])
            #print('')

                ##print('actions>value:', dat)
            ##print(registro['restriction']['ids'])

            #fase = '360001196111'
            #print(fase.replace('360001196111','lobaton'))
            #act = registro['actions']
            #print('actions:', act.replace('360001196111','jesus'))

            arreglo.append(registro)
        objeto["macros"] = arreglo
        file = generar_archivo(objeto,"CambiodeIdAutomatization_","1")
    return "/// Se ha generado correctamente el archivo: "+file

clear()
parser = argparse.ArgumentParser()
parser.add_argument(
    "-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Archivo a procesar (JSON)")
parser.add_argument(
    "-r", "--row", help="Cuantos Registros se va a Generar por archivo")
parser.add_argument(
    "-o", "--option", help="Debe especificar si es users, tickets, groups, organzations, u-cfo, macros, gm=group_memberships")
parser.add_argument("-d", "--dictionary", help="Archivo del Diccionario (JSON)")

args = parser.parse_args()

if args.option == 'users':
    url = 'users/create_many.json  -  users/create_or_update_many.json'
    method = 'POST'
elif args.option == 'macros':
    doc = 'https://developer.zendesk.com/rest_api/docs/support/macros#create-macro'
    url = '/api/v2/macros.json'
    method = 'POST'

else:
    url = ''
    method = ''

print ("///////////////////////////////////////////////////////")
print ("///")
print ("/// Doc: "+doc)
print ("/// URL: "+url)
print ("/// METHOD: "+method)
if (args.file):
    ##print (procesar(args.file, args.row, args.option))
    print (convertir(args.dictionary, args.file, args.row, args.option))    
print ("/// Use Ctrl + V y para pegarlo en la API Console")
print ("///")
print ("//////////////////////////////////////////////////////")