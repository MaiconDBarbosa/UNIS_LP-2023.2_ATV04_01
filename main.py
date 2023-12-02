import tkinter as tk
from tkinter import messagebox
import mysql.connector

def conectar_bd():
    # Substitua 'root' e '' pela senha do seu banco de dados MySQL
    conexao_bd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ATV04_LG_UNIS"
    )
    return conexao_bd

def criar_tabelas():
    conexao_bd = conectar_bd()
    cursor = conexao_bd.cursor()

    # Criar tabela Dados_usuario se não existir
    criar_tabela_usuario_query = """
    CREATE TABLE IF NOT EXISTS Dados_usuario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(50) NOT NULL,
        endereco VARCHAR(100)
    )
    """
    cursor.execute(criar_tabela_usuario_query)

    # Criar tabela Calculo_IMC se não existir
    criar_tabela_imc_query = """
    CREATE TABLE IF NOT EXISTS Calculo_IMC (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        altura FLOAT NOT NULL,
        peso FLOAT NOT NULL,
        imc FLOAT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES Dados_usuario(id)
    )
    """
    cursor.execute(criar_tabela_imc_query)

    conexao_bd.commit()
    cursor.close()
    conexao_bd.close()

def salvar_dados_usuario(nome, endereco):
    conexao_bd = conectar_bd()
    cursor = conexao_bd.cursor()

    inserir_dados_query = "INSERT INTO Dados_usuario (nome, endereco) VALUES (%s, %s)"
    dados = (nome, endereco)
    cursor.execute(inserir_dados_query, dados)
    conexao_bd.commit()

    usuario_id = cursor.lastrowid  # Obtém o ID do usuário recém-inserido

    cursor.close()
    conexao_bd.close()

    return usuario_id

def salvar_calculo_imc(usuario_id, altura, peso, imc):
    conexao_bd = conectar_bd()
    cursor = conexao_bd.cursor()

    inserir_calculo_query = "INSERT INTO Calculo_IMC (usuario_id, altura, peso, imc) VALUES (%s, %s, %s, %s)"
    dados_calculo = (usuario_id, altura, peso, imc)
    cursor.execute(inserir_calculo_query, dados_calculo)
    conexao_bd.commit()

    cursor.close()
    conexao_bd.close()

def calcular_imc():
    try:
        nome = entry_nome.get()
        endereco = entry_endereco.get()
        peso = float(entry_peso.get())
        altura = float(entry_altura.get()) / 100  # Convertendo altura para metros
        imc = peso / (altura ** 2)

        resultado = f"IMC: {imc:.2f} - {classificar_imc(imc)}"

        # Salvar dados do usuário e cálculo do IMC no banco de dados
        usuario_id = salvar_dados_usuario(nome, endereco)
        salvar_calculo_imc(usuario_id, altura, peso, imc)

        # Atualizando o rótulo de resultado
        label_resultado.config(text=resultado)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos para peso e altura.")

def classificar_imc(imc):
    if imc < 16.00:
        return "Magreza Grau III"
    elif 16.00 <= imc < 16.99:
        return "Magreza Grau II"
    elif 17.00 <= imc < 18.49:
        return "Magreza Grau I"
    elif 18.50 <= imc < 24.99:
        return "Normal"
    elif 25.00 <= imc < 29.99:
        return "Sobrepeso"
    elif 30.00 <= imc < 34.99:
        return "Obesidade Grau I"
    elif 35.00 <= imc < 39.99:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def reiniciar():
    entry_nome.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_altura.delete(0, tk.END)
    entry_peso.delete(0, tk.END)
    label_resultado.config(text="Resultado")

# Criando a janela principal
root = tk.Tk()
root.title("Calculadora de IMC")

# Criando os widgets
label_nome = tk.Label(root, text="Nome do Paciente:")
entry_nome = tk.Entry(root)

label_endereco = tk.Label(root, text="Endereço Completo:")
entry_endereco = tk.Entry(root)

label_altura = tk.Label(root, text="Altura (cm):")
entry_altura = tk.Entry(root)

label_peso = tk.Label(root, text="Peso (Kg):")
entry_peso = tk.Entry(root)

label_resultado = tk.Label(root, text="Resultado")

botao_calcular = tk.Button(root, text="Calcular", command=calcular_imc)
botao_reiniciar = tk.Button(root, text="Reiniciar", command=reiniciar)
botao_sair = tk.Button(root, text="Sair", command=root.destroy)

# Criar tabelas no banco de dados
criar_tabelas()

# Posicionando os widgets na grade
label_nome.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_endereco.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
entry_endereco.grid(row=1, column=1, padx=10, pady=5)

label_altura.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
entry_altura.grid(row=2, column=1, padx=10, pady=5)

label_peso.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
entry_peso.grid(row=3, column=1, padx=10, pady=5)

label_resultado.grid(row=4, column=0, columnspan=2, pady=10)

botao_calcular.grid(row=5, column=0, pady=10)
botao_reiniciar.grid(row=5, column=1, pady=10)
botao_sair.grid(row=6, column=0, columnspan=2, pady=10)

# Iniciando o loop principal da interface gráfica
root.mainloop()
