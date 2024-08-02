class Navigation:
    def __init__(self):
        self.current_floor = 1

    def navigate(self, detections):
        messages = []
        for detection in detections:
            if detection['label'] == 'elevator':
                messages.append("Elevator detected. Please move towards it.")
            else:
                messages.append(f"{detection['label']} detected.")

        if not messages:
            return "No significant landmarks detected."

        return " ".join(messages)
