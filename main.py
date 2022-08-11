import ast
import traceback
import yaml

from Database import Database
from flask import Flask, request
from flask_caching import Cache
from flask_cors import CORS
from flask_restful import Resource, Api
from marshmallow import Schema, fields
from urllib.parse import unquote

with open("credentials.yaml", "r", encoding="utf8") as stream:
    yaml_data = yaml.safe_load(stream)

app = Flask(__name__)
api = Api(app)
CORS(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def query(statement, *args):
    data = [i for i in Database.get(statement, *args)]
    if not data:
        return None
    result = [dict(row) for row in data]
    return result


def artifacts_parser(header: [], lst_of_lst: []):
    lst = ast.literal_eval(lst_of_lst)

    if not lst:
        return None
    new_data = zip(header, lst)
    lst = dict(new_data)

    return lst


def stats_parser(header: [], lst_of_lst: []):
    lst = ast.literal_eval(lst_of_lst)

    if not lst:
        return None
    for n, l in enumerate(lst):
        new_data = zip(header, l)
        lst[n] = dict(new_data)

    return lst


class Artifact(Resource):
    @cache.cached(timeout=604800, query_string=True)
    def get(self):
        try:
            name = request.args.get('name', None)
            if name:
                name = unquote(request.args['name']).replace('_', ' ')
                result = query(f" SELECT * FROM artifacts WHERE setName = ? ", name)
                lst = result

                if not lst:
                    return {'Error': 'Name does not exist for artifact.'}, 400

                lst = result[0]['setEffect']
                headers = ['2 Set Effect', '4 Set Effect']
                new_lst = artifacts_parser(headers, lst) if lst else None
                result[0]['setEffect'] = new_lst
                return result[0], 200

            data = [i for i in Database.get('SELECT * FROM artifacts ')]
            result = [dict(row) for row in data]
            headers = ['2 Set Effect', '4 Set Effect']

            for dicts in result:
                new_lst = artifacts_parser(headers, dicts['setEffect']) if dicts['setEffect'] else None
                dicts['setEffect'] = new_lst

            return result, 200

        except:
            traceback.print_exc()


class Character(Resource):
    @cache.cached(timeout=604800, query_string=True)
    def get(self):
        try:
            name = request.args.get('name', None)
            if name:
                name = unquote(request.args['name']).replace('_', ' ')
                result = query(f" SELECT * FROM characters WHERE characterName = ? ", name)
                lst = result

                if not lst:
                    return {'Error': 'Name does not exist for character.'}, 400

                lst = result[0]['characterStats']
                headers = ['Level', 'HP', 'Attack', 'DEF', 'Secondary Stats']
                new_lst = stats_parser(headers, lst)
                result[0]['characterStats'] = new_lst
                return result[0], 200

            data = [i for i in Database.get('SELECT * FROM characters ')]
            result = [dict(row) for row in data]
            headers = ['Level', 'HP', 'Attack', 'DEF', 'Secondary Stats']

            for dicts in result:
                new_lst = stats_parser(headers, dicts['characterStats'])
                dicts['characterStats'] = new_lst

            return result, 200

        except:
            traceback.print_exc()


class Weapon(Resource):
    @cache.cached(timeout=604800, query_string=True)
    def get(self):
        try:
            name = request.args.get('name', None)
            weapon_type = request.args.get('type', None)

            if name and weapon_type:
                weapon_name = unquote(request.args['name']).replace('_', ' ')
                result = query(f' SELECT * FROM weapons WHERE weaponType = ? AND weaponName = ?', request.args['type'],
                               weapon_name)
                lst = result

                if not lst:
                    return {'Error': 'Name or weapon type does not exist for weapon.'}, 400

                lst = result[0]['weaponStats']
                headers = ['Level', 'Attack', 'Secondary Stats']
                new_lst = stats_parser(headers, lst)
                result[0]['weaponStats'] = new_lst
                return result[0], 200

            if weapon_type:
                result = query(f' SELECT * FROM weapons WHERE weaponType = ? ', request.args['type'])
                headers = ['Level', 'Attack', 'Secondary Stats']
                valid_weapon_types = ["Claymores", "Swords", "Catalysts", "Bows", "Polearms"]
                if not result:
                    return {
                               'Error': f'Weapon type does not exist for weapon. Valid weapon types are: {str(valid_weapon_types)}'}, 400

                for dicts in result:
                    new_lst = stats_parser(headers, dicts['weaponStats'])
                    dicts['weaponStats'] = new_lst
                return result, 200

            if name:
                name = unquote(request.args['name']).replace('_', ' ')
                result = query(f" SELECT * FROM weapons WHERE weaponName = ? ", name)
                lst = result

                if not lst:
                    return {'Error': 'Name does not exist for weapon.'}, 400

                lst = result[0]['weaponStats']
                headers = ['Level', 'Attack', 'Secondary Stats']
                new_lst = stats_parser(headers, lst)
                result[0]['weaponStats'] = new_lst
                return result[0], 200

            data = [i for i in Database.get('SELECT * FROM weapons ')]
            result = [dict(row) for row in data]
            headers = ['Level', 'Attack', 'Secondary Stats']

            for dicts in result:
                new_lst = stats_parser(headers, dicts['weaponStats'])
                dicts['weaponStats'] = new_lst

            return result, 200

        except:
            traceback.print_exc()


if __name__ == '__main__':
    api.add_resource(Artifact, '/artifacts', endpoint='api/artifacts')
    api.add_resource(Character, '/characters', endpoint='api/characters')
    api.add_resource(Weapon, '/weapons', endpoint='api/weapons')

    app.run(host='0.0.0.0', port=80)
