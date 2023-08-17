from flask import Flask, render_template, request, jsonify
import json
from functions_au import all_prop_list, reconstruct_prop_dict, get_attribute_id, write_dict_to_csv, write_dict_recursive

app = Flask(__name__)

prop_dict = {'key': 'value'}
all_properties = []
selected_properties = []


@app.route('/')
def index():
    # print('prop_dict:', prop_dict)
    return render_template('index.html', prop_dict=json.dumps(prop_dict), all_properties=all_properties, selected_properties=selected_properties)

@app.route('/upload', methods=['POST'])
def upload():
    global prop_dict
    file = request.files['file']
    file_contents = file.read().decode('utf-8')
    prop_dict = json.loads(file_contents)
    return jsonify({'filename': file.filename})

@app.route('/all_props', methods=['GET', 'POST'])
def all_props():
    global prop_dict, all_properties, selected_properties
    if request.method == 'POST':
        selected_properties = request.json['selected_properties']
        return jsonify({'message': 'Selected properties stored successfully'})
    else:
        props = all_prop_list(prop_dict)
        all_properties += props
        return jsonify({'all_props': all_properties, 'selected_properties': selected_properties})


@app.route('/update_properties', methods=['POST'])
def update_properties():
    global selected_properties
    selected_properties = request.json['selected_properties']
    # add this line to check the value of selected_properties
    print(selected_properties)
    return jsonify({'message': 'Selected properties updated successfully' + str(selected_properties)})

@app.route('/reconstruct', methods=['POST'])
def reconstruct():
    global prop_dict, selected_properties
    reconstructed_dict = reconstruct_prop_dict(prop_dict, selected_properties)
    return render_template('result.html', reconstructed_dict=reconstructed_dict, prop_dict=prop_dict)

@app.route('/write_csv', methods=['POST'])
def write_csv():
    global prop_dict, selected_properties
    filename = "reconstructed.csv"
    write_dict_to_csv(prop_dict, filename, headers=selected_properties)
    return jsonify({'message': 'CSV file written successfully'})

if __name__ == '__main__':
    app.run(debug=True)