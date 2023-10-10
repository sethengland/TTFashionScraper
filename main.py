import time
from tiktokapipy.api import TikTokAPI
import csv
import warnings
from tiktokapipy import TikTokAPIWarning

warnings.filterwarnings("ignore", category=TikTokAPIWarning)


def getHashtaggedVideos():
    seen = set()
    arr = []
    with TikTokAPI() as api:
        challenge = api.challenge(challenge_name="fashion", video_limit=100)
        # some videos are unable to be parsed by this api, we give a little cushion here to make sure we can get to 100 total
        for video in challenge.videos.limit(120):
            if not video:
                continue
            if video.id not in seen:
                seen.add(video.id)
                arr.append(video)
            # return once we find 100
            if len(arr) == 100:
                return arr
    return arr


if __name__ == "__main__":
    print("fetching videos")
    startTime = round(time.time())

    vids = getHashtaggedVideos()
    rows = []
    for vid in vids:
        row = [vid.id, vid.desc, [c.title for c in vid.challenges], vid.stats.play_count, vid.stats.comment_count, vid.stats.share_count, vid.video.play_addr, vid.video.download_addr, vid.music.id, vid.music.title, vid.author.unique_id, vid.create_time, startTime]
        rows.append(row)

    field_names = ["VideoID", "VideoDescription", "HashTags", "PlayCount", "CommentCount", "ShareCount", "VideoPlayAddr", "VideoDownloadAddr", "MusicID", "AuthorID", "DatePosted", "DateFetched"]

    csv_file_path = f"scraped_data_{startTime}.csv"

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        print(f"writing file to {csv_file_path}")
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerows(rows)

    print("exited successfully")