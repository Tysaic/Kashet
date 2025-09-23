# Comandos rápidos para subir código / Quick commands to upload code

## Para código nuevo / For new code
```bash
git clone https://github.com/Tysaic/SmillerB.git
cd SmillerB
# Copia tus archivos aquí / Copy your files here
git add .
git commit -m "Agregar código inicial"
git push origin main
```

## Para código existente / For existing code
```bash
cd tu-directorio-de-codigo
git init
git remote add origin https://github.com/Tysaic/SmillerB.git
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