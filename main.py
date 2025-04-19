import network
import socket
import time
import machine
import random  # apenas para simular o nível de som

# Cria rede Wi-Fi Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='SomStick', password='12345678')
print('Aguardando conexão...')
while ap.active() == False:
    pass

print('AP ativo, IP:', ap.ifconfig()[0])

# Simulando leitura do som (pode trocar por I2S futuramente)
def ler_nivel_som():
    return random.randint(10, 100)  # simulação; troque por leitura real se possível

# Página HTML
def pagina_html(valor):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="1">
    <title>Nível de Som</title>
</head>
<body style="text-align:center; font-family:sans-serif;">
    <h1>Nível de Som</h1>
    <p style="font-size:48px;">{valor}</p>
    <p>Conecte-se à rede <b>SomStick</b> e acesse <b>192.168.4.1</b></p>
</body>
</html>"""

# Inicia servidor web
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Servidor rodando...')

while True:
    conn, addr = s.accept()
    print('Conexão de', addr)
    request = conn.recv(1024)
    valor_som = ler_nivel_som()
    response = pagina_html(valor_som)
    conn.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
    conn.sendall(response)
    conn.close()
