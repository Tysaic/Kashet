# Comandos rápidos para subir código / Quick commands to upload code

## Para código nuevo / For new code
```bash
git clone https://github.com/Tysaic/Kashet.git
cd Kashet
# Copia tus archivos aquí / Copy your files here
git add .
git commit -m "Agregar código inicial"
git push origin main
```

## Para código existente / For existing code
```bash
cd tu-directorio-de-codigo
git init
git remote add origin https://github.com/Tysaic/Kashet.git
git pull origin main
git add .
git commit -m "Agregar mi código"
git push origin main
```

## Para actualizaciones / For updates
```bash
git add .
git commit -m "Describir cambios"
git push origin main
```

## Comandos útiles / Useful commands
- `git status` - Ver estado de archivos
- `git log --oneline` - Ver historial
- `git diff` - Ver cambios antes de commit
- `git pull origin main` - Descargar últimos cambios

## ¿Problemas? / Issues?
1. Configurar git: `git config --global user.name "Tu Nombre"`
2. Configurar email: `git config --global user.email "tu@email.com"`
3. Si hay conflictos: `git pull origin main` primero

# Configuración permanente del remoto Git

Este documento describe cómo evitar el error:

```
remote: {"auth_status":"auth_error","body":"Invalid username or token. Password authentication is not supported for Git operations."}
```


## HTTPS con token (usando un *credential helper*)

> **Ventaja:** Rápido si ya dispones de un Personal Access Token (PAT).  
> **Requisito:** Un *credential helper* configurado (Windows → `manager-core`, macOS → `osxkeychain`, Linux → `cache` o `store`).

```bash
# Configura el helper (ejemplo para Windows)
git config --global credential.helper manager-core   # macOS: osxkeychain ; Linux: cache o store

# Sustituye <TU_USUARIO> y <TU_TOKEN> por tus datos
git remote set-url origin https://<TU_USUARIO>:<TU_TOKEN>@github.com/<TU_USUARIO>/<REPOSITORIO>.git

# Verifica
git remote -v
# > origin  https://<TU_USUARIO>:<TU_TOKEN>@github.com/<TU_USUARIO>/<REPOSITORIO>.git (fetch)
# > origin  https://<TU_USUARIO>:<TU_TOKEN>@github.com/<TU_USUARIO>/<REPOSITORIO>.git (push)

# Ya puedes hacer push sin volver a introducir credenciales
git push
```