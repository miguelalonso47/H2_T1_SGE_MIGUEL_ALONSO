import pandas as pd
from database import get_encuestas

def export_to_excel(encuestas):
    df = pd.DataFrame(encuestas)
    df.to_excel("encuestas.xlsx", index=False)

