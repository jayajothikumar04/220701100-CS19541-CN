import random

def read_sender_buffer():
    with open('Sender_Buffer.txt', 'r') as file:
        lines = file.readlines()
    return [{'Frame_No': int(line.split()[0]), 'DATA': line.split()[1]} for line in lines]

def write_ack_to_buffer(acks):
    with open('Receiver_Buffer.txt', 'w') as file:
        for ack in acks:
            file.write(f"{ack}\n")

def receiver():
    frames = read_sender_buffer()
    print("Received frames:", frames)

    expected_frame_no = [frame['Frame_No'] for frame in frames]

    # Simulate an error by randomly changing the frame number
    if random.random() < 0.2:  # 20% chance to introduce an error
        expected_frame_no[random.randint(0, len(expected_frame_no) - 1)] = -1

    if all(frame['Frame_No'] == expected_frame_no[i] for i, frame in enumerate(frames)):
        print("Frames received correctly, sending ACKs")
        write_ack_to_buffer(expected_frame_no)
    else:
        print("Error in received frames, sending NACKs")
        write_ack_to_buffer([-1] * len(frames))

if __name__ == "__main__":
    receiver()
