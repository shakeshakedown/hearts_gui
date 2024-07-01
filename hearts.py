import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

# Player class: stores id, name and total points
class Player:
    def __init__(self, player_id, player_name, player_points):
        self.player_id = player_id
        self.player_name = player_name
        self.player_points = int(player_points)

# Launch screen for hearts scoring
class Intro(tk.Tk):
    def __init__(self):
        super().__init__()

        # Attributes
        self.title("Hearts Scoreboard")
        self.var = tk.IntVar()
        self.var.set(3)
        self.var.trace_add("write", self.update_player_names)
        self.entries = []
        self.score_max = 100

        # Frames
        self.intro_frame = tk.Frame(self)
        self.intro_frame.grid()
        self.button_frame = tk.Frame(self)
        self.button_frame.grid()

        # Methods
        self.header()
        self.score_cap()
        self.num_players()
        self.update_player_names()
        self.btn_start_game()

    # Header
    def header(self):
        frame = self.intro_frame
        self.display = tk.Label(frame, text="Hearts Scoreboard", font=font.Font(size=28, weight="bold"))
        self.display.grid(row=0)

    def score_cap(self):
        frame = self.intro_frame
        tk.Label(frame, text="What score are you playing to?").grid(row=1)
        self.score_entry = tk.Entry(frame, width=25, justify="center")
        self.score_entry.grid(row=2)
        self.score_entry.insert(0, f"{self.score_max}")

    # Radio buttons for choosing 3 or 4 players
    def num_players(self):
        frame = self.intro_frame
        tk.Label(frame, text="How many players?").grid(row=3)
        Radiobutton(frame, text="3 Players", variable=self.var, value=3).grid(row=4)
        Radiobutton(frame, text="4 Players", variable=self.var, value=4).grid(row=5)

    # If number of players changes, destroys all entries and adds new entries equal to the number of players selected
    # FIXME: Already input player names should stay when changing        
    def update_player_names(self, *args):
        frame = self.intro_frame
        for entry in self.entries:
            entry.destroy()
        self.entries = []
        for num in range(self.var.get()):
            entry = tk.Entry(frame, width=50)

            # debug, so player names don't have to be filled in each time
            entry.insert(0, f"Player {num + 1}")
            entry.grid()
            self.entries.append(entry)

    # Creates button to start game, links to start_game
    def btn_start_game(self):
        frame = self.button_frame
        start_button = tk.Button(frame, text="Start Game", command=self.start_game)
        start_button.grid(row=1)

    # Gets entries for player names, initializes Player objects, adds them to players list
    # FIXME: Check to make sure no entry is empty
    def start_game(self):
        player_names = [entry.get() for entry in self.entries]
        players = []
        for id, name in enumerate(player_names):
            player = Player(id, name, 0)
            players.append(player)

        self.score_max = int(self.score_entry.get())
        self.switch_to_scoreboard(players, self.score_max)

    # Switch over to Scoreboard class
    def switch_to_scoreboard(self, players, score_max):
        for widget in self.winfo_children():
            widget.destroy()
        Scoreboard(self, players, self.score_max)

class Scoreboard(tk.Frame):
    def __init__(self, master, players, score_max):
        super().__init__(master)
        self.pack()

        # Attributes
        self.players = players
        self.score_max = score_max
        self.current_pass = []
        self.points_labels = []
        self.passing_cycle = None
        self.num_hands = 0
        self.prev_hands = {}

        # Frames
        self.game_info_frame = tk.Frame(self)
        self.game_info_frame.grid()
        self.name_pts_frame = tk.Frame(self)
        self.name_pts_frame.grid()
        self.entry_btn_frame = tk.Frame(self)
        self.entry_btn_frame.grid()

        # Methods to set up board
        self.passing()
        self.game_info()
        self.scoreboard_names_pts()
        self.score_entry()
        self.btn_score_entry()

    def passing(self):
        self.current_pass = ["Left", "Right", "Hold"] if len(self.players) == 3 else ["Left", "Right", "Across", "Hold"]

    def game_info(self):
        frame = self.game_info_frame
        cycle_index = self.num_hands % len(self.players)
        tk.Label(frame, text="Game Info", font=font.Font(weight="bold")).grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        tk.Label(frame, text="Dealer", font=font.Font(size=9, underline=True)).grid(row=1, column=0, columnspan=2)
        dealer = tk.Label(frame, text=f"{self.players[cycle_index].player_name}")
        dealer.grid(row=2, column=0, columnspan=2)
        tk.Label(frame, text="Pass", font=font.Font(size=9, underline=True)).grid(row=1, column=2, columnspan=2)
        passing = tk.Label(frame, text=f"{self.current_pass[cycle_index]}")
        passing.grid(row=2, column=2, columnspan=2)

    # Retrieve names and current points from players
    def scoreboard_names_pts(self):
        frame = self.name_pts_frame
        tk.Label(frame, text="Player Name", font=font.Font(weight="bold")).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame, text="Total Points", font=font.Font(weight="bold")).grid(row=1, column=0, padx=10, pady=10)
        for id, player in enumerate(self.players):
            name = tk.Label(frame, text=f"{player.player_name}")
            name.grid(row=0, column=(id + 1), padx=10, pady=10)
            points = tk.Label(frame, text=f"{player.player_points}")
            points.grid(row=1, column=(id + 1), padx=10, pady=10)
            self.points_labels.append(points)
    
    # Retrieve the previous hands played and their point values
    def hands_list_update(self):
        frame = self.name_pts_frame
        for hand in range(self.num_hands):
            tk.Label(frame, text=f"Hand {hand + 1}", font=font.Font(weight="bold")).grid(row=hand + 2, column=0, padx=10, pady=10)
            for score in range(len(self.players)):
                tk.Label(frame, text=f"{self.prev_hands[hand + 1][score]}").grid(row=(hand + 2), column=(score + 1))

    # Create 3 or 4 entries for scoring points
    def score_entry(self):
        self.pts_to_add = []
        for id, player in enumerate(self.players):
            pts = tk.Entry(self.entry_btn_frame, justify="center")
            pts.grid(row=(self.num_hands + 3), column=id)
            self.pts_to_add.append(pts)

    # Button for adding points
    def btn_score_entry(self):
        btn_add_pts = tk.Button(self.entry_btn_frame, text="Add Points", command=lambda: [self.add_pts(), self.hands_list_update(), self.game_info()])
        btn_add_pts.grid(row=4)

    # Logic for adding points to player's scores
    def add_pts(self):
        try:
            adjust_pts = [int(points.get()) for points in self.pts_to_add]

            # Checks that the value of the points is exactly 26
            if sum(adjust_pts) != 26:
                messagebox.showerror("Points Error", "Total value of all points scored must equal 26.")
                return
            
            # Checks if any player shot the moon
            shoot_the_moon = [id for id, score in enumerate(adjust_pts) if score == 26]
            if shoot_the_moon:
                for id, score in enumerate(adjust_pts):
                    adjust_pts[id] = 26 if id not in shoot_the_moon else 0

            for id, player in enumerate(self.players):
                player.player_points += adjust_pts[id]
                self.points_labels[id].config(text=str(self.players[id].player_points))
            self.num_hands += 1
            self.prev_hands[self.num_hands] = adjust_pts
            print(self.prev_hands)
            
        except ValueError:
            messagebox.showerror("Points Error", "Please enter a number for each player's scored points.")

def main():
    board = Intro()
    board.mainloop()

if __name__ == "__main__":
    main()