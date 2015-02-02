import sys, math

creo = 0
intellego = 1
muto = 2
perdo = 3
rego = 4
animal = 5
aquam = 6
auram = 7
corpus = 8
herbam = 9
ignem = 10
imaginem = 11
mentem = 12
terram = 13
vim = 14
summoning = 15
binding = 16
commanding = 17
arts = [0] * 18

intelligence = 0
perception = 1
strength = 2
stamina = 3
presence = 4
communication = 5
dexterity = 6
quickness = 7
characteristics = [0] * 8

infernal_lore = 0
fairie_lore = 1
magic_lore = 2
penetration = 3
concentration = 4
enigmatic_wisdom = 5
skills = [0] * 6
skill_specs = [''] * 6
	
hierarchy_score = 0
other = [0] * 1
	
spells = {}
	
def art_to_index(art):
	if art == 'creo': return 0
	if art == 'intellego': return 1
	if art == 'muto': return 2
	if art == 'perdo': return 3
	if art == 'rego': return 4
	if art == 'animal': return 5
	if art == 'aquam': return 6
	if art == 'auram': return 7
	if art == 'corpus': return 8
	if art == 'herbam': return 9
	if art == 'ignem ': return10
	if art == 'imaginem': return 11
	if art == 'mentem': return 12
	if art == 'terram': return 13
	if art == 'vim': return 14
	if art == 'summoning': return 15
	if art == 'binding': return 16
	if art == 'commanding': return 17
	
def read_spells():
	spell_file = open('spells.cfg')
	
	current_spell = {}
	for line in spell_file:
		if line[0] == '%' or len(line) == 1: continue
		code = str.split(line)[0][:-1]
		value = ' '.join(str.split(line)[1:])
		if code == 'NAME':
			if len(current_spell) > 0:
				spells[current_spell['name']] = current_spell
			current_spell = {code.lower(): value}
		elif code in ['LEVEL', 'MASTERY_LEVEL', 'MASTERY_EXP']: current_spell[code.lower()] = int(value)
		else: current_spell[code.lower()] = value
	
	spell_file.close()

def read_character():
	char_file = open('gerhardt.cfg')
	arts_read = 0
	while (arts_read != 18):
		line = char_file.readline()
		if line[0] == '%' or len(line) == 1: continue
		arts[arts_read] = int(str.split(line)[1])
		arts_read += 1
	
	characteristics_read = 0
	while (characteristics_read != 8):
		line = char_file.readline()
		if line[0] == '%' or len(line) == 1: continue
		characteristics[characteristics_read] = int(str.split(line)[1])
		characteristics_read += 1
	
	skills_read = 0
	while (skills_read != 6):
		line = char_file.readline()
		if line[0] == '%' or len(line) == 1: continue
		skills[skills_read] = int(str.split(line)[-1])
		skill_specs[skills_read] = str.split(line)[-2]
		skills_read += 1
	
	other_read = 0
	while (other_read != 1):
		line = char_file.readline()
		if line[0] == '%' or len(line) == 1: continue
		other[other_read] = int(str.split(line)[-1])
		other_read += 1
	
	char_file.close()
	
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
		elif integer == 'return': return 'return'
		else: cont = True
	
def use_summoning():
	total = characteristics[presence] + arts[summoning] + 3
	
	realm = ''
	realm_skill = 0
	cont = True
	while(cont):
		cont = False
		realm = raw_input('realm: ').lower()
		if realm == 'infernal':
			realm_skill = skills[infernal_lore]
			if skill_specs[infernal_lore].lower() == 'demons': realm_skill += 1
			total += other[hierarchy_score] * 5
		elif realm == 'magic':
			realm_skill = skills[magic_lore]
			if skill_specs[magic_lore].lower() == 'creatures': realm_skill += 1
		elif realm == 'fairie':
			realm_skill = skills[fairie_lore]
			if skill_specs[fairie_lore].lower() == 'fairies': realm_skill += 1
		elif realm == 'return': return
		else: cont = True
	total += realm_skill
	
	aura = input_integer('aura: ')
	if aura == 'return': return
	total += aura
	
	pen_mult = input_integer('penetration multiplier: ')
	if pen_mult == 'return': return
	pen = skills[penetration]
	if skill_specs[penetration].lower() == 'mentem': pen += 1
	total += pen * pen_mult
	
	lab_med = ''
	cont = True
	while (cont):
		cont = False
		lab_med = raw_input('Labyrinth meditation? ').lower()
		if lab_med == 'y': total += int(math.ceil(skills[enigmatic_wisdom] / 2))
		elif lab_med == 'n': break
		elif lab_med == 'return': return
		else: cont = True
	
	sacrifice = input_integer('sacrifice: ')
	if sacrifice == 'return': return
	total += sacrifice
	
	if realm == 'infernal' and skill_specs[penetration].lower() == 'mentem':
		print('Summoning total:\n')
		print('Demon in spirit form:\t\t' + str(total) + '/' + str(total - arts[summoning] + arts[rego]) + '/' + str(total - realm_skill + arts[vim]) + '/' + str(total - arts[summoning] - realm_skill + arts[rego] + arts[vim]) + ' + stress die')
		total -= pen_mult
		print('Demon not in spirit form:\t'  + str(total) + '/' + str(total - arts[summoning] + arts[rego]) + '/' + str(total - realm_skill + arts[vim]) + '/' + str(total - arts[summoning] - realm_skill + arts[rego] + arts[vim]) + ' + stress die\n')
		total += pen_mult
	else:
		print('Summoning total:\t\t' + str(total) + '/' + str(total - arts[summoning] + arts[rego]) + '/' + str(total - realm_skill + arts[vim]) + '/' + str(total - arts[summoning] - realm_skill + arts[rego] + arts[vim]) + ' + stress die\n')
	
	result = input_integer('result: ')
	if result == 'return': return
	if realm == 'infernal':
		for i in range(1, 6):
			print('Demon hierarchy score: ' + str(i))
			print('\t\tSummons level ' + str( (result / 2) - (i * 5) ) + ' securely')
			print('\t\tSummons level ' + str(result - i * 5) + ' unsecurely')
	else:
		print('Summons level ' + str(result / 2) + ' securely')
		print('Summons level ' + str(result) + ' unsecurely')
	
def use_commanding():
	total = characteristics[communication] + arts[commanding]
	
	realm = ''
	realm_skill = 0
	cont = True
	while(cont):
		cont = False
		realm = raw_input('realm: ').lower()
		if realm == 'infernal':
			realm_skill = skills[infernal_lore]
			if skill_specs[infernal_lore].lower() == 'demons': realm_skill += 1
			total += other[hierarchy_score] * 5
		elif realm == 'magic':
			realm_skill = skills[magic_lore]
			if skill_specs[magic_lore].lower() == 'creatures': realm_skill += 1
		elif realm == 'fairie':
			realm_skill = skills[fairie_lore]
			if skill_specs[fairie_lore].lower() == 'fairies': realm_skill += 1
		elif realm == 'return': return
		else: cont = True
	total += realm_skill
	
	aura = input_integer('aura: ')
	if aura == 'return': return
	total += aura
	
	pen_mult = input_integer('penetration multiplier: ')
	if pen_mult == 'return': return
	pen = skills[penetration]
	if skill_specs[penetration].lower() == 'mentem': pen += 1
	total += pen * pen_mult
	
	lab_med = ''
	cont = True
	while (cont):
		cont = False
		lab_med = raw_input('Labyrinth meditation? ').lower()
		if lab_med == 'y': total += int(math.ceil(skills[enigmatic_wisdom] / 2))
		elif lab_med == 'n': break
		elif lab_med == 'return': return
		else: cont = True
	
	sacrifice = input_integer('sacrifice: ')
	if sacrifice == 'return': return
	total += sacrifice
	
	print('Commanding total:\t\t' + str(total) + '/' + str(total - arts[commanding] + arts[rego]) + '/' + str(total - realm_skill + arts[vim]) + '/' + str(total - arts[commanding] - realm_skill + arts[rego] + arts[vim]) + ' + stress die')
	
	result = input_integer('result: ')
	if result == 'return': return
	if realm == 'infernal':
		for i in range(1, 6):
			print('Demon hierarchy score: ' + str(i))
			print('\t\tCommands level ' + str(result - i * 5 - 1) + ' in summoning circle')
			print('\t\tCommands level ' + str( (result / 2) - (i * 5) - 1 ) + ' not in summoning circle')
	else:
		print('Commands level ' + str(result - 1) + ' in summoning circle')
		print('Commands level ' + str(result / 2 - 1) + ' not in summoning circle')
		
def use_scouring():
	total = characteristics[presence] + arts[summoning] + 3
	
	realm = ''
	realm_skill = 0
	cont = True
	while(cont):
		cont = False
		realm = raw_input('realm: ').lower()
		if realm == 'infernal':
			realm_skill = skills[infernal_lore]
			if skill_specs[infernal_lore].lower() == 'demons': realm_skill += 1
		elif realm == 'magic':
			realm_skill = skills[magic_lore]
			if skill_specs[magic_lore].lower() == 'creatures': realm_skill += 1
		elif realm == 'fairie':
			realm_skill = skills[fairie_lore]
			if skill_specs[fairie_lore].lower() == 'fairies': realm_skill += 1
		elif realm == 'return': return
		else: cont = True
	total += realm_skill
	
	aura = input_integer('aura: ')
	if aura == 'return': return
	total += aura
	
	total += skills[penetration]
	if skill_specs[penetration].lower() == 'mentem': total += 1
	
	lab_med = ''
	cont = True
	while (cont):
		cont = False
		lab_med = raw_input('Labyrinth meditation? ').lower()
		if lab_med == 'y': total += int(math.ceil(skills[enigmatic_wisdom] / 2))
		elif lab_med == 'n': break
		elif lab_med == 'return': return
		else: cont = True
	
	sacrifice = input_integer('sacrifice: ')
	if sacrifice == 'return': return
	total += sacrifice
	
	print('Summoning total:\t\t' + str(total) + '/' + str(total - arts[summoning] + arts[rego]) + '/' + str(total - realm_skill + arts[vim]) + '/' + str(total - arts[summoning] - realm_skill + arts[rego] + arts[vim]) + ' + stress die\n')
	
	result = input_integer('result: ')
	if result == 'return': return
	print('Summons level ' + str(result / 2) + ' securely')
	print('Summons level ' + str(result) + ' unsecurely')
		
def use_casting():
	spell = ''
	while (True):
		input = raw_input('spell: ').lower()
		spell = input
		if str.split(input)[-1] == '-ac': input = ' '.join(str.split(input)[:-1])
		if input == 'return': return
		elif input in spells: break
		else:
			similar_spells = find_similar_spell_names(input)
			if len(similar_spells) == 0: print('No such spell\n')
			else:
				print('No such spell, did you mean any of these?\n')
				for spell_name in similar_spells:
					print('\t' + spell_name[1] + '\n')
	
	use_ac = False
	if str.split(spell)[-1] == '-ac':
		use_ac = True
		spell_name = ' '.join(str.split(spell)[:-1])
	else: spell_name = spell
	spell = spells[spell_name]
	
	total = arts[art_to_index(spell['technique'])] + arts[art_to_index(spell['form'])] + characteristics[stamina]
	
	aura = input_integer('aura: ')
	if aura == 'return': return
	total += aura

	saruman = input_integer('words & gestures: ')
	if saruman == 'return': return
	total += saruman
	
	pen = skills[penetration]
	if skill_specs[penetration].lower() in [spell['technique'], spell['form']]: pen += 1
	if use_ac:
		pen_mult = input_integer('penetration multiplier: ')
		if pen_mult == 'return': return
		pen *= pen_mult
	
	goetic_mastery = False
	cast_on_demon = False
	for i in range(1, spell['mastery_level'] + 1):
		goetic_mastery = spell['mastery_' + str(i)] == 'goetic mastery'
	if goetic_mastery:
		goetic_skill = ''
		while (True):
			input = raw_input('(S)ummoning, (C)ommanding, (B)inding or (A)blating: ').lower()
			if input == 'return': return
			elif input == 's' or input == 'c' or input == 'b' or input == 'a':
				goetic_skill = input
				break
		if goetic_skill == 's': total += arts[summoning]
		elif goetic_skill == 'c': total += arts[commanding]
		elif goetic_skill == 'b': total += arts[binding]
		elif goetic_skill == 'a': print('Character does not have Ablating!\n')
		
		while (True):
			input = raw_input('Spell cast on demon? ').lower()
			if input == 'return': return
			elif input == 'n': break
			elif input == 'y':
				cast_on_demon = True
				break
		if cast_on_demon:
			pen += (other[hierarchy_score] * 5)
	
	print('Casting total:\t\t' + str(total) + ' + die')
	
	result = input_integer('result: ')
	if result == 'return': return
	if (result >= spell['level']):
		if cast_on_demon:
			print('Spell is cast, penetration:\t' + str(result - spell['level'] + pen) + ' - demon\'s (Hierarchy Score x 5)\n')
		else:
			print('Spell is cast, penetration:\t' + str(result - spell['level'] + pen) + '\n')
	elif (result >= spell['level'] - 10):
		print('Spell is cast, no penetration, 1 fatigue level lost\n')
	else:
		print ('Spell is not cast, 1 fatigue level lost\n')


def find_similar_spell_names(spell_name):
	similar_spells = []
	spell_name_words = str.split(spell_name)
	for name in spells:
		name_words = str.split(name)
		for word in spell_name_words:
			if (word in name_words) and (not name in [a[1] for a in similar_spells]): similar_spells.append([0, name])
		for word in name_words:
			if (word in spell_name_words) and (not name in [a[1] for a in similar_spells]): similar_spells.append([0, name])
	return similar_spells
	
def print_spell():
	spell_name = ''
	while (True):
		spell_name = raw_input('spell: ').lower()
		if spell_name == 'return': return
		elif spell_name in spells: break
		else:
			similar_spells = find_similar_spell_names(spell_name)
			if len(similar_spells) == 0: print('No such spell\n')
			else:
				print('No such spell, did you mean any of these?\n')
				for spell in similar_spells:
					print('\t' + spell[1] + '\n')
	spell = spells[spell_name]
	
	print_str = spell_name.upper() + '\n\t' + spell['technique'] + ' ' + spell['form'] + ' '
	if spell['requisites'] != '': print_str += 'reqs: (' + spell['requisites'] + ') '
	print_str += 'lvl ' + str(spell['level'])
	print_str += '\n\t' + spell['range'] + ' ' + spell['duration'] + ' ' + spell['target']
	if spell['mastery_level'] > 0:
		print_str += '\n\t' + 'mastery lvl: ' + str(spell['mastery_level']) + ' (' + str(spell['mastery_exp']) + ' exp)'
		for i in range(spell['mastery_level']):
			print_str += '\n\t\t' + spell['mastery_' + str(i + 1)]
	elif spell['mastery_exp'] > 0:
		print_str += '\n\tmastery exp:' + str(spell['mastery_exp'])
	print_str += '\n\t' + spell['description']
	
	print
	print(print_str)
	print
	
def print_all_spell_names():
	print
	for name in spells:
		print(name)
	print
	
def input_loop():
	while (True):
		command = raw_input('command: ')
		if command == 'exit': break
		elif command == 'summon': use_summoning()
		elif command == 'scour': use_scouring()
		elif command == 'command': use_commanding()
		elif command == 'cast': use_casting()
		elif command == 'spell': print_spell()
		elif command == 'all spells': print_all_spell_names()
	
def main(arguments):	
	read_character()
	read_spells()
	input_loop()

if __name__ == "__main__":
	main(sys.argv[1:])