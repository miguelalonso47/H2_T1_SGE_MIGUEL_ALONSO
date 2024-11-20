import pymysql

# Configura los datos de conexión a la base de datos
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",  # Cambia esto
        password="curso",  # Cambia esto
        database="encuestas",  # Cambia esto
        cursorclass=pymysql.cursors.DictCursor
    )

def execute_query(query, params=()):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()  # Confirmar que los cambios se guardan
            print(f"Consulta ejecutada correctamente: {query}")
    except Exception as e:
        print(f"Error en la consulta: {e}")
    finally:
        connection.close()



def insert_encuesta(data):
    # Primero obtenemos el último idEncuesta de la base de datos
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(idEncuesta) FROM encuesta")
            last_id = cursor.fetchone()['MAX(idEncuesta)']
            next_id = last_id + 1 if last_id else 1  # Si no hay registros, el siguiente ID será 1

            # Insertamos el nuevo registro con el idEncuesta generado
            query = """
                INSERT INTO encuesta (idEncuesta, Edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
                                       BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol,
                                       ProblemasDigestivos, TensionAlta, DolorCabeza)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data.insert(0, next_id)  # Agregamos el nuevo idEncuesta al principio de la lista de datos
            cursor.execute(query, data)
            connection.commit()
    finally:
        connection.close()



def get_encuestas():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM encuesta")
            return cursor.fetchall()
    finally:
        connection.close()

def update_encuesta(data, id_encuesta):
    query = """
        UPDATE encuesta
        SET Edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s, 
            BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, 
            DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s
        WHERE idEncuesta=%s
    """
    data.append(id_encuesta)

    # Imprimir la consulta SQL y los parámetros para verificar
    print("Consulta SQL:", query)
    print("Datos para actualizar:", data)

    execute_query(query, data)




def delete_encuesta(id_encuesta):
    query = "DELETE FROM encuesta WHERE idEncuesta = %s"
    execute_query(query, (id_encuesta,))

def get_encuestas_filtradas(campo, valor):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # Usamos una consulta SQL dinámica para filtrar por el campo y valor proporcionados
            query = f"SELECT * FROM encuesta WHERE {campo} = %s"
            cursor.execute(query, (valor,))
            return cursor.fetchall()
    finally:
        connection.close()




