def is_number(n):
	try:
		float(n)
		return True
	except ValueError:
		return False
	
def input_integer(command):
	integer = 0
	cont = True
	while (cont):
		cont = False
		integer = raw_input(command)
		if is_number(integer): return int(integer)
		elif integer == 'exit': return 'exit'
		else: cont = True

def main():
	spells_file = open('spells.cfg', 'a+')
	
	while (True):
		name = raw_input('\nname: ').lower()
		if name == 'exit': break
		technique = raw_input('technique: ').lower()
		if technique == 'exit': break
		form = raw_input('form: ').lower()
		if form == 'exit': break
		requisites = raw_input('requisites: ').lower()
		if requisites == 'exit': break
		level = input_integer('level: ')
		if level == 'exit': break
		spell_range = raw_input('range: ').lower()
		if spell_range == 'exit': break
		duration = raw_input('duration: ').lower()
		if duration == 'exit': break
		target = raw_input('target: ').lower()
		if target == 'exit': break
		mastery_level = input_integer('mastery level: ')
		if mastery_level == 'exit': break
		mastery_exp = input_integer('mastery exp: ')
		masteries = [''] * mastery_level
		if mastery_level > 0:
			for i in range(mastery_level):
				masteries[i] = raw_input('mastery ' + str(i+1) + ': ').lower()
				if masteries[i] == 'exit':
					spells_file.close()
					return
		description = raw_input('description: ')
		if description == 'exit': break
		
		spells_file.write('NAME: ' + name + '\n')
		spells_file.write('TECHNIQUE: ' + technique + '\n')
		spells_file.write('FORM: ' + form + '\n')
		spells_file.write('REQUISITES: ' + requisites + '\n')
		spells_file.write('LEVEL: ' + str(level) + '\n')
		spells_file.write('RANGE: ' + spell_range + '\n')
		spells_file.write('DURATION: ' + duration + '\n')
		spells_file.write('TARGET: ' + target + '\n')
		spells_file.write('MASTERY_LEVEL: ' + str(mastery_level) + '\n')
		spells_file.write('MASTERY_EXP: ' + str(mastery_exp) + '\n')
		for i in range(mastery_level):
			spells_file.write('MASTERY_' + str(i+1) + ': ' + masteries[i] + '\n')
		spells_file.write('DESCRIPTION: ' + description + '\n')
		spells_file.write('\n')
	
	spells_file.close()

main()