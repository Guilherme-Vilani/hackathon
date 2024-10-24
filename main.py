from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
from typing import List

app = FastAPI()

class Registro(BaseModel):
    nome:str
    telefone:str
    serie:str
    dt_nasc:str

# Defina os domínios permitidos
origins = [
    "http://localhost",
    "http://localhost:3000",  # Exemplo de uma URL front-end em React
    "*",  # Para permitir o acesso de qualquer origem (não recomendado em produção)
]

# Configurar o middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite essas origens
    allow_credentials=True,  # Permite envio de credenciais (cookies, cabeçalhos HTTP)
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

@app.put("/inserir-dados")
def inserir_registro(body: Registro):
    # Nome do arquivo CSV
    arquivo_csv = "dados.csv"
    
    # Abra o arquivo em modo append (adicionar)
    with open(arquivo_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Escreva o cabeçalho se o arquivo estiver vazio
        if file.tell() == 0:
            writer.writerow(["nome", "telefone", "serie", "dt_nasc"])
        
        # Escreva os dados do registro
        writer.writerow([body.nome, body.telefone, body.serie, body.dt_nasc])
    
    return {"message": "Registro inserido com sucesso!"}

# Rota para listar todos os registros do CSV
@app.get("/listar-dados", response_model=List[Registro])
def listar_dados():
    registros = []
    arquivo_csv = "dados.csv"
    
    try:
        with open(arquivo_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                registros.append(Registro(**row))
    except FileNotFoundError:
        return {"message": "Nenhum registro encontrado!"}
    
    return registros