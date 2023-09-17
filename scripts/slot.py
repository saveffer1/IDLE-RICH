import random
from settings import slot_img

class SlotItem:
    def __init__(self, name:str, image:any, emoji:str="", 
                 stack:set={3:15, 4:45, 5:200}, skill:str="price"):
        self.name = name
        self.image = image
        self.emoji = emoji
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
        self.nTilesPerCol = rows
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
        
        # self.win_patterns = [
        #     [(2, 1), (2, 2), (1, 3), (2, 4), (2, 5)],
        #     [(0, 0), (0, 1), (1, 2), (0, 3), (0, 4)],
        #     [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
        #     [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
        #     [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
        #     [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
        #     [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
        #     [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
        #     [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]
        # ]

        self.win_patterns = [
            # winline 1
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            # winline 2
            [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
            # winline 3
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            # winline 4
            [(2, 0), (2, 1), (1, 2), (2, 3), (2, 4)],
            # winline 5
            [(0, 0), (0, 1), (1, 2), (0, 3), (0, 4)],
            # winline 6
            [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
            # winline 7
            [(1, 0), (0, 1), (0, 2), (0, 3), (1, 4)],
            # winline 8
            [(2, 0), (1, 1), (0, 2), (1, 3), (2, 4)],
            # winline 9
            [(0, 0), (1, 1), (2, 2), (1, 3), (0, 4)]
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
                
        self.reels.append(item)
        
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

        return result
    
    def check_winlines(self, result):
        max_prize = 0
        freespins = 0
        bonus_flag = False
        winning_lines = []

        for i, pattern in enumerate(self.win_patterns):
            valid_pattern = True
            symbols = []

            for row, col in pattern:
                if 0 <= row < len(result) and 0 <= col < len(result[0]):
                    symbol = result[row][col]
                    symbols.append(symbol)

                    if symbol is None:
                        valid_pattern = False

            if valid_pattern and len(set(symbols)) == 1 and symbols[0] is not None:
                winning_lines.append(i + 1)
                symbol = symbols[0]
                prize = symbol.stack[len(self.win_patterns[0])]

                if symbol.skill == "freespin":
                    freespins += symbol.stack[len(self.win_patterns[0])]
                elif symbol.skill == "bonus":
                    bonus_flag = True

                if prize > max_prize:
                    max_prize = prize

        return max_prize, freespins, bonus_flag, winning_lines
    
    # def check_winlines(self, result):
    #     max_prize = 0
    #     freespins = 0
    #     winning_lines = []
    #     bonus_flag = False

    #     for i, winline in enumerate(self.winlines):
    #         line_prize = 0
    #         line_freespins = 0
    #         line_bonus_flag = False
    #         consecutive_symbols = []
    #         wildcard_count = 0

    #         for j in range(len(result)):
    #             line = result[j]
    #             for k in range(len(line)):
    #                 symbol = result[j][k]

    #                 if symbol.skill == "freespin":
    #                     line_freespins += symbol.stack[len(line)]
    #                 elif symbol.skill == "wild":
    #                     consecutive_symbols.append(symbol)
    #                     wildcard_count += 1
    #                 else:
    #                     consecutive_symbols.append(symbol)

    #                 if symbol.skill == "bonus":
    #                     line_bonus_flag = True

    #         # Check if there are 5 wildcards in a line and use their stack value
    #         if wildcard_count == len(winline):
    #             line_prize += consecutive_symbols[0].stack[len(winline)]

    #         # Calculate prize if any symbol occurs more than 2 times
    #         symbol_counts = {symbol: consecutive_symbols.count(symbol) for symbol in set(consecutive_symbols)}
    #         for symbol, count in symbol_counts.items():
    #             if count > 2:
    #                 line_prize += symbol.stack[len(winline)] * (count - 2)

    #         # Check if the line has at least one non-wildcard symbol
    #         if any(symbol.skill != "wild" for symbol in consecutive_symbols) and line_prize > 0:
    #             if line_prize > max_prize:
    #                 max_prize = line_prize
    #                 freespins = line_freespins
    #                 winning_lines = [i + 1]
    #                 if line_bonus_flag:
    #                     bonus_flag = True
    #             elif line_prize == max_prize:
    #                 winning_lines.append(i + 1)
    #                 if line_bonus_flag:
    #                     bonus_flag = True

    #     return max_prize, freespins, bonus_flag, winning_lines



    def spin(self):
        if self.spin_count == 0:
            self.shuffle_nodes()

        self.result = self.__random()
        max_prize, freespins, bonus_flag, winning_lines = self.check_winlines(self.result)

        bonus = "Bonusgame!" if bonus_flag else "No Bonus"

        # Define highlight colors for each winning line
        highlight_colors = ["\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m", "\033[98m", "\033[99m"]

        # Initialize a flag to check if any win was found
        win_found = False

        for line_idx, row in enumerate(self.result):
            for symbol_idx, item in enumerate(row):
                if item is not None:
                    format = item.emoji +" "+ item.name
                    if line_idx + 1 in winning_lines:
                        color = highlight_colors[winning_lines.index(line_idx + 1)]
                        print(f"{color}{format:10}\033[0m | ", end=" ")
                        win_found = True
                    else:
                        print(f"{format:10} | ", end=" ")
                else:
                    print(" " * 10 + " | ", end=" ")  # Empty cell
            print()

        print()
        
        if win_found:
            return f"Winning lines: {winning_lines}\nPrize: {max_prize}\nFreespins: {freespins}\n{bonus}"
        else:
            return f"You have no luck this time!\n{bonus}"


if __name__ == "__main__":
    symbols = [
        SlotItem("jackpot", emoji="👑", image=slot_img["jackpot"]),
        SlotItem("game", emoji="🃏", image= slot_img["game"]),
        SlotItem("bigprize", emoji="💰", image= slot_img["bigprize"]),
        SlotItem("freespin", emoji="🆓", image= slot_img["freespin"], skill="freespin"),
        SlotItem("wildcard", emoji="🍀", image= slot_img["wildcard"], skill="wild"),
        SlotItem("banana", emoji="🍌", image= slot_img["banana"]),
        SlotItem("banana", emoji="🍌", image= slot_img["banana"]),
        SlotItem("cherry", emoji="🍒", image= slot_img["cherry"]),
        SlotItem("cherry", emoji="🍒", image= slot_img["cherry"]),
        SlotItem("lemon", emoji="🍋", image= slot_img["lemon"]),
        SlotItem("lemon", emoji="🍋", image= slot_img["lemon"])
    ]
    random.shuffle(symbols)
    slot_machine = SlotMachine()
    
    for symbol in symbols:
        slot_machine.add_item(symbol)
    
    print()
    spin_result = slot_machine.spin()
    print(spin_result)