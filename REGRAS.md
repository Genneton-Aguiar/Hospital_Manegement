Gestão de Usuários:
Cadastro de Usuários:

[CHECK]Permitir o registro de usuários com diferentes papéis (administrador, recepcionista, médico, paciente).
[CHECK]Autenticação JWT: Implementar autenticação via JWT para proteger os endpoints.
[CHECK]Administradores podem gerenciar médicos e pacientes.
[CHECK]Recepcionistas podem gerenciar agendamentos e pacientes.
[]Médicos podem ver seus agendamentos e dados financeiros.

Cadastro de Pacientes:
CRUD de Pacientes:

[CHECK]Permitir o cadastro, edição, visualização e exclusão de pacientes.
[CHECK]Informações do Paciente: Nome, data de nascimento, CPF, telefone, email, endereço.

2. Histórico de Consultas:

[CHECK] Associar cada paciente a um histórico de consultas realizadas.

Agendamento de Consultas:
CRUD de Consultas:

[CHECK]Criar, editar, visualizar e excluir agendamentos de consultas.
[CHECK]Ao criar o agendamento da consulta, ela (consulta) deve ficar com status de agendado enquanto não for realizada.
[CHECK]Informações do Agendamento: Data, hora, paciente, médico responsável, status (agendado, realizado, cancelado).
[CHECK]Validações de Conflitos: Garantir que médicos não tenham dois compromissos ao mesmo tempo.
[CHECK]Realizar consulta: O médico deve ser capaz de mudar o status do atendimento(consulta) para algo que indique foi concluído.


Gestão Financeira:
Registro de Pagamentos:

[CHECK]Associar consultas aos pagamentos recebidos.
[CHECK]Permitir registrar diferentes métodos de pagamento (cartão, dinheiro, transferência).
[CHECK] Realizar o cálculo automático do repasse financeiro ao médico com base nas consultas realizadas e no
percentual acordado para cada médico.


Relatórios Financeiros:
[CHECK] Administradores podem gerar relatórios mensais com o resumo financeiro de receitas e despesas. No relatório deve conter as colunas de: atendimento(consulta), data, medico, paciente, valor pago, método de pagamento.

[CHECK] Relatório financeiro dos médicos: O relatório deve conter, paciente, data do atendimento, valor do pagamento, valor repassado, data do repasse. (acesso único para os médicos)

Observações:

[OK]Os médicos recebem 70% do valor das consultas e a clinica 30%.
[OK]Os administrados são responsáveis por realizar repasses.
[OK]O cadastro de pacientes é de responsabilidade dos recepcionistas (CRUD)
[OK]Os agendamentos são realizados pelos recepcionistas ou médicos.
[OK]Apenas os médicos podem modificar os agendamentos(mudança de data)
[OK]Apenas administrados podem cadastrar, editar ou excluir médicos.
[OK]Apenas administrados podem acessar as informações financeiras gerais.
[OK]Os médicos podem acesso as suas consultas realizadas e repasses recebidos


