import time
import os

def send_frames(message, window_size):
    sender_buffer = "Sender_Buffer.txt"
    receiver_buffer = "Receiver_Buffer.txt"
    frame_number = 0
    total_frames = len(message)
    ack_received = 0  # Track the highest ACK received
    
    while frame_number < total_frames:
        # Prepare the window
        window = []
        for i in range(window_size):
            if frame_number + i < total_frames:
                frame = [frame_number + i, message[frame_number + i]]
                window.append(frame)
        
        # Send the frames in the current window
        with open(sender_buffer, 'w') as f:
            for frame in window:
                f.write(f"{frame[0]},{frame[1]}\n")
        
        print(f"Sent frames: {[frame[0] for frame in window]}")

        # Wait for acknowledgment
        time.sleep(2)  # Simulate delay
        
        if not os.path.exists(receiver_buffer):
            print("Receiver_Buffer file not found.")
            break

        with open(receiver_buffer, 'r') as f:
            ack = f.read().strip()

        if ack.isdigit():
            ack = int(ack)
            if ack > ack_received:
                print(f"Received ACK for Frame {ack - 1}")
                ack_received = ack
                frame_number = ack  # Move the window to the new frame number
            else:
                print(f"Received NACK or duplicate ACK for Frame {ack - 1}, Resending frames")
        else:
            print("Invalid acknowledgment received.")
        
    print("All frames sent successfully.")

def receive_frames():
    sender_buffer = "Sender_Buffer.txt"
    receiver_buffer = "Receiver_Buffer.txt"
    expected_frame = 0
    
    while True:
        if not os.path.exists(sender_buffer):
            print("Sender_Buffer file not found.")
            break
        
        with open(sender_buffer, 'r') as f:
            frames = f.readlines()
        
        if not frames:
            break
        
        for frame in frames:
            frame_no, data = frame.strip().split(',')
            frame_no = int(frame_no)
            
            if frame_no == expected_frame:
                print(f"Received Frame {frame_no}: {data}")
                expected_frame += 1
                ack = expected_frame
            else:
                print(f"Error: Expected Frame {expected_frame}, but received Frame {frame_no}")
                ack = expected_frame  # Send NACK for the expected frame
                break
        
        with open(receiver_buffer, 'w') as f:
            f.write(str(ack))
        
        print(f"Sent ACK for Frame {ack - 1}")
        time.sleep(2)  # Simulate delay

if __name__ == "__main__":
    mode = input("Choose mode (send/receive): ").strip().lower()
    
    if mode == "send":
        window_size = int(input("Enter window size: "))
        message = input("Enter the text message to send: ")
        send_frames(message, window_size)
    elif mode == "receive":
        receive_frames()
    else:
        print("Invalid mode selected. Please choose 'send' or 'receive'.")
