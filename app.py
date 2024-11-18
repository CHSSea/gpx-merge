"""
app

Author: xiaohai
Date: 2024/11/15
Desc: 
"""
import json
import os
import uuid

from flask import Flask, request

from merge import merge_file

app = Flask(__name__)


@app.route('/merge_gpx', methods=['POST'])
def merge_gpx():
    files = request.files.getlist('file')

    gpx_file_path = os.path.join(os.path.abspath('.'), 'gpx_file')
    if not os.path.exists(gpx_file_path):
        os.makedirs(gpx_file_path)

    for file in files:
        filename = file.filename
        _, ext = os.path.splitext(filename)
        if ext != '.gpx':
            response = {'code': '400', 'msg': 'error file format'}
            return json.dumps(response)

    uuid_path = str(uuid.uuid4())
    current_path = os.path.join(gpx_file_path, uuid_path)
    os.makedirs(current_path)
    print('current_path={}'.format(current_path))

    gpx_files_path = []
    out_file_path = os.path.join(current_path, 'out_merge.gpx')
    for file in files:
        file.save(os.path.join(current_path, file.filename))
        gpx_files_path.append(os.path.join(current_path, file.filename))

    merge_file(gpx_files_path, out_file_path)

    response = {'code': '200', 'msg': 'save success'}
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
