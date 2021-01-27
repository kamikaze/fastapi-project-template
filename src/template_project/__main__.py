import uvicorn
from template_project.api.http import app


uvicorn.run(app, host='0.0.0.0', port=8080)
