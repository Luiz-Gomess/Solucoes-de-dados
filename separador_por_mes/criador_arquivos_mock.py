import pandas as pd

df = pd.DataFrame(
    {
        "a" : [i for i in range(30)],
        "b" : [i for i in range(30)],
        "c" : [i for i in range(30)],
    }
)

for mes in range(1,13):
    for dia in range(1,31):
        df.to_excel(f"contas_altas/Contas Altas {dia}.{mes}.2024.xlsx")
        
    