
-- Tabela de médicos
CREATE TABLE medico (
    id_med INT NOT NULL AUTO_INCREMENT,
    nome_med VARCHAR(150) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    email VARCHAR(45) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    dt_criacao DATETIME NOT NULL,
    dt_atualizacao DATETIME NOT NULL,

    CONSTRAINT pk_medico PRIMARY KEY (id_med)
);

-- Tabela de pacientes
CREATE TABLE paciente (
    id_pac INT NOT NULL AUTO_INCREMENT,
    nome_pac VARCHAR(150) NOT NULL,
    telefone_pac VARCHAR(11) NOT NULL,
    dt_criacao_pac DATETIME NOT NULL,
    dt_atualizacao_pac DATETIME,

    CONSTRAINT pk_paciente PRIMARY KEY (id_pac)
);

-- Tabela de motivos de atendimento
CREATE TABLE motivo_atendimento (
    id_mot_aten INT NOT NULL AUTO_INCREMENT,
    gravidade ENUM('Leve', 'Moderado', 'Grave') NOT NULL,
    motivo_mot_aten TEXT NOT NULL,
    especialidade_destino VARCHAR(45),
    dt_criacao_mot_aten DATETIME NOT NULL,
    dt_atualizacao_mot_aten DATETIME,

    CONSTRAINT pk_motivo_atendimento PRIMARY KEY (id_mot_aten)
);

-- Tabela de conversas
CREATE TABLE conversa (
    id_conversa INT NOT NULL AUTO_INCREMENT,
    tel_conversa VARCHAR(11) NOT NULL,
    dt_criacao_conv DATETIME NOT NULL,
    dt_atualizacao_conv DATETIME NOT NULL,
    medico_id_med INT NOT NULL,

    CONSTRAINT pk_conversa PRIMARY KEY (id_conversa),
    CONSTRAINT fk_conversa_medico FOREIGN KEY (medico_id_med) REFERENCES medico(id_med)
);

-- Tabela de mensagens
CREATE TABLE mensagem (
    id_men INT NOT NULL AUTO_INCREMENT,
    tipo_men VARCHAR(45) NOT NULL,
    texto TEXT NOT NULL,
    dt_men DATETIME NOT NULL,
    conversa_id_conversa INT NOT NULL,

    CONSTRAINT pk_mensagem PRIMARY KEY (id_men),
    CONSTRAINT fk_mensagem_conversa FOREIGN KEY (conversa_id_conversa) REFERENCES conversa(id_conversa)
);

-- Tabela de atendimentos
CREATE TABLE atendimento (
    id_aten INT NOT NULL AUTO_INCREMENT,
    dt_atendimento DATETIME NOT NULL,
    dt_criacao DATETIME NOT NULL,
    dt_atualizacao DATETIME NOT NULL, 
    status_aten VARCHAR(45) NOT NULL,
    observacoes TEXT,
    conversa_id_conversa INT NOT NULL,
    paciente_id_pac INT NOT NULL, 
    historico_paciente_id_hist_pac INT NOT NULL,
    medico_id_med INT NOT NULL,

    CONSTRAINT pk_atendimento PRIMARY KEY (id_aten),
    CONSTRAINT fk_atendimento_conversa FOREIGN KEY (conversa_id_conversa) REFERENCES conversa(id_conversa),
    CONSTRAINT fk_atendimento_paciente FOREIGN KEY (paciente_id_pac) REFERENCES paciente(id_pac),
    CONSTRAINT fk_atendimento_motivo_atendimento FOREIGN KEY (historico_paciente_id_hist_pac) REFERENCES motivo_atendimento(id_mot_aten),
    CONSTRAINT fk_atendimento_medico FOREIGN KEY (medico_id_med) REFERENCES medico(id_med)
);
