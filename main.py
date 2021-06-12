from configparser import ConfigParser
import time
config = ConfigParser()
try:   
    open('config.ini' , 'r')
except: 
    open('config.ini', 'w').write("")
    config.read('config.ini')
    config.add_section('api')
    config.add_section('method')
    config.add_section('filenames')
    config.set('api', 'clientid', input('Introduce el client id\n'))
    config.set('api', 'clientsec', input('Introduce el client secret\n'))
    config.set('method', 'gamemode', input('Introduce el gamemode (osu, mania, taiko, fruits)\n'))
    config.set('method', 'country', input('Introduce el país\n'))
    config.set('filenames', 'playersoutput', input('introduce el nombre del archivo donde irán los jugadores \n'))
    config.set('filenames', 'playsoutput', input('introduce el nombre del archivo donde irán las plays \n'))
    with open('config.ini', 'w') as f:
        config.write(f)
else:
    import worker
