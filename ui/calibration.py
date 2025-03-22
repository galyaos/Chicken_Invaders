import tkinter as tk
from PIL import Image, ImageTk


def show_calibration_screen(IMAGE_PATH, game_controller):
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Fullscreen mode
    root.attributes("-topmost", True)  # Fullscreen mode
    root.configure(bg="black")  
    root.lift()
    root.focus_force()

    try:
        image = Image.open(IMAGE_PATH)
        bg_image = ImageTk.PhotoImage(image)

        img_label = tk.Label(root, image=bg_image)
        img_label.image = bg_image
        img_label.pack(expand=True, fill="both")

    except Exception as e:
        print(f"Error loading image: {e}")

    # Display Text in the Center
    label = tk.Label(root, text="CALIBRATION MODE\nPlease Don't Move", fg="black",
                     font=("Impact", 60, "bold"))
    label.place(relx=0.5, rely=0.2, anchor="center")

    def close_window():
        root.destroy()

    def capture_first_frame():
        game_controller.process_frame()
        if game_controller.mode == 'double':
            if game_controller.player_centers[0][0] > game_controller.player_centers[1][0]:
                left_player_color, right_player_color = "red", "blue"
            else:
                left_player_color, right_player_color = "blue", "red"

            # create new labels one at the left and one at the right with space between the labels
            left_label = tk.Label(root, text="Left Player", fg=left_player_color, font=("Impact", 40, "bold"))
            right_label = tk.Label(root, text="Right Player", fg=right_player_color, font=("Impact", 40, "bold"))
            left_label.place(relx=0.25, rely=0.6, anchor="center")
            right_label.place(relx=0.75, rely=0.6, anchor="center")

    root.after(2000, capture_first_frame)
    root.after(5000, close_window)  # Close after 5 seconds
    root.mainloop()
