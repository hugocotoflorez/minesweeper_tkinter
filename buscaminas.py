from functools import partial
import random
from threading import Thread
from time import sleep
import tkinter as tk
from tkinter import font

global seconds
seconds = 0

size = (16,16)
mines = 30

def conv(x:int,y:int)->int:
    'Transforms an x,y index to an equivalent i.'
    return x*size[1] + y
        
def invconv(i:int)->tuple[int,int]:
    'Transforms an i index to an equivalent x,y.'
    return i//(size[1]), i%size[1]

def new_board(size:tuple[int,int],minas:int)->list[int]:
    'returns board (size: x*y):\n\n0 -> empty cell\n\n1-8 -> number\n\n9 -> mine'
    
    
    seconds = 0

    #we save in buffer the mine(1) and non mine(0)
    buffer = [1 if i< minas else 0 for i in range(size[0]*size[1])]

    random.shuffle(buffer) # suffle where the mines are

    #create the board
    global board
    board = [0]*(size[0]*size[1])

    for i,e in enumerate(buffer):
        if e:#mine in i
            board[i] = 9
            x,y = invconv(i)
            #the lines before set the number of near mines in each cell
            if x!=0 and y!=0: 
                board[conv(x-1,y-1)]+=1
                board[conv(x-1,y)]+=1
                board[conv(x,y-1)]+=1
            elif x!=0:
                board[conv(x-1,y)]+=1
            elif y!=0:
                board[conv(x,y-1)]+=1
            if x!=size[0]-1 and y!=size[1]-1:
                board[conv(x+1,y+1)]+=1
                board[conv(x+1,y)]+=1
                board[conv(x,y+1)]+=1
            elif x!=size[0]-1:
                board[conv(x+1,y)]+=1
            elif y!=size[1]-1:
                board[conv(x,y+1)]+=1  
            if x!=0 and y!=size[1]-1:
                board[conv(x-1,y+1)]+=1   
            if x!=size[0]-1 and y!=0:
                board[conv(x+1,y-1)]+=1
    
    board = [a if a<9 else 9 for a in board]    
    initialize_board()   
    

              

def printarr(arr,size):
    'prints an array as a matrix'
    print('-'*2*size[1])
    print('\n'.join([' '.join([str(a) for a in arr[b*size[1]:b*size[1]+size[1]]]) for b in range(size[0])]))     
    print('-'*2*size[1])
        
   
    
#printarr(board,size)
C2 = '#1D2538' # texto
C3 = '#7C8DA5' # color boton
C1 = '#E0E1DC' # color bg
C4 = '#FF6555' # rojo

root = tk.Tk()
root.configure(bg=C1,padx=10,pady=10)

FONT = font.Font( family = "Comic Sans MS", size = 10, weight = "bold")  


header = tk.Frame(root,bg=C1);header.pack()
cellsFrame = tk.Frame(root,bg=C1);cellsFrame.pack()

tl = tk.Toplevel(root)
query_frame = tk.Frame(tl,bg=C1);query_frame.pack()
tk.Label(query_frame,text='Game options').grid(row=0,column=0,padx=5)
tk.Label(query_frame,text='width:').grid(row=1,column=0,padx=5)
x_entry = tk.Entry(query_frame);x_entry.grid(row=1,column=1,padx=5)
x_entry.insert(0,'16')
tk.Label(query_frame,text='height:').grid(row=2,column=0,padx=5)
y_entry = tk.Entry(query_frame);y_entry.grid(row=2,column=1,padx=5)
y_entry.insert(0,'16')
tk.Label(query_frame,text='mines:').grid(row=3,column=0)
mines_entry = tk.Entry(query_frame);mines_entry.grid(row=3,column=1,padx=5)
mines_entry.insert(0,'40')

spacer = tk.Label(header,text=' '*20,bg=C1);spacer.grid(row=0,column=1,pady=5)
crono_label = tk.Label(header,text='0',bg=C1,fg=C2,font=FONT);crono_label.grid(row=0,column=2,pady=5)

def check():
    if not x_entry.get() or int(x_entry.get()) > 100:
        x_entry.delete(0,tk.END)
        x_entry.insert(0,'Invalid number')
    
    elif not y_entry.get() or int(y_entry.get()) > 100:
        y_entry.delete(0,tk.END)
        y_entry.insert(0,'Invalid number')
    
    elif not mines_entry.get() or int(mines_entry.get()) > int(int(x_entry.get())*int(y_entry.get())/2):
        mines_entry.delete(0,tk.END)
        mines_entry.insert(0,'Invalid number')
        
    else:
        new_board((int(x_entry.get()),int(y_entry.get())),int(mines_entry.get()))
        
    
    
tk.Button(tl,text='Start',command=check).pack()
tk.Button(header,text='Restart',bg=C2,fg=C1,font=FONT,command=check).grid(row=0,column=0,pady=5)#restart button

def on_click(x,y,none=None):
    global seconds
    if not seconds:
        seconds = 1
    match board[conv(x,y)]:
        case 0:
            elem = ' '
            board[conv(x,y)] = -1
            empty_cell_click(x,y)
            
        case k if -1<k<9:
            elem = str(k)
            
        
        case 9:
            elem = 'M'
            seconds=0
            for x1 in range(size[0]):
                for y1 in range(size[1]):
                    if board[conv(x1,y1)] == 9:
                       tk.Label(cellsFrame,text=elem,font=FONT,bg=C4,fg=C2).grid(row=x1,column=y1,padx=1,pady=1,sticky='nesw')
            return #avoid change bg in the general label 
        
        case -1:
            elem = ' '
    
    tk.Label(cellsFrame,text=elem,font=FONT,bg=C1,fg=C2).grid(row=x,column=y,padx=1,pady=1,sticky='nesw')   
         
def empty_cell_click(x,y):
    if x!=0 and y!=0: 
        on_click(x-1,y-1)
        on_click(x-1,y)
        on_click(x,y-1)
    elif x!=0:
        on_click(x-1,y)
    elif y!=0:
        on_click(x,y-1)
    if x!=size[0]-1 and y!=size[1]-1:
        on_click(x+1,y+1)
        on_click(x+1,y)
        on_click(x,y+1)
    elif x!=size[0]-1:
        on_click(x+1,y)
    elif y!=size[1]-1:
        on_click(x,y+1)  
    if x!=0 and y!=size[1]-1:
        on_click(x-1,y+1)   
    if x!=size[0]-1 and y!=0:
        on_click(x+1,y-1)

        
def right_click(bttn,none=None):
    bttn['text']='F' if bttn['text']==' ' else ' '

def initialize_board():  
    crono_label['text'] = '0'
    for x in range(size[0]):
        for y in range(size[1]):
            bttn = tk.Button(cellsFrame,text=' ',relief=tk.FLAT,bg=C3,height=2,width=5,font=FONT)
            bttn.bind("<Button-1>", partial(on_click,*(x,y)))
            bttn.bind("<Button-2>", partial(right_click,*(bttn,)))
            bttn.bind("<Button-3>", partial(right_click,*(bttn,))) #both bttn 2 and 1 can be right click
            bttn.grid(row=x,column=y,padx=1,pady=1)
 
def start_crono():
    while True:
        if seconds:
            crono_label['text'] = str(int(crono_label['text'])+1)
        sleep(1)

Thread(target=start_crono,daemon=True).start()          
      
root.mainloop()