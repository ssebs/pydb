# pydb

Python based DB / REST api.

Just supply a `db.json` file, and you're good to go.

> See pydb/files/default.json for example

## Usage
- After install / running...
- Create a db.json file with the structure you want.
- `make api`
- Use REST requests
  > We'll use \<key\>, this would be something like users

## API Spec
- GET
  - `/api/<key>`
    - Get all of a key
      - e.g. GET `/api/users`
  - `/api/<key>/<query>`
    - Search thru the key
      - e.g. GET `/api/users/seb`
  - `/api/<key>/<id>`
    - Get 1 via the id field
      - e.g. GET `/api/users/2`
- POST
  - `/api/<key>`
    - Create a new record for a key
      - e.g. POST `/api/posts`, `{"text": "My 3rd post"}`
- PUT / PATCH
  - `/api/<key>/<id>`
    - Update a record for a key
      - e.g. PUT `/api/posts/3`, `{"id": 3 , "text": "Updated post"}`
- DELETE
  - `/api/<key>/<id>`
    - Delete a record for a key
      - e.g. DELETE `/api/posts/3`

## Running
```bash
$ make install
$ make api
```

## LICENSE 
&copy; MIT 2020 Sebastian Safari
