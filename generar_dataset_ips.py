import pandas as pd
import random

paises = ['United States', 'Russia', 'China', 'Brazil', 'Germany', 'France', 'India', 'Colombia', 'Canada', 'Argentina']
isps = ['Google', 'Amazon', 'Microsoft', 'Comcast', 'AT&T', 'ChinaNet', 'Movistar', 'Claro', 'Tigo', 'Bharti Airtel']
proxies = ['Yes', 'No']

def generar_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

datos = []
for _ in range(10000):
    ip = generar_ip()
    pais = random.choice(paises)
    isp = random.choice(isps)
    rpm = random.randint(0, 100)
    proxy = random.choice(proxies)
    reputacion = round(random.uniform(0, 1), 2)
    clase = 1 if (rpm > 70 or reputacion > 0.7 or proxy == 'Yes') else 0
    datos.append([ip, pais, isp, rpm, proxy, reputacion, clase])

df = pd.DataFrame(datos, columns=['IP', 'Country', 'ISP', 'ConnectionsPerMinute', 'Proxy', 'ReputationScoreVT', 'Class'])
df.to_csv("ip_prediction_dataset_10000.csv", index=False)
print("✅ Dataset generado: ip_prediction_dataset_10000.csv")
