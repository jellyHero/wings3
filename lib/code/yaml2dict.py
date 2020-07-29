import yaml

def yaml2dict(yaml_str):
    yaml_data = yaml.safe_load(yaml_str)
    return yaml_data

def yaml2dict_fromFile(file_path):
    with open(file_path) as yaml_str:
        yaml_data = yaml.safe_load(yaml_str)
    return yaml_data
#
# test='''name: poc-yaml-example-com
# rules:
#   - method: GET
#     path: "/update"
#     expression: "true"
#     search: |
#       <input type="hidden" name="csrftoken" value="(?P<token>.+?)"
#   - method: POST
#     path: "/update"
#     body: |
#       id=';echo(md5(123));//&csrftoken={{token}}
#     expression: |
#       status == 200 && body.bcontains(b'202cb962ac59075b964b07152d234b70')'''
#
# print(yaml2dict(test))