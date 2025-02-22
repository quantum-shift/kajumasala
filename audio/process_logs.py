

def process_logs(context):
    if not context.get('action_logs'):
        raise RuntimeError("Missing action_logs in process_logs")
    
    action_logs = context.get('action_logs')
    action_logs = action_logs.split('\n')
    action_logs = [line for line in action_logs if line.strip()]
    
    # keep only lines with "Next goal:"
    action_logs = [line for line in action_logs if "Next goal:" in line]
    
    # remove the "Next goal:" prefix
    action_logs = [line.replace("Next goal:", "").strip() for line in action_logs]
    
    context.update('action_log_filtered', action_logs)

if __name__ == "__main__":
    with open("./audio/action_log.txt", "r") as file:
        action_logs = file.read()
    with open("./audio/action_log_filtered.txt", "w") as file:
        file.write(process_logs(action_logs))
    