import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font

# Player class: stores id, name and total points
class Player:
    def __init__(self, player_id, player_name, player_points):
        self.player_id = player_id
        self.player_name = player_name
        self.player_points = player_points

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
            entry.pack()
            self.entries.append(entry)

    # Creates button to start game, links to _start_game
    def _btn_start_game(self):
        button_frame = tk.Frame(master=self)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        start_button = tk.Button(master=button_frame, text="Start Game", command=self._start_game)
        start_button.pack()

    # Gets entries for player names, initializes Player objects, adds them to players list
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
        self.pack(fill=tk.BOTH, expand=True)
        self.players = players
        self.scoreboard_names_pts()

    def scoreboard_names_pts(self):
        for id, player in enumerate(self.players):
            frame = tk.Frame(self)
            frame.grid(row=0, column=id, padx=5, pady=5)
            name = tk.Label(frame, text=f"{player.player_name}", font=font.Font(size=18))
            name.pack(padx=10, pady=10)
            points = tk.Label(frame, text=f"{player.player_points}", font=font.Font(size=20, weight="bold"))
            points.pack(padx=10, pady=10)

def main():
    board = Intro()
    board.mainloop()

if __name__ == "__main__":
    main()