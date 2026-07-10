from sqids import Sqids
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

sqids = Sqids(min_length=6)


@app.post('/generate')
async def gen_short_url(url: str = Body(embed=True)):
  insert_response = supabase.table('links').insert({ 'url': url }).select('id').execute()
  link_id = insert_response.data[0]['id']

  short_slug = sqids.encode([link_id])
  supabase.table('links').update({ 'short_url': short_slug }).eq('id', link_id).execute()

  return JSONResponse(status_code=201,
    content={
      'slug': short_slug  
    }
  )


@app.get('/{short_url}')
async def redirect_short_url(short_url: str):
  response = supabase.table('links').select('url').eq('short_url', short_url).execute()

  if not response.data:
    return RedirectResponse(url='/', status_code=302)
  
  long_url = 'https://' + response.data[0]['url']
  return RedirectResponse(url=long_url, status_code=307)