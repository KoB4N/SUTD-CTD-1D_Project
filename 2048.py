from distutils.dist import command_re
import tkinter as tk
import random
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import font
from turtle import bgcolor
import colors as c
import database_interface as db
import sys
from PIL import ImageTk, Image


### Global varaiables for db storing and display ###
scoreValue = 0
username = ""


class SplashScreen(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.master.geometry("600x600")
        self.master.configure(background="Black")
        self.master.title('CTD 1D Project Team 11C')    


        width=400
        height=400
        
        image = Image.open("1.jpg")
        resize_image = image.resize((width, height))
        img = ImageTk.PhotoImage(resize_image)
        label1 = tk.Label(self.master,image=img)
        label1.image = img
        label1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


        self.bt1=tk.Button(
            self.master,
            text="Play",
            width=10,
            height=2,
            fg="black",
            font=("OCR A Extended", 14, "bold"),
            command=self.start
            )
        self.bt1.place(relx=0.15, rely=0.8, anchor=tk.CENTER)
        

        self.exit_button=tk.Button(
            self.master,
            text='Exit',
            font=('OCR A Extended', 14, "bold"), 
            bg='gold', 
            bd=5, 
            width=10,
            height=2,
            command=self.quit
            )
        self.exit_button.place(relx=0.85, rely=0.8, anchor=tk.CENTER)
        

    def start(self):
        self.master.destroy()
        start_window = Game()
        start_window.mainloop()
        

    def quit(self):
        sys.exit()


class Game(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title('CTD 1D Project Team 11C')

        self.main_grid = tk.Frame(
            self, 
            bg=c.GRID_COLOR, 
            bd=3, 
            width=400, 
            height=400
            )
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)


    def make_GUI(self):
        
        ### Make Grid Layout ###

        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100
                    )
                
                cell_frame.grid(
                    row=i, 
                    column=j, 
                    padx=5, 
                    pady=5
                    )
                
                cell_number = tk.Label(
                    self.main_grid, 
                    bg=c.EMPTY_CELL_COLOR
                    )
                
                cell_number.grid(
                    row=i, 
                    column=j
                    )
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)


        ### Make Score Header ###

        score_frame = tk.Frame(self)
        score_frame.place(
            relx=0.5, 
            y=40, 
            anchor="center"
            )
        tk.Label(
            score_frame,
            text="SCORE",
            font=c.SCORE_LABEL_FONT).grid(
            row=0
            )
        self.score_label = tk.Label(
            score_frame, 
            text="0", 
            font=c.SCORE_FONT
            )
        self.score_label.grid(row=1)


    def start_game(self):
        
        ### Create Matrix of Zeroes ###

        self.matrix = [[0] * 4 for _ in range(4)]


        ### Fill 2 random cells with 2s

        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
            )
        while(self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2"
            )

        self.score = 0


    ### Matrix Manipulation Functions ###

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix


    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]


    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix


    ### Add a new 2 or 4 tile randomly to an empty cell ###

    def add_new_tile(self):
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while(self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)
            self.matrix[row][col] = random.choice([2, 4])


    ### Update the GUI to match the matrix ###

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR, 
                        text=""
                        )
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                        )
        self.score_label.configure(text=self.score)
        global scoreValue
        scoreValue = self.score_label.cget("text")
        self.update_idletasks()


    ### Arrow-Press Functions ###

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()


    ### Check if any moves are possible ###

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False


    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False


    ### Check if Game is Over (Win/Lose) ###

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Button(
                game_over_frame,
                text="You Win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT,
                command=self.show_signup
                ).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Button(
                game_over_frame,
                text="Game Over!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT,
                command=self.show_signup
                ).pack()
            
    
    def show_signup(self):
        self.destroy()
        signup_window = signUp()
        signup_window.mainloop()
            

### Display Sign Up Page ###

class signUp(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("500x500")
        self.master.title('CTD 1D Project Team 11C')


        ### Label
        self.label = tk.Label(
            self, 
            text="Fill in to Record Your Score!", 
            font=c.SCORE_LABEL_FONT
            ).place(relx=0.5, rely=0.05, anchor=tk.CENTER)


        ### Username Label
        self.entry_label = tk.Label(
            self, 
            text="Username:",
            font=c.USERNAME_LABEL
            ).place(relx=0.21, rely=0.28)
    
        
        ### Username Entry
        validate_cmd = self.register(self.validate_username)

        self.user_entry = tk.Entry(self, validate="key", validatecommand=(validate_cmd, "%P"))
        self.user_entry.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        

        ### Submit Btn
        self.submit_btn = tk.Button(
            self,
            text="SUBMIT",
            font=c.SUBMIT_BTN,
            border=3,
            command=self.dbUpload
            )
        self.submit_btn.place(relx=0.72, rely=0.3, anchor=tk.CENTER)


        ### Next Btn 
        self.next_btn = tk.Button(
            self, 
            text="NEXT >",
            font=c.NEXT_BTN,
            border=5,
            command=self.show_scores
            ).place(relx=0.85, rely=0.70, anchor=tk.CENTER)
        

    def validate_username(self, new_value):
        return len(new_value) <= 20
        

    def dbUpload(self):
        self.submit_btn.configure(state='disabled')
        username = self.user_entry.get().strip()
        db.update_score(username, scoreValue)
        
            
    def show_scores(self):
        self.destroy()
        scores_window = Scores()
        scores_window.mainloop()
        

### Display Score Page ###

class Scores(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("500x500")
        self.master.title('CTD 1D Project Team 11C')


        ### Dropdown Menu
        options = ["Leaderboard", "Recent Scores"]     

        self.selected_option = tk.StringVar(self)
        self.selected_option.set(options[0])

        self.selectionDropdown = tk.OptionMenu(
            self,
            self.selected_option,
            *options,
            command=self.show
            )
        self.selectionDropdown.config(font=c.SCORE_LABEL_FONT)
        self.selectionDropdown.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        
        
        self.display_scores = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            width=50, 
            height=15, 
            state='disabled',
            )
        self.display_scores.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        

        ### Next Btn 
        self.next_btn = tk.Button(
            self, 
            text="NEXT >",
            font=c.NEXT_BTN,
            border=5,
            command=self.show_ending
            ).place(relx=0.85, rely=0.75, anchor=tk.CENTER)
        
        self.show()


    def show(self, *args):
        selected_option = self.selected_option.get()
        leaderboard_content = db.fetch_high_scores()
        recent_content = db.fetch_latest_scores()
        content = leaderboard_content


        if (selected_option == "Leaderboard"):
            content = leaderboard_content
        elif (selected_option == "Recent Scores"):
            content = recent_content


        self.display_scores.configure(state='normal')
        self.display_scores.delete(1.0, tk.END)
        for row in content:
            row_str = str(row).strip('{}')
            self.display_scores.insert(tk.END, row_str + "\n\n")
        self.display_scores.configure(state='disabled')


    def show_ending(self):
        self.destroy()
        ending_window = Ending()
        ending_window.mainloop()


### Display Ending Credits Page ###

class Ending(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.geometry("500x500")
        self.master.title('CTD 1D Project Team 11C')
        

        ### Labels
        self.label = tk.Label(
            self, 
            text="THANK YOU FOR PLAYING!", 
            font=c.SCORE_LABEL_FONT
            ).place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        

        self.label1 = tk.Label(
            self, 
            text="CREDITS:", 
            font=c.SCORE_LABEL_FONT
            ).place(relx=0.5, rely=0.15, anchor=tk.CENTER)
        

        self.label2 = tk.Label(
            self, 
            text="1. Afrith Ahamed A. (1008109)\n\n 2. Darrell Lu Jun Qiang (1007857)\n\n 3. Khoo Li Cheng Dylan (1005088)\n\n 4. Tan Tian Kovan (1007519)\n\n 5. Varsha Ramesh (1008477)\n\n 6. Chong Zhi Xun (1008140)", 
            font=c.USERNAME_LABEL
            ).place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        

        ### Return to Game Btn 
        self.play_agn_btn = tk.Button(
            self, 
            text="PLAY AGAIN?",
            font=c.NEXT_BTN,
            border=5,
            command=self.confirm_prompt
            ).place(relx=0.85, rely=0.7, anchor=tk.CENTER)
        
        
        ### Return to Display Score Page
        self.back_btn = tk.Button(
            self,
            text="< BACK",
            font=c.NEXT_BTN,
            border=5,
            command=self.goBack
            ).place(relx=0.15, rely=0.7, anchor=tk.CENTER)
        
    
    def confirm_prompt(self):
        response = messagebox.askyesno("Play Again :))", "Are You Sure You Want To Play Again?")
        if (response == 1):
            self.show_game()
        elif (response == 0):
            sys.exit()
            

    def goBack(self):
        self.master.destroy()
        scores_window = Scores()
        scores_window.mainloop()
        

    def show_game(self):
        self.master.destroy()
        ending_window = Game()
        ending_window.mainloop()
    

if __name__ == "__main__":
    root = tk.Tk()
    game_instance = SplashScreen(master = root)
    game_instance.mainloop()