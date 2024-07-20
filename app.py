import itertools
from flask import Flask, render_template, request, jsonify
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules,fpgrowth
import os
import util.finding_best_recommendation
from util.visualize_graph.visualize_graph import visualize_graph,visualize_graph_2,visualize_graph_3
from util.finding_best_recommendation.finding_best_recommendation import find_best_recommendation_item
from util.execute_transaction.execute_transaction import get_all_unique_item_from_transaction

import util as util

from flask import session

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
import logging
logging.basicConfig(level=logging.DEBUG)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



@app.route('/')
def index_view():
    return render_template('landing_page/index.html')

@app.route('/visualize_graph_1')
def visualize_graph_1_view():
    return render_template('visualize_graph_1/index.html', active_page='visualize_graph_1')

@app.route('/visualize_graph_2')
def visualize_graph_2_view():
    return render_template('visualize_graph_2/index.html', active_page='visualize_graph_2')

@app.route('/finding_best_recommendation')
def recommendation_page_view():
    return render_template('recommendation_page/index.html', active_page='recommendation_page')

@app.route('/get_unique_items')
def get_unique_items_view():
    return render_template('get_unique_items/index.html', active_page='get_unique_items')

@app.route('/visualize_graph_1', methods=['POST'])
def visualize_graph_1_render():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    K = int(request.form['k'])
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file.filename.endswith('.csv'):
        tempdir = os.path.join(os.path.dirname(__file__), 'temp')
        file_path = os.path.join(tempdir, file.filename)
        file.save(file_path)
        graph_data=visualize_graph(file_path,K)
        return jsonify(graph_data)
    return jsonify({'error': 'Invalid file format'})
@app.route('/visualize_graph_2', methods=['POST'])
def visualize_graph_2_render():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    K = int(request.form['k'])
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file.filename.endswith('.csv'):
        tempdir = os.path.join(os.path.dirname(__file__), 'temp')
        file_path = os.path.join(tempdir, file.filename)
        file.save(file_path)
        graph_data=visualize_graph_2(file_path,K)
    
        return jsonify(graph_data)
    return jsonify({'error': 'Invalid file format'})
@app.route('/visualize_graph_3', methods=['POST'])
def visualize_graph_3_render():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    num_of_item = int(request.form['k'])
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file.filename.endswith('.csv'):
        tempdir = os.path.join(os.path.dirname(__file__), 'temp')
        file_path = os.path.join(tempdir, file.filename)
        file.save(file_path)
        graph_data=visualize_graph_3(file_path,num_of_item)
        return jsonify(graph_data)
    return jsonify({'error': 'Invalid file format'})
@app.route('/finding_best_recommendation', methods=['POST'])
def finding_best_recommendation_render():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    num_of_item = int(request.form['num_of_item'])
    item=str(request.form["item"]).split(",")
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file.filename.endswith('.csv'):
        tempdir = os.path.join(os.path.dirname(__file__), 'temp')
        file_path = os.path.join(tempdir, file.filename)
        file.save(file_path)
        best_rule=find_best_recommendation_item(item,file_path,num_of_item,0.3)
        return jsonify(best_rule)
    return jsonify({'error': 'Invalid file format'})
@app.route('/get_unique_items_from_files', methods=['POST'])
def get_unique_items_from_files():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file.filename.endswith('.csv'):
        tempdir = os.path.join(os.path.dirname(__file__), 'temp')
        file_path = os.path.join(tempdir, file.filename)
        file.save(file_path)
        unique_items=list(get_all_unique_item_from_transaction(file_path))
        return jsonify(unique_items)
    return jsonify({'error': 'Invalid file format'})
if __name__ == '__main__':
    app.run(debug=True)

