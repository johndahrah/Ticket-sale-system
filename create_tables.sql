CREATE TABLE IF NOT EXISTS Organizers (
  ID       INTEGER NOT NULL,
  Name     varchar(255) NOT NULL,
  Address  varchar(255) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Coupons (
  ID            SERIAL NOT NULL,
  DateUsed      varchar(255) NOT NULL,
  UsedInCheckID INT NOT NULL,
  CouponData    varchar(255) NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Users (
  ID          SERIAL NOT NULL,
  Login       varchar(255),
  Password    varchar(255),
  AccessLevel INT NOT NULL,
  PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Checks (
  ID            SERIAL NOT NULL,
  TicketsAmount INT NOT NULL,
  TotalPrice    FLOAT NOT NULL,
  CouponUsed    BOOLEAN NOT NULL,
  CouponID      INT,
  WorkerID      INT NOT NULL,
  PRIMARY KEY (ID), 
  FOREIGN KEY(CouponID) REFERENCES Coupons(ID),
  FOREIGN KEY(WorkerID) REFERENCES Users (ID)
);

CREATE TABLE IF NOT EXISTS Tickets (
  ID                    SERIAL NOT NULL,
  OpenedForSelling      BOOLEAN NOT NULL,
  EventDate             varchar(255),
  EventTime             varchar(255),
  EventPlace            varchar(255),
  EventOrganizerName    varchar(255),
  SellPrice             INT NOT NULL,
  Comment               varchar(255),
  OrganizerID           INT NOT NULL,
  SerialNumber          varchar(255) NOT NULL,
  isSold                BOOLEAN NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY(OrganizerID) REFERENCES Organizers(ID)
);

CREATE TABLE IF NOT EXISTS Check_ticketsID (
  CheckID    INT NOT NULL,
  TicketID  INT NOT NULL,
  PRIMARY KEY (CheckID),
  FOREIGN KEY (TicketID) REFERENCES Tickets(ID)
);
