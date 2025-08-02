-- Tabela medico
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

-- Tabela conversa
CREATE TABLE conversa (
    id_con INT NOT NULL AUTO_INCREMENT,
    tel_conversa VARCHAR(11) NOT NULL,
    status_con VARCHAR(45) NOT NULL,
    dt_criacao_conv DATETIME NOT NULL,
    dt_atualizacao_conv DATETIME NOT NULL,
    medico_id_med INT NOT NULL,

    CONSTRAINT pk_conversa PRIMARY KEY (id_con),
    CONSTRAINT fk_conversa_medico FOREIGN KEY (medico_id_med) REFERENCES medico(id_med)
);

-- Tabela paciente
CREATE TABLE paciente (
    id_pac INT NOT NULL AUTO_INCREMENT,
    nome_pac VARCHAR(150) NOT NULL,
    telefone_pac VARCHAR(11) NOT NULL,
    dt_criacao_pac DATETIME NOT NULL,
    dt_atualizacao_pac DATETIME NOT NULL,
    conversa_id_con INT NOT NULL,

    CONSTRAINT pk_paciente PRIMARY KEY (id_pac),
    CONSTRAINT fk_paciente_conversa FOREIGN KEY (conversa_id_con) REFERENCES conversa(id_con)
);

-- Tabela motivo_atendimento
CREATE TABLE motivo_atendimento (
    id_hist_pac INT NOT NULL AUTO_INCREMENT,
    motivo_hist_pac TEXT NOT NULL,
    dt_men DATETIME NOT NULL,
    dt_criacao_hist_pac DATETIME NOT NULL,
    dt_atualizacao_hist_pac DATETIME,
    conversa_id_con INT NOT NULL,

    CONSTRAINT pk_motivo_atendimento PRIMARY KEY (id_hist_pac),
    CONSTRAINT fk_motivo_conversa FOREIGN KEY (conversa_id_con) REFERENCES conversa(id_con)
);

-- Tabela mensagem
CREATE TABLE mensagem (
    id_men INT NOT NULL AUTO_INCREMENT,
    tipo_men VARCHAR(45) NOT NULL,
    texto TEXT NOT NULL,
    dt_men DATETIME NOT NULL,
    conversa_id_con INT NOT NULL,

    CONSTRAINT pk_mensagem PRIMARY KEY (id_men),
    CONSTRAINT fk_mensagem_conversa FOREIGN KEY (conversa_id_con) REFERENCES conversa(id_con)
);

-- Tabela horario_padrao_med
CREATE TABLE horario_padrao_med (
    id_hor INT NOT NULL AUTO_INCREMENT,
    dia_semana INT NOT NULL,
    hr_inicio_expediente TIME NOT NULL,
    ht_fim_expediente TIME NOT NULL,
    intervalo_minutos_consulta INT NOT NULL,
    hr_inicio_almoco TIME NOT NULL,
    hr_fim_almoco TIME NOT NULL,
    medico_id_med INT NOT NULL,

    CONSTRAINT pk_horario_padrao PRIMARY KEY (id_hor),
    CONSTRAINT fk_horario_medico FOREIGN KEY (medico_id_med) REFERENCES medico(id_med)
);


-- Tabela atendimento
CREATE TABLE atendimento (
    id_aten INT NOT NULL AUTO_INCREMENT,
    dt_criacao DATETIME NOT NULL,
    dt_atualizacao DATETIME NOT NULL,
    status_aten VARCHAR(45) NOT NULL,
    observacoes TEXT,
    conversa_id_con INT NOT NULL,
    medico_id_med INT NOT NULL,

    CONSTRAINT pk_atendimento PRIMARY KEY (id_aten),
    CONSTRAINT fk_atendimento_conversa FOREIGN KEY (conversa_id_con) REFERENCES conversa(id_con),
    CONSTRAINT fk_atendimento_medico FOREIGN KEY (medico_id_med) REFERENCES medico(id_med)
);

-- Tabela agenda_atendimento
CREATE TABLE agenda_atendimento (
    id_disp INT NOT NULL AUTO_INCREMENT,
    data_agen DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    disponivel BOOLEAN NOT NULL, 
    atendimento_id_aten INT NOT NULL,

    CONSTRAINT pk_agenda PRIMARY KEY (id_disp),
    CONSTRAINT fk_atendimento_id_aten FOREIGN KEY (atendimento_id_aten) REFERENCES atendimento(id_aten)
);

