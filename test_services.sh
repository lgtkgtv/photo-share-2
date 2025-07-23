#!/bin/bash
# Exit immediately if any command fails
set -e

## 🧠 Tips for Understanding
#
#   curl -s:        makes a silent HTTP request (no progress bar)
#   jq:             command-line JSON processor (used to format/parse response)
#   Bearer $TOKEN:  is how the JWT token is sent to authenticate Alice

# Base URL of the gateway where all services are routed through
BASE_URL="http://localhost:8080"

# ---------------------------------------------------------------
# ✅ STEP 1: Register a new user called "alice"
# Sends a POST request to /auth/register with JSON payload
# The response will include a JWT token
echo "✅ Registering user 'alice'..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}' \
  | jq -r .access_token)

# Save and display the access token
echo "🔑 Got token: $TOKEN"

# ---------------------------------------------------------------
# 📝 STEP 2: Update Alice's profile
# Sends a POST request to /users/me with authorization header and new profile data
echo "📝 Updating profile..."
curl -s -X POST "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "bio": "Photographer"}' \
  | jq .

# ---------------------------------------------------------------
# 📄 STEP 3: Fetch Alice's profile
# Sends a GET request to /users/me with the same token
echo "📄 Fetching profile..."
curl -s -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

# ---------------------------------------------------------------
# 📸 STEP 4: Upload a test photo
# Sends a multipart POST request to /photos/upload with image file
echo "📸 Uploading photo..."
curl -s -X POST "$BASE_URL/photos/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_photo.jpg" \
  | jq .

# ---------------------------------------------------------------
# 🖼️ STEP 5: List uploaded photos
# Sends a GET request to /photos/photos to list all uploaded images for Alice
echo "🖼️  Listing uploaded photos..."
curl -s -X GET "$BASE_URL/photos/photos" \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

