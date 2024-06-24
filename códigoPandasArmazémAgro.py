# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:46:11 2024

@author: Afons
"""

import pandas as pd

produtos_df = pd.read_csv('planilhaTrabalhoAgro.csv',sep = ',')
print(produtos_df)
arquivo = 'planilhaTrabalhoAgro.csv'

while(True):
    interacao = input('O que você deseja fazer? (inserir/retirar/sair) ')
    
    if interacao == 'inserir' or interacao == 'retirar':
        quantidade = int(input('Qual quantidade você deseja? '))
        produto = input('Qual produto você deseja? ')

        # Identificar a coluna correta
        if produto == 'Saco de Esterco':
            coluna = 'Saco de Esterco'
        elif produto == 'creatina':
            coluna = 'Creatina de Cavalo'
        elif produto == 'pesticida':
            coluna = 'Pesticida'
        elif produto == 'Sacos':
            coluna = 'Sacos'
        elif produto == 'Botas':
            coluna = 'Botas'
        else:
            print('Produto não encontrado!')
            continue

        indice = produtos_df.index[produtos_df[coluna] == produtos_df[coluna].max()][0]

        if interacao == 'inserir':
            produtos_df.at[indice, coluna] += quantidade
            print(produtos_df)
        elif interacao == 'retirar':
            produtos_df.at[indice, coluna] -= quantidade
            print(produtos_df)
    elif interacao == 'sair':
        break

produtos_df.to_csv(arquivo, sep=',', index=False)

  
    
        
    
