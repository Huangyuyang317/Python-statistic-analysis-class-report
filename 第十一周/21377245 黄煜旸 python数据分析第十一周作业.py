import os
import librosa
from multiprocessing import Process, Queue


def calculate_features(filename, result_queue):
    y, sr = librosa.load(filename)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    basename = os.path.basename(filename)
    with open(f"{basename}.txt", "w") as f:
        f.write(f"Pitches: {pitches}\n")
        f.write(f"RMS: {rms[0][0]}")
    result_queue.put((filename, pitches, rms[0][0]))

def process_files(files):
    result_queue = Queue(3)
    processes = [Process(target=calculate_features, args=(filename, result_queue)) for filename in files]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    while not result_queue.empty():
        filename, pitch, rms = result_queue.get()
        print(f"{filename}: Pitch={pitch}, RMS={rms}")



class SubProcess(Process):
        def __init__(self,filename, result_queue):
            super().__init__()
            self._filename=filename
            self._result_queue=result_queue
        def run(self):
            y, sr = librosa.load(self._filename)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            rms = librosa.feature.rms(y=y)
            basename = os.path.basename(self._filename)
            with open(f"{basename}.txt", "w") as f:
                f.write(f"Pitches: {pitches}\n")
                f.write(f"RMS: {rms[0][0]}")
            self._result_queue.put((self._filename, pitches, rms[0][0]))

def process(files):
    result_queue = Queue(3)
    plist=[SubProcess(filename, result_queue) for filename in files]
    for p in plist:
        p.start()
    for p in plist:
        p.join()
    while not result_queue.empty():
        filename, pitch, rms = result_queue.get()
        print(f"{filename}: Pitch={pitch}, RMS={rms}")

if __name__=='__main__':
    audio_dir = r"C:\Users\黄煜旸\Desktop\audio"
    files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".wav")]
    '''process_files(files)'''
    process(files)