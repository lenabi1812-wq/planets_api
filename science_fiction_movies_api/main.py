from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()
movies_db = [
    {"id": 1, "title": "Интерстеллар", "director": "Кристофер Нолан", "year": 2014},
    {"id": 2, "title": "Начало", "director": "Кристофер Нолан", "year": 2010}
]

class MovieCreate(BaseModel):
    title: str = Field(..., min_length=2, description="Название фильма (мин. 2 символа)")
    director: str = Field(..., min_length=2, description="Режиссёр (мин. 2 символа)")
    year: int = Field(..., ge=1900, le=2030, description="Год выпуска (от 1900 до 2030)")


class Movie(MovieCreate):
    id: int

@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Фильм с указанным id не найден")

@app.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(new_movie: MovieCreate):
    for movie in movies_db:
        if movie["title"].lower() == new_movie.title.lower():
            raise HTTPException(status_code=400, detail="Фильм с таким названием уже существует")

    new_id = max([m["id"] for m in movies_db], default=0) + 1

    movie_dict = new_movie.model_dump()
    movie_dict["id"] = new_id

    movies_db.append(movie_dict)
    return movie_dict

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)