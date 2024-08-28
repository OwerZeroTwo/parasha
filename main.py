from fastapi import FastAPI, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

notes = [
    {"id": 1, "title": "Note 1", "content": "This is note 1"},
    {"id": 2, "title": "Note 2", "content": "This is note 2"},
    {"id": 3, "title": "Note 3", "content": "This is note 3"},
]

@app.get("/")
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

@app.get("/notes/{note_id}")
async def read_note(note_id: int):
    note = next((note for note in notes if note["id"] == note_id), None)
    if note is None:
        return Response(status_code=404)
    return {"title": note["title"], "content": note["content"]}

@app.post("/notes/")
async def create_note(title: str = Form(...), content: str = Form(...)):
    new_note = {"id": len(notes) + 1, "title": title, "content": content}
    notes.append(new_note)
    return RedirectResponse(url="/", status_code=302)

@app.post("/notes/{note_id}/delete")
async def delete_note(note_id: int):
    note = next((note for note in notes if note["id"] == note_id), None)
    if note is not None:
        notes.remove(note)
    return RedirectResponse(url="/", status_code=302)