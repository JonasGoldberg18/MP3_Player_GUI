#edit this one
import tkinter
import pyglet
import os
import random
import threading
import sys
import pickle
from tkinter import filedialog
import time
from tkinter import messagebox


file_Paths = {}
Flag = False
Song_Paused = False
music_files = []
original_directory = os.getcwd()


def on_close(window):
    window.destroy()
    pyglet.app.exit()

    sys.exit()


################################################################################################################################
def main_menu():
    global first_button
    first_button = False

    # button functions
    def add_song_button():
        folder_path = filedialog.askdirectory()
        if folder_path == '':
            pass
        else:
            name = folder_path.split("/")
            name = name[len(name) - 1]
            global file_Paths
            if name in file_Paths:
                messagebox.showerror(title='Warning', message='Directory has already been added')
            else:

                file_Paths[name] = folder_path
                create_button_for_song_directory(name)


    def play_song(file_directory):
        try:
            os.chdir(file_directory)
            window.destroy()
            audio_player(file_directory)

        except FileNotFoundError:
            text_message = 'The path\"' + file_directory + '\" could not be found'
            messagebox.showerror(title='Directory Not found', message=text_message)
    global packed_x
    packed_x = 20
    global packed_y_counter
    packed_y_counter = 0
    global x_cord
    x_cord = 20
    global y_cord
    y_cord = 100
    def create_button_for_song_directory(name):
        global file_Paths
        global packed_x
        global packed_y_counter
        global x_cord
        global y_cord
        screen_height = window.winfo_screenheight()
        file_path = file_Paths[name]
        button = tkinter.Button(text=name, font=('Microsoft Sans Serif', 10), command=lambda: play_song(file_path))
        global first_button
        if first_button == False:
            #first_button = True
            #button.pack(anchor='nw', pady=(100, 0), padx=20)
        #else:
            y_cord += 10
            if y_cord > screen_height - 300:
                packed_y_counter = 0
                packed_x += 100
                y_cord = 100
                x_cord += 500
            button.place(x=x_cord, y=y_cord)
            y_cord += 30
            #button.pack(anchor='nw', padx= packed_x)
        with open('mp3_saved_data.pickle', 'wb') as file:
            pickle.dump(file_Paths, file)

    def destroy_button(window, value, main_window):
        window.destroy()
        global file_Paths
        file_Paths.pop(value)

        with open('mp3_saved_data.pickle', 'wb') as file:
            pickle.dump(file_Paths, file)

        main_window.destroy()
        main_menu()
    def create_button(window2, val, main_window, x_val, y_val):
        button = tkinter.Button(window2, text=val, command=lambda :destroy_button(window2, val, main_window))
        button.place(x = x_val, y = y_val)
    def delete_button(main_window):
        window2 = tkinter.Tk(className='Select playlist to delete')
        window2.state('zoomed')
        label_text = tkinter.Label(window2, text='Select Playlist to Delete', font=('Arial, 40'))
        label_text.pack()
        x = 0
        y = 70
        global file_Paths

        for val in file_Paths:
            if y > window2.winfo_screenheight() - 300:
                y = 70
                x += 300
            create_button(window2, val, main_window, x, y)
            y += 40

        window2.mainloop()


    window = tkinter.Tk(className=' Main Menu')
    window.state('zoomed')

    # buttons here:
    button = tkinter.Button(text='Add Music\nPlaylist',
                            font=('Microsoft Sans Serif', 20), command=add_song_button)

    path = original_directory + '\\icon images'
    trash_image = tkinter.PhotoImage(file=path + '\\delete1.png')
    delete_button1 = tkinter.Button(image=trash_image, command=lambda: delete_button(window))
    delete_button1.pack()
    button.place(x=10, y=10)
    os.chdir(original_directory)
    global file_Paths

    if 'mp3_saved_data.pickle' in os.listdir():
        with open('mp3_saved_data.pickle', 'rb') as file:
            file_Paths = pickle.load(file)
        for val in file_Paths:
            create_button_for_song_directory(val)

    def on_close1():
        global player
        try:
            if player:
                player.pause()
                player.delete()
        except NameError:
            pass
        pyglet.app.exit()
        window.destroy()
        sys.exit()

    window.protocol("WM_DELETE_WINDOW", on_close1)


    window.mainloop()


#END of main####################################################################################################################
def PauseSong(event):
    global player
    global Song_Paused
    if Song_Paused == False:
        Song_Paused = True
        player.pause()
        pause.config(image=pause_image)
    else:
        Song_Paused = False
        player.play()
        pause.config(image=play_image)
def text_size_calc(text, screen_Width):
    length = len(text)

    return int(screen_Width * 1.3 // length)

#START OF SECONDARY MENU###########################################################################################
def audio_player(path):
    global selected_music_file

    def skip_button(music_files):
        pyglet.app.exit()
        global player
        global Flag
        global Song_Paused
        global offset
        offset = 0
        if Song_Paused == True:
            PauseSong(None)
        if player:
            player.pause()
            player.delete()

        Flag = True
        pick_song()

    def playSong(song):
        global player
        player = None
        player = pyglet.media.Player()
        duration_label = tkinter.Label(text='')
        duration_label.place(x=window.winfo_screenwidth() // 2.28, y=window.winfo_screenheight() // 1.28) # 840 by 830
        audio_source = pyglet.media.load(song)
        duration = audio_source.duration
        duration = round(duration)
        time_string = format_time(duration)
        duration_label.config(text=time_string)
        player.queue(audio_source)
        player.play()
        thread2 = threading.Thread(target=show_time, args=(player, duration,))
        thread2.start()
        pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), audio_source.duration)

    def play_audio_in_thread(song):
        global audio_thread
        audio_thread = threading.Thread(target=playSong, args=(song,))
        audio_thread.start()

    def show_time(player, duration):

        time_label = tkinter.Label(text='')
        time_label.place(x=window.winfo_screenwidth() // 2.28, y=window.winfo_screenheight() // 1.4) # 840 by 780
        global offset
        while time_label:
            #song_time = round(player.time - offset)
            song_time = round(int(player.time) - offset)
            if song_time > duration:
                offset = 0
                pick_song()
                break

            time_string = format_time(song_time)
            try:
                time_label.config(text=time_string)
            except:
                time_label = False
            time.sleep(0.5)

    def format_time(song_time):
        hours = int(song_time / 60 / 60)
        song_time = song_time - hours * 3600
        minutes = int(song_time / 60)
        song_time = song_time - minutes * 60
        if minutes < 10:
            minutes = '0' + str(minutes)
        if song_time < 10:
            song_time = '0' + str(song_time)
        time_string = str(hours) + ':' + str(minutes) + ':' + str(song_time)
        return time_string

    def pick_song():
        global music_files
        if len(music_files) == 0:
            music_files = os.listdir()
        global selected_music_file
        selected_music_file = random.choice(music_files)
        music_files.remove(selected_music_file)

        text_to_display = selected_music_file
        custom_font = ('Microsoft Sans Serif', text_size_calc(text_to_display, window.winfo_screenwidth()))
        text_label = tkinter.Label(window, text='Now playing:', font=500)
        song_name.config(text=text_to_display, font=custom_font)
        text_label.place(x=10, y=10)

        if Flag == False:
            play_audio_in_thread(selected_music_file)
        else:
            global player
            player = pyglet.media.Player()
            audio_source = pyglet.media.load(selected_music_file)
            player.queue(audio_source)
            player.play()

            duration_label = tkinter.Label(text='')
            duration_label.place(x=window.winfo_screenwidth() // 2.28, y= window.winfo_screenheight() // 1.28) #840 by 830

            duration = audio_source.duration
            duration = round(duration)
            time_string = format_time(duration)
            duration_label.config(text=time_string)

            thread2 = threading.Thread(target=show_time, args=(player,duration,))
            thread2.start()
            pyglet.clock.schedule_once(lambda dt: pyglet.app.exit(), audio_source.duration)
            global Song_Paused
            Song_Paused = False

    def exit_button():
        global player
        if player:
            player.pause()
            player.delete()
        window.destroy()
        pyglet.app.exit()
        main_menu()

    os.chdir(path)

    window = tkinter.Tk(className=' Music Player')
    window.state('zoomed')

    # buttons here
    button = tkinter.Button(window, text='Skip Song\n(Press Enter)', command=lambda: skip_button(music_files))
    button.place(x=window.winfo_screenwidth() // 1.8, y=window.winfo_screenheight() // 1.35) # 960 by 800

    def backwards_10_func():
        global player
        global offset
        time_mark = round(player.time, 2) - 10
        if time_mark < 10:
            time_mark = 0
            offset = 0
        player.seek(time_mark)
        PauseSong(None)
        time.sleep(0.1)
        offset -= 0.4
        PauseSong(None)

    def backwards_10_bound(event):
        backwards_10_func()

    def forwards_10_func():
        global player
        player.seek(round(player.time, 2) + 10)
        PauseSong(None)
        time.sleep(0.1)
        global offset
        offset += 0.4
        PauseSong(None)

    global offset
    def forwards_10_bound(event):
        forwards_10_func()
    def restart_song_fun(event):
        global player
        global offset
        player.seek(0)
        offset = 0
        PauseSong(None)
        time.sleep(0.1)
        PauseSong(None)

    offset = 0
    # BUTTONS GO HERE
    global play_image
    global pause_image
    global pause
    path = original_directory + '\\icon images'
    play_image = tkinter.PhotoImage(file=path + '\\play1.png')
    pause_image = tkinter.PhotoImage(file=path + '\\pause1.png')
    #restart_song
    restart_song = tkinter.Button(text='Restart Song\n(Backspace)', command=lambda :restart_song_fun(None))
    restart_song.place(x=window.winfo_screenwidth() // 3.4, y= window.winfo_screenheight() // 1.35) # 670 by 800 2.83
    forward_10_image = tkinter.PhotoImage(file=path + '\\forward_10_1.png')
    back_10_image = tkinter.PhotoImage(file=path + '\\back_10_1.png')
    pause = tkinter.Button(window, image=play_image, command=lambda : PauseSong(None))
    pause.place(x=window.winfo_screenwidth() // 2.26, y=window.winfo_screenheight() // 1.35) # x is 850
    backwards_10 = tkinter.Button(window, image=back_10_image, command=backwards_10_func)
    backwards_10.place(x=window.winfo_screenwidth() // 2.71, y=window.winfo_screenheight() // 1.35)
    forwards_10 = tkinter.Button(window, image=forward_10_image, command=forwards_10_func)
    forwards_10.place(x=window.winfo_screenwidth() // 2, y=window.winfo_screenheight() // 1.35)
    font1 = ('Arial', 20)
    exit_button = tkinter.Button(text='Exit to Main Menu', font=font1, command=exit_button)
    exit_button.pack(anchor='ne')
    window.protocol("WM_DELETE_WINDOW", lambda: on_close(window))
    song_name = tkinter.Label(window, text='', font='Arial')
    song_name.place(x=10, y=50)
    global music_files
    music_files = os.listdir()
    window.bind("<space>", PauseSong)
    window.bind("<Right>", forwards_10_bound)
    window.bind("<Left>", backwards_10_bound)
    window.bind("<Return>", skip_button)
    window.bind("<BackSpace>", restart_song_fun)
    pick_song()
    window.mainloop()

main_menu()