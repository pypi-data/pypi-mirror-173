import json
from colorama import init, Fore, Back
from collections import deque

def __printObj(o, id = None):
	
	init(autoreset=True)
	
	txtcor = Fore.LIGHTWHITE_EX
	txtcor_inv = Fore.BLACK
	bgcor = Back.LIGHTWHITE_EX
	desc = o
	tipo = type(o).__name__
	difin = 20 if tipo == 'function' else 15 if tipo == 'type' else 0 
	rows = []
	id = ' \x1B[4m\x1B[3m' + str(id) + ':\x1B[0m ' if id != None else ''

	if tipo in ['list', 'dict', 'tuple', 'set']:
		txtcor = Fore.LIGHTGREEN_EX
		txtcor_inv = Fore.BLACK
		bgcor = Back.LIGHTGREEN_EX
		id = '\033[1m' + txtcor + str(id) if id != None else ''

		if tipo in ['list', 'tuple', 'set']:
			label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' '
			rows.append( label + txtcor + Back.RESET + ' → ' + str(desc))

		else:
			label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' ' + Back.RESET + txtcor + ' ↓'
			rows.append(label)
			rows.append('\033[1m' + txtcor + json.dumps(o, sort_keys=True, indent=4, ensure_ascii=False))
	
	elif tipo == 'int':
		txtcor = Fore.LIGHTYELLOW_EX
		txtcor_inv = Fore.BLACK
		bgcor = Back.LIGHTYELLOW_EX
		id = '\033[1m' + txtcor + str(id) if id != None else ''
		label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' '
		rows.append( label + txtcor + Back.RESET + ' → ' + str(desc))
	
	elif tipo == 'str':
		txtcor = Fore.LIGHTBLUE_EX
		txtcor_inv = Fore.BLACK
		bgcor = Back.LIGHTBLUE_EX
		id = '\033[1m' + txtcor + str(id) if id != None else ''
		label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' '
		rows.append( label + txtcor + Back.RESET + ' → ' + str(desc))
	
	elif tipo == 'function':
		txtcor = Fore.LIGHTMAGENTA_EX
		txtcor_inv = Fore.BLACK
		bgcor = Back.LIGHTMAGENTA_EX
		id = '\033[1m' + txtcor + str(id) if id != None else ''
		label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' '
		rows.append( label + txtcor + Back.RESET + ' → ' + desc.__name__ + str(desc.__code__.co_varnames).replace("'", ""))
	
	elif tipo == 'type':
		txtcor = Fore.LIGHTCYAN_EX
		txtcor_inv = Fore.BLACK
		bgcor = Back.LIGHTCYAN_EX
		id = '\033[1m' + txtcor + str(id) if id != None else ''
		label = id + '\033[1m' + txtcor_inv + bgcor + ' class '
		rows.append( label + txtcor + Back.RESET + ' → ' + desc.__name__)

	else:
		id = '\033[1m' + txtcor + str(id) if id != None else ''
		label = id + '\033[1m' + txtcor_inv + bgcor + ' ' + tipo + ' '
		rows.append( label + txtcor + Back.RESET + ' → ' + str(desc))
	
	for row in rows:
		print(row)

	print('\033[1m' + txtcor + '--------------------')


def show(o, *_o, id = None):

	print()

	objs = deque([o, *list(_o)])

	while objs:
		__printObj(objs.popleft(), id=id)

	print()
