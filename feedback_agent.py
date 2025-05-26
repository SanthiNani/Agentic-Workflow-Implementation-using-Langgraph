class FeedbackAgent:
    def validate(self, task_output):
        if "error" in task_output.lower():
            return False, "Task execution failed."
        if len(task_output.strip()) < 10:
            return False, "Output is too short."
        return True, "Looks good."
