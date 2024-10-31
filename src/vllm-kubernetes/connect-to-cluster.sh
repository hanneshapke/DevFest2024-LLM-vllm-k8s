#!/bin/bash

# Check if tmux is installed
if ! command -v tmux &> /dev/null
then
  echo "tmux could not be found, please install it first."
  exit 1
fi

# Start a new tmux session
tmux new-session -d -s vllm_server

# Split the window into two panes
tmux split-window -v

# Run kubectl port-forward in the first pane
tmux send-keys -t vllm_server:0.0 'kubectl port-forward service/llm-service 8000:8000' C-m

# Run kubectl logs in the second pane
tmux send-keys -t vllm_server:0.1 'kubectl logs -f -l app=gemma2-server' C-m

# Attach to the tmux session
tmux attach -t vllm_server
