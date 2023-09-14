import random
from settings import slot_img

class SlotItem:
    def __init__(self, name:str, image:any, description:str="", 
                 stack:set={3:15, 4:45, 5:200}, skill:str="price"):
        self.name = name
        self.image = image
        self.description = description
        self.stack = stack
        if skill not in ["price", "spin", "wild", "bonus"]:
            self.skill = "price"
        else:
            self.skill = skill
            
        self.next = None
        self.prev = None

class SlotMachine:
    def __init__(self, rows=3, columns=5):
        self.head = None
        self.tail = None
        self.length = 0
        self.rows = rows
        self.columns = columns
        self.reels = []
        self.spin_count = 0
        self.winlines = [
            (# winline 1
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 0, 1, 1]
            ),
            (# winline 2
                [1, 1, 0, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0]
            ),
            (# winline 3
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ),
            (# winline 4
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0]
            ),
            (# winline 5
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ),
            (# winline 6
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0]
            ),
            (# winline 7
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ),
            (# winline 8
                [0, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 1]
            ),
            (# winline 9
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0]
            ) 
        ]
        
    def add_item(self, item: SlotItem):
        if self.tail is None:
            self.head = item
            self.tail = item
            self.head.next = self.tail
            self.head.prev = self.tail
            self.tail.next = self.head
            self.tail.prev = self.head
        else:
            item.prev = self.tail
            item.next = self.head
            self.tail.next = item
            self.head.prev = item
            self.tail = item
                
        self.length += 1
    
    def __len__(self):
        return self.length
    
    def shuffle_nodes(self):
        if self.length > 1:
            node_list = []
            current = self.head
            for _ in range(self.length):
                node_list.append(current)
                current = current.next

            # Shuffle the nodes using random.shuffle for better randomness
            random.seed(None)
            random.shuffle(node_list)
            
            # Reconstruct the linked list with shuffled nodes
            self.head = node_list[0]
            self.tail = node_list[-1]

            for i in range(self.length):
                node_list[i].next = node_list[(i + 1) % self.length]
                node_list[i].prev = node_list[(i - 1) % self.length]
    
    def __random(self):
        if self.head is None:
            return []

        result = []
        current = self.head
        for _ in range(self.rows):
            temp = []
            direction = random.choice(["next", "prev"])
            for __ in range(self.columns):
                temp.append(current)
                if direction == "next":
                    current = current.next
                elif direction == "prev":
                    current = current.prev
            result.append(temp)
        
        self.spin_count += 1
        if self.spin_count >= 5:
            self.shuffle_nodes()
            self.spin_count = 0
        elif self.spin_count == 1:
            self.shuffle_nodes()

        return result

    def spin(self):
        result = self.__random()
        for row in result:
            for item in row:
                print(f"{item.name:10}", end=" | ")
            print()
        print()

        prize = 0  # Initialize prize to 0

        # Check for winlines
        
        

        if prize > 0:
            return f"You win {prize} credits!"
        else:
            return "No win this time."


    
                

if __name__ == "__main__":
    symbols = [
        SlotItem("game", slot_img["game"]),
        SlotItem("game", slot_img["game"]),
        SlotItem("banana", slot_img["banana"]),
        SlotItem("banana", slot_img["banana"]),
        SlotItem("banana", slot_img["banana"]),
        SlotItem("bigprize", slot_img["bigprize"]),
        SlotItem("bigprize", slot_img["bigprize"]),
        SlotItem("cherry", slot_img["cherry"]),
        SlotItem("cherry", slot_img["cherry"]),
        SlotItem("cherry", slot_img["cherry"]),
        SlotItem("freespin", slot_img["freespin"]),
        SlotItem("freespin", slot_img["freespin"]),
        SlotItem("wildcard", slot_img["wildcard"]),
        SlotItem("wildcard", slot_img["wildcard"]),
        SlotItem("lemon", slot_img["lemon"]),
        SlotItem("lemon", slot_img["lemon"]),
        SlotItem("lemon", slot_img["lemon"]),
        SlotItem("jackpot", slot_img["jackpot"])
    ]
    slot_machine = SlotMachine()
    
    for symbol in symbols:
        slot_machine.add_item(symbol)
    
    print()
    spin_result = slot_machine.spin()
    print(spin_result)
        
    