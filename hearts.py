import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font

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
        self.title("Hearts Scoreboard")
        self.var = tk.IntVar()
        self.var.set(3)
        self.var.trace("w", self._update_player_names)
        self.header()
        self._num_players()
        self._create_entry_frame()
        self._update_player_names()
        self._btn_start_game()

    # Main header
    def header(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(master=display_frame, text="Hearts Scoreboard", font=font.Font(size=28, weight="bold"))
        self.display.pack()

    # Radio buttons for choosing 3 or 4 players
    def _num_players(self):
        tk.Frame(master=self).pack(fill=tk.X)
        tk.Label(master=self, text="How many players?").pack()
        Radiobutton(self, text="3 Players", variable=self.var, value=3).pack(anchor=W)
        Radiobutton(self, text="4 Players", variable=self.var, value=4).pack(anchor=W)

    # Creates the entries for player names
    def _create_entry_frame(self):
        tk.Frame(master=self).pack(fill=tk.X)
        self.entries = []

    # If number of players changes, destroys all entries and adds new entries equal to the number of players selected
    # FIXME: Already input player names should stay when changing        
    def _update_player_names(self, *args):
        for entry in self.entries:
            entry.destroy()
        self.entries = []
        for num in range(self.var.get()):
            entry = tk.Entry(master=self, width=50)

            # debug, so player names don't have to be filled in each time
            entry.insert(0, f"Player {num + 1}")
            entry.pack()
            self.entries.append(entry)

    # Creates button to start game, links to _start_game
    def _btn_start_game(self):
        btn_frame = tk.Frame(master=self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        start_button = tk.Button(master=btn_frame, text="Start Game", command=self._start_game)
        start_button.pack()

    # Gets entries for player names, initializes Player objects, adds them to players list
    # FIXME: Check to make sure no entry is empty
    def _start_game(self):
        player_names = [entry.get() for entry in self.entries]
        players = []
        for id, name in enumerate(player_names):
            player = Player(id, name, 0)
            players.append(player)

        # debug
        for player in players:
            print(f"Player Name: {player.player_name}")
        
        self.switch_to_scoreboard(players)

    # Switch over to Scoreboard class with Player objects and players list
    def switch_to_scoreboard(self, players):
        for widget in self.winfo_children():
            widget.destroy()
        Scoreboard(self, players)

class Scoreboard(tk.Frame):
    def __init__(self, master, players):
        super().__init__(master)
        self.pack()
        self.players = players
        self.points_labels = []
        self.num_hands = 0
        self.prev_hands = {}
        self.common_frame = tk.Frame(self)
        self.common_frame.grid()
        self.entry_btn_frame = tk.Frame(self)
        self.entry_btn_frame.grid()
        self.scoreboard_names_pts()
        self.score_entry()
        self.btn_score_entry()

    # Retrieve names and current points from players
    def scoreboard_names_pts(self):
        frame = self.common_frame
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
        frame = self.common_frame
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
        btn_add_pts = tk.Button(self.entry_btn_frame, text="Add Points", command=lambda: [self.add_pts(), self.hands_list_update()])
        btn_add_pts.grid(row=4)

    # Logic for adding points to player's scores
    def add_pts(self):
        try:
            adjust_pts = [int(points.get()) for points in self.pts_to_add]
            for id, player in enumerate(self.players):
                player.player_points += adjust_pts[id]
                self.points_labels[id].config(text=str(self.players[id].player_points))
            self.num_hands += 1
            self.prev_hands[self.num_hands] = adjust_pts
            print(self.prev_hands)
        except ValueError:
            print(f"Invalid input for a player. Enter a number.")

def main():
    board = Intro()
    board.mainloop()

if __name__ == "__main__":
    main()