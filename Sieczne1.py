import PySimpleGUI as sg
import numpy as num

ZP = -1  # początek przedzialu
ZK = 1  # koniec przedziału
Dyskretyzacja = 0.50000
Sieczne_Blad = 0.50000
#Funkcja obliczajaca miejsca zerowe
def sieczne(a, b, fx):
    if fx(a) * fx(b) > 0:
        return None
    for j in range(20):
        siecza = a - fx(a) * (b - a) / (fx(b) - fx(a))
        f_sieczna = fx(siecza)
        if f_sieczna == 0:
            return siecza
        if abs(f_sieczna) < Sieczne_Blad:
            return siecza
        if fx(a) * f_sieczna < 0:
            b = siecza
        elif fx(b) * f_sieczna < 0:
            a = siecza
    return siecza

# Layout SimpleGUI
layout = [
    [sg.Text('Poziom Dyskretyzacji ', key='-TEXT1-')],
    [sg.Spin(['0.50000', '0.20000', '0.10000', '0.01000', '0.00100', '0.00010', '0.00001'], key='INPUT1'),
     sg.Button('Wprowadź', key='-GUZIK1')],
    [sg.Text('Dokładność wyznaczonego pierwiastka ', key='-TEXT2-')],
    [sg.Spin(['0.500000', '0.200000', '0.100000', '0.010000', '0.001000', '0.000100', '0.000010', '0.000001'], key='INPUT2'), sg.Button('Wprowadź', key='-GUZIK2')],
    [sg.Text('======OBECNE USTAWIENIA=======')],
    [sg.Text('DYSKRETYZACJA = 0.50000', key='-TEXT3-')],
    [sg.Text('DOKLADNOSC = 0.500000', key='-TEXT4-')],
    [sg.Button('OBLICZ PIERWIASTEK', key='-BUTTON1')],
    [sg.Text('____________________WYNIK____________________')],
    [sg.Text('X1 = ', key='-WYNIK1-')],
    [sg.Text('X2 = ', key='-WYNIK2-')],
    [sg.Text('X3 = ', key='-WYNIK3-')],
    [sg.Text('_______________Powered by MJ_________________')]
]
window = sg.Window('Siecznych', layout)
# pętla obsługująca zmiane stanów przycisków i okienek
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '-GUZIK1':
        window['-TEXT3-'].update('DYSKRETYZACJA = ' + values[ 'INPUT1'])
        a = values['INPUT1']
        Dyskretyzacja = float((a))  # dokladnosc podzialki

    if event == '-GUZIK2':
        window['-TEXT4-'].update('DOKLADNOSC = ' +values['INPUT2'])
        b = values['INPUT2']

        Sieczne_Blad = float((b))  # EPSX = 0.000001 # dokladnosc porownywania z zerem

    if event == '-BUTTON1':
        # Funkcja
        # f(x) = x^3 - 0,165*x^2+3,993*10^-4
        fx = lambda x: (x*x*x) - (0.165 * (x*x)) + 3.993 * 0.0001
        window['-WYNIK1-'].update('X1 = ')
        window['-WYNIK2-'].update('X2 = ')
        window['-WYNIK3-'].update('X3 = ')

        x = num.arange(ZP, ZK, Dyskretyzacja)
        y = num.vectorize(fx)(x)
        nr_of_roots = 0
        set_num = y[0]
        roots = []
        
        for i in range(len(y) - 1):
            if y[i] * set_num < 0:
                set_num = y[i]
                nr_of_roots += 1
                root = sieczne(x[i - 1], x[i], fx)
                roots.append(root)
        roots = [i for i in roots if i]  # remove None
        if len(roots) > 0:
            window['-WYNIK1-'].update('X1 = ' + str(roots[0]))
        if len(roots) > 1:
            window['-WYNIK2-'].update('X2 = ' + str(roots[1]))
        if len(roots) > 2:
            window['-WYNIK3-'].update('X3 = ' + str(roots[2]))
        #if roots[0] == None:
         #   print('brak rozwiazan')
          #  a = 0
           # window['-WYNIK1-'].update('Brak rozwiazan')
window.close()


