from flask import Flask, render_template, session, request, redirect, Response
import numpy as np
import sys
import json
sys.path.append('/home/lera/Downloads/flask_app/etereum-project-repo/optimalsolutiontokenalgorithm1.py')
sys.path.append('/home/lera/Downloads/flask_app/etereum-project-repo/opt2.py')
from optimalsolutiontokenalgorithm1 import Discrete
from opt2 import Continuous


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
        parsed_json=js_variable['vektor_a']
        #print('array ',parsed_json)
        A = np.array(parsed_json)
        variant =A[0] #
        A=np.delete(A, 0)

        N = len(A)
        if variant == 1:
          k = 3
          my_res_1 = Discrete(A, N, k)
          res_1, my_B= my_res_1.preprocess()
          res_distri = my_res_1.distribution(res_1, my_B)
          res_distri = res_distri.tolist() #1st algoritm result
        else:
          #A=np.delete(A, 0)
          my_var = np.var(A)
          length = len(A)
          my_min = np.min(A)
          my_max = np.max(A)
          rand1 = np.random.randint(my_min, my_max + 1, size=length)
          rand2 = np.random.randint(my_min, my_max + 1, size=length)
          cov_rand = np.cov(rand1, rand2)[0, 0]
          var_red = cov_rand/my_var
          my_res_1 = Continuous(N, A, var_red)

          res_1 = my_res_1.search()
          res_distri = my_res_1.construct_pack(res_1)
          #res_distri = my_res_1.construct_pack(res_1) - надо будет добавить
          #res_distri = res_distri.astype(int)
          res_distri = res_distri.tolist() #  2 algoritm result
          #print('res2', res_distri)
    return Response(json.dumps(res_distri), mimetype='application/json')


