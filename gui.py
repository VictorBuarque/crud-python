from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
from database import Database

class GUI:
    def __init__(self, root):
        #Configurações da tela
        self.root = root
        self.root.title("Cadastro de Usuários")
        self.root.geometry('1440x1297')
        self.root.minsize(800, 600)
        self.root.maxsize(1440, 900)
        self.root.configure(bg="lightblue")

        # Variáveis
        self.nome = StringVar()
        self.cpf = StringVar()
        self.telefone = StringVar()
        self.email = StringVar()

        # Variável auxiliar
        self.selected_item = None

        # Funções
        self.db = Database()

        # Labels e Entradas
        label_nome = Label(root, text="Nome:")
        label_nome.pack(pady=5)
        entry_nome = Entry(root, textvariable=self.nome)
        entry_nome.pack(pady=5)

        label_cpf = Label(root, text="CPF:")
        label_cpf.pack(pady=5)
        entry_cpf = Entry(root, textvariable=self.cpf)
        entry_cpf.pack(pady=5)

        label_telefone = Label(root, text="Telefone:")
        label_telefone.pack(pady=5)
        entry_telefone = Entry(root, textvariable=self.telefone)
        entry_telefone.pack(pady=5)

        label_email = Label(root, text="Email:")
        label_email.pack(pady=5)
        entry_email = Entry(root, textvariable=self.email)
        entry_email.pack(pady=5)

        # Botões
        frame_buttons = Frame(root, bg="lightblue")
        frame_buttons.pack(pady=10)

        btn_create = Button(frame_buttons, text="Salvar", command=self.create)
        btn_create.pack(side=LEFT, padx=10)
        btn_update = Button(frame_buttons, text="Atualizar", command=self.update)
        btn_update.pack(side=LEFT, padx=10)
        btn_delete = Button(frame_buttons, text="Excluir", command=self.delete)
        btn_delete.pack(side=LEFT, padx=10)
        btn_clear = Button(frame_buttons, text="Limpar", command=self.limpar_campos)
        btn_clear.pack(side=LEFT, padx=10)

        # Treeview
        self.tree = ttk.Treeview(root, columns=("ID", "Nome", "CPF", "Telefone", "Email"), show="headings", selectmode="browse")
        self.tree.heading('ID', text="ID", anchor='center')
        self.tree.heading('Nome', text="Nome", anchor='center')
        self.tree.heading('CPF', text="CPF", anchor='center')
        self.tree.heading('Telefone', text="Telefone", anchor='center')
        self.tree.heading('Email', text="Email")
        self.tree.column('ID', anchor='center', width=50, stretch=YES)
        self.tree.column('Nome', anchor='center', width=150, stretch=YES)
        self.tree.column('CPF', anchor='center', width=100, stretch=YES)
        self.tree.column('Telefone', anchor='center', width=100, stretch=YES)
        self.tree.column('Email', anchor='center', width=150, stretch=YES)
        self.tree.pack(fill=BOTH, expand=1)

        # Configurar a função OnSelect para ser chamada quando um item do treeview for selecionado
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Inicializar os dados no Treeview
        self.read()

    def create(self):
        nome = self.nome.get()
        cpf = self.cpf.get()
        telefone = self.telefone.get()
        email = self.email.get()
        if nome == "" or cpf == "" or telefone == "" or email == "":
            tkMessageBox.showerror("Cadastro de Usuários", "Por favor, preencha todos os campos.")
        else:
            self.db.create(nome, cpf, telefone, email)
            tkMessageBox.showinfo("Cadastro de Usuários", "Registro criado com sucesso.")
            self.limpar_campos()
            self.read()

    def read(self):
        self.tree.delete(*self.tree.get_children())
        data = self.db.read()
        for row in data:
            self.tree.insert('', 'end', values=row)

    def on_select(self, event):
        selected_item = self.tree.item(self.tree.selection())
        if selected_item:
            values = selected_item['values']
            self.selected_item = values[0]
            self.nome.set(values[1])
            self.cpf.set(values[2])
            self.telefone.set(values[3])
            self.email.set(values[4])

    def update(self):
        if not self.selected_item:
            tkMessageBox.showerror("Cadastro de Usuários", "Por favor, selecione um registro para atualizar.")
            return
        nome = self.nome.get()
        cpf = self.cpf.get()
        telefone = self.telefone.get()
        email = self.email.get()
        if nome == "" or cpf == "" or telefone == "" or email == "":
            tkMessageBox.showerror("Cadastro de Usuários", "Por favor, preencha todos os campos.")
            return
        self.db.update(self.selected_item, nome, cpf, telefone, email)
        tkMessageBox.showinfo("Cadastro de Usuários", "Registro atualizado com sucesso.")
        self.limpar_campos()
        self.selected_item = None
        self.read()

    def delete(self):
        if not self.selected_item:
            tkMessageBox.showerror("Cadastro de Usuários", "Por favor, selecione um registro para excluir.")
            return
        result = tkMessageBox.askquestion('Cadastro de Usuários', 'Você tem certeza que deseja excluir o registro?', icon="warning")
        if result == 'yes':
            self.db.delete(self.selected_item)
            tkMessageBox.showinfo("Cadastro de Usuários", "Registro excluído com sucesso.")
            self.limpar_campos()
            self.selected_item = None
            self.read()

    def limpar_campos(self):
        self.nome.set("")
        self.cpf.set("")
        self.telefone.set("")
        self.email.set("")


if __name__ == "__main__":
    root = Tk()
    app = GUI(root)
    root.mainloop()
