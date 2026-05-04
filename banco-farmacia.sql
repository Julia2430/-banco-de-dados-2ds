CREATE TABLE FARMACIA 
( 
    CNPJ_farmacia INT PRIMARY KEY,  
    tel_farmacia VARCHAR(20),  
    nome_farmacia VARCHAR(100),  
    end_farmacia VARCHAR(200)  
); 

CREATE TABLE PRODUTO 
( 
    cod_produto INT PRIMARY KEY,  
    CNPJ_farmacia INT,  
    qtd_produto INT,  
    valor_produto DECIMAL(10,2),  
    FOREIGN KEY (CNPJ_farmacia) REFERENCES FARMACIA (CNPJ_farmacia)
); 

CREATE TABLE FARMACEUTICO 
( 
    RG_farmaceutico INT PRIMARY KEY,  
    CNPJ_farmacia INT,  
    nome_farmaceutico VARCHAR(100),  
    FOREIGN KEY (CNPJ_farmacia) REFERENCES FARMACIA (CNPJ_farmacia)
); 

