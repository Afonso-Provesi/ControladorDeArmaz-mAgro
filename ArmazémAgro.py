# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:46:11 2024

@author: Afons
"""

import pandas as pd
import tkinter as tk
from tkinter import messagebox

class Item:
    def __init__(self, nome, quantidade):
        self.nome = nome
        self.quantidade = quantidade

class Armazem:
    def __init__(self):
        self.arquivo = 'planilhaTrabalhoAgro.csv'
        self.itens = self.carregar_itens()

    def carregar_itens(self):
        try:
            produtos_df = pd.read_csv(self.arquivo, sep=',')
            itens = {coluna: Item(coluna, produtos_df[coluna].max()) for coluna in produtos_df.columns}
            return itens
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")
            return {}

    def salvar_itens(self):
        try:
            produtos_df = pd.DataFrame({nome: [item.quantidade] for nome, item in self.itens.items()})
            produtos_df.to_csv(self.arquivo, sep=',', index=False)
            messagebox.showinfo("Sucesso", "Arquivo salvo com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def adicionar_item(self, nome, quantidade):
        if nome.strip() == "":
            messagebox.showerror("Erro", "Por favor, insira um nome para o item")
            return

        if nome in self.itens:
            self.itens[nome].quantidade += quantidade
        else:
            self.itens[nome] = Item(nome, quantidade)

    def remover_item(self, nome, quantidade):
        if nome in self.itens:
            if self.itens[nome].quantidade >= quantidade:
                self.itens[nome].quantidade -= quantidade
                if self.itens[nome].quantidade == 0:
                    del self.itens[nome]
                messagebox.showinfo("Sucesso", f"{quantidade} unidades de {nome} removidas")
            else:
                messagebox.showerror("Erro", "Quantidade insuficiente no estoque")
        else:
            messagebox.showerror("Erro", f"Item '{nome}' não encontrado")

    def limpar_armazem(self):
        self.itens.clear()
        messagebox.showinfo("Sucesso", "Armazém limpo com sucesso")

    def listar_itens(self):
        return [(item.nome, item.quantidade) for item in self.itens.values()]

class AplicacaoArmazem:
    def __init__(self, root):
        self.armazem = Armazem()
        self.root = root
        self.root.title("Simulação de Armazém")

        # Configura o tamanho mínimo da janela
        self.root.minsize(730, 400)

        # Configura o layout da grade para ser responsivo
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame principal
        self.frame_principal = tk.Frame(root)
        self.frame_principal.grid(sticky="nsew")

        for i in range(6):
            self.frame_principal.columnconfigure(i, weight=1)
        self.frame_principal.rowconfigure(0, weight=1)
        self.frame_principal.rowconfigure(1, weight=1)
        self.frame_principal.rowconfigure(2, weight=1)
        self.frame_principal.rowconfigure(3, weight=1)

        # Fonte grande para todos os widgets
        fonte_grande = ("Helvetica", 14)

        # Interface de adicionar item
        self.label_nome_adicionar = tk.Label(self.frame_principal, text="Nome do Item:", font=fonte_grande)
        self.label_nome_adicionar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.entry_nome_adicionar = tk.Entry(self.frame_principal, font=fonte_grande)
        self.entry_nome_adicionar.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        self.label_quantidade_adicionar = tk.Label(self.frame_principal, text="Quantidade:", font=fonte_grande)
        self.label_quantidade_adicionar.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.entry_quantidade_adicionar = tk.Entry(self.frame_principal, font=fonte_grande)
        self.entry_quantidade_adicionar.grid(row=0, column=4, sticky="ew", padx=5, pady=5)
        self.botao_adicionar = tk.Button(self.frame_principal, text="Adicionar", font=fonte_grande,
                                         command=self.adicionar_item)
        self.botao_adicionar.grid(row=0, column=5, sticky="ew", padx=5, pady=5)

        # Interface de remover item
        self.label_nome_remover = tk.Label(self.frame_principal, text="Nome do Item:", font=fonte_grande)
        self.label_nome_remover.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.entry_nome_remover = tk.Entry(self.frame_principal, font=fonte_grande)
        self.entry_nome_remover.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        self.label_quantidade_remover = tk.Label(self.frame_principal, text="Quantidade:", font=fonte_grande)
        self.label_quantidade_remover.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        self.entry_quantidade_remover = tk.Entry(self.frame_principal, font=fonte_grande)
        self.entry_quantidade_remover.grid(row=1, column=4, sticky="ew", padx=5, pady=5)
        self.botao_remover = tk.Button(self.frame_principal, text="Remover", font=fonte_grande,
                                       command=self.remover_item)
        self.botao_remover.grid(row=1, column=5, sticky="ew", padx=5, pady=5)

        # Botão para limpar o armazém
        self.botao_limpar = tk.Button(self.frame_principal, text="Limpar Armazém", font=fonte_grande,
                                      command=self.limpar_armazem)
        self.botao_limpar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        # Botão para salvar o armazém
        self.botao_salvar = tk.Button(self.frame_principal, text="Salvar Armazém", font=fonte_grande,
                                      command=self.salvar_armazem)
        self.botao_salvar.grid(row=2, column=3, columnspan=3, sticky="ew", padx=5, pady=5)

        # Área de texto para exibir os itens
        self.texto_itens = tk.Text(self.frame_principal, height=10, font=fonte_grande, state='disabled')
        self.texto_itens.grid(row=3, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)
        self.atualizar_listagem()

    def adicionar_item(self):
        nome = self.entry_nome_adicionar.get()
        try:
            quantidade = int(self.entry_quantidade_adicionar.get())
            if quantidade <= 0:
                raise ValueError
            self.armazem.adicionar_item(nome, quantidade)
            self.entry_nome_adicionar.delete(0, tk.END)
            self.entry_quantidade_adicionar.delete(0, tk.END)
            self.atualizar_listagem()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número positivo para a quantidade")

    def remover_item(self):
        nome = self.entry_nome_remover.get()
        try:
            quantidade = int(self.entry_quantidade_remover.get())
            if quantidade <= 0:
                raise ValueError
            self.armazem.remover_item(nome, quantidade)
            self.entry_nome_remover.delete(0, tk.END)
            self.entry_quantidade_remover.delete(0, tk.END)
            self.atualizar_listagem()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número positivo para a quantidade")

    def limpar_armazem(self):
        self.armazem.limpar_armazem()
        self.atualizar_listagem()

    def salvar_armazem(self):
        self.armazem.salvar_itens()

    def atualizar_listagem(self):
        self.texto_itens.config(state='normal')  # Habilita a edição temporariamente
        self.texto_itens.delete(1.0, tk.END)
        itens = self.armazem.listar_itens()
        for nome, quantidade in itens:
            self.texto_itens.insert(tk.END, f"Item: {nome}, Quantidade: {quantidade}\n")
        self.texto_itens.config(state='disabled')  # Desabilita a edição novamente

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoArmazem(root)
    root.mainloop()
