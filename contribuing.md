📘 Guia de Colaboração com Git \& GitHub para o Projeto de Forecast

Este documento é o guia oficial para contribuir com o projeto. Seguir estes passos garante que o trabalho seja organizado, rastreável e que a qualidade do nosso código principal seja mantida.



A Regra de Ouro: Ninguém, nem mesmo o dono do projeto, envia alterações diretamente para a branch main. Todo o trabalho é feito em cópias e branches separadas, e integrado através de Pull Requests.



🎭 Os Papéis no Projeto

Temos dois papéis principais neste fluxo de trabalho:



O Mantenedor (Dono do Projeto):



Responsável por revisar as contribuições (Pull Requests).



Tirar dúvidas sobre o código proposto.



Aprovar e integrar (merge) as contribuições ao projeto principal.



Gerenciar as tarefas e o direcionamento do projeto na aba "Issues".



O Colaborador (Membros da Equipe):



Responsável por executar uma tarefa específica em uma "branch" isolada.



Propor sua contribuição através de um "Pull Request" detalhado.



Realizar os ajustes solicitados pelo Mantenedor.



🚀 Fluxo de Trabalho do Colaborador

Este é o passo a passo para qualquer membro da equipe que queira adicionar uma nova funcionalidade, análise ou correção.



(A) Preparação Inicial (Feita apenas uma vez)

🍴 Passo 1: Faça o Fork (Sua Cópia Pessoal)

Crie uma cópia completa do repositório principal na sua própria conta do GitHub.



Acesse a página do repositório principal: https://github.com/Flavio-AzL/Projeto\_Forecast\_Varejo-com\_IA



Clique no botão Fork no canto superior direito.



💻 Passo 2: Clone o SEU Fork para o Computador

Baixe o código da sua cópia para a sua máquina local.



Vá para a página do seu fork (ex: github.com/SEU\_USUARIO/Projeto...).



Clique no botão verde <> Code.



Copie a URL HTTPS.



No terminal, execute:



Bash



git clone URL\_COPIADA\_DO\_SEU\_FORK

(B) O Ciclo de Contribuição (Para cada nova tarefa)

🌿 Passo 3: Crie uma Branch para a Tarefa

Nunca trabalhe na branch main. Para cada nova tarefa, crie um "ramo" de trabalho isolado.



Navegue para a pasta do projeto no seu computador.



Execute o comando, usando um nome descritivo para a tarefa:



Bash



\# Exemplo: git checkout -b feature/cria-grafico-vendas

git checkout -b nome-da-sua-branch

✍️ Passo 4: Realize o Trabalho

Agora é a hora de codificar! Abra o projeto no VS Code, edite os arquivos, crie novas análises, etc.



💾 Passo 5: Salve e Envie o Progresso (para o seu Fork)

Quando terminar a tarefa (ou uma parte importante dela), salve seu progresso no Git e envie para o seu fork no GitHub.



Adicione os arquivos modificados:



Bash



git add .

Crie um "ponto de salvamento" com uma mensagem clara:



Bash



git commit -m "O que você fez (ex: Adiciona gráfico de vendas por loja)"

Envie as alterações para a sua branch no seu fork:



Bash



git push origin nome-da-sua-branch

📬 Passo 6: Abra um Pull Request (O Pedido de Contribuição)

Peça formalmente para que o Mantenedor revise e integre seu trabalho ao projeto principal.



Vá para a página do seu fork no GitHub.



O GitHub mostrará um aviso para criar um Pull Request. Clique no botão Contribute e depois em Open a pull request.



Escreva um título claro e uma descrição detalhada das suas alterações.



Clique em Create pull request. Parabéns, sua contribuição foi proposta!



✅ Fluxo de Trabalho do Mantenedor

Este é o passo a passo para o dono do projeto revisar e integrar as contribuições.



🔔 Passo 1: Receba a Notificação do Pull Request

O GitHub irá te notificar por e-mail e na própria plataforma. Acesse a aba Pull Requests no seu repositório.



👀 Passo 2: Revise as Alterações

Analise o código proposto para garantir a qualidade e o alinhamento com os objetivos do projeto.



Abra o Pull Request.



Leia a descrição para entender o objetivo das mudanças.



Vá para a aba Files Changed para ver o "antes e depois" do código.



Se necessário, deixe comentários em linhas específicas para pedir ajustes ou tirar dúvidas.



✔️ Passo 3: Aprove e Integre (Merge)

Se o código estiver bom, é hora de incorporá-lo ao projeto principal.



Volte para a aba Conversation.



Clique no botão verde Merge pull request.



Confirme o merge.



(Opcional, mas recomendado) Delete a branch da contribuição para manter o repositório limpo.



📋 Organização de Tarefas com "Issues"

Para que todos saibam o que precisa ser feito e quem está trabalhando em quê, devemos usar a aba Issues do GitHub.



Criação: O Mantenedor (ou qualquer membro) pode criar uma nova Issue para cada tarefa (ex: "Tratar dados faltantes da coluna CPI").



Atribuição: O Mantenedor pode atribuir (assign) a Issue a um colaborador específico.



Referência: Ao fazer um commit, o colaborador pode referenciar a Issue (ex: git commit -m "Finaliza tratamento de CPI. Closes #12"), o que cria um link automático entre o código e a tarefa.

