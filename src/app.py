from fastapi import FastAPI
import src.endpoints.picture_invert as ep_1
import src.endpoints.prime_number as ep_2

app = FastAPI(
    title="Zaawansowane programowanie - FastAPI"
)

app.include_router(ep_2.router)
app.include_router(ep_1.router)


@app.get("/", tags=["Default"])
async def read_root():
    return {"Hello": "World"}
