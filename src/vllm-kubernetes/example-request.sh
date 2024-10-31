#!/bin/bash

PROMPT=$(cat << EOF
<start_of_turn>user
You are a helpful AI assistant excellent in writing poetry.
Please write a Haiku about the amazing DevFest Silicon Valley and Responsible AI
<end_of_turn>
<start_of_turn>model
EOF
)

RESPONSE=$(curl -s -X POST http://localhost:8000/v1/completions \
-H "Content-Type: application/json" \
-H "Authorization: Bearer token-abc123" \
-d @- <<EOF
{
  "model": "google/gemma-2-2b-it",
  "prompt": "${PROMPT}",
  "max_tokens": 256
}
EOF
)

echo "$RESPONSE" | jq .
