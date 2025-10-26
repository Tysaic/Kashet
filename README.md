# Kashet
Sistema de caja chica.

## Cómo subir tu código a este repositorio / How to upload your code to this repository

### Español

#### Primera vez - Clonando el repositorio
Si es la primera vez que trabajas con este repositorio:

```bash
# 1. Clona el repositorio
git clone https://github.com/Tysaic/Kashet.git

# 2. Navega al directorio
cd Kashet

# 3. Copia tus archivos de código al directorio del repositorio

# 4. Agrega los archivos al staging area
git add .

# 5. Haz un commit con un mensaje descriptivo
git commit -m "Agregar código inicial del sistema de caja chica"

# 6. Sube los cambios al repositorio remoto
git push origin main
```

#### Si ya tienes código local y quieres conectarlo a este repositorio

```bash
# 1. Navega a tu directorio de código existente
cd /ruta/a/tu/codigo

# 2. Inicializa git (si no está inicializado)
git init

# 3. Agrega el repositorio remoto
git remote add origin https://github.com/Tysaic/Kashet.git

# 4. Descarga los archivos existentes del repositorio
git pull origin main

# 5. Agrega tus archivos
git add .

# 6. Haz un commit
git commit -m "Agregar mi código al repositorio"

# 7. Sube los cambios
git push origin main
```

#### Para actualizaciones futuras

```bash
# 1. Asegúrate de estar en el directorio del repositorio
cd Kashet

# 2. Descarga los últimos cambios (opcional pero recomendado)
git pull origin main

# 3. Agrega los archivos modificados
git add .

# 4. Haz un commit con un mensaje descriptivo
git commit -m "Descripción de los cambios realizados"

# 5. Sube los cambios
git push origin main
```

### English

#### First time - Cloning the repository
If this is your first time working with this repository:

```bash
# 1. Clone the repository
git clone https://github.com/Tysaic/Kashet.git

# 2. Navigate to the directory
cd Kashet

# 3. Copy your code files to the repository directory

# 4. Add files to staging area
git add .

# 5. Commit with a descriptive message
git commit -m "Add initial petty cash system code"

# 6. Push changes to remote repository
git push origin main
```

#### If you already have local code and want to connect it to this repository

```bash
# 1. Navigate to your existing code directory
cd /path/to/your/code

# 2. Initialize git (if not already initialized)
git init

# 3. Add the remote repository
git remote add origin https://github.com/Tysaic/Kashet.git

# 4. Pull existing files from the repository
git pull origin main

# 5. Add your files
git add .

# 6. Commit your changes
git commit -m "Add my code to the repository"

# 7. Push changes
git push origin main
```

#### For future updates

```bash
# 1. Make sure you're in the repository directory
cd Kashet

# 2. Pull latest changes (optional but recommended)
git pull origin main

# 3. Add modified files
git add .

# 4. Commit with a descriptive message
git commit -m "Description of changes made"

# 5. Push changes
git push origin main
```

## Comandos Git útiles / Useful Git commands

```bash
# Ver el estado de los archivos
git status

# Ver el historial de commits
git log --oneline

# Ver diferencias antes de hacer commit
git diff

# Deshacer cambios en un archivo específico
git checkout -- nombre_del_archivo

# Ver archivos ignorados por .gitignore
git ls-files --others --ignored --exclude-standard
```

## Solución de problemas / Troubleshooting

### Error: "Permission denied (publickey)"
- Asegúrate de tener configurada tu clave SSH o usa HTTPS
- Para HTTPS: `git remote set-url origin https://github.com/Tysaic/Kashet.git`

### Error: "Updates were rejected because the remote contains work"
- Primero haz pull: `git pull origin main`
- Resuelve conflictos si existen
- Luego haz push: `git push origin main`

### Configurar git por primera vez
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```
