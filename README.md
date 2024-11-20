Proyecto: Gestión de Encuestas de Consumo de Alcohol
Este proyecto permite la gestión de encuestas sobre el consumo de alcohol, incluyendo la adición, actualización, eliminación y filtrado de encuestas. Además, ofrece la posibilidad de exportar los datos a un archivo Excel y generar gráficos de los resultados. Está desarrollado en Python utilizando la biblioteca tkinter para la interfaz gráfica y matplotlib para la creación de gráficos.

Requisitos
Antes de comenzar, asegúrate de tener instalado lo siguiente:

Python 3.x (se recomienda la versión 3.6 o superior).
Bibliotecas de Python:
tkinter (para la interfaz gráfica)
matplotlib (para gráficos)
pandas (para la exportación a Excel)
pymysql (para la conexión a la base de datos)
Para instalar las bibliotecas necesarias, ejecuta el siguiente comando en tu terminal o línea de comandos:

bash
Copiar código
pip install matplotlib pandas pymysql openpyxl
Base de datos MySQL: El proyecto utiliza una base de datos MySQL para almacenar las encuestas. Asegúrate de tener una base de datos MySQL configurada.

Puedes crear una base de datos llamada encuestas y una tabla llamada encuesta con la siguiente estructura SQL:

sql
Copiar código
CREATE DATABASE encuestas;

USE encuestas;

CREATE TABLE encuesta (
    idEncuesta INT AUTO_INCREMENT PRIMARY KEY,
    Edad INT,
    Sexo VARCHAR(10),
    BebidasSemana INT,
    CervezasSemana INT,
    BebidasFinSemana INT,
    BebidasDestiladasSemana INT,
    VinosSemana INT,
    PerdidasControl INT,
    DiversionDependenciaAlcohol INT,
    ProblemasDigestivos INT,
    TensionAlta INT,
    DolorCabeza INT
);
Configuración
Base de datos MySQL:

Modifica las credenciales de la base de datos en el archivo database.py si tu configuración es diferente a la predeterminada:

python
Copiar código
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",  # Cambia esto
        password="curso",  # Cambia esto
        database="encuestas",  # Cambia esto
        cursorclass=pymysql.cursors.DictCursor
    )
Archivos requeridos: Asegúrate de que los siguientes archivos estén en el mismo directorio:

main.py: Contiene el código principal de la interfaz gráfica.
database.py: Contiene las funciones de acceso a la base de datos.
export.py: Contiene las funciones para exportar a Excel.
graphs.py: Contiene las funciones para generar gráficos.
Ejecución
Para ejecutar el proyecto, sigue estos pasos:

Asegúrate de tener la base de datos y la tabla configuradas correctamente.

Modifica las credenciales de la base de datos en database.py si es necesario.

Ejecuta el archivo main.py desde la terminal o desde tu IDE preferido:

bash
Copiar código
python main.py
Características
Agregar Encuesta: Permite ingresar los datos de una nueva encuesta, como edad, sexo y consumo de alcohol.
Filtrar Encuestas: Permite filtrar las encuestas por cualquier campo (como "Edad" o "Sexo") y mostrar solo las encuestas que coinciden con el valor proporcionado.
Actualizar Encuesta: Permite actualizar los datos de una encuesta ya existente.
Eliminar Encuesta: Permite eliminar una encuesta seleccionada.
Mostrar Gráfico: Genera gráficos de barras o líneas basados en los datos de las encuestas.
Exportar a Excel: Permite exportar las encuestas filtradas a un archivo Excel.
Archivos
main.py
Este archivo contiene la interfaz gráfica de usuario utilizando tkinter y las funcionalidades para agregar, eliminar, actualizar y filtrar encuestas.

database.py
Contiene las funciones necesarias para interactuar con la base de datos, como insertar, actualizar, eliminar y obtener encuestas.

export.py
Contiene la función para exportar los datos de las encuestas a un archivo Excel.

graphs.py
Contiene las funciones para generar gráficos de las encuestas, en particular gráficos de barras.

Notas
El proyecto utiliza MySQL para almacenar los datos. Asegúrate de tener una base de datos configurada y de que el servidor MySQL esté en funcionamiento.
La interfaz gráfica permite realizar todas las operaciones de manera intuitiva.
Se utiliza matplotlib para la creación de gráficos de barras y líneas basados en los datos de las encuestas.
Contribuciones
Si deseas contribuir al proyecto, puedes seguir estos pasos:

Haz un fork del repositorio.
Crea una nueva rama para realizar tus cambios.
Realiza los cambios necesarios y prueba que todo funcione correctamente.
Abre un pull request para que los cambios sean revisados y fusionados al proyecto principal.
Licencia
Este proyecto está bajo la licencia MIT. Puedes ver más detalles en el archivo LICENSE (si aplica).
