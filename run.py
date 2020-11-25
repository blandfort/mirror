

if __name__=='__main__':
    import logger

    from emotions import EmotionShard, EmotionLens
    from behavior import WindowShard, ScreenShard
    from faces import FaceShard, FaceswapLens
    from mirror import Mirror
    from shards import CamShard
    from lenses import LogLens
    from blocks import CountdownBlock

    from config import MIRRORLOG, WINDOWLOG, SCREENSHOT_DIR, SCREENSHOT_RESOLUTION, TIMESTEP
    from config import DEVICE, EMOTIONLOG, FACE_DIR

    emotion_shard = EmotionShard(logfile=EMOTIONLOG, device=DEVICE)
    #shards = [CamShard(), FaceShard(FACE_DIR, device=DEVICE), emotion_shard]
    shards = [CamShard(), FaceShard(FACE_DIR, device=DEVICE)]

    # Viewing live
    #mirror = Mirror(shards=shards, lens=EmotionLens(), timestep=.1, logfile=MIRRORLOG)
    #mirror = Mirror(shards=shards, lens=LogLens(), timestep=.5, logfile=MIRRORLOG)
    mirror = Mirror(shards=shards, lens=FaceswapLens(), timestep=.0, logfile=MIRRORLOG)
    mirror.run(memorize=False)

    # Logic to not remember everything in each step
    cam_block = CountdownBlock(blocking_shards=['webcam'], classes=emotion_shard.classes,
                                frequencies={'neutral': 20})
    face_block = CountdownBlock(blocking_shards=['faces'], classes=emotion_shard.classes,
                                frequencies={'neutral': 20})
    screenshot_block = CountdownBlock(blocking_shards=['screenshot'], classes=emotion_shard.classes,
                                      frequencies={'neutral': 50}, base_frequency=2)

    # Logging
    shards.append(WindowShard(logfile=WINDOWLOG))
    shards.append(ScreenShard(logdir=SCREENSHOT_DIR, resolution=SCREENSHOT_RESOLUTION))
    #mirror = Mirror(shards=shards, lens=LogLens(names=['emotions']), timestep=TIMESTEP, logfile=MIRRORLOG)
    #mirror.run(memorize=True, memory_blocks=[face_block.apply, screenshot_block.apply])
    #mirror.run(memorize=True)

    # Dreaming
    #mirror = Mirror(shards=shards, lens=EmotionLens(), timestep=.5, logfile=MIRRORLOG)
    #mirror.dream(from_date=datetime.datetime(year=2020, month=10, day=29, hour=12))
