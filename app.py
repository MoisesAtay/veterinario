from flask import Flask, render_template,request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#mysql connetion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'allinProgram22_'
app.config['MYSQL_DB'] = 'veterinaria'

mysql = MySQL(app)

#settings
app.secret_key='codigosecreto'


@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM mascota")
    data = cur.fetchall()

    return render_template('index.html', contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method=='POST':
        nombre=request.form['nombre']
        fechaNac=request.form['fechaNac']
        raza=request.form['raza']
        nombreDueno=request.form['nombreDueno']
        dniDueno=request.form['dniDueno']        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO mascota (nombre, fechaNac, raza, nombreDueno,dniDueno) VALUES (%s, %s, %s, %s, %s)',
        (nombre, fechaNac, raza, nombreDueno, dniDueno))
        mysql.connection.commit()
        flash('Mascota agregado')

    return redirect(url_for('index'))

@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mascota WHERE id = {0}'.format(id))
    data = cur.fetchall()  #para obtener todos los datos

    return render_template('edit.html', contact=data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre=request.form['nombre']
        fechaNac=request.form['fechaNac']
        raza=request.form['raza']
        nombreDueno=request.form['nombreDueno']
        dniDueno=request.form['dniDueno'] 
    cur=mysql.connection.cursor()
    cur.execute("""
        UPDATE mascota 
        SET nombre = %s, 
            fechaNac = %s, 
            raza = %s,
            nombreDueno = %s,
            dniDueno = %s 
        WHERE id = %s
    """,(nombre, fechaNac, raza, nombreDueno, dniDueno, id))
    mysql.connection.commit()
    flash('datos de la mascota actualizado')
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM mascota WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Mascota eliminado')
    return redirect(url_for('index'))
 

if __name__=='__main__':
    app.run(port = 3000,  debug = True)
