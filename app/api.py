from datetime import datetime
import time
import json
from bson import ObjectId

#from mongoengine import *
from flask import Flask, request, abort, Response

from app import mininote
from app import model


@mininote.route('/notes', methods=['GET'])
def get_all_notes():
    if model.Note.objects.count() == 0:
        return Response(json.dumps([]),  mimetype='application/json')
    notes = [note.to_mongo() for note in model.Note.objects]

    for note in notes:
        note['note_id'] = str(note['_id'])
        del note['_id']
        note['creation_time'] = int(note['creation_time'].strftime("%s")) * 1000
        note['modification_time'] = int(note['modification_time'].strftime("%s")) * 1000

    return Response(json.dumps(notes),  mimetype='application/json')


@mininote.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    if not ObjectId.is_valid(note_id):
        abort(404)
    if not model.Note.objects(pk=note_id):
        abort(404)

    note = model.Note.objects(pk=note_id)[0].to_mongo()

    note['note_id'] = str(note['_id'])
    del note['_id']
    note['creation_time'] = int(note['creation_time'].strftime("%s")) * 1000
    note['modification_time'] = int(note['modification_time'].strftime("%s")) * 1000

    return Response(json.dumps(note),  mimetype='application/json')


@mininote.route('/notes', methods=['POST'])
def make_note():
    try:
        body = request.json['body']
        subject = request.json['subject']
    except:
        abort(400)

    if len(subject) == 0:
        subject = 'New note'

    model.Note(body=body, subject=subject, creation_time=datetime.now(), modification_time = datetime.now()).save()

    return Response(json.dumps({"SUCCESS": "You made a new note"}), mimetype='application/json')


@mininote.route('/notes/<note_id>', methods=['PUT'])
def edit_note(note_id):
    if not ObjectId.is_valid(note_id):
        abort(400)
    if not model.Note.objects(pk=note_id):
        abort(404)

    try:
        body = request.json['body']
        subject = request.json['subject']
    except:
        abort(400)

    if model.Note.objects(pk=note_id)[0].body != body:
        model.Note.objects(pk=note_id)[0].update(set__body=body)
    if model.Note.objects(pk=note_id)[0].subject != subject:
        model.Note.objects(pk=note_id)[0].update(set__subject=subject)
    model.Note.objects(pk=note_id)[0].update(set__modification_time=datetime.now())

    return Response(json.dumps({"SUCCESS": "Note was modified"}), mimetype='application/json')


@mininote.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    if not ObjectId.is_valid(note_id):
        abort(400)
    if not model.Note.objects(pk=note_id):
        abort(404)

    model.Note.objects(pk=note_id)[0].delete()

    return Response(json.dumps({"SUCCESS": "Note was deleted"}), mimetype='application/json')


@mininote.route('/about', methods=['GET'])
def get_info():
    info_about = {
    "name": "Mininote",
    "description": "RESTful web app for working with notes.",
    "version": "0.1 pre-alfa",
    "license": "GPL",
    "author": "A. Stringfield",
    "source code": "https://github.com/a-stringfield/mininote",
    "API Reference": "https://github.com/a-stringfield/mininote/wiki",
    "feedback": "https://github.com/a-stringfield/minichan/issues"
    }

    return Response(json.dumps(info_about), mimetype='application/json')


@mininote.route('/coffee', methods=['GET'])
def teapot():
	abort(418)


@mininote.errorhandler(404)
def page_not_found(e):
    return Response(json.dumps({"ERROR": {"Code": 404, "Message": "Not found."}}), mimetype='application/json'), 404


@mininote.errorhandler(400)
def page_not_found(e):
    return Response(json.dumps({"ERROR": {"Code": 400, "Message": "Bad Request."}}), mimetype='application/json'), 400


@mininote.errorhandler(500)
def page_not_found(e):
    return Response(json.dumps({"ERROR": {"Code": 500, "Message": "Internal Server Error."}}), mimetype='application/json'), 500


@mininote.errorhandler(418)
def page_not_found(e):
    return Response(json.dumps({"ERROR": {"Code": 418, "Message": "I am a teapot."}}), mimetype='application/json'), 418
