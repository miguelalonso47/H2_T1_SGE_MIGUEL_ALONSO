import matplotlib.pyplot as plt
from database import get_encuestas

def mostrar_grafico_barras(encuestas):
    # Aquí puedes implementar un gráfico de barras con los datos de encuestas
    edades = [encuesta['edad'] for encuesta in encuestas]  # Cambio de 'Edad' a 'edad'
    sexo = [encuesta['Sexo'] for encuesta in encuestas]

    plt.bar(sexo, edades)
    plt.ylabel('Sexo')
    plt.xlabel('Edad')
    plt.title('Gráfico de Edades por Sexo')
    plt.show()



