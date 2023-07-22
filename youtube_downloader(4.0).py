
import customtkinter as atk
from tkinter import ttk,messagebox
from tkinter import *
from pytube import YouTube,Stream,Playlist
import threading
import os
from math import ceil

from PIL import Image

import time
# from tkinter.tix import *
from tkinter.filedialog import askdirectory

root = atk.CTk()

root.geometry("764x431+400+150")
icon = PhotoImage(file = './/resources4.0//icon.png')
root.iconphoto(False, icon)
root.title("Youtube video downloader")
root.resizable(0,0)

atk.set_appearance_mode("white")  # Modes: system (default), light, dark
atk.set_default_color_theme("green")


#defalut variables
url_entry=StringVar()
All_list=[]
All_list2=[]
path=os.path.expanduser("~")+"\\Downloads\\"
total_download_count=0
download_count=0
downloading=0

position_dict={0:"yes",1:"yes",2:"yes",3:"yes",4:"yes"}
current_position=0

previous_playlists=[]


#new implementations
def on_closing():
        root.destroy()
        os._exit(0)	



def search1():
    global current_position
    try:
        global All_list,All_list2,w,search_complete_check,variable
        
        title1.configure(text="")
        message.configure(text="Please wait a while.......") 
        All_list=[]
        All_list2=[]
        w.configure(values=[])

        if("playlist" in url.get() or "Playlist" in url.get()):
            youtube1=Playlist(url.get())
            print("The url :",url.get())
            variable.set(str("Mp4"+"     "+"720P"+"      ---- MB"+"       True"))
        else:
            try:
                youtube1=YouTube(url.get())
                a=youtube1.streams.filter(mime_type="video/mp4",progressive= True )
                for i in a:
                    root.update()
                    All_list.append(i)
            except Exception as e:
                print("The  inside error is :",e)
            try:
                b=youtube1.streams.filter(mime_type="video/mp4",progressive= False )
                for i in b:
                    root.update()
                    All_list.append(i)
            except:
                pass
            try:
                c=youtube1.streams.filter(only_audio=True).all()
                for i in c:
                    root.update()
                    All_list.append(i)
            except:
                pass
            try:
                for i in All_list:
                    root.update()
                    k=f"""{"%.2f" %float(((i.filesize)/1024)/1024)}"""  #size in mb
                    if i.resolution==None:   #resolution
                        j=i.abr              #bitrate
                    else:
                        j=i.resolution
                    l=i.is_progressive
                    root.update()
                    m=i.subtype            #file type
                    All_list2.append(str(m)+"     "+str(j)+"      "+str(k)+" MB"+"      "+str(l))
                    root.update()
            except: 
                pass
            w.configure(values=All_list2)
        search_complete_check=0
        message.configure(text="Choose the resolution/format ......")
        print(youtube1.title)
        title1.configure(text=youtube1.title)
    except Exception as e:
        search_complete_check=0
        message.configure(text="")
        print("the search exception is : ",e)
        messagebox.showerror("showerror", "1.Check Your internet connection... \n2.Or Fill the url properly.... ")


#select directory  function
def select_directory():
    global path
    a=path
    path=askdirectory()
    if path=="":
        path=a
    else:
        pass


def download(index,yes):
    global current_position,position_dict,All_list,total_download_count,download_count,downloading
    managing_previous_position=current_position
    try:
        try:
            def on_progress(stream, chunk, bytes_remaining):
                """Callback function"""
                total_size = stream.filesize
                bytes_downloaded = total_size - bytes_remaining
                pct_completed = bytes_downloaded / total_size * 100
                download_per.configure(text=f"{round(pct_completed, 2)} %")
                prog=bytes_downloaded / total_size
                progress_bar.set(prog)
        except EXCEPTION as e:
            print("error : ",e)
        if (yes=="yes"):
            print("Entered in yes")
            youtube1=YouTube(index)
            link= youtube1.streams.get_highest_resolution()
            link.download(path)
        else:
            All_list=[]
            total_download_count+=1
            youtube1=YouTube(url.get())
            try:
                lab3.configure(text=f"Downloading status : {download_count} / {total_download_count}")
                current_title=youtube1.title
            except:
                current_title="Unable to get title"  
                        
            try:
                a=youtube1.streams.filter(mime_type="video/mp4",progressive= True )
                for i in a:
                    root.update()
                    All_list.append(i)
            except:
                pass
            try:
                b=youtube1.streams.filter(mime_type="video/mp4",progressive= False )
                for i in b:
                    root.update()
                    All_list.append(i)
            except:
                pass
            try:
                c=youtube1.streams.filter(only_audio=True).all()
                for i in c:
                    root.update()
                    All_list.append(i)
            except:
                pass
        if(yes!="yes"):    
            progress_bar=atk.CTkProgressBar(root, orientation="horizontal",
                            width=350, mode="determinate")
            progress_bar.place(x=350,y=215+current_position*50)
            progress_bar.set(0)

            title=atk.CTkLabel(root,text=current_title,anchor="w",width=480)
            title.place(x=350,y=185+current_position*50)

            download_per=atk.CTkLabel(root,text="0 %")
            download_per.place(x=705,y=205+current_position*50)
            All_list[index].download(path)
            download_per.configure(text="100 %")
            progress_bar.set(1)
            messagebox.showinfo("downloaded successfully..",f"{current_title}\n Path : {path}")

    except Exception as e:
        print("The exception is : ",e)
        messagebox.showerror("Download Failed", "Check Your internet connection...") 
    try:
        if(yes!="yes"):  
            time.sleep(10)
            progress_bar.destroy()
            download_per.destroy()
            title.destroy()
            position_dict[managing_previous_position]="yes"
        else:
            downloading=0  
        download_count+=1
        lab3.configure(text=f"Downloading status : {download_count} / {total_download_count}")
    except Exception as e:
        print("Error occuring :",e)
        if(yes!="yes"):  
            time.sleep(10)
            position_dict[managing_previous_position]="yes"
        else:
            downloading=0 
        

#process handling functions
search_complete_check=0
def test():
    global search_complete_check
    try:
        if search_complete_check==0:
            search_complete_check=1
            threading.Thread(target=search1).start()
    except:
        pass



def playlist_download():
    global position_dict,current_position,variable,total_download_count,download_count,downloading
    count=0
    for i in position_dict:
        if position_dict[i]=="yes":
            current_position=i
            position_dict[i]="no"
            count=1
            break
    if count==0:
        messagebox.showinfo("info","Maximum 5 downloads are allowed at a time")
    try:
        play_list = Playlist(url.get())
        number=len(play_list)
        total_download_count+=number
        lab3.configure(text=f"Downloading status : {download_count} / {total_download_count}")
        progress_bar=atk.CTkProgressBar(root, orientation="horizontal",
                        width=350, mode="determinate")
        progress_bar.place(x=350,y=215+current_position*50)
        progress_bar.set(0)

        title=atk.CTkLabel(root,text="Video title",anchor="w",width=480)
        title.place(x=350,y=185+current_position*50)

        download_per=atk.CTkLabel(root,text="0 %")
        download_per.place(x=705,y=205+current_position*50)

        
        for link in play_list:
            youtube1=YouTube(link)
            try:
                current_title=youtube1.title
            except:
                current_title="Unable to get the title "
            while(downloading):
                root.update()
                continue
            title.configure(text=current_title)
            per='%.2f' % (download_count/total_download_count*100)
            download_per.configure(text=f"{per} %")
            progress_bar.set(download_count/total_download_count)
            
            threading.Thread(target=download,args=(link,"yes")).start()
            downloading=1
                    
        lab3.configure(text=f"Downloading status : {download_count} / {total_download_count}")
    except:
        print("There is an error")
    try:
        lab3.configure(text=f"Downloading status : {download_count} / {total_download_count}")
        download_per.configure(text="100 %")                        
        progress_bar.set(1)
        messagebox.showinfo("info",f"Playlist : {play_list.title} \nDownloaded Successfully .....")
    except:
        pass
    time.sleep(10)
    progress_bar.destroy()
    download_per.destroy()
    title.destroy()
    position_dict[current_position]="yes"



#position dictionary having value is_empty
def test1():
    global position_dict,current_position,variable,All_list2,previous_playlists
    try:
        if ("playlist" in url.get() or "Playlist" in url.get()):
            if(url.get() not in previous_playlists):
                previous_playlists.append(url.get())
            else:
                messagebox.showinfo("Info","Your playlist is already downloading\nYou can download another playlist")
                return
            messagebox.showinfo("Info","Don't close the app your playlist is downloading..")
            threading.Thread(target=playlist_download).start()
        else:
            print("The values: ",w.get())
            index=w.get()
            print(All_list2.index(w.get()))
            try:
                index=All_list2.index(w.get())
                count=0
                for i in position_dict:
                    if position_dict[i]=="yes":
                        current_position=i
                        position_dict[i]="no"
                        threading.Thread(target=download,args=(index,"no")).start()
                        messagebox.showinfo("Info","Don't close the app your file is downloading..")
                        count=1
                        break
                if count==0:
                    messagebox.showinfo("info","Maximum 5 downloads are allowed at a time")
                        
            except Exception as e:
                print("The error is : ",e)
                messagebox.showerror("info","First select the option from the dropdown menu......")
        variable.set("Type   bitrate/resol      size      progressive ")
    except:
        pass

# button_image_1 = PhotoImage(file=".//resources//search.png")
url = atk.CTkEntry(root, placeholder_text="Paste the url here",width=357.0,height=25.0)
url.place(x=301.0,y=25)

search_button = atk.CTkButton(root,text="Search",width=84.0,height=28,command=test)
search_button.place(x=673.0,y=23)

lab2=atk.CTkLabel(root,text="Status :")
lab2.place(x=301,y=55)

titlelab=atk.CTkLabel(root,text="Title :")
titlelab.place(x=301,y=85)

title1=atk.CTkLabel(root,text="",width=500,anchor="w")
title1.place(x=335,y=85)

message=atk.CTkLabel(root,text="")
message.place(x=350,y=55)


Download_button =atk.CTkButton(root,text="Download",width=104,height=28,command=test1,)
Download_button.place(x=659.0,y=127)



lab3=atk.CTkLabel(root,text="Downloading status .......")
lab3.place(x=301,y=162)

button_image_1= atk.CTkImage(light_image=Image.open(".//resources4.0//file.png"),size=(30, 30))


ch_button = atk.CTkButton(root,text="",image=button_image_1,width=1,height=3,command=select_directory,fg_color="transparent")
ch_button.place(x=618,y=120)

abc= atk.CTkImage(light_image=Image.open(".//resources4.0//message.png"),size=(286,431))
frame = atk.CTkFrame(master=root,width=286,height=431)
frame.place(x=0,y=0)
flab=atk.CTkLabel(frame,image=abc,text="")
flab.place(x=0,y=0)

variable = atk.StringVar()
variable.set("Type   bitrate/resol      size      progressive ") # default value
w = atk.CTkComboBox(root,variable=variable,width=315,values=[""],font=("Inter Regular", 14 * -1))
w.place(x=300,y=127)

#Progressbar of song
s = ttk.Style()
s.theme_use('default')

root.protocol("WM_DELETE_WINDOW", on_closing)
# root.configure(fg_color="red")
root.mainloop()
