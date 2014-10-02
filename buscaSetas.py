import pxssh
import socket
import os
import sys

def estaAbierto(ip, puerto):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((ip, puerto))
    s.shutdown(2)
    return True
  except:
    return False

def tienePing(ip):
  respuesta = os.system("ping -c 1 " + ip + " >/dev/null")
  if respuesta == 0:
    return True
  else:
    return False

s = pxssh.pxssh()
passwd1=0
passwd2=0
hostsConPass1=[]
hostsConPass2=[]
hostsActivos=0
sshAbiertos=0
n=0
total=65025

for x in range(0,255):
  for y in range(0,255):
    n += 1
    ip = '1.2.' + str(x) + '.' + str(y)
    cuadrados = round(n/float(total) * 50)
    rayas = 50 - cuadrados
    progreso = '(' + str (n) + '/' + str(total) + ') [' + '#' * int(cuadrados) + '-' * int(rayas) + '] Analizando ' + ip
    sys.stdout.write('%s\r' % progreso)
    if tienePing(ip):
      hostsActivos += 1
      if estaAbierto(ip,22):
        sshAbiertos += 1
        try:
          if s.login(ip, 'usuario', 'passwd1'):
            passwd1 += 1
            hostsConPass1.append(ip)
            s.logout()
          elif s.login(ip, 'usuario', 'passwd2'):
            passwd2 += 1
            hostsConPass2.append(ip)
            s.logout()
        except:
          continue

print str(n) + ' hosts analizados. ' + str(hostsActivos) + ' hosts activos. ' + str(sshAbiertos) + ' servicios ssh identificados.'
print str(passwd1) + ' SSH con usuario/passwd1 detectados.'
print hostsConPass1
print str(passwd2) + ' SSH con usuario/passwd2 detectados'
print hostsConPass2
