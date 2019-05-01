import requests
import json
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

# Flask / Bootstrap initialization
app = Flask(__name__)
Bootstrap(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_volume_group', methods=['POST'])
def create_volume_group():
    if request.method == 'POST':
        volume_group_name = request.form['volume_group_name']
        api_url = "https://k2_ip/api/v2/volume_groups"
        payload = {'name': volume_group_name}
        request_command = "requests.post(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin)))"

        return render_template('create_volume_group.html', volume_group_name=volume_group_name, request_command=request_command)


@app.route('/create_volume', methods=['POST'])
def create_volume():
    if request.method == 'POST':
        volume_name = request.form['volume_name']
        volume_size_gb = request.form['volume_size']
        volume_size_kb = int(volume_size_gb)*1000000
        volume_group = request.form['volume_group']
        vmware_enabled = request.form['vmware_support']
        description = request.form['volume_description']
        api_url = "https://k2_ip/api/v2/volumes"
        payload = {'name': volume_name, 'size': volume_size_kb, 'volume_group': volume_group, 'vmware_enabled': vmware_enabled, 'description': description}
        request_command = "requests.post(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin)))"

        return render_template('create_volume.html', volume_name=volume_name, volume_size_gb=volume_size_gb, request_command=request_command)


@app.route('/create_host_group', methods=['POST'])
def create_host_group():
    if request.method == 'POST':
        host_group_name = request.form['host_group_name']
        connectivity_type = request.form['connectivity_type']
        host_group_description = request.form['host_group_description']
        allow_different_host_types = request.form['allow_different_host_types']
        if allow_different_host_types == "True":
            allow_different_host_types_bool = True
        elif allow_different_host_types == "False":
            allow_different_host_types_bool = False
        api_url = "https://k2_ip/api/v2/host_groups"
        payload = {'name': host_group_name, 'connectivity_type': connectivity_type, 'description': host_group_description, 'allow_different_host_types': allow_different_host_types_bool}
        request_command = "requests.post(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin))"

        return render_template('create_host_group.html', host_group_name=host_group_name, request_command=request_command)


@app.route('/create_host', methods=['POST'])
def create_host():
    if request.method == 'POST':
        host_name = request.form['host_name']
        host_type = request.form['host_type']
        host_group = request.form['host_group']
        api_url = "https://k2_ip/api/v2/hosts"
        payload = {'name': host_name, 'type': host_type, 'host_group': host_group}
        request_command = "requests.post(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin))"

        return render_template('create_host.html', host_name=host_name, host_type=host_type, host_group=host_group, request_command=request_command)


@app.route('/fc_pwwn_lookup', methods=['POST'])
def fc_pwwn_lookup():
    if request.method == 'POST':
        pwwn = request.form['pwwn']
        api_url = "https://k2_ip/api/v2/host_fc_ports?pwwn=" + pwwn
        payload = {'pwwn': pwwn}
        request_command = "requests.get(" + api_url + ", auth=('admin', 'admin))"

        return render_template('fc_pwwn_lookup.html', pwwn=pwwn, request_command=request_command)


@app.route('/fc_pwwn_host_modify', methods=['POST'])
def fc_pwwn_host_modify():
    if request.method == 'POST':
        pwwn = request.form['pwwn']
        pwwn_get_request = "request.get(https://k2_ip/api/v2/host_fc_ports?pwwn=" + pwwn + ", auth=('admin', 'admin))"
        pwwn_json_example = '''
        {
            "hits": [
                {
                    "host": "host1",
                    "id": 2,
                    "pwwn": "12:34:56:78:90:ab:cd:e1"
                }
            ]
        }
        '''
        pwwn_data = json.loads(pwwn_json_example)
        print(pwwn_data)
        pwwn_id = str(pwwn_data['hits'][0]['id'])
        print(pwwn_id)

        associated_host = request.form['associated_host']
        associated_host_get_request = "request.get(https://k2_ip/api/v2/hosts?name=" + associated_host + ", auth=('admin', 'admin))"
        associated_host_json_example = '''
                {
                    "host_group": {
                        "ref": "/host_groups/16"
                    },
                        "id": 7,
                        "is_part_of_group": true,
                        "name": "host5",
                        "type": "Windows",
                        "views_count": 0,
                        "volumes_count": 10
                }
                '''
        associated_host_data = json.loads(associated_host_json_example)
        associated_host_id = str(associated_host_data['id'])
        print(associated_host_id)

        api_url = "https://k2_ip/api/v2/host_fc_ports/" + pwwn_id
        payload = {'host': {"ref": "/hosts/" + associated_host_id}}
        request_command = "requests.patch(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin))"

        return render_template('fc_pwwn_host_modify.html', pwwn=pwwn, pwwn_get_request=pwwn_get_request, pwwn_json_example=pwwn_json_example, pwwn_id=pwwn_id, associated_host_get_request=associated_host_get_request, associated_host_json_example=associated_host_json_example, associated_host_id=associated_host_id, request_command=request_command)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
