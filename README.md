# 👥 Microsoft Teams Presence Monitor

Este projeto monitora em tempo real o status (presença) de um grupo específico de usuários do Microsoft Teams, utilizando a **Microsoft Graph API**.

Ele registra a **disponibilidade** e **atividade** de cada usuário, salvando os dados em **arquivos CSV individuais**, formando uma **linha do tempo diária** para análise posterior (como tempo online, em reunião, ocupado, etc).

---

## 🚀 Funcionalidades

- Monitoramento contínuo de múltiplos usuários (por ID)
- Armazenamento dos dados em CSV, por usuário
- Atualizações a cada minuto (ou tempo configurável)
- Código limpo e modular com autenticação via Graph API
- Ideal para geração de relatórios para gestão/diretoria

---

## 📂 Estrutura do Projeto

```plaintext
teams-monitor/
├── monitor.py              # Script principal de monitoramento
├── .env                    # Dados sensíveis e configurações (NÃO versionar!)
├── .env.example            # Modelo de variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── .gitignore              # Ignora arquivos sensíveis e CSVs
├── data/                   # CSVs com os relatórios de cada usuário
└── utils/
    └── graph_api.py        # Funções de autenticação e consulta à API
```

---

## 🧪 Pré-requisitos

- Python 3.7+
- Uma conta com permissão de administrador no Microsoft 365
- Um aplicativo registrado no **Azure Portal** com as permissões:
  - `Presence.Read.All` (**Application**)
  - `User.Read.All` (**Application**)


---

## 🔧 Como usar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/teams-monitor.git
cd teams-monitor
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o `.env`
Crie um arquivo `.env` na raiz com base no `.env.example`:

```env
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret

USERS={"Nome1":"ID1","Nome2":"ID2","Nome3":"ID3"}

INTERVAL=60

GERAL_PATH=Caminho-para-a-pasta-onde-o-arquivo-geral-de-status-será-salvo,-os-arquivos-de-status-individuais-serão-salvos-na-mesma-pasta,-mas-com-o-nome-do-usuário.

EMAIL_REMETENTE=Email-do-remetente
EMAIL_SENHA=Senha-do-email-do-remetente
EMAIL_DESTINATARIO=Email-do-destinatário
```

> 🛡️ **Importante:** nunca commit o `.env` com credenciais reais!

> Coloque o `.env` no `.gitignore` para proteger credenciais sensíveis.

### 4. Execute o monitor
```bash
python monitor.py
```

---

## ✉️ Exemplo do e-mail de erro
Se o monitoramento falhar ao tentar renovar o token ou iniciar o ciclo, o sistema envia um alerta por e-mail:

![Email de Erro](https://via.placeholder.com/600x300.png?text=Exemplo+de+Email+HTML+de+Erro)

### 💡 Layout do e-mail:
- Título com ícone de alerta
- Data e hora do erro
- Detalhes do erro ocorrido
- Aviso visual em vermelho

Apenas **um e-mail é enviado por falha**. Quando o sistema se recupera, o envio é reabilitado.

---

## 📊 Exemplo de saída no CSV

Cada arquivo gerado em `data/NOME_USUARIO.csv` conterá:

```csv
Data,Hora,Disponibilidade,Atividade
27/03/2025,14:00:01,Available,InAMeeting
27/03/2025,14:01:01,Busy,InACall
```

---

## 🕐 Horário de execução
- Segunda a sexta-feira
- Das 08:00 às 17:59
- Fora desse período, o monitoramento é pausado automaticamente

---

## 📌 Recomendações

- Execute o script em segundo plano ou via agendador (ex: `pm2`, `cron`, `task scheduler`, etc.)
- Use Power BI ou Excel para criar dashboards com os CSVs

---

## 📄 Licença

MIT © [Davi Mendes / Celer Biotecnologia]

