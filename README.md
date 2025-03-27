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
TENANT_ID=seu-tenant-id
CLIENT_ID=seu-client-id
CLIENT_SECRET=seu-client-secret

USERS={
  "Nome-Usuario1":"ID do usuario 1",
  "Nome-Usuario2":"ID do usuario 2"
}

INTERVAL=60
```

> 🛡️ **Importante:** nunca commit o `.env` com credenciais reais!

### 4. Execute o monitor
```bash
python monitor.py
```

---

## 📊 Exemplo de saída no CSV

Cada arquivo gerado em `data/NOME_USUARIO.csv` conterá:

```csv
Data,Hora,Disponibilidade,Atividade
27/03/2025,14:00:01,Available,InAMeeting
27/03/2025,14:01:01,Busy,InACall
```

---

## 📌 Recomendações

- Execute o script em segundo plano ou via agendador (ex: `pm2`, `cron`, `task scheduler`, etc.)
- Use Power BI ou Excel para criar dashboards com os CSVs

---

## 🤝 Contribuindo

Sinta-se à vontade para abrir *issues* ou enviar *pull requests* com melhorias. 

---

## 📄 Licença

MIT © [Seu Nome / Organização]

---

Com ❤️ para quem precisa monitorar a produtividade com responsabilidade e transparência!
