import json
# import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


class Logger:
    def __init__(self, output):
        self.output = output

    def write(self, agent_id, user_id, user_input, detected_signal, response_type, coherence_score_impact=None, escalation_flag=False, session_id=None):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = {"timestamp": current_time,
                "agent_id": agent_id, 
                "user_id": user_id,
                "user_input": user_input, 
                "detected_signal": detected_signal,
                "response_type": response_type,
                "coherence_score_impact": coherence_score_impact,
                "escalation_flag": escalation_flag,
                "session_id": session_id}
        
        # Write each json object to its own line (appending to file)
        with open(self.output, 'a') as f:
            f.write(json.dumps(data) + '\n')


    def retrieve(self, agent_id, user_id):
        # Open jsonl file and sort by timestamp
        data = []
        with open(self.output, 'r') as f:
            data = [json.loads(x) for x in f]
        data = reversed(sorted(data, key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S")))

        # Get 10 most recent entries for given user-agent pair
        head = []
        for entry in data:
            if entry["user_id"] == user_id and entry["agent_id"] == agent_id:
                head.append(entry)
                if len(head) >= 10:
                    break
        
        # Pick 5 with escalation_flag=true or most recent
        for i in range(len(head) - 1, -1, -1):
            entry = head[i]
            if len(head) <= 5:
                break
            if entry["escalation_flag"] == False:
                head.pop(i)

        return head[:5]
    

    def visualize(self, agent_id, user_id):
        # Open jsonl file and load all entries
        data = []
        with open(self.output, 'r') as f:
            data = [json.loads(x) for x in f]

        # Get all frequencies for given user-agent pair
        freq = {}
        for entry in data:
            if entry["user_id"] == user_id and entry["agent_id"] == agent_id:
                s_type = entry["detected_signal"]
                freq[s_type] = freq.get(s_type, 0) + 1

        # Basic bar graph for now
        plt.bar(freq.keys(), freq.values())
        plt.xlabel("Signal Type")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()
    

if __name__ == "__main__":
    test = Logger("test.jsonl")

    # Some mock entries for now
    test.write("M", "nic", "hello", "signal placeholder a", "response placeholder")
    test.write("M", "nic", "what's up", "signal placeholder b", "response placeholder", escalation_flag=True)
    test.write("M", "jup", "hello", "signal placeholder", "response placeholder")
    test.write("M", "nic", "hello", "signal placeholder a", "response placeholder")
    test.write("M", "ev", "hello", "signal placeholder", "response placeholder")
    test.write("Axis", "nic", "greetings", "signal placeholder", "response placeholder", escalation_flag=True)
    test.write("M", "nic", "greetings", "signal placeholder a", "response placeholder", escalation_flag=True)
    test.write("Selah", "nic", "greetings", "signal placeholder c", "response placeholder", escalation_flag=True)
    test.write("Selah", "ev", "what's up", "greeting", "uhh")
    test.write("M", "ev", "what's up", "greeting", "uhh")
    test.write("M", "nic", "what's up", "signal placeholder c", "uhh")

    # Testing retrieval
    for x in test.retrieve("M", "nic"):
        print(x)

    # Basic visualization
    test.visualize("M", "nic")