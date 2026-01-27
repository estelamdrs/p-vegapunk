# 🏦 Vegapunk Payments API

Backend robusto para processamento de transações financeiras entre usuários, focado em integridade de dados e segurança contra condições de corrida (_Race Conditions_).

## 🎯 Destaques Técnicos

Este projeto vai além do básico, implementando padrões de engenharia de software para garantir a confiabilidade financeira:

- **Integridade Transacional (ACID):** Uso de `transaction.atomic()` para garantir que débitos e créditos ocorram simultaneamente ou falhem juntos.
- **Controle de Concorrência (Optimistic Locking):** Implementação de versionamento no banco de dados para impedir que duas requisições simultâneas alterem o mesmo saldo erroneamente.
- **Segurança (Idempotência):** Suporte a chaves de idempotência (`idempotency_id`) para evitar duplicidade de pagamentos em caso de falhas de rede.
- **Database Constraints:** Uso de `CheckConstraint` no nível do banco de dados para garantir que saldos nunca fiquem negativos, servindo como uma segunda camada de defesa além da aplicação.
- **Arquitetura Modular:** Separação clara de responsabilidades entre identidade (`apps/core`) e domínio financeiro (`apps/payments`).

## 🛠️ Tecnologias

- **Linguagem:** Python 3.x
- **Framework:** Django Rest Framework / Django
- **Banco de Dados:** MySQL / Extensível para PostgreSQL
- **Autenticação:** Custom User Model (CPF/Email)

## 🏗 Estrutura do Projeto

```text
├── apps/
│   ├── core/      # Gerenciamento de Identidade (User, Auth)
│   └── payments/  # Lógica Financeira (Wallet, Transaction, Locking)
├── config/        # Configurações globais do Django
├── requirements.txt
└── manage.py
```
