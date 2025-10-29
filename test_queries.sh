#!/bin/bash

API_URL="http://localhost:8001/query"
TOP_K=3
RETURN_CONTEXT=true

run_query() {
    local query="$1"
    echo -e "\nQuery: $query\n"

    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\", \"top_k\": $TOP_K, \"return_context\": $RETURN_CONTEXT}" \
        | jq

    echo -e "\n---------------------------"
}

queries=(
    "What time of day do people buy the most coffee?"
    "Are morning sales higher than evening sales?"
    "Which coffee is sold most frequently?"
    "Which coffee earns the most revenue?"
    "What's the top 3 selling coffee names in August?"
    "Is weekend revenue higher than weekday revenue?"
    "Which weekday has the highest number of transactions?"
    "How are sales trending over time?"
    "Any day with zero coffee sales?"
    "Is there a relationship between hour_of_day and coffee_name?"
    "When should we run happy hour promotions?"
    "What's the best day to launch new coffee flavor?"
    "Which coffee had the lowest revenue?"
    "Do people buy more coffee on Mondays or Fridays?"
)

for q in "${queries[@]}"; do
    run_query "$q"
done
