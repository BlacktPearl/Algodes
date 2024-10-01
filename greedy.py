"""
Idea:
You're attending an anime convention where multiple events (like panels, screenings, and meet-and-greets) happen simultaneously, and you want to attend as many as possible. Each event has a start and end time, and your goal is to maximize the number of events you can attend without overlap.

How the Greedy Algorithm Works:
Sort the events based on their end time.
Start by selecting the event that ends the earliest.
Then, for each remaining event, pick the next one that starts after the current event finishes.
Repeat this until you've scheduled as many events as possible without conflicts.
Why it's fun:
You could add anime-themed events, like voice actor panels, screenings of popular anime episodes, or cosplay contests.
You can make it visually engaging by representing the schedule as a timeline, or even using popular anime characters as placeholders for events.
You could even add some randomization where the user inputs their favorite anime genres, and the algorithm suggests a personalized schedule of relevant events!

"""
class event:
    def __init__(self, name ,startT ,endT ):
        self.name = name
        self.start_time = startT
        self.end_time = endT

def main():
    events = get_events()


    for event in events: 
        print(f"{event.name} : {str(event.start_time)[0:2]}:{str(event.start_time)[2:4]} - {str(event.end_time)[0:2]}:{str(event.end_time)[2:4]} ") 
        # There's a bug here when outputing the times like 06:50 cuz when i converted them to integers to make it easier for calculations
        # when they are converted back to strings they lose the  initial 0 and therefore the bugg accures in my slicing technique
        # but i won't fix it cuz this like is just to see if my events list is accurate and i don't really need to print the times...
        # aka this is just a debugging temporary line 


def get_events():
    print("What are the events of the anime convention and their scheduale? ")
    events_list = []
    while True: 
        name = input("Enter event's name or ; to finish: ")
        if name == ";":
            break
        else:
            while True:
                starting = input("Enter starting time (foramt : HH:MM in 24h system ex: 16:59): ")
                if(len(starting) != 5 or int(starting[0:2]) < 0 or int(starting[0:2]) > 23  or int(starting[3:5]) < 0 or int(starting[3:5]) > 59):
                    print("WRONG INPUT")
                    continue
                else:
                    start = int(starting[0:2] + starting[3:5])
                    break
                
            while True:
                ending = input("Enter ending time (foramt : HH:MM in 24h system ex: 16:59):   ")
                if(len(ending) != 5 or int(ending[0:2]) < 0 or int(ending[0:2]) > 23  or int(ending[3:5]) < 0 or int(ending[3:5]) > 59):
                    print("WRONG INPUT")
                    continue

                end = int(ending[0:2] + ending[3:5])
                if end < start:
                    print("WRONG INPUT")
                    continue
                
                else:
                    break

            events_list.append(event(name, start, end))
        
    return events_list


main()
