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
        assumed_successful_json_response = '''
        200 OK
        {{
             "capacity_policy": null,
             "capacity_state": "ok",
             "creation_time": 1470296567.234391,
             "description": null,
             "id": 4,
             "is_dedup": false,
             “is_default”: false,
             "iscsi_tgt_converted_name": "test.anmir",
             "last_restored_from": null,
             "last_restored_time": null,
             "last_snapshot_creation_time": 1507446023,
             "logical_capacity": 0.0,
             "mapped_hosts_count": 1,
             "name": "{volume_group_name}",
             "quota": null,
             "replication_peer_volume_group": null,
             "replication_rpo_history": null,
             "replication_session": null,
             "snapshots_count": 3,
             "snapshots_logical_capacity": 0,
             "snapshots_overhead_state": "ok",
             "views_count": 0,
             "volumes_count": 8,
             "volumes_logical_capacity": 0,
             "volumes_provisioned_capacity": 21474836480
        }}
            '''.format(volume_group_name=volume_group_name)

        return render_template('create_volume_group.html', volume_group_name=volume_group_name, request_command=request_command, assumed_successful_json_response=assumed_successful_json_response)


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
        assumed_successful_json_response = '''
        200 OK
        {{
             "hits": [
                {{
                 "avg_compressed_ratio": 0,
                 "avg_compressed_ratio_timestamp": 0,
                 "creation_time": 1470316792.4950581,
                 "current_replication_stats": null,
                 "current_stats": {{
                 "ref": "/stats/volumes/11"
                 }},
                 “dedup_source”: 0,
                 “dedup_target”: 0
                 "description": null,
                 "id": 11,
                 "is_new": false,
                 “is_dedup”: true,
                 "iscsi_tgt_converted_name": "esx-srv1-vol-datastore0",
                 "last_restored_from": null,
                 "last_restored_time": null,
                 "logical_capacity": 0.0,
                 "marked_for_deletion": false,
                 "name": "{volume_name}",
                 "no_dedup": 0,
                 "node_id": 8,
                 "replication_peer_volume": null,
                 "scsi_sn": "d5030007",
                 "scsi_suffix": 7,
                 "size": {volume_size_kb},
                 "snapshots_logical_capacity": 0,
                 "stream_avg_compressed_size_in_bytes": 763
                 "vmware_support": true,
                 "volume_group": {{
                 "ref": "/volume_groups/10"
                 }}
                 }}
             }}
        '''.format(volume_name=volume_name, volume_size_kb=volume_size_kb)

        return render_template('create_volume.html', volume_name=volume_name, volume_size_gb=volume_size_gb, volume_group=volume_group, request_command=request_command, assumed_successful_json_response=assumed_successful_json_response)


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
        assumed_successful_json_response = '''
        200 OK
        {{
            "hits": [
                {{
                "allow_different_host_types": {allow_different_host_types_bool},
                "description": {host_group_description},
                "hosts_count": 2,
                "id": 16,
                "name": "{host_group_name}",
                "views_count": 0,
                "volumes_count": 3,
                "connectivity_type": "{connectivity_type}"
         }}               
        '''.format(host_group_name=host_group_name, host_group_description=host_group_description, allow_different_host_types_bool=allow_different_host_types_bool, connectivity_type=connectivity_type)

        return render_template('create_host_group.html', host_group_name=host_group_name, request_command=request_command, assumed_successful_json_response=assumed_successful_json_response)


@app.route('/create_host', methods=['POST'])
def create_host():
    if request.method == 'POST':
        host_name = request.form['host_name']
        host_type = request.form['host_type']
        host_group = request.form['host_group']
        api_url = "https://k2_ip/api/v2/hosts"
        payload = {'name': host_name, 'type': host_type, 'host_group': host_group}
        request_command = "requests.post(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin'))"

        return render_template('create_host.html', host_name=host_name, host_type=host_type, host_group=host_group, request_command=request_command)


@app.route('/fc_pwwn_lookup', methods=['POST'])
def fc_pwwn_lookup():
    if request.method == 'POST':
        pwwn = request.form['pwwn']
        api_url = "https://k2_ip/api/v2/host_fc_ports?pwwn=" + pwwn
        payload = {'pwwn': pwwn}
        request_command = "requests.get(" + api_url + ", auth=('admin', 'admin'))"
        assumed_successful_json_response = '''
        200 OK
        {{
            "hits": [
                {{
                    "host": "host1",
                    "id": 2,
                    "pwwn": "{pwwn}"
                }}
            ]
        }}
        '''.format(pwwn=pwwn)

        return render_template('fc_pwwn_lookup.html', pwwn=pwwn, request_command=request_command, assumed_successful_json_response=assumed_successful_json_response)


@app.route('/fc_pwwn_host_modify', methods=['POST'])
def fc_pwwn_host_modify():
    if request.method == 'POST':
        pwwn = request.form['pwwn']
        pwwn_get_request = "request.get(https://k2_ip/api/v2/host_fc_ports?pwwn=" + pwwn + ", auth=('admin', 'admin'))"
        pwwn_assumed_json_response = '''
        {{
            "hits": [
                {{
                    "host": "host1",
                    "id": 2,
                    "pwwn": "{pwwn}"
                }}
            ]
        }}
        '''.format(pwwn=pwwn)
        pwwn_data = json.loads(pwwn_assumed_json_response)
        pwwn_id = str(pwwn_data['hits'][0]['id'])
        associated_host = request.form['associated_host']
        associated_host_get_request = "request.get(https://k2_ip/api/v2/hosts?name=" + associated_host + ", auth=('admin', 'admin'))"
        associated_host_assumed_json_response = '''
        200 OK
        {{
            "host_group": {{
                "ref": "/host_groups/16"
            }},
                "id": 7,
                "is_part_of_group": true,
                "name": "{associated_host}",
                "type": "Windows",
                "views_count": 0,
                "volumes_count": 10
        }}
        '''.format(associated_host=associated_host)
        associated_host_data = json.loads(associated_host_assumed_json_response)
        associated_host_id = str(associated_host_data['id'])
        api_url = "https://k2_ip/api/v2/host_fc_ports/" + pwwn_id
        payload = {'host': {"ref": "/hosts/" + associated_host_id}}
        request_command = "requests.patch(" + api_url + ", json=" + str(payload) + ", auth=('admin', 'admin'))"
        assumed_successful_json_response = '''
        200 OK
        {{
            "hits": [
                {{
                    "host": "{associated_host}",
                    "id": 2,
                    "pwwn": "{pwwn}"
                }}
            ]
        }}
        '''.format(pwwn=pwwn, associated_host=associated_host)

        return render_template('fc_pwwn_host_modify.html', pwwn=pwwn, pwwn_get_request=pwwn_get_request, pwwn_assumed_json_response=pwwn_assumed_json_response, pwwn_id=pwwn_id, associated_host=associated_host, associated_host_get_request=associated_host_get_request, associated_host_assumed_json_response=associated_host_assumed_json_response, associated_host_id=associated_host_id, request_command=request_command, assumed_successful_json_response=assumed_successful_json_response)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
