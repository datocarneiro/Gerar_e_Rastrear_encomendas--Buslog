from consultar_tracking.consultar_objeto import rastrear_objeto
from gerar_encomenda.m_gerar_encomenda import gerar_encomenda
from cotacao.cotar_frete import realizar_cotação
from authentication.authenticate import registra_usuario
from export_arquivo_base.export import base_arquivo, base_arquivo_cotacao
from consultar_emissao.consultar_bd import consultar_banco
from fiscal.docfiscal import get_doc_fiscal
from PIL import Image, ImageTk
from tkinter import Label, Entry, ttk
import tkinter as tk
import os

def interface(chave_session):
    app = tk.Tk()
    # Define o tamanho da janela
    largura = 1100
    altura = 700

    # Obtém a largura e altura da tela do usuário
    largura_tela = app.winfo_screenwidth()
    altura_tela = app.winfo_screenheight()

    # Calcula a posição x e y para centralizar a janela na tela
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)

    # Define a geometria da janela
    app.geometry(f'{largura}x{altura}+{pos_x}+{pos_y}')
    app.title("Dato® || Gerar e Rastrear encomendas - Buslogs")
    app.configure(background='#273142')

    # Nome e Input Usuario
    bold_font = ('Arial', 14, 'bold')  # Substitua 'Arial' pelo nome da fonte que você deseja usar

    margem_direita = 37  # Aproximadamente 1 cm em pixels
    marca = Label(app, text='dato®', background='#273142', foreground='#ffae00', font=bold_font)
    marca.place(relx=1.0, x=-margem_direita, y=10, anchor='ne')

    usuario = Label(app, text='Usuário', background='#273142', foreground='#ffae00', font=bold_font, anchor='w')
    usuario.place(x=20,y=60, width=100, height=20)
    input_usuario = Entry(app, background='#dde', foreground='#161616',font=5)
    input_usuario.place(x=20,y=90,width=300, height=35,)
    btn_gravar_usuario = tk.Button(app, text="Registrar usuário", background='#3f8f57', foreground='#fff', command=lambda:registra_usuario(input_usuario.get()), width=13, height=1)
    btn_gravar_usuario.place(x=218,y=129)

    texto = 'O layout da planilha, deve estar como a base abaixo:'
    texto_base = Label(app, text=texto, background='#273142', foreground='#dde',anchor='w')
    texto_base.place(x=20,y=240, width=300, height=20)

    # Carrega a imagem e redimensiona
    imagem_original = Image.open("bases/imagens/base_planilha.png")
    imagem_redimensionada = imagem_original.resize((330, 110))  # Altere o tamanho conforme necessário
    imagem = ImageTk.PhotoImage(imagem_redimensionada)
    # Cria um widget Label para exibir a imagem com tamanho e posição controlados
    label_imagem = Label(app, image=imagem)
    label_imagem.place(x=20, y=280, width=330, height=110)  # Controla a posição e o tamanho

    texto_obrigatorio = "** Campos obrigatórios: 'FRANQUIA' e 'ORDEM'."
    texto_obrigatorio = Label(app, text=texto_obrigatorio, background='#273142', foreground='#dde',anchor='w')
    texto_obrigatorio.place(x=20,y=258, width=400, height=20)

    # Botão Rastrear
    btn_rastrear_objeto = tk.Button(app, text="Rastrear", background='#dde', font=5, command=lambda: rastrear_objeto(input_usuario.get(), progress_label, progress_label_descricao), width=20, height=2)
    btn_rastrear_objeto.pack(pady=(150, 5))

    # Botão Gerar encomenda
    btn_gerar_encomenda = tk.Button(app, text="Gerar encomendas", background='#dde',font=5,command=lambda: gerar_encomenda(chave_session, input_usuario.get(), progress_label , progress_label_descricao), width=20, height=2)
    btn_gerar_encomenda.pack(pady=(35, 25))

    
    # Botão Cotação
    btn_cotacao = tk.Button(app, text="Cotação", background='#dde',font=5,command=lambda: realizar_cotação(input_usuario.get(), progress_label, progress_label_descricao), width=15, height=1)
    btn_cotacao.pack(pady=(35, 5))
    
    # Botão para exportar arquivo
    btn_exportar = tk.Button(app, text="Baixe a planilha base aqui", background='#ffae00',command=lambda:base_arquivo())
    # btn_exportar.pack(pady=(30, 5))
    btn_exportar.place(x=40,y=400, width=200, height=20)

    # Botão para exportar arquivo
    btn_exportar = tk.Button(app, text="Baixe a base para cotação", background='#ffae00',command=lambda:base_arquivo_cotacao())
    btn_exportar.pack(pady=(1, 5))
    # btn_exportar.place(x=40,y=480, width=200, height=20)
    
    # Documento fiscal
    btn_doc_fiscal = tk.Button(app, text="Doc Fiscal", background='#dde',font=5,command=lambda: get_doc_fiscal(input_usuario.get()), width=15, height=1)
    btn_doc_fiscal.pack(pady=(35, 5))

    # # Criar Barra de Progressbar com o estilo personalizado
    # progress = ttk.Progressbar(app, orient='horizontal', length=600, mode='determinate', style="TProgressbar")
    # progress.pack(pady=(5, 5))

    # Label para mostrar o progresso (Ex: "3/10")
    progress_label = Label(app, text="", background='#273142', foreground='#ffae00', font=bold_font)
    progress_label.pack(pady=(10, 2))  # Mantém a barra com um espaçamento menor

    # Label para exibir a descrição logo abaixo
    progress_label_descricao = Label(app, text="Aguardando...", background='#273142', foreground='#dde')
    progress_label_descricao.pack(pady=(2, 10))  # Mantém a descrição logo abaixo da barra 


    consulta_emissão = Label(app, text="Log's emissão, consultar por numero de ordem", background='#273142', foreground='#ffae00', anchor='e')
    # consulta_emissão.place(x=410,y=670)
    consulta_emissão.pack(pady=(1, 1))

    input_consulta_emissão = Entry(app, background='#dde', foreground='#161616', font=1)
    # input_consulta_emissão.place(x=430,y=640)
    input_consulta_emissão.pack(pady=(1, 1))

    btn_consulta_emissão = tk.Button(app, text="Buscar", background='#3f8f57', foreground='#fff', command=lambda:consultar_banco(input_consulta_emissão.get()), width=9, height=1)
    btn_consulta_emissão.place(x=581,y=641)
    btn_consulta_emissão.pack(pady=(1, 1))

    # Estilo para personalizar a Progressbar
    style = ttk.Style()
    # Definir o estilo da Progressbar com uma cor de fundo (#dde) e progresso verde
    style.theme_use('clam')  # Modo de estilo que permite personalizações
    style.configure("TProgressbar",
                    troughcolor='#273142',  # Cor de fundo (fundo da barra)
                    background='green',  # Cor do progresso
                    thickness=80,  # Altura da barra
                    borderwidth=1)  # Remove a borda
    

    app.mainloop()