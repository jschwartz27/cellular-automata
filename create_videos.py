import os
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc


def cellular_automata_Generator(state, rule_n: int):
    rule_b: str = "{0:08b}".format(rule_n)
    states = ["{0:03b}".format(k) for k in range(8)][::-1]
    tRules = {states[i]: rule_b[i] for i in range(8)}

    while True:
        state_wrap = state[-1] + state + state[0] 
        state = ""
        for i in range(len(state_wrap) - 2):
            state += (tRules[state_wrap[i:i+3]])
        yield state   


def create_CA_tensor(rule_n: int, frame_n: int, W: int, H: int):
    seed = "".join(["0" for i in range(W-1)] + ["1"])
    cell_Generator = cellular_automata_Generator(seed, rule_n)

    state_M = [["0"]*W for x in range(H-1)] + [seed]
    tensor = [state_M]
    for _ in range(frame_n - 1):
        del state_M[0]
        state_M.append(next(cell_Generator))
        tensor.append(state_M)
    
    return tensor


def convert_tensor_color(ca_tensor):

    def _transform(x: str, zellenfarbe, hintergrundfarbe):
        return zellenfarbe if x == "1" else hintergrundfarbe

    b_color = np.float32([0, 0, 0])   # black
    color = np.float32([50, 205, 50]) # limegreen

    tensor_color = list()
    for frame in ca_tensor:
        frame_color = list()
        for row in frame:
            colorized = list(map(
                lambda x: _transform(x, color, b_color), row))
            frame_color.append(colorized)
        tensor_color.append(frame_color)
    
    return tensor_color


def create_video(ca_tensor, FPS, seconds, W, H, rule_n) -> None:
    fourcc = VideoWriter_fourcc(*'MP42')
    filename = './CA_video_rule_{}.avi'.format(rule_n)
    video = VideoWriter(filename, fourcc, float(FPS), (W, H))

    for frame in ca_tensor:
        video.write(np.float32(frame))
    video.release()


def main():
    FPS, seconds = 10, 10
    FRAMES_n = FPS * seconds
    W, H = 1920, 1080 
    rule_n = 22  # 195  # range(256)

    ca_tensor = create_CA_tensor(rule_n, FRAMES_n, W, H)
    ca_tensor_color = convert_tensor_color(ca_tensor)
    #for i in ca_tensor_color:
    #    print(i)

    create_video(ca_tensor_color, FPS, seconds, W, H, rule_n)
    print("\n\tVideo Completed!")

if __name__ == "__main__":
    main()
