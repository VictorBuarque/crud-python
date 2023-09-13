from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import mysql.connector

root = Tk()
root.title("Cadastro de Usuários")
root.geometry('1490x1200')
root.configure(bg="lightblue")

# Variáveis
nome = StringVar()
cpf = StringVar()
telefone = StringVar()
email = StringVar()

# Variável auxiliar
selected_item = None

# Funções
def Database():
    global conn, cursor
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='crud')
    cursor = conn.cursor()

def Create():
    if nome.get() == "" or cpf.get() == "" or telefone.get() == "" or email.get() == "":
        tkMessageBox.showerror("Cadastro de Usuários", "Por favor, preencha todos os campos.")
    else:
        Database()
        cursor.execute("INSERT INTO usuario (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)",
                       (str(nome.get()), str(cpf.get()), str(telefone.get()), str(email.get())))
        conn.commit()
        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Cadastro de Usuários", "Registro criado com sucesso.")
        nome.set("")
        cpf.set("")
        telefone.set("")
        email.set("")
        Read()

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM usuario")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4]))
    cursor.close()
    conn.close()

def OnSelect(event):
    global selected_item
    selected_item = tree.item(tree.selection())['values'][0]  # Pega o valor da primeira coluna (ID)
    item = tree.item(tree.selection())
    values = item['values']
    nome.set(values[1])
    cpf.set(values[2])
    telefone.set(values[3])
    email.set(values[4])

def Update():
    global selected_item
    if not selected_item:
        tkMessageBox.showerror("Cadastro de Usuários", "Por favor, selecione um registro para atualizar.")
        return
    if nome.get() == "" or cpf.get() == "" or telefone.get() == "" or email.get() == "":
        tkMessageBox.showerror("Cadastro de Usuários", "Por favor, preencha todos os campos.")
        return
    Database()
    cursor.execute("UPDATE usuario SET nome = %s, cpf = %s, telefone = %s, email = %s WHERE id = %s",
                   (str(nome.get()), str(cpf.get()), str(telefone.get()), str(email.get()), selected_item))
    conn.commit()
    cursor.close()
    conn.close()
    tkMessageBox.showinfo("Cadastro de Usuários", "Registro atualizado com sucesso.")
    nome.set("")
    cpf.set("")
    telefone.set("")
    email.set("")
    selected_item = None
    Read()

def Delete():
    global selected_item
    if not selected_item:
        tkMessageBox.showerror("Cadastro de Usuários", "Por favor, selecione um registro para excluir.")
        return
    result = tkMessageBox.askquestion('Cadastro de Usuários', 'Você tem certeza que deseja excluir o registro?', icon="warning")
    if result == 'yes':
        Database()
        cursor.execute("DELETE FROM usuario WHERE id = %s" % selected_item)
        conn.commit()
        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Cadastro de Usuários", "Registro excluído com sucesso.")
        nome.set("")
        cpf.set("")
        telefone.set("")
        email.set("")
        selected_item = None
        Read()
        
def Limpar_Campos():
    nome.set("")
    cpf.set("")
    telefone.set("")
    email.set("")
# Labels e Entradas
label_nome = Label(root, text="Nome:")
label_nome.pack(pady=5)
entry_nome = Entry(root, textvariable=nome)
entry_nome.pack(pady=5)

label_cpf = Label(root, text="CPF:")
label_cpf.pack(pady=5)
entry_cpf = Entry(root, textvariable=cpf)
entry_cpf.pack(pady=5)

label_telefone = Label(root, text="Telefone:")
label_telefone.pack(pady=5)
entry_telefone = Entry(root, textvariable=telefone)
entry_telefone.pack(pady=5)

label_email = Label(root, text="Email:")
label_email.pack(pady=5)
entry_email = Entry(root, textvariable=email)
entry_email.pack(pady=5)

# Botões
btn_create = Button(root, text="Salvar", command=Create)
btn_create.pack(pady=10)
btn_update = Button(root, text="Atualizar", command=Update)
btn_update.pack(pady=10)
btn_delete = Button(root, text="Excluir", command=Delete)
btn_delete.pack(pady=10)
btn_clear = Button(root, text="Limpar", command=Limpar_Campos)
btn_clear.pack(pady=10)


# Treeview
tree = ttk.Treeview(root, columns=("ID", "Nome", "CPF", "Telefone", "Email"), show="headings", selectmode="browse")
tree.heading('ID', text="ID")
tree.heading('Nome', text="Nome")
tree.heading('CPF', text="CPF")
tree.heading('Telefone', text="Telefone")
tree.heading('Email', text="Email")
tree.pack(pady=20)

# Configurar a função OnSelect para ser chamada quando um item do treeview for selecionado
tree.bind('<<TreeviewSelect>>', OnSelect)

# Inicializar os dados no Treeview
Read()

root.mainloop()
