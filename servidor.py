from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector

class MiServidor(BaseHTTPRequestHandler):
    def plantilla(self, contenido):
        with open("plantilla.html", "r", encoding="utf-8") as archivo:
            html = archivo.read()
        fondo = """
        <style>
            body {
                background-image: url('/fotogimnasio.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                min-height: 100vh;
            }
        </style>
        """
        html = html.replace("{contenido}", fondo + contenido)
        return html

    def do_GET(self):
        if self.path == '/':
            contenido = """
            <div class="card">
                <h2>Inicio</h2>
                <p>Bienvenido al gimnasio</p>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/fotogimnasio.jpg':
            with open("fotogimnasio.jpg", "rb") as archivo:
                imagen = archivo.read()
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(imagen)

        elif self.path == '/clientes':
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre, apellido, telefono, email, dni, id_plan FROM clientes")
                resultados = cursor.fetchall()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            contenido = "<div class='card'>"
            contenido += "<h2>Lista de alumnos</h2>"
            contenido += "<table class='tabla-clientes' style='border-collapse: collapse; width: 100%;'>"
            contenido += "<thead><tr>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Nombre</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Apellido</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Teléfono</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Email</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Dni</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Plan</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Eliminar</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Modificar</th>"
            contenido += "</tr></thead>"
            contenido += "<tbody>"
            for nombre, apellido, telefono, email, dni, id_plan in resultados:
                contenido += "<tr>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{nombre}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{apellido}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{telefono}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{email}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{dni}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{id_plan}</td>"

                contenido += f"""<td style='border: 1px solid #333; padding: 8px;'>
                    <form method="POST" action="/eliminar_cliente" style="margin:0;">
                        <input type="hidden" name="dni" value="{dni}">
                        <button type="submit">Eliminar</button>
                    </form>
                </td>"""
                contenido += f"""<td style='border: 1px solid #333; padding: 8px;'>
                    <a href="/modificar_cliente?dni={dni}">Modificar</a>
                </td>"""
                contenido += "</tr>"
            contenido += "</tbody></table>"
            contenido += "</div>"
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/profesores':
          
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT id_profesor, nombre_profe, apellido_profe, especialidad FROM profesores")
                resultados = cursor.fetchall()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            contenido = "<div class='card'>"
            contenido += "<h2>Lista de profesores</h2>"
            for id_profesor, nombre_profe, apellido_profe,especialidad in resultados:
                contenido += f"""<div style="margin: 16px 0;">
                    <strong>{nombre_profe} {apellido_profe}</strong> — id_profesor: {id_profesor} | Especialidad: {especialidad}
                    <a href="/modificar_profesor?id={id_profesor}">Modificar</a>
                    <form method="POST" action="/eliminar_profesor" style="display:inline; margin:0;">
                        <input type="hidden" name="id_profesor" value="{id_profesor}">
                        <button type="submit">Eliminar</button>
                    </form>
                </div>"""
            contenido += "</div>"
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

    

        elif self.path == '/registroclientes':
            contenido = """
            <div class="card">
                <h2>Registrar Alumno</h2>
                <form method="POST" action="/guardar_cliente">
                    <p>Nombre:<br><input type="text" name="nombre" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" required></p>
                    <p>Telefono:<br><input type="text" name="telefono" required></p>
                    <p>Email:<br><input type="email" name="email" required></p>
                    <p>DNI:<br><input type="number" name="dni" required></p>
                    <p>Plan:<br>
                        <select name="id_plan">
                            <option value="1">Mensual</option>
                            <option value="2">Trimestral</option>
                            <option value="3">Anual</option>
                        </select>
                    </p>
                    <p><button type="submit">Guardar</button></p>
                </form>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/registroprofe':
            contenido = """
            <div class="card">
                <h2>Registrar Profesor</h2>
                <form method="POST" action="/guardar_profe">
                    <p>Nombre:<br><input type="text" name="nombre" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" required></p>
                    <p>Especialidad:<br><input type="text" name="especialidad" required></p>
                    <p><button type="submit">Guardar</button></p>
                </form>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

       

        elif self.path.startswith('/modificar_cliente'):
            from urllib.parse import urlparse, parse_qs
            parametros = parse_qs(urlparse(self.path).query)
            dni = parametros.get('dni', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre, apellido, telefono, email, id_plan FROM clientes WHERE dni = %s", (dni,))
                alumno = cursor.fetchone()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            if alumno is None:
                self.send_error(404, "Alumno no encontrado")
                return

            nombre, apellido, telefono, email, id_plan = alumno

            contenido = f"""
            <div class="card">
                <h2>Modificar Alumno</h2>
                <form method="POST" action="/guardar_modificacion">
                    <input type="hidden" name="dni" value="{dni}">
                    <p>Nombre:<br><input type="text" name="nombre" value="{nombre}" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" value="{apellido}" required></p>
                    <p>Telefono:<br><input type="text" name="telefono" value="{telefono}" required></p>
                    <p>Email:<br><input type="email" name="email" value="{email}" required></p>
                    <p>Plan:<br>
                        <select name="id_plan">
                            <option value="1" {"selected" if str(id_plan) == "1" else ""}>Mensual</option>
                            <option value="2" {"selected" if str(id_plan) == "2" else ""}>Trimestral</option>
                            <option value="3" {"selected" if str(id_plan) == "3" else ""}>Anual</option>
                        </select>
                    </p>
                    <p><button type="submit">Guardar cambios</button></p>
                </form>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))


        elif self.path.startswith('/modificar_profesor'):
            from urllib.parse import urlparse, parse_qs
            parametros = parse_qs(urlparse(self.path).query)
            id_profesor = parametros.get('id', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre_profe, apellido_profe, especialidad FROM profesores WHERE id_profesor = %s", (id_profesor,))
                profesor = cursor.fetchone()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            if profesor is None:
                self.send_error(404, "Profesor no encontrado")
                return

            nombre_profe, apellido_profe, especialidad = profesor

            contenido = f"""
            <div class="card">
                <h2>Modificar Profesor</h2>
                <form method="POST" action="/guardar_modificacion_profe">
                    <input type="hidden" name="id_profesor" value="{id_profesor}">
                    <p>Nombre:<br><input type="text" name="nombre" value="{nombre_profe}" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" value="{apellido_profe}" required></p>
                    <p>Especialidad:<br><input type="text" name="especialidad" value="{especialidad}" required></p>
                    <p><button type="submit">Guardar cambios</button></p>
                </form>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))


    def do_POST(self):
        if self.path == '/guardar_cliente':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            nombre   = campos.get('nombre', [''])[0]
            apellido = campos.get('apellido', [''])[0]
            telefono = campos.get('telefono', [''])[0]
            email    = campos.get('email', [''])[0]
            id_plan  = campos.get('id_plan', [''])[0]
            dni      = campos.get('dni', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO clientes (dni, id_plan, nombre, apellido, telefono, email) VALUES (%s, %s, %s, %s, %s, %s)",
                    (dni, id_plan, nombre, apellido, telefono, email)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al guardar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/clientes')
            self.end_headers()

        elif self.path == '/guardar_profe':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            nombre_profe   = campos.get('nombre', [''])[0]
            apellido_profe = campos.get('apellido', [''])[0]
            especialidad = campos.get('especialidad', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO profesores (nombre_profe, apellido_profe, especialidad) VALUES (%s, %s, %s)",
                    (nombre_profe, apellido_profe, especialidad)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al guardar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/profesores')
            self.end_headers()

        elif self.path == '/eliminar_cliente':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            dni = campos.get('dni', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al eliminar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/clientes')
            self.end_headers()

        elif self.path == '/guardar_modificacion':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            dni      = campos.get('dni', [''])[0]
            nombre   = campos.get('nombre', [''])[0]
            apellido = campos.get('apellido', [''])[0]
            telefono = campos.get('telefono', [''])[0]
            email    = campos.get('email', [''])[0]
            id_plan  = campos.get('id_plan', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "UPDATE clientes SET nombre = %s, apellido = %s, telefono = %s, email = %s, id_plan = %s WHERE dni = %s",
                    (nombre, apellido, telefono, email, id_plan, dni)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al modificar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/clientes')
            self.end_headers()

        elif self.path == '/eliminar_profesor':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            id_profesor = campos.get('id_profesor', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM profesores WHERE id_profesor = %s", (id_profesor,))
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al eliminar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/profesores')
            self.end_headers()

        elif self.path == '/guardar_modificacion_profe':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            id_profesor    = campos.get('id_profesor', [''])[0]
            nombre_profe   = campos.get('nombre', [''])[0]
            apellido_profe = campos.get('apellido', [''])[0]
            especialidad   = campos.get('especialidad', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "UPDATE profesores SET nombre_profe = %s, apellido_profe = %s, especialidad = %s WHERE id_profesor = %s",
                    (nombre_profe, apellido_profe, especialidad, id_profesor)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al modificar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/profesores')
            self.end_headers()

        else:
            self.send_error(404, "Ruta POST no encontrada")

servidor = HTTPServer(('localhost', 8000), MiServidor)
print("Servidor corriendo en http://localhost:8000")
servidor.serve_forever()