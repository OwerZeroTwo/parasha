from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import List
from pathlib import Path

app = FastAPI()

class Note(BaseModel):
    id: int
    text: str

class NoteRequest(BaseModel):
    text: str

notes = [
    Note(id=1, text="This is note 1"),
    Note(id=2, text="This is note 2"),
]

@app.get("/notes/")
async def get_notes():
    return notes

@app.post("/notes/")
async def create_note(note_request: NoteRequest):
    new_note = Note(id=len(notes) + 1, text=note_request.text)
    notes.append(new_note)
    return new_note

@app.get("/notes/{note_id}")
async def get_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            return note
    return JSONResponse(status_code=404, content={"error": "Note not found"})

@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    for note in notes:
        if note.id == note_id:
            notes.remove(note)
            return JSONResponse(status_code=200, content={"message": "Note deleted"})
    return JSONResponse(status_code=404, content={"error": "Note not found"})

@app.get("/")
async def index():
    html = """
    <html>
        <head>
            <title>Notes App</title>
        </head>
        <body>
            <h1>Notes App</h1>
            <table id="notes-table">
                <tr>
                    <th>ID</th>
                    <th>Text</th>
                </tr>
                {% for note in notes %}
                <tr>
                    <td>{{ note.id }}</td>
                    <td>{{ note.text }}</td>
                </tr>
                {% endfor %}
            </table>
            <form action="/notes/" method="post">
                <input type="text" name="text" placeholder="Enter note text">
                <button type="submit">Add Note</button>
            </form>
            <script>
                async function deleteNote(noteId) {
                    const response = await fetch(`/notes/${noteId}`, { method: 'DELETE' });
                    if (response.ok) {
                        const table = document.getElementById('notes-table');
                        const row = document.querySelector(`tr:nth-child(${noteId + 1})`);
                        table.removeChild(row);
                    }
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)