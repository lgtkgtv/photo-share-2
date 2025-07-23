# decode_access_token() is used to check token and extract username

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from shared.config import decode_access_token

app = FastAPI(title="User Service")
# Initializes the API and sets a title for Swagger docs

user_profiles = {}
# 🚧 Temporary in-memory database for user profile data:
# {
#   "alice": {"name": "Alice", "bio": "Photographer"},
#   "bob":   {"name": "Bob",   "bio": "Guitarist"}
# }

# ✅ View Your Profile
#   Requires the Authorization header (e.g. "Bearer <token>")
#       Extracts and decodes the JWT token
#       Looks up the user’s profile by username (from the token)
#
#       curl -H "Authorization: Bearer <token>" http://localhost:8002/me
# 
#       Returns this:
#           {
#               "username": "alice",
#               "profile": {"name": "Alice", "bio": "Photographer"}
#           }
@app.get("/me")
def read_profile(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
        return {"username": username, "profile": user_profiles.get(username, {})}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✍️ Update Your Profile
#
#   curl -X POST http://localhost:8002/me \
#       -H "Authorization: Bearer <token>" \
#       -H "Content-Type: application/json" \
#       -d '{"name": "Alice", "bio": "Photographer"}'
#
#   API verifies the token and finds the username
#   Stores the profile `{"name": "Alice", "bio": "Photographer"}` under that user
#    Returns: `{"status": "updated"}`
@app.post("/me")
def update_profile(data: dict, authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
        user_profiles[username] = data
        return {"status": "updated"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

#🔓 Allow CORS (for testing from browser)
# Lets your frontend (e.g. a React app on localhost) make requests without being blocked.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
| Endpoint | Auth Required? | Method | Purpose                  |
| -------- | -------------- | ------ | ------------------------ |
| `/me`    | ✅ Yes         | GET    | Return your user profile |
| `/me`    | ✅ Yes         | POST   | Update your user profile |

🔧 Next Steps (if this were production)
| Improvement                                     | Why                               |
| ----------------------------------------------- | --------------------------------- |
| Replace `user_profiles = {}` with real database | Otherwise data is lost on restart |
| Add user validation                             | Don't allow empty bios, etc.      |
| Return error on malformed JSON                  | Right now any `dict` is accepted  |
| Rate limiting / throttling                      | Prevent abuse                     |

"""