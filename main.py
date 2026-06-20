import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from markitdown import MarkItDown

app = FastAPI(title="Resume Parser API using MarkItDown")
md = MarkItDown()

@app.get("/")
def read_root():
    return {"status": "Parser service is running online"}

@app.post("/convert")
async def convert_file(file: UploadFile = File(...)):
    # 1. Validate file extension
    allowed_extensions = {'.pdf', '.docx', '.txt', '.pptx', '.xlsx'}
    _, ext = os.path.splitext(file.filename.lower())
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type {ext}")

    # 2. Create a safe temporary file path
    temp_path = f"temp_{file.filename}"
    
    try:
        # 3. Stream the uploaded file to disk
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 4. Convert document to Markdown text
        result = md.convert(temp_path)
        return {"markdown": result.text_content}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
        
    finally:
        # 5. Clean up the temp file from disk whether it succeeded or failed
        if os.path.exists(temp_path):
            os.remove(temp_path)