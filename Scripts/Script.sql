-- Tabla de clientes
CREATE TABLE Customer (
    idCustomer VARCHAR(500) PRIMARY KEY,
    creation_date DATE,
    customer_name VARCHAR(500),
    email VARCHAR(200),
    referral_source VARCHAR(50)
);

-- Tabla de ítems
CREATE TABLE Item (
    idItem SERIAL PRIMARY KEY,
	item_name VARCHAR(100) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL
);

-- Tabla de colaboradores
CREATE TABLE Collaborator (
    idCollaborator VARCHAR(50) PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Sales
CREATE TABLE Sales (
    idSale SERIAL PRIMARY KEY,
    idItem SERIAL NOT NULL,
    idCustomer VARCHAR(500) NOT NULL,
    idCollaborator VARCHAR(50),
    payment_type VARCHAR(200),
    sale_date timestamp NOT NULL,
    quantity INT NOT NULL,
    total_amount FLOAT NOT NULL,
    CONSTRAINT fk_item FOREIGN KEY (idItem) REFERENCES Item(idItem),
    CONSTRAINT fk_customer FOREIGN KEY (idCustomer) REFERENCES Customer(idCustomer),
    CONSTRAINT fk_collaborator FOREIGN KEY (idCollaborator) REFERENCES Collaborator(idCollaborator)
);