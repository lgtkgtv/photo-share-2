#!/bin/bash
set -e

BASE_URL="http://localhost:8080"

echo "✅ Registering user 'alice'..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/register" -H "Content-Type: application/json" -d '{"username": "alice", "password": "password123"}' | jq -r .access_token)

echo "🔑 Got token: $TOKEN"

echo "📝 Updating profile..."
curl -s -X POST "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "bio": "Photographer"}' | jq .

echo "📄 Fetching profile..."
curl -s -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" | jq .

echo "📸 Uploading photo..."
curl -s -X POST "$BASE_URL/photos/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_photo.jpg" | jq .

echo "🖼️  Listing uploaded photos..."
curl -s -X GET "$BASE_URL/photos/photos" \
  -H "Authorization: Bearer $TOKEN" | jq .
