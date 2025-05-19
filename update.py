import datetime
import subprocess

date = datetime.datetime.now().strftime('%d-%m-%y - %H:%M')

print('Processo iniciado...')
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', date])
subprocess.run(['git', 'push', 'origin', 'main'])
print('Finalizado !')
