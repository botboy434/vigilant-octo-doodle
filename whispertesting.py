import logging
import traceback
import diart.operators as dops
import rich
import rx.operators as ops
from diart import OnlineSpeakerDiarization, PipelineConfig
from diart.sources import MicrophoneAudioSource

# not my code, code is from Juanma Coria, I'm using it to better understand how to implement whisper and diart into my code.

# Suppress whisper-timestamped warnings for a clean output
logging.getLogger("whisper_timestamped").setLevel(logging.ERROR)

config = PipelineConfig(
    duration=5,
    step=0.5,
    latency="min",
    tau_active=0.5,
    rho_update=0.1,
    delta_new=0.57
)
dia = OnlineSpeakerDiarization(config)
source = MicrophoneAudioSource(config.sample_rate)

asr = WhisperTranscriber(model="small")

transcription_duration = 2
batch_size = int(transcription_duration // config.step)
source.stream.pipe(
    dops.rearrange_audio_stream(
        config.duration, config.step, config.sample_rate
    ),
    ops.buffer_with_count(count=batch_size),
    ops.map(dia),
    ops.map(concat),
    ops.filter(lambda ann_wav: ann_wav[0].get_timeline().duration() > 0),
    ops.starmap(asr),
    ops.map(colorize_transcription),
).subscribe(on_next=rich.print, on_error=lambda _: traceback.print_exc())

print("Listening...")
source.read()