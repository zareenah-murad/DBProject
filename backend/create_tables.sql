-- Active: 1746420074469@@127.0.0.1@3306@db_project
USE db_project;

SET FOREIGN_KEY_CHECKS = 0;

-- Drop if exists
DROP TABLE IF EXISTS AnalysisResult;
DROP TABLE IF EXISTS Field;
DROP TABLE IF EXISTS Project;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Institute;
DROP TABLE IF EXISTS SocialMedia;

-- Create SocialMedia table
CREATE TABLE SocialMedia (
    MediaName VARCHAR(100) PRIMARY KEY
);

-- Create Institute table
CREATE TABLE Institute (
    InstituteName VARCHAR(100) PRIMARY KEY
);

-- Create Users table
CREATE TABLE Users (
    UserID VARCHAR(100),
    Username VARCHAR(100) NOT NULL,
    MediaName VARCHAR(100) NOT NULL,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    BirthCountry VARCHAR(100),
    ResidenceCountry VARCHAR(100),
    Age INT,
    Gender VARCHAR(50),
    IsVerified BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (UserID),
    FOREIGN KEY (MediaName) REFERENCES SocialMedia(MediaName)
);

-- Create Posts table
CREATE TABLE Posts (
    PostID VARCHAR(100),
    UserID VARCHAR(100) NOT NULL,
    PostText TEXT NOT NULL,
    PostDateTime DATETIME NOT NULL,
    RepostedByUserID VARCHAR(100),
    RepostDateTime DATETIME,
    City VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100),
    Likes INT,
    Dislikes INT,
    HasMultimedia BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (PostID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (RepostedByUserID) REFERENCES Users(UserID)
);

-- Create Project table
CREATE TABLE Project (
    ProjectName VARCHAR(100) PRIMARY KEY,
    ManagerFirstName VARCHAR(100) NOT NULL,
    ManagerLastName VARCHAR(100) NOT NULL,
    InstituteName VARCHAR(100) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    FOREIGN KEY (InstituteName) REFERENCES Institute(InstituteName)
);

-- Create Field table
CREATE TABLE Field (
    FieldName VARCHAR(100),
    ProjectName VARCHAR(100),
    PRIMARY KEY (FieldName, ProjectName),
    FOREIGN KEY (ProjectName) REFERENCES Project(ProjectName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create AnalysisResult table
CREATE TABLE AnalysisResult (
    ProjectName VARCHAR(100),
    PostID VARCHAR(100),
    FieldName VARCHAR(100),
    FieldValue TEXT NOT NULL,
    PRIMARY KEY (ProjectName, PostID, FieldName),
    FOREIGN KEY (ProjectName) REFERENCES Project(ProjectName)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (PostID) REFERENCES Posts(PostID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (FieldName, ProjectName) REFERENCES Field(FieldName, ProjectName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SET FOREIGN_KEY_CHECKS = 1;
