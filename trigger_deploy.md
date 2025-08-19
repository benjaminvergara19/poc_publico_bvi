# Como activar el deployment desde poc_publico_bvi

## Método 1: Repository Dispatch via GitHub API

Usar curl con PAT token para activar deployment manualmente.

## Método 2: GitHub Actions Workflow (RECOMENDADO)

Crear archivo `.github/workflows/trigger-deploy.yml` en poc_publico_bvi:

```yaml
name: Trigger Deploy to Databricks

on:
  push:
    branches: [main, dev]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'development'
        type: choice
        options:
        - development
        - production

jobs:
  trigger-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger deployment
        run: |
          curl -X POST \
            -H "Accept: application/vnd.github.v3+json" \
            -H "Authorization: token ${{ secrets.REPO_DISPATCH_TOKEN }}" \
            https://api.github.com/repos/benjaminvergara19/poc_sensible_bvi/dispatches \
            -d '{
              "event_type": "deploy_${{ github.event.inputs.environment || (github.ref == 'refs/heads/main' && 'produccion' || 'desarrollo') }}",
              "client_payload": {
                "repo_owner": "benjaminvergara19",
                "repo_name": "poc_publico_bvi",
                "target_env": "${{ github.event.inputs.environment || (github.ref == 'refs/heads/main' && 'production' || 'development') }}"
              }
            }'
```

## Configuración necesaria para Método 2:

En poc_publico_bvi, agregar secret:
- **Name:** `REPO_DISPATCH_TOKEN`  
- **Value:** `[SAME PAT TOKEN AS USED IN poc_sensible_bvi]`

## Flujo automático:
- **Push a branch dev** → deploy a development
- **Push a branch main** → deploy a production
- **Manual trigger** → seleccionar environment