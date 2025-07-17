#!/bin/bash

echo "Testing Movie API Endpoints"
echo "=========================="
echo ""

# Base URL
BASE_URL="http://localhost:8000"

echo "1. Testing root endpoint:"
echo "   Command: curl $BASE_URL/"
curl -s "$BASE_URL/" | python -m json.tool
echo ""

echo "2. Testing /movies/all endpoint (first 3 movies):"
echo "   Command: curl $BASE_URL/movies/all"
curl -s "$BASE_URL/movies/all" | python -m json.tool | head -30
echo ""

echo "3. Testing /movies/ratings endpoint (available ratings):"
echo "   Command: curl $BASE_URL/movies/ratings"
curl -s "$BASE_URL/movies/ratings" | python -m json.tool
echo ""

echo "4. Testing /movies?rating=PG-13 (first 3 PG-13 movies):"
echo "   Command: curl \"$BASE_URL/movies?rating=PG-13\""
curl -s "$BASE_URL/movies?rating=PG-13" | python -m json.tool | head -30
echo ""

echo "5. Testing /movies?rating=R (first 3 R-rated movies):"
echo "   Command: curl \"$BASE_URL/movies?rating=R\""
curl -s "$BASE_URL/movies?rating=R" | python -m json.tool | head -30
echo ""

echo "6. Testing /movies?rating=PG (first 3 PG movies):"
echo "   Command: curl \"$BASE_URL/movies?rating=PG\""
curl -s "$BASE_URL/movies?rating=PG" | python -m json.tool | head -30
echo ""

echo "7. Testing /movies without rating parameter (returns all movies, showing first 3):"
echo "   Command: curl $BASE_URL/movies"
curl -s "$BASE_URL/movies" | python -m json.tool | head -30
echo ""

echo "8. API Documentation available at:"
echo "   http://localhost:8000/docs"
echo ""