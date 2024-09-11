import os
import time

def create_frames(text, window_size):
    frames = []
    for i in range(len(text)):
        frames.append({'Frame_No': i, 'DATA': text[i]})
    return frames

def write_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for frame in data:
            file.write(f"{frame['Frame_No']} {frame['DATA']}\n")

def read_from_file(file_name, timeout=10):
    elapsed_time = 0
    while not os.path.exists(file_name):
        if elapsed_time >= timeout:
            print(f"Timeout: {file_name} was not created by the receiver within {timeout} seconds.")
            return None  # Return None if timeout occurs
        print(f"Waiting for {file_name} to be created by receiver...")
        time.sleep(1)  # Wait for 1 second before checking again
        elapsed_time += 1
    
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return lines

def send_frames(frames, window_size):
    sender_buffer = frames[:window_size]
    write_to_file('Sender_Buffer.txt', sender_buffer)
    print("Sent frames:", sender_buffer)

    time.sleep(2)  # Simulate delay

    receiver_ack = read_from_file('Receiver_Buffer.txt')
    if receiver_ack is None:
        print("Exiting due to receiver not responding.")
        return frames  # Exit or handle accordingly

    ack_numbers = [int(ack.strip()) for ack in receiver_ack]

    if ack_numbers == [frame['Frame_No'] for frame in sender_buffer]:
        print("ACKs received:", ack_numbers)
        frames = frames[window_size:]  # Move the window
    else:
        print("NACK received, resending frames")
    
    return frames

def sliding_window_protocol(window_size, text):
    frames = create_frames(text, window_size)
    while frames:
        frames = send_frames(frames, window_size)

if __name__ == "__main__":
    window_size = int(input("Enter window size: "))
    text = input("Enter text message: ")

    sliding_window_protocol(window_size, text)
