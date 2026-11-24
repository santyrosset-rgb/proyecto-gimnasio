from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector
import os

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
                <h2>Bienvenido a El Nacho</h2>
                <p>El Nacho es un gimnasio ubicado en el centro de Alta Gracia, Córdoba, Argentina. Abrimos con la idea de que cualquier persona pueda entrenar cómoda, sin importar su edad o su nivel, y con profesores que la acompañen en cada clase.</p>
                <p><strong>Ubicación:</strong> Alta Gracia, Córdoba, Argentina (zona centro).</p>
                <p><strong>Horarios:</strong> lunes a viernes de 7:00 a 22:00 y sábados de 9:00 a 14:00.</p>
                <p><strong>Instalaciones:</strong> el salón tiene más de 600 m² y cuenta con 60 máquinas en total: 12 cintas de correr, 10 máquinas de dorsales, 10 máquinas de press de pecho, 8 de jalón al pecho, 8 bancos de press plano, 4 multifuerzas con poleas, 4 prensas de piernas y 4 racks funcionales. Además hay una zona de pesas libres con mancuernas de 2 a 50 kg, una zona de funcional con colchonetas y un sector de estiramiento.</p>
                <p><strong>Profesores:</strong> nuestro equipo está formado por profesores especializados en musculación, funcional, crossfit y entrenamiento aeróbico. Podés ver quiénes son en la sección Profesores.</p>
                <p><strong>Planes:</strong> tenemos plan mensual, trimestral y anual, para que cada alumno elija el que más le conviene.</p>
                <p><strong>Servicios:</strong> vestuarios con duchas, bebederos, lockers y wifi para los socios.</p>
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

        elif self.path.startswith('/fotos/'):
            nombre = self.path.split('/')[-1]
            with open("fotos/" + nombre, "rb") as archivo:
                imagen = archivo.read()
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(imagen)

        elif self.path.startswith('/maquinaria/'):
            nombre = self.path.split('/')[-1]
            with open("maquinaria/" + nombre, "rb") as archivo:
                imagen = archivo.read()
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(imagen)

        elif self.path == '/maquinaria':
            maquinas = [
                ("maquina1.jpg", "Multifuerza con poleas", "Estructura con barra guiada, poleas altas y bajas y soportes para discos. Sirve para hacer sentadillas, press y ejercicios con poleas en un mismo lugar."),
                ("maquina2.jpg", "Prensa de piernas", "Máquina inclinada con discos donde se empuja una plataforma con las piernas. Trabaja cuádriceps y glúteos."),
                ("maquina3.jpg", "Rack funcional", "Rack con dos poleas regulables, barra para dominadas y soportes para discos. Se usa para entrenamiento funcional y ejercicios con barra."),
                ("maquina4.jpg", "Banco de press plano", "Banco con soportes para la barra olímpica. Se usa para hacer press de pecho."),
                ("maquina5.jpg", "Jalón al pecho", "Máquina con asiento y apoyo para las piernas, donde se tira de una barra hacia abajo. Trabaja la espalda y los brazos."),
                ("maquina6.jpg", "Cinta de correr", "Cinta con pantalla para elegir velocidad e inclinación. Se usa para caminar, trotar y correr."),
                ("maquina7.jpg", "Máquina de dorsales", "Máquina con selector de peso donde se tira de las manijas hacia abajo. Trabaja la espalda."),
                ("maquina8.jpg", "Press de pecho", "Máquina sentada con selector de peso. Se empujan las manijas hacia adelante para trabajar pecho, hombros y tríceps."),
            ]

            contenido = "<div class='card'>"
            contenido += "<h2>Maquinaria</h2>"
            for foto, nombre, descripcion in maquinas:
                contenido += f"""<div style="margin: 16px 0;">
                    <img src='/maquinaria/{foto}' width='200'><br>
                    <strong>{nombre}</strong><br>
                    {descripcion}
                </div>"""
            contenido += "</div>"

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
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Veces por semana</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Dni</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Plan</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Eliminar</th>"
            contenido += "<th style='border: 1px solid #333; padding: 8px; text-align: left;'>Modificar</th>"
            contenido += "</tr></thead>"
            contenido += "<tbody>"
            for nombre, apellido, telefono, veces, dni, id_plan in resultados:
                plan = "Anual"
                if str(id_plan) == "1":
                    plan = "Mensual"
                elif str(id_plan) == "2":
                    plan = "Trimestral"
                contenido += "<tr>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{nombre}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{apellido}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{telefono}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{veces}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{dni}</td>"
                contenido += f"<td style='border: 1px solid #333; padding: 8px;'>{plan}</td>"

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
                foto = ""
                if os.path.exists(f"fotos/profe_{id_profesor}.jpg"):
                    foto = f"<img src='/fotos/profe_{id_profesor}.jpg' width='80'>"
                contenido += f"""<div style="margin: 16px 0;">
                    {foto}
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
                    <p>Veces por semana:<br>
                        <select name="veces">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                        </select>
                    </p>
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
                <form method="POST" action="/guardar_profe" enctype="multipart/form-data">
                    <p>Nombre:<br><input type="text" name="nombre" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" required></p>
                    <p>Especialidad:<br><input type="text" name="especialidad" required></p>
                    <p>Foto:<br><input type="file" name="foto" accept="image/*"></p>
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

            nombre, apellido, telefono, veces, id_plan = alumno

            contenido = f"""
            <div class="card">
                <h2>Modificar Alumno</h2>
                <form method="POST" action="/guardar_modificacion">
                    <input type="hidden" name="dni" value="{dni}">
                    <p>Nombre:<br><input type="text" name="nombre" value="{nombre}" required></p>
                    <p>Apellido:<br><input type="text" name="apellido" value="{apellido}" required></p>
                    <p>Telefono:<br><input type="text" name="telefono" value="{telefono}" required></p>
                    <p>Veces por semana:<br>
                        <select name="veces">
                            <option value="1" {"selected" if str(veces) == "1" else ""}>1</option>
                            <option value="2" {"selected" if str(veces) == "2" else ""}>2</option>
                            <option value="3" {"selected" if str(veces) == "3" else ""}>3</option>
                            <option value="4" {"selected" if str(veces) == "4" else ""}>4</option>
                            <option value="5" {"selected" if str(veces) == "5" else ""}>5</option>
                            <option value="6" {"selected" if str(veces) == "6" else ""}>6</option>
                        </select>
                    </p>
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
            veces    = campos.get('veces', [''])[0]
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
                    (dni, id_plan, nombre, apellido, telefono, veces)
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
            datos = self.rfile.read(longitud)

            limite = self.headers['Content-Type'].split('boundary=')[1].encode()
            partes = datos.split(b'--' + limite)

            nombre_profe = ''
            apellido_profe = ''
            especialidad = ''
            foto = b''

            for parte in partes:
                if b'name="foto"' in parte:
                    foto = parte.split(b'\r\n\r\n', 1)[1][:-2]
                elif b'name="nombre"' in parte:
                    nombre_profe = parte.split(b'\r\n\r\n', 1)[1].strip().decode('utf-8')
                elif b'name="apellido"' in parte:
                    apellido_profe = parte.split(b'\r\n\r\n', 1)[1].strip().decode('utf-8')
                elif b'name="especialidad"' in parte:
                    especialidad = parte.split(b'\r\n\r\n', 1)[1].strip().decode('utf-8')

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
                id_nuevo = cursor.lastrowid
                conexion.commit()
                cursor.close()
                conexion.close()
            except Exception as e:
                self.send_error(500, f"Error al guardar: {e}")
                return

            if foto != b'':
                os.makedirs("fotos", exist_ok=True)
                with open(f"fotos/profe_{id_nuevo}.jpg", "wb") as archivo:
                    archivo.write(foto)

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
            veces    = campos.get('veces', [''])[0]
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
                    (nombre, apellido, telefono, veces, id_plan, dni)
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

            if os.path.exists(f"fotos/profe_{id_profesor}.jpg"):
                os.remove(f"fotos/profe_{id_profesor}.jpg")

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