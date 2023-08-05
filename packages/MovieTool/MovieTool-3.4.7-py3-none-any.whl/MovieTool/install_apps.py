import platform
import os


# ¡Instalación de apps necesarias!
run_in = platform.system()
platforms = {'Windows': 'Windows', 'Linux': 'Linux', 'Mac': 'Darwin'}  # Plataformas (Sí, Mac es Darwin XD)

#       Comandos:

# - Windows:
apps_commands_win = {'Jackett': 'winget install -e --id Jackett.Jackett', 'qBitTorrent': 'winget install -e --id qBittorrent.qBittorrent', 'Plex': 'winget install -e --id Plex.Plex', 'Python 3.9': 'winget install -e --id Python.Python.3.9'}




# INFO:
print('Tus aplicaciones se comenzarán a instalar. Una vez se comiencen a instalar le recomendamos no canelar la instalación, esto podría conllevar serios problemas.')

# Preguntamos al usuario si queire continuar, para que una vez comenzado,
# se trade de evitar la mayor cantidad de errores posibles.
continue_ask = input('¿Seguro quiere continuar? [Y] Yes, [N] No. | ---------->  ').upper()

# Pregunt si tienen Python, ya que es util  que tambíen se pueda instalar desde acá.
python_ask = input('¿Quiere instalar Python? [Y] Yes, [N] No. | ---------->  ').upper()

if continue_ask == 'Y':
    print('Los programas se comenzarán a instalar. No cancele nada por favor. Es probable que se pidan permisos de administrador.')

    if run_in == 'Windows':
        if python_ask == 'Y':
            for command_count, command in enumerate(list(apps_commands_win.values())[:-1]):
                print(command)
                i = os.system(command)

                if i == 0:
                    print(f' ======== Hemos instalado correctamente {list(apps_commands_win.keys())[command_count]} ======== ')

                else:
                    print(f'Hemos tenido un error al instalar {list(apps_commands_win.keys())[command_count]}')


        else:
            for command_count, command in enumerate(list(apps_commands_win.values())):
                print(command)
                i = os.system(command)

                if i == 0:
                    print(f' ======== Hemos instalado correctamente {list(apps_commands_win.keys())[command_count]} ======== ')

                else:
                    print(f'Hemos tenido un error al instalar {list(apps_commands_win.keys())[command_count]}')


    # TODO: Instalación para Linux y Mac.

else:
    print('Perfecto! Cuidate uwu.')
    exit()
