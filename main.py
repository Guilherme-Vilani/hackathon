from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

class Atendimento(BaseModel):
    cliente: str
    telefone: int
    descricao_equipamento: str
    tecnico_responsavel: str


atendimentos = []

@app.get("/consulta-atendimentos")
async def consulta_atendimentos():
    return atendimentos

@app.get("/consulta-atendimento-telefone")
async def consulta_atendimentos_telefone(telefone: int):
    # Filtrar os atendimentos com o número de telefone correspondente
    resultado = [
        atendimento for atendimento 
        in atendimentos 
        if atendimento.telefone == telefone
        ]
    return resultado


@app.get("/consulta-atendimento-nome")
async def consulta_atendimentos_nome(nome: str):
    # Filtrar os atendimentos com o número de telefone correspondente
    resultado = [
        atendimento for atendimento 
        in atendimentos 
        if atendimento.cliente == nome
    ]
    return resultado


@app.put("/cadastra-atendimento")
async def cadastra_atendimento(body: Atendimento):
    
    atendimentos.append(body)
    
    return body

#COMENTOD

# Rota para alterar o atendimento
@app.post("/altera-registro-atendimento")
async def atualiza_atendimento(telefone: int, body: Atendimento):
    # Verificar se o atendimento com o telefone existe
    for i, atendimento in enumerate(atendimentos):
        if atendimento.telefone == telefone:
            # Atualizar o registro encontrado
            atendimentos[i] = body
            return {"message": "Atendimento atualizado com sucesso", "atendimento": body}
    
    # Se não encontrar o atendimento, lançar exceção
    raise HTTPException(status_code=404, detail="Atendimento não encontrado")