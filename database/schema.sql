-- ============================================================
-- SISTEMA DE GESTIÓN ESCOLAR (SGE)
-- Archivo: schema.sql
-- Descripción: Diseño completo de la base de datos
-- ============================================================

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS sge_escolar
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sge_escolar;

-- ------------------------------------------------------------
-- TABLA: colegios
-- Raíz del sistema, todo depende de esta tabla
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS colegios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    departamento VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- TABLA: profesores
-- Un profesor pertenece a un colegio
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profesores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colegio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colegio_id) REFERENCES colegios(id)
);

-- ------------------------------------------------------------
-- TABLA: estudiantes
-- Un estudiante pertenece a un colegio
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colegio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    grado VARCHAR(20) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colegio_id) REFERENCES colegios(id)
);

-- ------------------------------------------------------------
-- TABLA: materias
-- Una materia pertenece a un colegio
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    colegio_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colegio_id) REFERENCES colegios(id)
);

-- ------------------------------------------------------------
-- TABLA: notas
-- Conecta estudiante + materia + profesor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    materia_id INT NOT NULL,
    profesor_id INT NOT NULL,
    periodo INT NOT NULL,
    nota DECIMAL(4,2) NOT NULL,
    observacion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

-- ------------------------------------------------------------
-- TABLA: asistencia
-- Registro diario por estudiante, materia y profesor
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS asistencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT NOT NULL,
    materia_id INT NOT NULL,
    profesor_id INT NOT NULL,
    fecha DATE NOT NULL,
    presente BOOLEAN NOT NULL,
    observacion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (materia_id) REFERENCES materias(id),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);