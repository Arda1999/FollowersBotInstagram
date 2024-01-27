import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import instaloader
import os



def get_own_followers(username, password):
    L = instaloader.Instaloader()

    try:
        L.context.login(username, password)
        profile = instaloader.Profile.from_username(L.context, username)
        followers = [follower.username for follower in profile.get_followers()]
        return followers
    except instaloader.exceptions.InstaloaderException as e:
        #print(f"Error in get_own_followers: {e}")
        return None
def download_profile_photos(username, followers):
    L = instaloader.Instaloader()
    save_directory = "new"
    
    os.makedirs(save_directory, exist_ok=True)

    try:
        for follower in followers:
            profile = instaloader.Profile.from_username(L.context, follower)
            pic_filename = os.path.join(save_directory, f"{follower}_profile_pic.jpg")
            L.download_profilepic(profile.username, filename=pic_filename)
    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error in download_profile_photos: {e}")

def get_own_follows(username, password):
    L = instaloader.Instaloader()
    
    try:
        L.context.login(username, password)
        print(L.context)
        profile = instaloader.Profile.from_username(L.context, username)
        follows = [follow.username for follow in profile.get_followees()]
        return follows
    
    except instaloader.exceptions.InstaloaderException as e:
        #print(f"Error in get_own_followers: {e}")
        return None

def find_not_following_back():
    username = entry_username.get()
    password = entry_password.get()
    
    own_followers = get_own_followers(username, password)
    own_follows = get_own_follows(username, password)
                
    if own_followers and own_follows:
        txt_output.config(state=tk.NORMAL)
        txt_output.delete(1.0, tk.END)
        txt_output.insert(tk.END, f"Kendi Takipçileriniz ({len(own_followers)} kişi):\n")

        txt_output.insert(tk.END, "Kendi Takipçileriniz:\n")
        for follower in own_followers:
            
            txt_output.insert(tk.END, f"{follower}\n")

        txt_output_2.config(state=tk.NORMAL)
        txt_output_2.delete(1.0, tk.END)
        txt_output_2.insert(tk.END, f"Kendi Takip Ettikleriniz ({len(own_follows)} kişi):\n")

        txt_output_2.insert(tk.END, "Kendi Takip Ettikleriniz:\n")
        for follows in own_follows:
            
            txt_output_2.insert(tk.END, f"{follows}\n")

        not_following_back = [user for user in own_follows if user not in own_followers]

        txt_output_3.config(state=tk.NORMAL)
        txt_output_3.delete(1.0, tk.END)

        txt_output_3.insert(tk.END, "Sizi Takip Etmeyenler:\n")
        for user in not_following_back:
            txt_output_3.insert(tk.END, f"{user}\n")

        txt_output.config(state=tk.DISABLED)
        txt_output_2.config(state=tk.DISABLED)
        txt_output_3.config(state=tk.DISABLED)
        download_profile_photos(username, own_followers)

    else:
        txt_output.config(state=tk.NORMAL)
        txt_output.delete(1.0, tk.END)
        txt_output.insert(tk.END, "Takipçiler veya takip ettikleriniz alınamadı.")

window = tk.Tk()
window.title("Instagram Follower Checker")

lbl_username = tk.Label(window, text="Instagram Username :")
lbl_username.grid(column=0, row=0, sticky=tk.W, padx=10, pady=5)

entry_username = ttk.Entry(window, width=20)
entry_username.grid(column=1, row=0, padx=10, pady=5)

lbl_password = tk.Label(window, text="Instagram Password:")
lbl_password.grid(column=0, row=1, sticky=tk.W, padx=10, pady=5)
entry_password = ttk.Entry(window, show="*", width=20)
entry_password.grid(column=1, row=1, padx=10, pady=5)

btn_check = ttk.Button(window, text="Find Who Not Followed You", command=find_not_following_back)
btn_check.grid(column=1, row=2, padx=10, pady=10)

notebook = ttk.Notebook(window)
notebook.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

frame_tab1 = ttk.Frame(notebook)
frame_tab2 = ttk.Frame(notebook)
frame_tab3 = ttk.Frame(notebook)

notebook.add(frame_tab1, text='Followers')
notebook.add(frame_tab2, text='Following')
notebook.add(frame_tab3, text='Who Not Follow You')

txt_output = scrolledtext.ScrolledText(frame_tab1, width=40, height=20, wrap=tk.WORD, state=tk.DISABLED)
txt_output.grid(row=0, column=0, padx=10, pady=10)

txt_output_2 = scrolledtext.ScrolledText(frame_tab2, width=40, height=20, wrap=tk.WORD, state=tk.DISABLED)
txt_output_2.grid(row=0, column=0, padx=10, pady=10)

txt_output_3 = scrolledtext.ScrolledText(frame_tab3, width=40, height=20, wrap=tk.WORD, state=tk.DISABLED)
txt_output_3.grid(row=0, column=0, padx=10, pady=10)

window.mainloop()
