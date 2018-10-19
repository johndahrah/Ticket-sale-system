CREATE TABLE IF NOT EXISTS Organizers (
  ID                INTEGER NOT NULL, 
  Name             varchar(255) NOT NULL,
  Address          varchar(255) NOT NULL,
  HasOpenedTickets INT,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Coupons (
  ID             INTEGER NOT NULL,
  DateUsed      varchar(255) NOT NULL,
  UsedInCheckID INT NOT NULL,
  CouponData    varchar(255) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Checks (
  ID            INTEGER NOT NULL,
  TicketsAmount INT NOT NULL,
  TicketsPrice  FLOAT NOT NULL,
  TotalPrice    FLOAT NOT NULL,
  CouponUsed    INT NOT NULL,
  CouponID      INT NOT NULL,
  WorkerID      INT NOT NULL,
  PRIMARY KEY (ID), 
  FOREIGN KEY(CouponID) REFERENCES Coupons(ID)
);

CREATE TABLE IF NOT EXISTS Tickets (
  ID                    INTEGER NOT NULL,
  OpenedForSelling      INT NOT NULL,
  OrderNumber           INT NOT NULL,
  EventDate             varchar(255),
  EventTime             varchar(255),
  EventPlace            varchar(255),
  EventOrganizerName    varchar(255),
  EventOrganizerAddress varchar(255),
  SellPrice             FLOAT NOT NULL,
  Comment               varchar(255),
  EventOrganizerID      INT NOT NULL,
  ticketID              INT NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY(EventOrganizerID) REFERENCES Organizers(ID),
  FOREIGN KEY(ticketID) REFERENCES Checks(ID)
);

CREATE TABLE IF NOT EXISTS Secure (
  ID          SERIAL NOT NULL,
  Login       varchar(255),
  Password    varchar(255), 
  AccessLevel INT NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Check_ticketsID (
  CheckID    INT NOT NULL,
  TicketsID  INT NOT NULL,
  PRIMARY KEY (CheckID)
);
