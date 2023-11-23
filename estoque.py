'''
NOTA: 
    ADICIONAR FUNÇÃO COM DATA ATUAL

import datetime
from datetime import date

x = datetime.datetime.now()

print(x.strftime("%d/%m/%Y %H:%M"))#dia do mês


'''

import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3

# conexão com o DB
conn = sqlite3.connect('DB_ESTOQUE.db')
c = conn.cursor()
# c.execute('''CREATE TABLE if not exists estoque
#              (id INTEGER PRIMARY KEY, nome text, quantidade text) ''')

# Interface e funções
root = tk.Tk()
root.title("Sistema de Estoque")

root.option_add("*Font", "Arial 12")

def vertabela():
    resultado = c.execute('SELECT * FROM estoque')
    text_output.delete(1.0, tk.END)
    for item in resultado.fetchall():
        # Converte o item[1] (nome do produto) para maiúsculas
        line = "|{:<3}|{:<30}|{:<5}|".format(item[0], item[1].upper(), item[2], item[3])
        text_output.insert(tk.END, line + '\n')

def inserirvalor():
    id_inserido = simpledialog.askstring("Inserir valor", "ID:")
    item_inserido = simpledialog.askstring("Inserir valor", "ITEM:")
    data_inserido = simpledialog.askstring("Inserir valor", "DATA DE INSERÇÃO:")
    qtd_inserido = simpledialog.askstring("Inserir valor", "QUANTIDADE DE INSERÇÃO:")
    
    try:
        c.execute(f"INSERT INTO estoque VALUES('{id_inserido}', '{item_inserido}', '{qtd_inserido}','{data_inserido}')")
        messagebox.showinfo("Info", "Valores inseridos com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro","Não foi possivel inserir os valores !")
        print(str(e))
    conn.commit()

def alterar():
    id_digitado = simpledialog.askstring("Alterar valor", "Digite o ID do produto que deseja alterar:")
    acao = simpledialog.askstring("Alterar valor", "Deseja alterar [NOME] [DATA] [QUANTIDADE] ?").lower()
    
    if acao == 'quantidade':
        nova_qtd = simpledialog.askstring("Alterar valor", "Digite a quantidade atual: ")
        c.execute(f"UPDATE estoque SET quantidade=? WHERE id=?", (nova_qtd, id_digitado))
        linha_att = (c.execute(f"SELECT * FROM estoque WHERE id = ?", (id_digitado,)).fetchone())
        messagebox.showinfo("Info", f'Valor atualizado com sucesso!\n {linha_att}')

    if acao == 'nome':
        new_name = simpledialog.askstring("Alterar valor", "Digite o novo nome: ")
        c.execute(f"UPDATE estoque SET nome=? WHERE id=?", (new_name, id_digitado))
        linha_att = (c.execute(f"SELECT * FROM estoque WHERE id = ?", (id_digitado,)).fetchone())
        messagebox.showinfo("Info", f'Valor atualizado com sucesso!\n {linha_att}')

    if acao == 'data':
        new_data = simpledialog.askstring("Alterar valor", "Digite a nova data: ")
        c.execute(f"UPDATE estoque SET data_add=? WHERE id=", (new_data, id_digitado))
        linha_att = (c.execute(f"SELECT * FROM estoque WHERE id = ?", (id_digitado,)).fetchone())
        messagebox.showinfo("Info", f'Valor atualizado com sucesso!\n {linha_att}')

# def deletar():
#     id_digitado = input('Digite o ID do produto que deseja alterar: ')
#     comando_digitado = c.execute(f'SELECT * FROM estoque WHERE id="{id_digitado}"')
#     linha = comando_digitado.fetchone()
#     user_enter = input(f'Deseja mesmo deletar{linha}?[SIM][NÃO]')
#     if user_enter == 'sim':
#         c.execute(f"DELETE FROM estoque WHERE id ={id_digitado};")
#         messagebox.showinfo(f'Deletar','O item foi deletado com sucesso')
#     else:
#         print('Comando encerrado.')
#     conn.commit()

def deletar():
    id_inserido = simpledialog.askstring("Inserir valor", "Digite o Id que deseja deletar:")
    comand_delete = c.execute(f'SELECT * FROM estoque WHERE id={id_inserido}')
    delete_row = comand_delete.fetchone()
    user_entry = messagebox.askquestion(' ','Deseja mesmo deletar este item ?')
    
    if user_entry == 'yes':
        c.execute(f"DELETE FROM estoque WHERE id={id_inserido};")
        messagebox.showinfo(f'Deletar', 'O item foi deletado com sucesso')
    elif user_entry == 'no':
        messagebox.showinfo('ENCERRANDO', 'Comando encerrado')
    
    conn.commit()
    root.exit()

    item_inserido = simpledialog.askstring("Inserir valor", "ITEM:")
    data_inserido = simpledialog.askstring("Inserir valor", "DATA DE INSERÇÃO:")
    qtd_inserido = simpledialog.askstring("Inserir valor", "QUANTIDADE DE INSERÇÃO:")



def sair():
    btn_sair = messagebox.askquestion('','Deseja mesmo sair ?')
    if btn_sair == 'yes':
        messagebox.showinfo('', 'Encerrando o Programa...')
        conn.commit()
        conn.close()
        root.quit()


# Botões
menu_frame = tk.Frame(root)
menu_frame.pack(pady=0, padx=0, anchor="n")

btn_ver = tk.Button(menu_frame, text="Mostrar Tabela", command=vertabela, width=15, height=2)
btn_ver.grid(row=0, column=0, padx=5)

btn_inserir = tk.Button(menu_frame, text="Inserir", command=inserirvalor, width=15, height=2)
btn_inserir.grid(row=0, column=1, padx=5)

btn_alterar = tk.Button(menu_frame, text="Alterar", command=alterar, width=15, height=2)
btn_alterar.grid(row=0, column=2, padx=5)

btn_deletar = tk.Button(menu_frame, text="Deletar", command=deletar, width=15, height=2)
btn_deletar.grid(row=0, column=2, padx=5)

btn_sair = tk.Button(menu_frame, text="Sair", command=sair, width=15, height=2)
btn_sair.grid(row=0, column=3, padx=5)

text_output = tk.Text(root, width=50, height=20)
text_output = tk.Text(root, width=50, height=20, font=("Courier New", 12))
text_output.pack(pady=3, padx=15)

text_output.tag_configure('center', justify='center') 

root.mainloop()
conn.commit()
