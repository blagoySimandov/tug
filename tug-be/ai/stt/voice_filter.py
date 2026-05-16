from io import BytesIO

import av


def remove_commentary(input: BytesIO) -> BytesIO:
    """
    Attenuates center-panned commentary using a side-channel pan trick,
    then applies a low-pass to suppress the voice frequency range.
    Works best on stereo broadcasts where commentary is center-panned.
    """
    output_buffer = BytesIO()
    with av.open(input) as in_container:
        audio = in_container.streams.audio[0]
        graph = av.filter.Graph()  # type: ignore

        abuffer = graph.add_abuffer(template=audio)
        # Subtract right from left (and vice versa) to cancel center-panned audio
        pan = graph.add("pan", "stereo|c0=c0-c1|c1=c1-c0")
        # Cut voice frequency range (1kHz–4kHz)
        equalizer = graph.add("equalizer", "f=2500:width_type=o:width=3:g=-12")
        abuffersink = graph.add("abuffersink")

        abuffer.link_to(pan)
        pan.link_to(equalizer)
        equalizer.link_to(abuffersink)
        graph.configure()

        with av.open(output_buffer, "w", format="mp3") as out_container:
            out_stream = out_container.add_stream("mp3")
            for packet in in_container.demux(audio):  # type: ignore
                for frame in packet.decode():
                    graph.push(frame)
                    while True:
                        try:
                            filtered = graph.pull()
                        except av.error.BlockingIOError:  # type: ignore
                            break
                        for out_packet in out_stream.encode(filtered):
                            out_container.mux(out_packet)
            graph.push(None)
            while True:
                try:
                    filtered = graph.pull()
                except (av.error.BlockingIOError, av.error.EOFError):  # type: ignore
                    break
                for out_packet in out_stream.encode(filtered):
                    out_container.mux(out_packet)
            for out_packet in out_stream.encode(None):
                out_container.mux(out_packet)

    output_buffer.seek(0)
    return output_buffer
