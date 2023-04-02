# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:03:53 2023

@author: João
"""

import MetaTrader5 as mt5
import time
import datetime

mt5.initialize()

data=datetime.now()
hr = time.strftime('%H:%M:%S')
account_info=mt5.account_info()
ctalgda = (account_info[0])
corretora1 = (account_info[25])
nome = (account_info[24])
lot = 1.0

selected=mt5.symbol_select("WDOK23",True)
symbol_info=mt5.symbol_info("WDOK23")
symbol = "WDOK23"
ativo = symbol
mt5.symbol_select(symbol, True)
tick = mt5.symbol_info_tick(symbol)
base = 0.5
df_operacoes_B = []
df_taxas_B = []
if corretora1 == 'OramaDTVM-Server':
    corretagem = 0.11  # Valor de corretagem da Rico
else:
    corretagem = 0.0

taxa_bmf = 0.40
emolumentos = 0.75

taxa = (taxa_bmf+emolumentos+corretagem)*-2 
ftr = 10

hr_inicial = '08:59:50'
hr_inicial_2 = '08:59:55'
hr_final_2 = '17:59:55:'
hr_final = '18:00:00:'

pr0 = 0 #(dados_dia['open'][0])
dia_Hcdl1 = 0 #dados_dia['high'][0]
dia_Lcdl1 = 0 #dados_dia['low'][0]
a_B = 0

account_info=mt5.account_info()
saldo = (account_info[10])
saldo1 = (account_info[10])
primeiroCandle = 'OFF'
op_abertura = 'OFF'
lot = 1
magic_number = 25232428
deviation = 0
alvo = 5
alvoA = alvo
trailing = 10
prB = 0
prB2 = 0
prA3 = 0
gap = 0
gap2 = 0

while hr < hr_final_2:
    hr = time.strftime('%H:%M:%S')
    account_info=mt5.account_info()
    saldo = (account_info[10])
    pts = (saldo - saldo1) / ftr
    while hr < hr_inicial_2:
        hr = time.strftime('%H:%M:%S')
        print(f'... Hora: {hr} | Aguardando horário para inicio das operações .... às {hr_inicial}', end='\r')
        time.sleep(1)
        pass
    
    if hr >= hr_inicial_2:
        # Candle M1
        ultimo = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
        prA = ultimo['open'][0]
        prAC = ultimo['close'][0]
        dt = ultimo['time'][0]
        prB = datetime.fromtimestamp(dt)
        
        while hr >= hr_inicial_2 and hr < hr_final_2:
            tick = mt5.symbol_info_tick(symbol)
            hr=time.strftime("%H:%M:%S")
            account_info=mt5.account_info()
            saldo = (account_info[10])
            pts = (saldo - saldo1) / ftr
            pr = tick.last
            if primeiroCandle == 'OFF':
                # Candle M1
                inicio = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
                prA2 = inicio['open'][0]
                dt2 = inicio['time'][0]
                prB2 = datetime.fromtimestamp(dt2)
            if prB != prB2:
                primeiroCandle = 'ON'
                inicio2 = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
                prA3 = inicio2['open'][0]
                # Candle diario
                dados_dia = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 1)
                pr0 = (dados_dia['open'][0])
                cl = dados_dia['close'][0]
            if op_abertura == 'OFF' and primeiroCandle == 'ON':
                
                if prA3 > prAC and prA3 - prAC < 6.0:
                    gap = prA3 - prAC
                    gap2 = 'ALTA'
                    op_abertura = 'ON Menor'
                # GAP de baixa - COMPRAR
                if prA3 > prAC and prA3 - prAC >= 6.0:
                    time.sleep(2)
                    gap = prA3 - prAC
                    gap2 = 'ALTA'
                    op_abertura = 'ON Maior'
                    #Vender na abertura com alvo de 5 pontos
                    #Stop de 10 pontos
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": ativo,
                        "volume": float(lot),             
                        "type": mt5.ORDER_TYPE_SELL,
                        "price": pr,
                        "sl": pr + trailing,
                        "tp": pr - alvoA,
                        "deviation": deviation,
                        "magic": magic_number,
                        "type_time": mt5.ORDER_TIME_DAY,
                        "type_filling": mt5.ORDER_FILLING_RETURN,
                    }
                    result = mt5.order_send(request)
                    # get position based on ticket_id
                    position = mt5.positions_get()
                    # check if position exists
                    if position:
                        position = position[0]
                        TICKET = position.ticket
                        price_open = position.price_open
                        price = price_open
                        request = {
                            "action": mt5.TRADE_ACTION_SLTP,
                            "position": TICKET,
                            "symbol": ativo,
                            "sl": price_open + trailing,
                            "tp": price_open - alvoA,
                            "deviation": deviation,
                            "magic": magic_number,
                        }
                        result = mt5.order_send(request)
                    
                        
                if prAC > prA3 and prAC - prA3 < 6.0:
                    gap = prAC - prA3
                    gap2 = 'BAIXA'
                    op_abertura = 'ON Menor'

                if prAC > prA3 and prAC - prA3 >= 6.0:
                    time.sleep(2)
                    gap = prAC - prA3
                    gap2 = 'BAIXA'
                    op_abertura = 'ON Maior'
                    #Comprar na abertura com alvo de 5 pontos
                    #Stop de 10 pontos
                    request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": ativo,
                        "volume": float(lot),             
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": pr,
                        "sl": pr - trailing,
                        "tp": pr + alvoA,
                        "deviation": deviation,
                        "magic": magic_number,
                        "type_time": mt5.ORDER_TIME_DAY,
                        "type_filling": mt5.ORDER_FILLING_RETURN,
                    }
                    result = mt5.order_send(request)
                    # get position based on ticket_id
                    position = mt5.positions_get()
                    # check if position exists
                    if position:
                        position = position[0]
                        TICKET = position.ticket
                        price_open = position.price_open
                        price = price_open
                        request = {
                            "action": mt5.TRADE_ACTION_SLTP,
                            "position": TICKET,
                            "symbol": ativo,
                            "sl": price_open - trailing,
                            "tp": price_open + alvoA,
                            "deviation": deviation,
                            "magic": magic_number,
                        }
                        result = mt5.order_send(request)
                        
            print(f'... | hora: {hr} | {a_B} | Gap: {gap} {gap2} | {op_abertura} | {prB} {prB2} | Pontos: {pts} |', end='\r')
            time.sleep(0.1)
            pass                         
    