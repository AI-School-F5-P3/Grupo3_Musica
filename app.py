from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

# Decorador para requerir inicio de sesión
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para requerir rol de administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'message': 'No tiene permiso para acceder a esta página'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Decorador para requerir rol de profesor
def profesor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'profesor':
            return jsonify({'message': 'No tiene permiso para acceder a esta página'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))
# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar las credenciales en la base de datos
        cursor.execute("SELECT rol FROM usuarios WHERE login = %s AND password = crypt(%s, password)", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            session['role'] = user[0]
            return redirect(url_for('dashboard'))
        return jsonify({'message': 'Credenciales incorrectas'}), 401
    
    return '''
        <form method="post">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    '''

# Ruta para el dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Ejemplo de datos para el dashboard
        num_alumnos = 100
        num_clases = 20
        num_profesores = 7
        return render_template('dashboard.html', num_alumnos=num_alumnos, num_clases=num_clases, num_profesores=num_profesores)
    except Exception as e:
        return jsonify({'message': 'Error al cargar el dashboard', 'error': str(e)}), 500

# Ruta para la gestión de alumnos
@app.route('/admin/alumnos')
@login_required
@admin_required
def admin_alumnos():
    try:
        cursor.execute("SELECT * FROM alumnos")
        alumnos = cursor.fetchall()
        return render_template('alumnos.html', alumnos=alumnos)
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al obtener alumnos', 'error': str(e)}), 500

# Ruta para la gestión de profesores
@app.route('/admin/profesores')
@login_required
@admin_required
def admin_profesores():
    try:
        cursor.execute("SELECT * FROM profesores")
        profesores = cursor.fetchall()
        return render_template('profesores.html', profesores=profesores)
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al obtener profesores', 'error': str(e)}), 500

# Ruta para la gestión de clases
@app.route('/admin/clases')
@login_required
@admin_required
def admin_clases():
    try:
        cursor.execute("""
            SELECT c.id, c.nombre, p.nombre, c.precio_base, n.nivel
            FROM clases c
            JOIN profesores p ON c.profesor_id = p.id
            LEFT JOIN niveles n ON c.id = n.clase_id
        """)
        clases = cursor.fetchall()
        return render_template('clases.html', clases=clases)
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al obtener clases', 'error': str(e)}), 500

# Ruta para añadir una nueva clase
@app.route('/admin/clases/nueva', methods=['GET', 'POST'])
@login_required
@admin_required
def nueva_clase():
    if request.method == 'POST':
        nombre = request.form['nombre']
        profesor_id = request.form['profesor_id']
        precio_base = request.form['precio_base']
        tipo_pack = request.form['tipo_pack']
        
        try:
            cursor.execute("""
                INSERT INTO clases (nombre, profesor_id, precio_base, tipo_pack)
                VALUES (%s, %s, %s, %s)
            """, (nombre, profesor_id, precio_base, tipo_pack))
            conn.commit()
            return redirect(url_for('admin_clases'))
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Error al añadir clase', 'error': str(e)}), 500
    
    # Obtener lista de profesores para el formulario
    cursor.execute("SELECT id, nombre FROM profesores")
    profesores = cursor.fetchall()
    return render_template('nueva_clase.html', profesores=profesores)

# Ruta para editar una clase existente
@app.route('/admin/clases/<int:clase_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_clase(clase_id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        profesor_id = request.form['profesor_id']
        precio_base = request.form['precio_base']
        tipo_pack = request.form['tipo_pack']
        
        try:
            cursor.execute("""
                UPDATE clases
                SET nombre = %s, profesor_id = %s, precio_base = %s, tipo_pack = %s
                WHERE id = %s
            """, (nombre, profesor_id, precio_base, tipo_pack, clase_id))
            conn.commit()
            return redirect(url_for('admin_clases'))
        except Exception as e:
            conn.rollback()
            return jsonify({'message': 'Error al editar clase', 'error': str(e)}), 500

    # Obtener la información de la clase y lista de profesores para el formulario
    cursor.execute("SELECT id, nombre, profesor_id, precio_base, tipo_pack FROM clases WHERE id = %s", (clase_id,))
    clase = cursor.fetchone()
    
    cursor.execute("SELECT id, nombre FROM profesores")
    profesores = cursor.fetchall()
    
    return render_template('editar_clase.html', clase=clase, profesores=profesores)

# Ruta para eliminar una clase existente
@app.route('/admin/clases/<int:clase_id>/eliminar', methods=['POST'])
@login_required
@admin_required
def eliminar_clase(clase_id):
    try:
        cursor.execute("DELETE FROM clases WHERE id = %s", (clase_id,))
        conn.commit()
        return redirect(url_for('admin_clases'))
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al eliminar clase', 'error': str(e)}), 500

# Ruta para la gestión de inscripciones
@app.route('/admin/inscripciones')
@login_required
@admin_required
def admin_inscripciones():
    try:
        cursor.execute("""
            SELECT i.id, a.nombre || ' ' || a.apellidos AS alumno, c.nombre AS clase, n.nivel
            FROM alumnos_clases i
            JOIN alumnos a ON i.alumno_id = a.id
            JOIN clases c ON i.clase_id = c.id
            LEFT JOIN niveles n ON i.nivel_id = n.id
        """)
        inscripciones = cursor.fetchall()
        return render_template('inscripciones.html', inscripciones=inscripciones)
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al obtener inscripciones', 'error': str(e)}), 500

# Ruta para la gestión de descuentos
@app.route('/admin/descuentos')
@login_required
@admin_required
def admin_descuentos():
    try:
        cursor.execute("SELECT * FROM precios")
        descuentos = cursor.fetchall()
        return render_template('descuentos.html', descuentos=descuentos)
    except Exception as e:
        conn.rollback()
        return jsonify({'message': 'Error al obtener descuentos', 'error': str(e)}), 500

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
