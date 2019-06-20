import PySimpleGUI as sg

sg.ListOfLookAndFeelValues()
#['SystemDefault', 'Reddit', 'Topanga', 'GreenTan', 'Dark', 'LightGreen', 'Dark2', 'Black', 'Tan', 'TanBlue',
# 'DarkTanBlue', 'DarkAmber', 'DarkBlue', 'Reds', 'Green', 'BluePurple', 'Purple', 'BlueMono', 'GreenMono',
# 'BrownBlue', 'BrightColors', 'NeutralBlue', 'Kayak', 'SandyBeach', 'TealMono']
#Temas "FRIOS":[]

sg.ChangeLookAndFeel('BluePurple')
layout = [
			[sg.Text('Sopa de Letras', font = ('Fixedsys',25), pad = (90,8),justification = 'center')],
			[sg.Text('PySimpleGUIWeb running on the web and in your browser!', size=(60,1), font=('Comic sans ms', 20), text_color='red')],
			[sg.Text('This program has been running for... ', size=(30,1)),sg.Text('', size=(30,1), key='_DATE_')],
			[sg.Text('', size=(30,1), key='_TEXT_')],
			[sg.Input('Single Line Input', do_not_clear=True, enable_events=True, size=(30,1))],
			[sg.Multiline('Multiline Input', do_not_clear=True, size=(40,4), enable_events=True)],
			# [sg.MultilineOutput('Multiline Output', size=(40,8),  key='_MULTIOUT_', font='Courier 12')],
			[sg.Output(font='Courier 11', size=(60,8))],
			[sg.Checkbox('Checkbox 1', enable_events=True, key='_CB1_'), sg.Checkbox('Checkbox 2', default=True, enable_events=True, key='_CB2_')],
			[sg.Combo(values=['Combo 1', 'Combo 2', 'Combo 3'], default_value='Combo 2', key='_COMBO_',enable_events=True, readonly=False, tooltip='Combo box', disabled=False, size=(12,1))],
			[sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(10,3), enable_events=True, key='_LIST_')],
			[sg.Slider((1,100), default_value=80, key='_SLIDER_', visible=True, enable_events=True)],
			[sg.Spin(values=(1,2,3),initial_value=2, size=(4,1))],
			[sg.OK(), sg.Button('Exit', button_color=('white', 'red'))],
			[sg.Button('Tema', key='TEMA')]
		]

window = sg.Window('').Layout(layout)
pos = 0
while True:				 # Event Loop
	event, val = window.Read()
	#print(event, val)
	if event == 'TEMA':
		window.Close()
		tamaño = len(sg.ListOfLookAndFeelValues())
		pos = (pos + 1) % tamaño
		sg.ChangeLookAndFeel(sg.ListOfLookAndFeelValues()[pos])
		window = sg.Window('').Layout(layout)
