from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector

class MiServidor(BaseHTTPRequestHandler):
    def plantilla(self, contenido):
        with open("plantilla.html", "r", encoding="utf-8") as archivo:
            html = archivo.read()
        html = html.replace("{contenido}", contenido)
        return html

    def do_GET(self):
        if self.path == '/':
            contenido = """
            <div class="card">
                <h2>Inicio</h2>
                <p>Bienvenido a la escuela</p>
            </div>
            """
            html = self.plantilla(contenido)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/clientes':
            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre, apellido, telefono, email, dni    ion FROM clientes")
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
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{telelfono}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{email}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{dni}</td>"

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
                cursor.execute("SELECT ID_profesor, nombre, apellido, mail, teléfono FROM PROFESORES")
                resultados = cursor.fetchall()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            contenido = "<div class='card'>"
            contenido += "<h2>Lista de profesores</h2>"
            for id_prof, nombre, apellido, mail, telefono in resultados:
                contenido += f"<p><strong>{nombre} {apellido}</strong> — Mail: {mail} | Tel: {telefono}</p>"
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
                <form method="POST" action="/guardar_alumno">
                    <p>Nombre:<br><input type="text" name="nombre" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" required></p>
                    <p>Division:<br>
                        A: <input type="radio" name="division" value="A" required><br>
                        B: <input type="radio" name="division" value="B"><br>
                        C: <input type="radio" name="division" value="C">
                    </p>
                    <p>Curso
                        <select name="curso">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                        </select>
                        DNI:<br><input type="number" name="dni" required>
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
                    <p>Mail<br><input type="email" name="mail" required></p>
                    <p>Telefono:<br><input type="text" name="telefono" required></p>
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
                cursor.execute("SELECT nombre, apellido,telefono , division, email, dni FROM clientes WHERE DNI = %s", (dni,))
                alumno = cursor.fetchone()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error: {e}")
                return

            if alumno is None:
                self.send_error(404, "Alumno no encontrado")
                return

            nombre, apellido, curso, division = alumno

            opciones_curso = ""
            for c in range(1, 8):
                seleccionado = "selected" if str(curso) == str(c) else ""
                opciones_curso += f'<option value="{c}" {seleccionado}>{c}</option>'

            contenido = f"""
            <div class="card">
                <h2>Modificar Alumno</h2>
                <form method="POST" action="/guardar_modificacion">
                    <input type="hidden" name="dni" value="{dni}">
                    <p>Nombre:<br><input type="text" name="nombre" value="{nombre}" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" value="{apellido}" required></p>
                    <p>Division:<br>
                        A: <input type="radio" name="division" value="A" {"checked" if division == "A" else ""} required><br>
                        B: <input type="radio" name="division" value="B" {"checked" if division == "B" else ""}><br>
                        C: <input type="radio" name="division" value="C" {"checked" if division == "C" else ""}>
                    </p>
                    <p>Curso
                        <select name="curso">
                            {opciones_curso}
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


    def do_POST(self):
        if self.path == '/guardar_alumno':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            nombre   = campos.get('nombre', [''])[0]
            apellido = campos.get('apellido', [''])[0]
            curso    = campos.get('curso', [''])[0]
            division = campos.get('division', [''])[0]
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
                    "INSERT INTO alumnos (NOMBRE, APELLIDO, curso, division, DNI) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, apellido, curso, division, dni)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al guardar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/alumnos')
            self.end_headers()

        elif self.path == '/guardar_profe':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            nombre   = campos.get('nombre', [''])[0]
            apellido = campos.get('apellido', [''])[0]
            mail     = campos.get('mail', [''])[0]
            telefono = campos.get('telefono', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO profesores (nombre, apellido, mail, teléfono) VALUES (%s, %s, %s, %s)",
                    (nombre, apellido, mail, telefono)
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

        elif self.path == '/guardar_materia':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            nombre      = campos.get('nombre', [''])[0]
            grado       = campos.get('grado', [''])[0]
            seccion     = campos.get('seccion', [''])[0]
            id_profesor = campos.get('id_profesor', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO materias (nombre, grado, seccion, id_profesor) VALUES (%s, %s, %s, %s)",
                    (nombre, grado, seccion, id_profesor)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al guardar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/materias')
            self.end_headers()

        elif self.path == '/eliminar_alumno':
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
                cursor.execute("DELETE FROM alumnos WHERE DNI = %s", (dni,))
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al eliminar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/alumnos')
            self.end_headers()

        elif self.path == '/guardar_modificacion':
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')

            from urllib.parse import parse_qs
            campos = parse_qs(datos)

            dni      = campos.get('dni', [''])[0]
            nombre   = campos.get('nombre', [''])[0]
            apellido = campos.get('apellido', [''])[0]
            curso    = campos.get('curso', [''])[0]
            division = campos.get('division', [''])[0]

            try:
                conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="mi_ignacio"
                )
                cursor = conexion.cursor()
                cursor.execute(
                    "UPDATE alumnos SET NOMBRE = %s, APELLIDO = %s, curso = %s, division = %s WHERE DNI = %s",
                    (nombre, apellido, curso, division, dni)
                )
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al modificar: {e}")
                return

            self.send_response(303)
            self.send_header('Location', '/alumnos')
            self.end_headers()

        else:
            self.send_error(404, "Ruta POST no encontrada")

servidor = HTTPServer(('localhost', 8000), MiServidor)
print("Servidor corriendo en http://localhost:8000")
servidor.serve_forever()