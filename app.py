from flask import Flask, render_template, session, request, redirect, Response
import numpy as np
import sys
import json
sys.path.append('/home/lera/Downloads/flask_app/optimalsolutiontokenalgorithm1.py')
from optimalsolutiontokenalgorithm1 import Discrete


app = Flask(__name__)
app.secret_key = 'super secret key'



@app.route('/login', methods=['GET', 'POST'])
def hello_world():
    render_template('login.html')
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '5f4d44dfaa1b1ed72a8a3e963500a05d0f55829ac42af044e33f39c9f6f71a3a':
            session['admin'] = request.form['username']
            return render_template('index.html')
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)



@app.route('/', methods=['GET', 'POST'])
def form_example():
    if 'admin' not in session:
        return redirect('http://127.0.0.1:5000/login')
        
        
        
    else:
        return render_template('index.html')


@app.route('/tokeninfo', methods=['GET', 'POST'])
def form_example1():
    if 'admin' not in session:
        return redirect('http://127.0.0.1:5000/login')
        
        
        
    else:
        return render_template('tokeninfo.html')


@app.route('/getjs', methods=['GET','POST'])
def get_js():
    if request.method == 'POST':
        js_variable = request.get_json(force=True)
        f = open('text.txt', 'w')
        parsed_json=js_variable['vektor_a']
        A = np.array(parsed_json)
        #A = np.array([3,4,3,5,8,2])
        N = len(A)
        k = 3
        my_res_1 = Discrete(A, N, k)
        res_1, my_B= my_res_1.preprocess()
        #f.write(f'a_star is {res_1}\nB is {my_B}')
        res_distri = my_res_1.distribution(res_1, my_B)
        res_distri = res_distri.tolist()
        return Response(json.dumps(res_distri), mimetype='application/json')


