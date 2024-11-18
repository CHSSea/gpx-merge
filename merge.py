import gpxpy.gpx as gpx
import gpxpy
import datetime

from typing import *


def get_time(g: gpx.GPX) -> Optional[datetime.datetime]:
    for t in g.tracks:
        for s in t.segments:
            for pt in s.points:
                if pt.time:
                    return pt.time
    return None


def clean_extensions(g: gpx.GPX) -> None:
    g.extensions = []
    for rte in g.routes:
        rte.extensions = []
        for pt in rte.points:
            pt.extensions = []
    for t in g.tracks:
        t.extensions = []
        for s in t.segments:
            s.extensions = []
            for p in s.points:
                p.extensions = []


def merge_file(gpx_files_path, out_file_path):
    sort_by_time = True

    keep_extensions = True

    if not gpx_files_path:
        print("Nothing to do")

    gpxs: List[gpx.GPX] = []

    for gpx_file in gpx_files_path:
        print(f"Reading {gpx_file}")
        gpxs.append(gpxpy.parse(open(gpx_file, encoding='utf-8')))

    if sort_by_time:
        gpxs = sorted(gpxs, key=get_time)

    base_gpx: Optional[gpx.GPX] = None
    merged_segment = gpx.GPXTrackSegment()

    for g in gpxs:
        if base_gpx is None:
            base_gpx = g.clone()
            base_gpx.tracks = []  # 清空原始轨迹
            base_gpx.routes = []

        for track in g.tracks:
            for segment in track.segments:
                for point in segment.points:
                    merged_segment.points.append(point)

    merged_track = gpx.GPXTrack()
    merged_track.segments.append(merged_segment)

    if base_gpx:
        base_gpx.tracks.append(merged_track)

        if not keep_extensions:
            clean_extensions(base_gpx)

        with open(out_file_path, "w") as f:
            f.write(base_gpx.to_xml())
